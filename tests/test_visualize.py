"""
test_visualize.py
Tests for visualize.py module.
"""

import sys
from pathlib import Path
import pytest
import numpy as np

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from pipeline.visualize import (
    render_cpr_fai, plot_hu_histogram, plot_radial_hu_profile, plot_summary,
    _fai_colormap, _compute_arclengths
)
from pipeline.pcat_segment import build_tubular_voi, apply_fai_filter

# Import fixtures from test_fixtures to avoid discovery issues
from tests.test_fixtures import simple_centerline, simple_radii, simple_voi_mask


def test_render_cpr_fai_creates_file(small_volume, simple_centerline, simple_radii, tmp_output_dir):
    """Test that output PNG exists and size > 1000 bytes."""
    spacing_mm = [1.0, 0.5, 0.5]
    vessel_name = "LAD"
    
    png_path = render_cpr_fai(
        small_volume, simple_centerline, simple_radii, spacing_mm,
        vessel_name, tmp_output_dir
    )
    
    assert png_path is not None
    assert png_path.exists()
    assert png_path.stat().st_size > 1000


def test_render_cpr_fai_returns_path(small_volume, simple_centerline, simple_radii, tmp_output_dir):
    """Test that return value is a Path."""
    spacing_mm = [1.0, 0.5, 0.5]
    vessel_name = "LAD"
    
    png_path = render_cpr_fai(
        small_volume, simple_centerline, simple_radii, spacing_mm,
        vessel_name, tmp_output_dir
    )
    
    assert isinstance(png_path, Path)


def test_render_cpr_fai_too_few_points_returns_none(tmp_output_dir):
    """Test that < 3 centerline points → returns None."""
    # Create centerline with only 2 points
    short_centerline = np.array([[0, 16, 16], [1, 16, 16]])
    radii = np.array([2.0, 2.0])
    volume = np.zeros((5, 32, 32), dtype=np.float32)
    spacing_mm = [1.0, 0.5, 0.5]
    
    png_path = render_cpr_fai(
        volume, short_centerline, radii, spacing_mm,
        "LAD", tmp_output_dir
    )
    
    assert png_path is None


def test_plot_hu_histogram_creates_file(small_volume, simple_voi_mask, tmp_output_dir):
    """Test that PNG exists and size > 1000 bytes."""
    vessel_name = "LAD"
    
    png_path = plot_hu_histogram(
        small_volume, simple_voi_mask, vessel_name, tmp_output_dir
    )
    
    assert png_path.exists()
    assert png_path.stat().st_size > 1000


def test_plot_hu_histogram_empty_voi(small_volume, tmp_output_dir):
    """Test that all-False simple_voi_mask → runs without error (no fat voxels edge case)."""
    empty_voi_mask = np.zeros(small_volume.shape, dtype=bool)
    vessel_name = "LAD"
    
    # Should not raise an exception
    png_path = plot_hu_histogram(
        small_volume, empty_voi_mask, vessel_name, tmp_output_dir
    )
    
    assert png_path.exists()


def test_plot_radial_hu_profile_creates_file(small_volume, simple_centerline, simple_radii, tmp_output_dir):
    """Test that PNG exists."""
    spacing_mm = [1.0, 0.5, 0.5]
    vessel_name = "LAD"
    
    png_path = plot_radial_hu_profile(
        small_volume, simple_centerline, simple_radii, spacing_mm,
        vessel_name, tmp_output_dir
    )
    
    assert png_path.exists()


def test_plot_radial_hu_profile_returns_path(small_volume, simple_centerline, simple_radii, tmp_output_dir):
    """Test that return value is a Path."""
    spacing_mm = [1.0, 0.5, 0.5]
    vessel_name = "LAD"
    
    png_path = plot_radial_hu_profile(
        small_volume, simple_centerline, simple_radii, spacing_mm,
        vessel_name, tmp_output_dir
    )
    
    assert isinstance(png_path, Path)


def test_plot_summary_creates_file(tmp_output_dir):
    """Test that PNG exists."""
    # Create sample vessel stats
    vessel_stats = {
        "LAD": {
            "vessel": "LAD",
            "n_voi_voxels": 1000,
            "n_fat_voxels": 300,
            "fat_fraction": 0.3,
            "hu_mean": -100.0,
            "hu_std": 20.0,
            "hu_median": -95.0,
            "hu_min_measured": -180.0,
            "hu_max_measured": -40.0,
            "hu_p25": -150.0,
            "hu_p75": -70.0,
            "FAI_HU_range": [-190.0, -30.0]
        }
    }
    
    png_path = plot_summary(vessel_stats, tmp_output_dir)
    
    assert png_path.exists()


