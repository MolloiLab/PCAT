"""
test_pcat_segment.py
Tests for pcat_segment.py module.
"""

import sys
from pathlib import Path
import pytest
import numpy as np

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from pipeline.pcat_segment import (
    build_tubular_voi, build_vessel_mask, apply_fai_filter, compute_pcat_stats
)

# Define local fixtures to avoid pytest resolution issues
@pytest.fixture
def simple_centerline():
    return np.array([[z, 32, 32] for z in range(2, 18)])

@pytest.fixture
def simple_radii():
    return np.full(16, 2.0)


def test_build_tubular_voi_shape(small_volume, small_meta, simple_centerline, simple_radii):
    """Test that output shape == volume_shape."""
    voi_mask = build_tubular_voi(
        small_volume.shape, simple_centerline, small_meta["spacing_mm"], simple_radii
    )
    assert voi_mask.shape == small_volume.shape


def test_build_tubular_voi_dtype(small_volume, small_meta, simple_centerline, simple_radii):
    """Test that output dtype == bool."""
    voi_mask = build_tubular_voi(
        small_volume.shape, simple_centerline, small_meta["spacing_mm"], simple_radii
    )
    assert voi_mask.dtype == bool


def test_build_tubular_voi_nonempty(small_volume, small_meta, simple_centerline, simple_radii):
    """Test that voi.sum() > 0."""
    voi_mask = build_tubular_voi(
        small_volume.shape, simple_centerline, small_meta["spacing_mm"], simple_radii
    )
    assert voi_mask.sum() > 0


def test_build_tubular_voi_inner_excluded(small_volume, small_meta, simple_centerline, simple_radii):
    """Test that centerline voxels are NOT in the VOI (since they're inside the vessel wall)."""
    voi_mask = build_tubular_voi(
        small_volume.shape, simple_centerline, small_meta["spacing_mm"], simple_radii
    )
    
    # Check that centerline points are not in VOI (they should be excluded)
    for pt in simple_centerline:
        z, y, x = pt.astype(int)
        if 0 <= z < voi_mask.shape[0] and 0 <= y < voi_mask.shape[1] and 0 <= x < voi_mask.shape[2]:
            assert not voi_mask[z, y, x]


def test_build_tubular_voi_outer_boundary(small_volume, small_meta, simple_centerline, simple_radii):
    """Test that voxels far outside the VOI are False."""
    voi_mask = build_tubular_voi(
        small_volume.shape, simple_centerline, small_meta["spacing_mm"], simple_radii
    )
    
    # Check a point far from the centerline
    far_point = [0, 0, 0]  # far from (32, 32)
    z, y, x = far_point
    assert not voi_mask[z, y, x]


def test_build_vessel_mask_shape(small_volume, small_meta, simple_centerline, simple_radii):
    """Test that shape == volume_shape."""
    vessel_mask = build_vessel_mask(
        small_volume.shape, simple_centerline, small_meta["spacing_mm"], simple_radii
    )
    assert vessel_mask.shape == small_volume.shape


def test_build_vessel_mask_dtype(small_volume, small_meta, simple_centerline, simple_radii):
    """Test that dtype == bool."""
    vessel_mask = build_vessel_mask(
        small_volume.shape, simple_centerline, small_meta["spacing_mm"], simple_radii
    )
    assert vessel_mask.dtype == bool


def test_build_vessel_mask_covers_centerline(small_volume, small_meta, simple_centerline, simple_radii):
    """Test that at least one centerline voxel is True in vessel mask."""
    vessel_mask = build_vessel_mask(
        small_volume.shape, simple_centerline, small_meta["spacing_mm"], simple_radii
    )
    
    # Check that at least one centerline point is in the vessel mask
    centerline_in_mask = False
    for pt in simple_centerline:
        z, y, x = pt.astype(int)
        if 0 <= z < vessel_mask.shape[0] and 0 <= y < vessel_mask.shape[1] and 0 <= x < vessel_mask.shape[2]:
            if vessel_mask[z, y, x]:
                centerline_in_mask = True
                break
    
    assert centerline_in_mask


