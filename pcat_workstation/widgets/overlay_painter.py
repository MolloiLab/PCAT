"""2D QPainter overlay for seed markers and centerline spline.

Draws on top of VTK slice views. All rendering is in screen space
using QPainter -- no VTK actors needed.
"""

from __future__ import annotations

from typing import Optional, Tuple

import numpy as np
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QColor, QFont, QPainter, QPainterPath, QPen
from PySide6.QtWidgets import QWidget

# Vessel colors (RGB) matching the workstation palette
VESSEL_COLORS = {
    "LAD": QColor(255, 69, 58),   # red
    "LCx": QColor(10, 132, 255),  # blue
    "RCA": QColor(48, 209, 88),   # green
}

SLAB_MM = 2.0  # default slab thickness for visibility filtering


# ---------------------------------------------------------------------------
# Coordinate conversion
# ---------------------------------------------------------------------------

def voxel_to_screen(
    ijk: Tuple[float, float, float],
    orientation: str,
    current_slice: int,
    spacing: Tuple[float, float, float],
    volume_shape: Tuple[int, int, int],
    widget_size: Tuple[int, int],
    parallel_scale: float,
    focal_point: Tuple[float, float, float],
    slab_mm: float = SLAB_MM,
) -> Optional[Tuple[float, float]]:
    """Convert voxel [z, y, x] to screen pixel (px, py), or None if outside slab.

    Parameters
    ----------
    ijk : (z, y, x) voxel coordinate.
    orientation : "axial", "coronal", or "sagittal".
    current_slice : integer slice index along the slicing axis.
    spacing : (sz, sy, sx) voxel spacing in mm.
    volume_shape : (Z, Y, X) volume dimensions.
    widget_size : (width, height) in pixels.
    parallel_scale : camera parallel scale (half-height in world mm).
    focal_point : (fx, fy, fz) camera focal point in world mm.
    slab_mm : half-slab thickness for visibility filtering.

    Returns
    -------
    (screen_x, screen_y) in pixels, or None if the point is outside the slab.
    """
    z, y, x = float(ijk[0]), float(ijk[1]), float(ijk[2])
    sz, sy, sx = float(spacing[0]), float(spacing[1]), float(spacing[2])

    # World coordinates (mm)
    wx = x * sx
    wy = y * sy
    wz = z * sz

    fx, fy, fz = float(focal_point[0]), float(focal_point[1]), float(focal_point[2])
    widget_w, widget_h = float(widget_size[0]), float(widget_size[1])

    if parallel_scale <= 0 or widget_h <= 0:
        return None

    scale_px_per_mm = widget_h / (2.0 * parallel_scale)

    if orientation == "axial":
        # Slab check along Z
        slice_mm = current_slice * sz
        if abs(wz - slice_mm) > slab_mm:
            return None
        # Camera at (cx, cy, cz-dist), looking +Z, ViewUp=(0,-1,0).
        # Camera right = +X, camera up = -Y.
        # VTK display Y = (fy - wy) * scale + h/2  (camera-up maps to +vtk_y)
        # Qt screen Y = h - vtk_y = (wy - fy) * scale + h/2
        screen_x = (wx - fx) * scale_px_per_mm + widget_w / 2.0
        screen_y = (wy - fy) * scale_px_per_mm + widget_h / 2.0

    elif orientation == "coronal":
        # Slab check along Y
        slice_mm = current_slice * sy
        if abs(wy - slice_mm) > slab_mm:
            return None
        # Camera at (cx, cy-dist, cz), looking +Y, ViewUp=(0,0,1).
        # Camera right = +X, camera up = +Z.
        # VTK display Y = (wz - fz) * scale + h/2
        # Qt screen Y = h - vtk_y = (fz - wz) * scale + h/2
        screen_x = (wx - fx) * scale_px_per_mm + widget_w / 2.0
        screen_y = (fz - wz) * scale_px_per_mm + widget_h / 2.0

    elif orientation == "sagittal":
        # Slab check along X
        slice_mm = current_slice * sx
        if abs(wx - slice_mm) > slab_mm:
            return None
        # Camera at (cx+dist, cy, cz), looking -X, ViewUp=(0,0,1).
        # Camera right = +Y, camera up = +Z.
        # VTK display Y = (wz - fz) * scale + h/2
        # Qt screen Y = h - vtk_y = (fz - wz) * scale + h/2
        screen_x = (wy - fy) * scale_px_per_mm + widget_w / 2.0
        screen_y = (fz - wz) * scale_px_per_mm + widget_h / 2.0

    else:
        return None

    return (screen_x, screen_y)


