"""Batch pipeline worker for sequential multi-patient processing.

Uses the same pipeline as the interactive workstation:
  Manual/pre-placed seeds → FMM+Vesselness centerline → tubular VOI → FAI stats
"""

from __future__ import annotations

from pathlib import Path
from typing import List

import numpy as np
from PySide6.QtCore import QThread, Signal

from pcat_workstation.models.patient_session import PatientSession


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
                results = self._process_patient(dicom_dir, patient_id)
                self.patient_completed.emit(i, patient_id, results)
                succeeded += 1
            except Exception as exc:
                self.patient_failed.emit(i, patient_id, str(exc))

        self.batch_completed.emit(total, succeeded)

    def _process_patient(self, dicom_dir: Path, patient_id: str) -> dict:
        """Run the full pipeline for one patient."""
        from pipeline.centerline import (
            VESSEL_CONFIGS,
            clip_centerline_by_arclength,
            estimate_vessel_radii,
        )
        from pcat_workstation.models.seed_editor import _fit_spline_centerline
        from pipeline.pcat_segment import build_tubular_voi, compute_pcat_stats
        from pcat_workstation.app.config import (
            CRISP_GAP_MM,
            CRISP_RING_MM,
            DEFAULT_PCAT_SCALE,
            VOI_MODE,
        )

        # Create session and load DICOM
        session_dir = self._output_dir / patient_id
        session_dir.mkdir(parents=True, exist_ok=True)
        session = PatientSession(session_dir)
        session.load_dicom(dicom_dir)

        volume = session.get_volume()
        meta = session.get_meta()
        spacing_mm = meta["spacing_mm"]

        # Load seeds from session (must be pre-placed)
        seeds_data = session.seeds_data
        if isinstance(seeds_data, dict) and "extended" in seeds_data:
            seeds_data = seeds_data["extended"]

        # Fallback: seeds JSON file
        if not seeds_data:
            import json
            seeds_json = session_dir / f"{session._prefix}_seeds.json"
            if seeds_json.exists():
                seeds_data = json.loads(seeds_json.read_text())

        if not seeds_data:
            raise RuntimeError("No seeds found for batch patient")

        vessels = ["LAD", "LCx", "RCA"]
        results = {}

        for vessel in vessels:
            # Find seeds for this vessel
            entry = None
            for key in (vessel, vessel.upper(), vessel.replace("x", "X")):
                if key in seeds_data:
                    entry = seeds_data[key]
                    break
            if entry is None:
                continue

            ostium = entry.get("ostium") or entry.get("ostium_ijk")
            if not ostium or any(c is None for c in ostium):
                continue
            waypoints = entry.get("waypoints", entry.get("waypoints_ijk", []))

            # Spline centerline through manual seeds
            self.batch_progress.emit(f"  {patient_id}/{vessel}: centerline...")
            ordered_seeds = [ostium] + [wp for wp in waypoints if wp]
            if len(ordered_seeds) < 2:
                continue
            centerline_full = _fit_spline_centerline(
                ordered_seeds, spacing_mm, volume.shape, step_mm=0.5
            )
            if centerline_full is None or len(centerline_full) < 3:
                continue

            vcfg = VESSEL_CONFIGS.get(vessel, {})
            centerline = clip_centerline_by_arclength(
                centerline_full, spacing_mm,
                start_mm=float(vcfg.get("start_mm", 0.0)),
                length_mm=float(vcfg.get("length_mm", 40.0)),
            )
            if len(centerline) < 5:
                continue

            radii_mm = estimate_vessel_radii(volume, centerline, spacing_mm)

            # VOI
            self.batch_progress.emit(f"  {patient_id}/{vessel}: VOI...")
            voi_mask = build_tubular_voi(
                volume_shape=volume.shape,
                centerline_ijk=centerline,
                spacing_mm=spacing_mm,
                radii_mm=radii_mm,
                voi_mode=VOI_MODE,
                crisp_gap_mm=CRISP_GAP_MM,
                crisp_ring_mm=CRISP_RING_MM,
                radius_multiplier=DEFAULT_PCAT_SCALE,
            )

            # Stats
            self.batch_progress.emit(f"  {patient_id}/{vessel}: statistics...")
            stats = compute_pcat_stats(volume, voi_mask, vessel)
            session.set_vessel_stats(vessel, stats)
            results[vessel] = stats

        return results