def test_apply_fai_filter_shape(small_volume, simple_centerline, simple_radii):
    """Test that output shape == volume shape."""
    spacing_mm = [1.0, 0.5, 0.5]
    voi_mask = build_tubular_voi(small_volume.shape, simple_centerline, spacing_mm, simple_radii)
    
    fai_volume = apply_fai_filter(small_volume, voi_mask)
    assert fai_volume.shape == small_volume.shape


def test_apply_fai_filter_nan_outside_voi(small_volume, simple_centerline, simple_radii):
    """Test that all voxels outside VOI are NaN."""
    spacing_mm = [1.0, 0.5, 0.5]
    voi_mask = build_tubular_voi(small_volume.shape, simple_centerline, spacing_mm, simple_radii)
    
    fai_volume = apply_fai_filter(small_volume, voi_mask)
    
    # Check that voxels outside VOI are NaN
    outside_voi = ~voi_mask
    assert np.all(np.isnan(fai_volume[outside_voi]))


def test_apply_fai_filter_fat_preserved(small_volume, simple_centerline, simple_radii):
    """Test that known fat voxels (HU -100) within VOI are preserved."""
    spacing_mm = [1.0, 0.5, 0.5]
    voi_mask = build_tubular_voi(small_volume.shape, simple_centerline, spacing_mm, simple_radii)
    
    # Create a volume with known fat value
    volume_with_fat = small_volume.copy()
    z, y, x = np.indices(volume_with_fat.shape)
    
    # Create a small region of fat within the VOI area
    fat_region = (y == 32) & (x == 40) & (z >= 5) & (z <= 10)
    volume_with_fat[fat_region] = -100.0  # fat HU
    
    # Ensure this region is in VOI
    voi_mask[fat_region] = True
    
    fai_volume = apply_fai_filter(volume_with_fat, voi_mask)
    
    # Check that fat voxels are preserved (not NaN)
    assert np.all(fai_volume[fat_region] == -100.0)


def test_apply_fai_filter_nonfat_nan(small_volume, simple_centerline, simple_radii):
    """Test that non-fat voxels within VOI are NaN."""
    spacing_mm = [1.0, 0.5, 0.5]
    voi_mask = build_tubular_voi(small_volume.shape, simple_centerline, spacing_mm, simple_radii)
    
    # Create a volume with known non-fat value
    volume_with_muscle = small_volume.copy()
    z, y, x = np.indices(volume_with_muscle.shape)
    
    # Create a small region of muscle within the VOI area
    muscle_region = (y == 32) & (x == 40) & (z >= 12) & (z <= 17)
    volume_with_muscle[muscle_region] = 50.0  # muscle HU
    
    # Ensure this region is in VOI
    voi_mask[muscle_region] = True
    
    fai_volume = apply_fai_filter(volume_with_muscle, voi_mask)
    
    # Check that muscle voxels are NaN (not in FAI range)
    assert np.all(np.isnan(fai_volume[muscle_region]))


def test_apply_fai_filter_custom_range(small_volume, simple_centerline, simple_radii):
    """Test that custom FAI range works with hu_min=-180, hu_max=-40."""
    spacing_mm = [1.0, 0.5, 0.5]
    voi_mask = build_tubular_voi(small_volume.shape, simple_centerline, spacing_mm, simple_radii)
    
    # Create a volume with known values
    volume_with_values = small_volume.copy()
    z, y, x = np.indices(volume_with_values.shape)
    
    # Create regions with different HU values
    fat1_region = (y == 32) & (x == 40) & (z >= 5) & (z <= 7)
    fat2_region = (y == 32) & (x == 42) & (z >= 8) & (z <= 10)
    
    volume_with_values[fat1_region] = -190.0  # below custom range [-180, -40]
    volume_with_values[fat2_region] = -100.0  # in both ranges
    
    # Ensure these regions are in VOI
    voi_mask[fat1_region] = True
    voi_mask[fat2_region] = True
    
    fai_volume = apply_fai_filter(volume_with_values, voi_mask, hu_min=-180, hu_max=-40)
    
    # Check that only fat2 is preserved (in custom range)
    assert np.all(np.isnan(fai_volume[fat1_region]))
    assert np.all(fai_volume[fat2_region] == -100.0)