def test_plot_summary_multiple_vessels(tmp_output_dir):
    """Test that handles 3 vessel stats dicts."""
    # Create sample vessel stats for 3 vessels
    vessel_stats = {
        "LAD": {
            "vessel": "LAD",
            "n_voi_voxels": 1000,
            "n_fat_voxels": 300,
            "fat_fraction": 0.3,
            "hu_mean": -100.0,
            "hu_std": 20.0,
            "hu_median": -95.0,
            "hu_min_measured": -180.0,
            "hu_max_measured": -40.0,
            "hu_p25": -150.0,
            "hu_p75": -70.0,
            "FAI_HU_range": [-190.0, -30.0]
        },
        "LCX": {
            "vessel": "LCX",
            "n_voi_voxels": 800,
            "n_fat_voxels": 200,
            "fat_fraction": 0.25,
            "hu_mean": -110.0,
            "hu_std": 25.0,
            "hu_median": -105.0,
            "hu_min_measured": -185.0,
            "hu_max_measured": -35.0,
            "hu_p25": -160.0,
            "hu_p75": -60.0,
            "FAI_HU_range": [-190.0, -30.0]
        },
        "RCA": {
            "vessel": "RCA",
            "n_voi_voxels": 1200,
            "n_fat_voxels": 360,
            "fat_fraction": 0.3,
            "hu_mean": -95.0,
            "hu_std": 18.0,
            "hu_median": -90.0,
            "hu_min_measured": -175.0,
            "hu_max_measured": -45.0,
            "hu_p25": -145.0,
            "hu_p75": -65.0,
            "FAI_HU_range": [-190.0, -30.0]
        }
    }
    
    png_path = plot_summary(vessel_stats, tmp_output_dir)
    
    assert png_path.exists()


def test_fai_colormap_valid():
    """Test that _fai_colormap() returns a valid matplotlib colormap."""
    cmap = _fai_colormap()
    
    # Check that it has the name attribute (matplotlib colormap property)
    assert hasattr(cmap, 'name')


def test_compute_arclengths_monotonic(simple_centerline):
    """Test that arc lengths are monotonically non-decreasing."""
    spacing_mm = [1.0, 0.5, 0.5]
    
    arclengths = _compute_arclengths(simple_centerline, spacing_mm)
    
    # Check that each value is >= the previous one
    for i in range(1, len(arclengths)):
        assert arclengths[i] >= arclengths[i-1]


def test_compute_arclengths_zero_start(simple_centerline):
    """Test that first value is 0.0."""
    spacing_mm = [1.0, 0.5, 0.5]
    
    arclengths = _compute_arclengths(simple_centerline, spacing_mm)
    
    assert arclengths[0] == 0.0


def test_compute_arclengths_shape(simple_centerline):
    """Test that output shape matches input length."""
    spacing_mm = [1.0, 0.5, 0.5]
    
    arclengths = _compute_arclengths(simple_centerline, spacing_mm)
    
    assert len(arclengths) == len(simple_centerline)


def test_plot_hu_histogram_fai_filtered(small_volume, simple_voi_mask, tmp_output_dir):
    """Test that histogram works with FAI-filtered data."""
    # Create volume with specific fat values
    volume_with_fat = small_volume.copy()
    volume_with_fat[simple_voi_mask] = -100.0  # Set VOI to fat value
    
    vessel_name = "LAD"
    
    png_path = plot_hu_histogram(
        volume_with_fat, simple_voi_mask, vessel_name, tmp_output_dir
    )
    
    assert png_path.exists()


def test_plot_radial_hu_profile_with_fat(small_volume, simple_centerline, simple_radii, tmp_output_dir):
    """Test that radial profile works when fat voxels are present."""
    # Create volume with fat ring around vessel
    spacing_mm = [1.0, 0.5, 0.5]
    volume_with_fat = small_volume.copy()
    
    # Add fat ring in the perivascular region
    z, y, x = np.indices(volume_with_fat.shape)
    fat_ring = ((y - 32)**2 + (x - 32)**2 > 4**2) & ((y - 32)**2 + (x - 32)**2 <= 8**2)
    volume_with_fat[fat_ring] = -100.0
    
    vessel_name = "LAD"
    
    png_path = plot_radial_hu_profile(
        volume_with_fat, simple_centerline, simple_radii, spacing_mm,
        vessel_name, tmp_output_dir
    )
    
    assert png_path.exists()


def test_render_cpr_fai_with_fai_data(small_volume, simple_centerline, simple_radii, simple_voi_mask, tmp_output_dir):
    """Test that CPR works with actual FAI-filtered data."""
    spacing_mm = [1.0, 0.5, 0.5]
    
    # Apply FAI filter to get fat-only volume
    fai_volume = apply_fai_filter(small_volume, simple_voi_mask)
    
    vessel_name = "LAD"
    
    png_path = render_cpr_fai(
        fai_volume, simple_centerline, simple_radii, spacing_mm,
        vessel_name, tmp_output_dir
    )
    
    assert png_path is not None
    assert png_path.exists()