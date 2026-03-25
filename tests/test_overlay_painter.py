"""Tests for pcat_workstation.widgets.overlay_painter coordinate conversion."""

from __future__ import annotations

import numpy as np
import pytest

from pcat_workstation.widgets.overlay_painter import voxel_to_screen, SLAB_MM


# ---------------------------------------------------------------------------
# Fixtures — a typical small CT volume
# ---------------------------------------------------------------------------

SPACING = (1.0, 0.5, 0.5)        # sz, sy, sx
SHAPE = (20, 64, 64)             # Z, Y, X
WIDGET_SIZE = (400, 400)         # square widget for easy reasoning

# Camera focal point at the center of the volume (matching reset_camera)
FX = 64 * 0.5 / 2.0   # nx * sx / 2 = 16.0
FY = 64 * 0.5 / 2.0   # ny * sy / 2 = 16.0
FZ = 20 * 1.0 / 2.0   # nz * sz / 2 = 10.0
FOCAL_POINT = (FX, FY, FZ)


def _axial_parallel_scale():
    """Compute the parallel scale for axial view (fit-to-viewport).

    For a square widget (400x400), aspect=1.
    half_w = wx/2 = 16.0, half_h = wy/2 = 16.0
    scale = max(half_h, half_w/aspect) = max(16.0, 16.0) = 16.0
    """
    return 16.0


def _coronal_parallel_scale():
    """Parallel scale for coronal view.

    half_w = wx/2 = 16.0, half_h = wz/2 = 10.0
    scale = max(10.0, 16.0/1.0) = 16.0
    """
    return 16.0


def _sagittal_parallel_scale():
    """Parallel scale for sagittal view.

    half_w = wy/2 = 16.0, half_h = wz/2 = 10.0
    scale = max(10.0, 16.0/1.0) = 16.0
    """
    return 16.0


# ---------------------------------------------------------------------------
# Axial tests
# ---------------------------------------------------------------------------

class TestAxialCenterVoxel:
    """Center voxel in axial view should map to the center of the widget."""

    def test_center_voxel(self):
        # Center voxel: z=10, y=32, x=32
        # World: wx=32*0.5=16.0, wy=32*0.5=16.0, wz=10*1.0=10.0
        # Focal: (16, 16, 10) => offsets are zero => screen center
        result = voxel_to_screen(
            ijk=(10, 32, 32),
            orientation="axial",
            current_slice=10,
            spacing=SPACING,
            volume_shape=SHAPE,
            widget_size=WIDGET_SIZE,
            parallel_scale=_axial_parallel_scale(),
            focal_point=FOCAL_POINT,
        )
        assert result is not None
        px, py = result
        assert abs(px - 200.0) < 0.01, f"Expected px=200, got {px}"
        assert abs(py - 200.0) < 0.01, f"Expected py=200, got {py}"

    def test_offset_voxel_right(self):
        # Voxel shifted +1 in x (right on screen)
        # wx = 33*0.5 = 16.5, offset = 0.5mm
        # scale = 400 / (2*16) = 12.5 px/mm
        # screen_x = 0.5 * 12.5 + 200 = 206.25
        result = voxel_to_screen(
            ijk=(10, 32, 33),
            orientation="axial",
            current_slice=10,
            spacing=SPACING,
            volume_shape=SHAPE,
            widget_size=WIDGET_SIZE,
            parallel_scale=_axial_parallel_scale(),
            focal_point=FOCAL_POINT,
        )
        assert result is not None
        px, py = result
        assert abs(px - 206.25) < 0.01
        assert abs(py - 200.0) < 0.01

    def test_offset_voxel_up(self):
        # Voxel shifted -1 in y (y=31 => wy=15.5, offset = -0.5mm from center)
        # In DICOM, smaller Y = more anterior. ViewUp=(0,-1,0) means anterior at top.
        # Qt screen_y = (wy - fy) * scale + h/2 = (15.5 - 16.0) * 12.5 + 200 = 193.75
        # 193.75 < 200 => above center => anterior at top. Correct.
        result = voxel_to_screen(
            ijk=(10, 31, 32),
            orientation="axial",
            current_slice=10,
            spacing=SPACING,
            volume_shape=SHAPE,
            widget_size=WIDGET_SIZE,
            parallel_scale=_axial_parallel_scale(),
            focal_point=FOCAL_POINT,
        )
        assert result is not None
        px, py = result
        assert abs(px - 200.0) < 0.01
        assert abs(py - 193.75) < 0.01
        # Anterior (smaller y) should be above center (smaller screen_y)
        assert py < 200.0

    def test_origin_voxel(self):
        """Voxel (0,0,0) should map to top-left quadrant in axial view."""
        result = voxel_to_screen(
            ijk=(0, 0, 0),
            orientation="axial",
            current_slice=0,
            spacing=SPACING,
            volume_shape=SHAPE,
            widget_size=WIDGET_SIZE,
            parallel_scale=_axial_parallel_scale(),
            focal_point=FOCAL_POINT,
        )
        assert result is not None
        px, py = result
        # wx=0: screen_x = (0-16)*12.5 + 200 = -200+200 = 0
        # wy=0 (anterior): should be at top, screen_y < 200
        assert px < 200.0
        assert py < 200.0