# ---------------------------------------------------------------------------
# OverlayPainter widget
# ---------------------------------------------------------------------------

class OverlayPainter(QWidget):
    """Transparent overlay that draws seed markers and centerline spline.

    Sits on top of a VTK slice view widget.  All drawing uses QPainter
    in screen-pixel coordinates -- no VTK actors involved.

    Usage::

        overlay = OverlayPainter(parent=vtk_widget)
        overlay.set_seed_editor(editor)
        overlay.set_view_params(...)
        overlay.update()  # triggers repaint
    """

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        # Make fully transparent to mouse events (clicks pass through)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setStyleSheet("background: transparent;")

        self._seed_editor = None  # SeedEditor reference

        # View parameters (set by the owning slice view)
        self._orientation: str = "axial"
        self._current_slice: int = 0
        self._spacing: Tuple[float, float, float] = (1.0, 1.0, 1.0)
        self._volume_shape: Tuple[int, int, int] = (1, 1, 1)
        self._parallel_scale: float = 1.0
        self._focal_point: Tuple[float, float, float] = (0.0, 0.0, 0.0)

        # Crosshair position in world mm (x, y, z); None = don't draw
        self._crosshair_world: Optional[Tuple[float, float, float]] = None

    # ------------------------------------------------------------------
    # Configuration
    # ------------------------------------------------------------------

    def set_seed_editor(self, editor) -> None:
        """Store a reference to the SeedEditor instance."""
        self._seed_editor = editor

    def set_view_params(
        self,
        orientation: str,
        current_slice: int,
        spacing,
        volume_shape,
        parallel_scale: float,
        focal_point,
    ) -> None:
        """Update the camera / slice parameters used for coordinate conversion.

        Called by the owning VTKSliceView whenever the view changes (scroll,
        zoom, pan).
        """
        self._orientation = orientation
        self._current_slice = current_slice
        self._spacing = tuple(spacing)  # type: ignore[assignment]
        self._volume_shape = tuple(volume_shape)  # type: ignore[assignment]
        self._parallel_scale = parallel_scale
        self._focal_point = tuple(focal_point)  # type: ignore[assignment]

    def set_crosshair(self, x_mm: float, y_mm: float, z_mm: float) -> None:
        """Set the crosshair position in world-mm coordinates."""
        self._crosshair_world = (x_mm, y_mm, z_mm)

    def clear_crosshair(self) -> None:
        """Remove the crosshair."""
        self._crosshair_world = None

    # ------------------------------------------------------------------
    # Internal coordinate helper
    # ------------------------------------------------------------------

    def _to_screen(self, ijk, slab_mm: float = SLAB_MM) -> Optional[Tuple[float, float]]:
        """Shorthand for voxel_to_screen with current view parameters."""
        return voxel_to_screen(
            ijk,
            self._orientation,
            self._current_slice,
            self._spacing,
            self._volume_shape,
            (self.width(), self.height()),
            self._parallel_scale,
            self._focal_point,
            slab_mm=slab_mm,
        )

    # ------------------------------------------------------------------
    # Paint
    # ------------------------------------------------------------------

    def paintEvent(self, event) -> None:  # noqa: N802 (Qt naming)
        if self.width() <= 0 or self.height() <= 0:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)

        self._draw_crosshair(painter)
        self._draw_centerlines(painter)
        self._draw_seeds(painter)
        self._draw_selection_highlight(painter)

        painter.end()

    # ------------------------------------------------------------------
    # Drawing helpers
    # ------------------------------------------------------------------

    def _draw_crosshair(self, painter: QPainter) -> None:
        """Draw thin dashed crosshair lines through the current crosshair position."""
        if self._crosshair_world is None:
            return

        x_mm, y_mm, z_mm = self._crosshair_world
        w, h = self.width(), self.height()

        if self._parallel_scale <= 0 or h <= 0:
            return

        scale = h / (2.0 * self._parallel_scale)
        fx, fy, fz = self._focal_point

        if self._orientation == "axial":
            sx = (x_mm - fx) * scale + w / 2.0
            sy = (y_mm - fy) * scale + h / 2.0
        elif self._orientation == "coronal":
            sx = (x_mm - fx) * scale + w / 2.0
            sy = (fz - z_mm) * scale + h / 2.0
        elif self._orientation == "sagittal":
            sx = (y_mm - fy) * scale + w / 2.0
            sy = (fz - z_mm) * scale + h / 2.0
        else:
            return

        pen = QPen(QColor(255, 255, 255, 120))
        pen.setWidthF(1.0)
        pen.setStyle(Qt.DashLine)
        painter.setPen(pen)

        # Horizontal line
        painter.drawLine(QPointF(0, sy), QPointF(w, sy))
        # Vertical line
        painter.drawLine(QPointF(sx, 0), QPointF(sx, h))

    def _draw_seeds(self, painter: QPainter) -> None:
        """Draw seed markers for all vessels."""
        if self._seed_editor is None:
            return

        editor = self._seed_editor
        active_vessel = editor.current_vessel

        for vessel, entry in editor.seeds.items():
            is_active = (vessel == active_vessel)
            base_alpha = 1.0 if is_active else 0.3
            color = VESSEL_COLORS.get(vessel, QColor(200, 200, 200))

            all_seeds = editor.get_all_seeds(vessel)
            has_ostium = entry["ostium"] is not None

            for flat_idx, seed_ijk in enumerate(all_seeds):
                sp = self._to_screen(seed_ijk)
                if sp is None:
                    continue

                sx, sy = sp

                # Determine seed type
                is_ostium = has_ostium and flat_idx == 0

                # Fill color with alpha
                fill = QColor(color)
                fill.setAlphaF(base_alpha)

                # White edge
                edge = QColor(255, 255, 255, int(255 * base_alpha))

                if is_ostium:
                    # Ostium: filled square, ~8px side
                    half = 4.0
                    pen = QPen(edge, 1.5)
                    painter.setPen(pen)
                    painter.setBrush(fill)
                    painter.drawRect(
                        QPointF(sx - half, sy - half).x(),
                        QPointF(sx - half, sy - half).y(),
                        half * 2,
                        half * 2,
                    )
                else:
                    # Waypoint: filled circle, ~6px diameter
                    radius = 3.0
                    pen = QPen(edge, 1.5)
                    painter.setPen(pen)
                    painter.setBrush(fill)
                    painter.drawEllipse(QPointF(sx, sy), radius, radius)

    def _draw_selection_highlight(self, painter: QPainter) -> None:
        """Draw a yellow ring around the currently selected seed."""
        if self._seed_editor is None:
            return

        editor = self._seed_editor
        vessel = editor.current_vessel
        if not vessel or editor.selection is None:
            return

        all_seeds = editor.get_all_seeds(vessel)
        if editor.selection < 0 or editor.selection >= len(all_seeds):
            return

        seed_ijk = all_seeds[editor.selection]
        sp = self._to_screen(seed_ijk)
        if sp is None:
            return

        sx, sy = sp
        radius = 7.0

        pen = QPen(QColor(255, 255, 0, 220), 2.0)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(QPointF(sx, sy), radius, radius)

    def _draw_centerlines(self, painter: QPainter) -> None:
        """Draw centerline splines for all vessels with slab-filtered breaks."""
        if self._seed_editor is None:
            return

        editor = self._seed_editor
        active_vessel = editor.current_vessel

        for vessel, cl in editor.centerlines.items():
            if cl is None or len(cl) < 2:
                continue

            is_active = (vessel == active_vessel)
            base_alpha = 0.8 if is_active else 0.3
            color = VESSEL_COLORS.get(vessel, QColor(200, 200, 200))
            line_color = QColor(color)
            line_color.setAlphaF(base_alpha)

            pen = QPen(line_color, 2.0)
            pen.setCapStyle(Qt.RoundCap)
            pen.setJoinStyle(Qt.RoundJoin)
            painter.setPen(pen)

            # Build a path with NaN-breaks for out-of-slab segments
            path = QPainterPath()
            in_segment = False

            for pt in cl:
                sp = self._to_screen(pt)
                if sp is None:
                    # Break the line
                    if in_segment:
                        painter.drawPath(path)
                        path = QPainterPath()
                        in_segment = False
                    continue

                sx, sy = sp
                if not in_segment:
                    path.moveTo(sx, sy)
                    in_segment = True
                else:
                    path.lineTo(sx, sy)

            if in_segment:
                painter.drawPath(path)
