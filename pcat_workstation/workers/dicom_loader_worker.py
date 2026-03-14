"""QThread worker for loading DICOM data with per-file progress.

Loads DICOM slices one-by-one in a QThread, yielding the GIL between
files so the Qt event loop stays responsive.  No subprocess/pickle
overhead — the numpy array lives in-process and is handed directly
to the finished signal.
"""

from __future__ import annotations

import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pydicom
from PySide6.QtCore import QThread, Signal


class DicomLoaderWorker(QThread):
    """Load DICOM files on a background thread with per-file progress.

    Signals
    -------
    progress     : str              – status message
    progress_pct : int, int         – (current, total) file count
    finished     : object, object   – (volume, meta) on success
    failed       : str              – error message on failure
    """

    progress = Signal(str)
    progress_pct = Signal(int, int)
    finished = Signal(object, object)
    failed = Signal(str)

    def __init__(self, dicom_dir: Path, session: Any, parent=None):
        super().__init__(parent)
        self.dicom_dir = Path(dicom_dir)
        self.session = session

    def run(self) -> None:
        try:
            volume, meta = self._load_dicom_incremental()

            # Update session state (lightweight attribute assignments)
            self.session._volume = volume
            self.session._meta = meta
            self.session.dicom_dir = self.dicom_dir
            self.session.patient_id = str(meta.get("patient_id", "unknown"))
            self.session.study_date = str(meta.get("study_date", ""))
            self.session.series_description = str(
                meta.get("series_description", "")
            )
            self.session.kVp = float(meta.get("kVp", 0.0))

            self.finished.emit(volume, meta)
        except Exception as exc:
            self.failed.emit(str(exc))

    # ------------------------------------------------------------------
    # Incremental DICOM loading (mirrors pipeline.dicom_loader logic)
    # ------------------------------------------------------------------

    def _load_dicom_incremental(self) -> Tuple[np.ndarray, Dict[str, Any]]:
        """Load DICOM series one file at a time, yielding GIL between files."""
        dcm_files = sorted(self.dicom_dir.glob("*.dcm"))
        if not dcm_files:
            raise FileNotFoundError(f"No .dcm files found in {self.dicom_dir}")

        total = len(dcm_files)
        self.progress.emit(f"Reading {total} DICOM files...")

        # Phase 1: read all headers (light — mostly I/O which releases GIL)
        slices: List[pydicom.Dataset] = []
        for i, f in enumerate(dcm_files):
            ds = pydicom.dcmread(str(f))
            slices.append(ds)
            if i % 20 == 0:
                self.progress_pct.emit(i, total)
                self.progress.emit(f"Reading DICOM: {i}/{total}")
                time.sleep(0)  # yield GIL so UI can repaint

        self.progress_pct.emit(total, total)
        self.progress.emit("Sorting slices...")
        time.sleep(0)

        # Sort by Z position
        def _z(ds: pydicom.Dataset) -> float:
            pos = getattr(ds, "ImagePositionPatient", None)
            if pos is not None:
                return float(pos[2])
            return float(getattr(ds, "InstanceNumber", 0))

        slices.sort(key=_z)

        # Reference slice
        ref = slices[0]
        rows = int(ref.Rows)
        cols = int(ref.Columns)
        pixel_spacing = [float(x) for x in ref.PixelSpacing]

        z_positions = [_z(s) for s in slices]
        if len(z_positions) > 1:
            z_diffs = np.diff(z_positions)
            z_spacing = float(np.median(np.abs(z_diffs)))
        else:
            z_spacing = float(getattr(ref, "SliceThickness", 1.0))

        spacing_mm = [z_spacing, pixel_spacing[0], pixel_spacing[1]]

        origin = getattr(ref, "ImagePositionPatient", [0.0, 0.0, 0.0])
        origin_mm = [float(v) for v in origin]
        orientation = [float(v) for v in getattr(ref, "ImageOrientationPatient", [1, 0, 0, 0, 1, 0])]
        rescale_slope = float(getattr(ref, "RescaleSlope", 1.0))
        rescale_intercept = float(getattr(ref, "RescaleIntercept", -1024.0))

        SENTINEL_HU = -8192.0
        HU_AIR = -1024.0
        HU_MAX_VALID = 3095.0

        # Phase 2: build volume slice-by-slice with progress
        self.progress.emit("Building volume...")
        volume = np.zeros((len(slices), rows, cols), dtype=np.float32)
        for i, ds in enumerate(slices):
            raw = ds.pixel_array.astype(np.float32)
            hu = raw * rescale_slope + rescale_intercept
            hu[hu <= SENTINEL_HU + 1] = HU_AIR
            np.clip(hu, HU_AIR, HU_MAX_VALID, out=hu)
            volume[i] = hu

            if i % 20 == 0:
                self.progress_pct.emit(i, len(slices))
                self.progress.emit(f"Building volume: {i}/{len(slices)}")
                time.sleep(0)  # yield GIL

        self.progress_pct.emit(len(slices), len(slices))
        self.progress.emit("Volume ready")

        meta = {
            "patient_dir": str(self.dicom_dir),
            "patient_id": str(getattr(ref, "PatientID", "unknown")),
            "study_description": str(getattr(ref, "StudyDescription", "")),
            "series_description": str(getattr(ref, "SeriesDescription", "")),
            "n_slices": len(slices),
            "rows": rows,
            "cols": cols,
            "spacing_mm": spacing_mm,
            "origin_mm": origin_mm,
            "orientation": orientation,
            "rescale_intercept": rescale_intercept,
            "rescale_slope": rescale_slope,
            "z_positions": z_positions,
            "shape": list(volume.shape),
            "study_date": str(getattr(ref, "StudyDate", "")),
            "kVp": float(getattr(ref, "KVP", 0.0)),
        }

        return volume, meta