class TestAxialSlab:
    """Slab filtering for axial view."""

    def test_on_slice_visible(self):
        """Point exactly on the current slice is visible."""
        result = voxel_to_screen(
            ijk=(10, 32, 32),
            orientation="axial",
            current_slice=10,
            spacing=SPACING,
            volume_shape=SHAPE,
            widget_size=WIDGET_SIZE,
            parallel_scale=_axial_parallel_scale(),
            focal_point=FOCAL_POINT,
        )
        assert result is not None

    def test_within_slab_visible(self):
        """Point within slab thickness is visible."""
        # z=11, slice=10, spacing_z=1.0 => distance=1.0mm <= SLAB_MM=2.0
        result = voxel_to_screen(
            ijk=(11, 32, 32),
            orientation="axial",
            current_slice=10,
            spacing=SPACING,
            volume_shape=SHAPE,
            widget_size=WIDGET_SIZE,
            parallel_scale=_axial_parallel_scale(),
            focal_point=FOCAL_POINT,
        )
        assert result is not None

    def test_at_slab_boundary_visible(self):
        """Point exactly at slab boundary is visible."""
        # z=12, slice=10, distance=2.0mm = SLAB_MM exactly => visible
        result = voxel_to_screen(
            ijk=(12, 32, 32),
            orientation="axial",
            current_slice=10,
            spacing=SPACING,
            volume_shape=SHAPE,
            widget_size=WIDGET_SIZE,
            parallel_scale=_axial_parallel_scale(),
            focal_point=FOCAL_POINT,
        )
        assert result is not None

    def test_outside_slab_invisible(self):
        """Point outside slab is invisible (returns None)."""
        # z=13, slice=10, distance=3.0mm > SLAB_MM=2.0 => None
        result = voxel_to_screen(
            ijk=(13, 32, 32),
            orientation="axial",
            current_slice=10,
            spacing=SPACING,
            volume_shape=SHAPE,
            widget_size=WIDGET_SIZE,
            parallel_scale=_axial_parallel_scale(),
            focal_point=FOCAL_POINT,
        )
        assert result is None

    def test_custom_slab_mm(self):
        """Custom slab thickness works."""
        # z=13, slice=10, distance=3.0mm; slab=5.0 => visible
        result = voxel_to_screen(
            ijk=(13, 32, 32),
            orientation="axial",
            current_slice=10,
            spacing=SPACING,
            volume_shape=SHAPE,
            widget_size=WIDGET_SIZE,
            parallel_scale=_axial_parallel_scale(),
            focal_point=FOCAL_POINT,
            slab_mm=5.0,
        )
        assert result is not None


# ---------------------------------------------------------------------------
# Coronal tests
# ---------------------------------------------------------------------------

class TestCoronalCenterVoxel:
    """Center voxel in coronal view maps to widget center."""

    def test_center_voxel(self):
        result = voxel_to_screen(
            ijk=(10, 32, 32),
            orientation="coronal",
            current_slice=32,
            spacing=SPACING,
            volume_shape=SHAPE,
            widget_size=WIDGET_SIZE,
            parallel_scale=_coronal_parallel_scale(),
            focal_point=FOCAL_POINT,
        )
        assert result is not None
        px, py = result
        assert abs(px - 200.0) < 0.01
        assert abs(py - 200.0) < 0.01

    def test_outside_slab(self):
        # y=40, slice=32, distance = (40-32)*0.5 = 4.0mm > 2.0
        result = voxel_to_screen(
            ijk=(10, 40, 32),
            orientation="coronal",
            current_slice=32,
            spacing=SPACING,
            volume_shape=SHAPE,
            widget_size=WIDGET_SIZE,
            parallel_scale=_coronal_parallel_scale(),
            focal_point=FOCAL_POINT,
        )
        assert result is None


# ---------------------------------------------------------------------------
# Sagittal tests
# ---------------------------------------------------------------------------

class TestSagittalCenterVoxel:
    """Center voxel in sagittal view maps to widget center."""

    def test_center_voxel(self):
        result = voxel_to_screen(
            ijk=(10, 32, 32),
            orientation="sagittal",
            current_slice=32,
            spacing=SPACING,
            volume_shape=SHAPE,
            widget_size=WIDGET_SIZE,
            parallel_scale=_sagittal_parallel_scale(),
            focal_point=FOCAL_POINT,
        )
        assert result is not None
        px, py = result
        assert abs(px - 200.0) < 0.01
        assert abs(py - 200.0) < 0.01

    def test_outside_slab(self):
        # x=40, slice=32, distance = (40-32)*0.5 = 4.0mm > 2.0
        result = voxel_to_screen(
            ijk=(10, 32, 40),
            orientation="sagittal",
            current_slice=32,
            spacing=SPACING,
            volume_shape=SHAPE,
            widget_size=WIDGET_SIZE,
            parallel_scale=_sagittal_parallel_scale(),
            focal_point=FOCAL_POINT,
        )
        assert result is None


