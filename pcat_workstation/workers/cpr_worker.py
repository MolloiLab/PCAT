"""Lightweight async CPR generator for live seed editing.

Mirrors Horos' CPRGenerator pattern: when the curved path (spline
through seeds) changes, a new CPR image is generated asynchronously
and delivered via signal.  Only the CPR computation runs here — no
vesselness, VOI, or statistics.
"""

from __future__ import annotations

import traceback
from typing import List

import numpy as np
from PySide6.QtCore import QThread, Signal


class CPRWorker(QThread):
    """Generate a CPR image from a spline centerline on a background thread.

    Signals
    -------
    cpr_ready       : str, object, float  – vessel, cpr_image, row_extent_mm
    cpr_frame_ready : str, object         – vessel, frame_data dict
    """

    cpr_ready = Signal(str, object, float)
    cpr_frame_ready = Signal(str, object)

    def __init__(
        self,
        vessel: str,
        volume: np.ndarray,
        centerline_ijk: np.ndarray,
        spacing_mm: List[float],
        parent=None,
    ):
        super().__init__(parent)
        self.vessel = vessel
        self.volume = volume
        self.centerline_ijk = centerline_ijk
        self.spacing_mm = spacing_mm

    def run(self) -> None:
        try:
            from pipeline.visualize import _compute_cpr_data

            cpr_vol, N_frame, B_frame, positions, arclengths, n_h, n_w = (
                _compute_cpr_data(
                    self.volume,
                    self.centerline_ijk,
                    self.spacing_mm,
                    slab_thickness_mm=3.0,
                    width_mm=25.0,
                    pixels_wide=512,
                    pixels_high=256,
                )
            )
            self.cpr_ready.emit(self.vessel, cpr_vol, 25.0)
            self.cpr_frame_ready.emit(self.vessel, {
                "N_frame": N_frame,
                "B_frame": B_frame,
                "positions_mm": positions,
                "arclengths": arclengths,
                "volume": self.volume,
                "spacing": self.spacing_mm,
            })
        except Exception:
            traceback.print_exc()
