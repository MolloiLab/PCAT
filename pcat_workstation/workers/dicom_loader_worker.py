"""QThread worker for loading DICOM data with per-file progress.

Wraps pipeline.dicom_loader.load_dicom_series with progress callbacks
and a memory-mapped volume cache for fast re-opens (~0.02s vs ~0.6s).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Tuple

import numpy as np
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
            # Try cached volume first (memory-mapped, ~0.02s)
            cache_result = self._try_load_cached()
            if cache_result is not None:
                volume, meta = cache_result
            else:
                # Full DICOM parse with progress via pipeline module
                from pipeline.dicom_loader import load_dicom_series

                volume, meta = load_dicom_series(
                    self.dicom_dir,
                    progress_callback=self._on_progress,
                )
                # Cache for next time (~0.7s, non-fatal if fails)
                self._save_cache(volume, meta)

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

    def _on_progress(self, current: int, total: int, message: str) -> None:
        """Progress callback passed to load_dicom_series."""
        self.progress_pct.emit(current, total)
        self.progress.emit(message)

    # ------------------------------------------------------------------
    # Volume cache (memory-mapped .npy)
    # ------------------------------------------------------------------

    def _cache_dir(self) -> Path:
        """Return cache directory next to the DICOM folder."""
        return self.dicom_dir / ".pcat_cache"

    def _try_load_cached(self) -> "Tuple[np.ndarray, Dict] | None":
        """Load volume from .npy cache using memory-mapped I/O."""
        cache = self._cache_dir()
        vol_path = cache / "volume.npy"
        meta_path = cache / "meta.json"

        if not vol_path.exists() or not meta_path.exists():
            return None

        try:
            self.progress.emit("Loading cached volume...")
            meta = json.loads(meta_path.read_text(encoding="utf-8"))

            # Invalidate cache if DICOM file count changed
            current_count = len(list(self.dicom_dir.glob("*.dcm")))
            if current_count != meta.get("n_slices", -1):
                return None

            # Memory-mapped: OS pages data in on demand, no 400MB copy
            volume = np.load(str(vol_path), mmap_mode="c")  # copy-on-write

            # Validate shape matches
            expected_shape = tuple(meta.get("shape", []))
            if volume.shape != expected_shape:
                return None

            self.progress.emit("Cached volume loaded")
            return volume, meta
        except Exception:
            return None

    def _save_cache(self, volume: np.ndarray, meta: Dict[str, Any]) -> None:
        """Save volume + meta to disk for fast re-open."""
        try:
            cache = self._cache_dir()
            cache.mkdir(parents=True, exist_ok=True)

            self.progress.emit("Caching volume for fast re-open...")
            np.save(str(cache / "volume.npy"), volume)
            (cache / "meta.json").write_text(
                json.dumps(meta, indent=2, default=str), encoding="utf-8"
            )
        except Exception:
            pass  # Cache failure is non-fatal