def test_compute_pcat_stats_keys(small_volume, simple_centerline, simple_radii):
    """Test that all required keys are present in output dict."""
    spacing_mm = [1.0, 0.5, 0.5]
    voi_mask = build_tubular_voi(small_volume.shape, simple_centerline, spacing_mm, simple_radii)
    
    stats = compute_pcat_stats(small_volume, voi_mask, "LAD")
    
    required_keys = [
        "vessel", "n_voi_voxels", "n_fat_voxels", "fat_fraction",
        "hu_mean", "hu_std", "hu_median", "hu_min_measured", "hu_max_measured",
        "hu_p25", "hu_p75", "FAI_HU_range"
    ]
    
    for key in required_keys:
        assert key in stats


def test_compute_pcat_stats_counts_positive(small_volume, simple_centerline, simple_radii):
    """Test that n_voi_voxels > 0."""
    spacing_mm = [1.0, 0.5, 0.5]
    voi_mask = build_tubular_voi(small_volume.shape, simple_centerline, spacing_mm, simple_radii)
    
    stats = compute_pcat_stats(small_volume, voi_mask, "LAD")
    assert stats["n_voi_voxels"] > 0


def test_compute_pcat_stats_fat_fraction_range(small_volume, simple_centerline, simple_radii):
    """Test that 0 <= fat_fraction <= 1."""
    spacing_mm = [1.0, 0.5, 0.5]
    voi_mask = build_tubular_voi(small_volume.shape, simple_centerline, spacing_mm, simple_radii)
    
    stats = compute_pcat_stats(small_volume, voi_mask, "LAD")
    assert 0.0 <= stats["fat_fraction"] <= 1.0


def test_compute_pcat_stats_hu_mean_in_range(small_volume, simple_centerline, simple_radii):
    """Test that hu_mean is between -190 and -30 (when fat voxels exist)."""
    spacing_mm = [1.0, 0.5, 0.5]
    voi_mask = build_tubular_voi(small_volume.shape, simple_centerline, spacing_mm, simple_radii)
    
    stats = compute_pcat_stats(small_volume, voi_mask, "LAD")
    
    if stats["n_fat_voxels"] > 0:
        assert -190.0 <= stats["hu_mean"] <= -30.0


def test_compute_pcat_stats_empty_voi(small_volume):
    """Test that handles all-False voi_mask without crashing."""
    empty_voi_mask = np.zeros(small_volume.shape, dtype=bool)
    
    # Should not raise an exception
    stats = compute_pcat_stats(small_volume, empty_voi_mask, "LAD")
    
    # Check basic stats for empty VOI
    assert stats["vessel"] == "LAD"
    assert stats["n_voi_voxels"] == 0
    assert stats["n_fat_voxels"] == 0
    assert stats["fat_fraction"] == 0.0
    assert np.isnan(stats["hu_mean"])


def test_build_tubular_voi_inner_margin(small_volume, simple_centerline, simple_radii):
    """Test that inner_margin_mm parameter works."""
    spacing_mm = [1.0, 0.5, 0.5]
    
    voi_mask_default = build_tubular_voi(
        small_volume.shape, simple_centerline, spacing_mm, simple_radii, inner_margin_mm=0.0
    )
    
    voi_mask_margin = build_tubular_voi(
        small_volume.shape, simple_centerline, spacing_mm, simple_radii, inner_margin_mm=1.0
    )
    
    # With margin, should have fewer voxels (inner boundary expanded)
    assert voi_mask_margin.sum() <= voi_mask_default.sum()