# ---------------------------------------------------------------------------
# Zoom tests
# ---------------------------------------------------------------------------

class TestZoomEffect:
    """Smaller parallel_scale = zoomed in = larger screen offsets."""

    def test_zoom_in_increases_offset(self):
        """A point 1mm off-center should be farther from screen center when zoomed in."""
        # Voxel (10, 34, 32): y=34, wy=34*0.5=17.0, fy=16.0, offset=1mm
        base_scale = _axial_parallel_scale()  # 16.0
        zoomed_scale = base_scale / 2.0       # 8.0 (2x zoom)

        result_normal = voxel_to_screen(
            ijk=(10, 34, 32),
            orientation="axial",
            current_slice=10,
            spacing=SPACING,
            volume_shape=SHAPE,
            widget_size=WIDGET_SIZE,
            parallel_scale=base_scale,
            focal_point=FOCAL_POINT,
        )
        result_zoomed = voxel_to_screen(
            ijk=(10, 34, 32),
            orientation="axial",
            current_slice=10,
            spacing=SPACING,
            volume_shape=SHAPE,
            widget_size=WIDGET_SIZE,
            parallel_scale=zoomed_scale,
            focal_point=FOCAL_POINT,
        )

        assert result_normal is not None
        assert result_zoomed is not None

        # Distance from screen center (200, 200)
        dist_normal = abs(result_normal[1] - 200.0)
        dist_zoomed = abs(result_zoomed[1] - 200.0)

        # Zoomed in => larger offset from center
        assert dist_zoomed > dist_normal
        # Should be exactly 2x larger
        assert abs(dist_zoomed / dist_normal - 2.0) < 0.01

    def test_zoom_center_unchanged(self):
        """The center voxel stays at screen center regardless of zoom."""
        for ps in [16.0, 8.0, 4.0, 32.0]:
            result = voxel_to_screen(
                ijk=(10, 32, 32),
                orientation="axial",
                current_slice=10,
                spacing=SPACING,
                volume_shape=SHAPE,
                widget_size=WIDGET_SIZE,
                parallel_scale=ps,
                focal_point=FOCAL_POINT,
            )
            assert result is not None
            assert abs(result[0] - 200.0) < 0.01
            assert abs(result[1] - 200.0) < 0.01


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

class TestEdgeCases:
    def test_invalid_orientation(self):
        result = voxel_to_screen(
            ijk=(10, 32, 32),
            orientation="oblique",
            current_slice=10,
            spacing=SPACING,
            volume_shape=SHAPE,
            widget_size=WIDGET_SIZE,
            parallel_scale=16.0,
            focal_point=FOCAL_POINT,
        )
        assert result is None

    def test_zero_parallel_scale(self):
        result = voxel_to_screen(
            ijk=(10, 32, 32),
            orientation="axial",
            current_slice=10,
            spacing=SPACING,
            volume_shape=SHAPE,
            widget_size=WIDGET_SIZE,
            parallel_scale=0.0,
            focal_point=FOCAL_POINT,
        )
        assert result is None

    def test_zero_widget_height(self):
        result = voxel_to_screen(
            ijk=(10, 32, 32),
            orientation="axial",
            current_slice=10,
            spacing=SPACING,
            volume_shape=SHAPE,
            widget_size=(400, 0),
            parallel_scale=16.0,
            focal_point=FOCAL_POINT,
        )
        assert result is None


# ---------------------------------------------------------------------------
# Cross-orientation consistency
# ---------------------------------------------------------------------------

class TestCrossOrientation:
    """The same voxel projected via different orientations should give
    consistent positions for the shared screen axes."""

    def test_axial_and_coronal_share_x(self):
        """Both axial and coronal map world X to screen X. An offset in x
        should produce the same screen_x shift in both orientations."""
        # Voxel (10, 32, 34): x=34, wx=17.0, fx=16.0, offset=1mm
        result_axial = voxel_to_screen(
            ijk=(10, 32, 34),
            orientation="axial",
            current_slice=10,
            spacing=SPACING,
            volume_shape=SHAPE,
            widget_size=WIDGET_SIZE,
            parallel_scale=16.0,
            focal_point=FOCAL_POINT,
        )
        result_coronal = voxel_to_screen(
            ijk=(10, 32, 34),
            orientation="coronal",
            current_slice=32,
            spacing=SPACING,
            volume_shape=SHAPE,
            widget_size=WIDGET_SIZE,
            parallel_scale=16.0,
            focal_point=FOCAL_POINT,
        )
        assert result_axial is not None
        assert result_coronal is not None
        # Screen X should be the same
        assert abs(result_axial[0] - result_coronal[0]) < 0.01
