"""Batch pipeline worker for sequential multi-patient processing."""

from __future__ import annotations

from pathlib import Path
from typing import List, Optional

import numpy as np
from PySide6.QtCore import QThread, Signal

from pcat_workstation.models.patient_session import PatientSession
from pcat_workstation.workers.pipeline_worker import PipelineWorker


class BatchWorker(QThread):
    """Process multiple patients sequentially.

    Signals
    -------
    patient_started : int, str  -- index, patient_id
    patient_completed : int, str, dict  -- index, patient_id, results
    patient_failed : int, str, str  -- index, patient_id, error
    batch_completed : int, int  -- total, succeeded
    batch_progress : str  -- status message
    """

    patient_started = Signal(int, str)
    patient_completed = Signal(int, str, dict)
    patient_failed = Signal(int, str, str)
    batch_completed = Signal(int, int)
    batch_progress = Signal(str)

    def __init__(self, dicom_dirs: List[Path], output_dir: Path, parent=None):
        super().__init__(parent)
        self._dicom_dirs = dicom_dirs
        self._output_dir = output_dir
        self._cancelled = False

    def cancel(self):
        self._cancelled = True

    def run(self):
        total = len(self._dicom_dirs)
        succeeded = 0

        for i, dicom_dir in enumerate(self._dicom_dirs):
            if self._cancelled:
                break

            patient_id = dicom_dir.name
            self.patient_started.emit(i, patient_id)
            self.batch_progress.emit(f"Processing {i + 1}/{total}: {patient_id}")

            try:
                # Create session
                session_dir = self._output_dir / patient_id
                session_dir.mkdir(parents=True, exist_ok=True)
                session = PatientSession(session_dir)

                # Load DICOM
                session.load_dicom(dicom_dir)

                # Run pipeline synchronously (we are already on a thread)
                from pipeline.auto_seeds import generate_seeds
                from pipeline.centerline import (
                    VESSEL_CONFIGS,
                    clip_centerline_by_arclength,
                    estimate_vessel_radii,
                    load_seeds,
                )
                from pipeline.contour_extraction import (
                    build_contour_based_voi,
                    extract_vessel_contours,
                )
                from pipeline.pcat_segment import compute_pcat_stats

                volume = session.get_volume()
                meta = session.get_meta()
                spacing_mm = meta["spacing_mm"]

                # Seeds
                seeds_json = session_dir / f"{session._prefix}_seeds.json"
                if not seeds_json.exists():
                    generate_seeds(dicom_dir=session.dicom_dir, output_json=seeds_json)

                seeds_data = load_seeds(seeds_json)
                vessels = ["LAD", "LCx", "RCA"]

                results = {}

                for vessel in vessels:
                    if vessel not in seeds_data:
                        continue
                    vsd = seeds_data[vessel]
                    ostium = vsd.get("ostium_ijk")
                    if not ostium or any(v is None for v in ostium):
                        continue

                    # Centerline
                    raw_dir = session_dir / "raw"
                    raw_dir.mkdir(parents=True, exist_ok=True)
                    npz_path = raw_dir / f"{session._prefix}_centerlines.npz"
                    if npz_path.exists():
                        cl_data = dict(np.load(str(npz_path), allow_pickle=True))
                        cl_key = f"{vessel}_centerline_ijk"
                        if cl_key not in cl_data:
                            continue
                        centerline_full = cl_data[cl_key]
                    else:
                        continue

                    if centerline_full is None or len(centerline_full) < 3:
                        continue

                    vcfg = VESSEL_CONFIGS.get(vessel, {})
                    centerline = clip_centerline_by_arclength(
                        centerline_full,
                        spacing_mm,
                        start_mm=float(vcfg.get("start_mm", 0.0)),
                        length_mm=float(vcfg.get("length_mm", 40.0)),
                    )

                    # Contours
                    cr = extract_vessel_contours(
                        volume, centerline, spacing_mm, vessel_name=vessel
                    )

                    # VOI
                    from pcat_workstation.app.config import (
                        CRISP_GAP_MM,
                        CRISP_RING_MM,
                        VOI_MODE,
                    )

                    voi_mask = build_contour_based_voi(
                        volume_shape=volume.shape,
                        contours=cr.contours,
                        centerline_mm=cr.positions_mm,
                        N_frame=cr.N_frame,
                        B_frame=cr.B_frame,
                        r_eq=cr.r_eq,
                        spacing_mm=spacing_mm,
                        voi_mode=VOI_MODE,
                        crisp_gap_mm=CRISP_GAP_MM,
                        crisp_ring_mm=CRISP_RING_MM,
                    )

                    # Stats
                    stats = compute_pcat_stats(volume, voi_mask, vessel)
                    session.set_vessel_stats(vessel, stats)
                    results[vessel] = stats

                self.patient_completed.emit(i, patient_id, results)
                succeeded += 1

            except Exception as exc:
                self.patient_failed.emit(i, patient_id, str(exc))

        self.batch_completed.emit(total, succeeded)
