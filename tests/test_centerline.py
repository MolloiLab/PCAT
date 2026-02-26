"""
test_centerline.py
Tests for centerline.py module.
"""

import sys
from pathlib import Path
import pytest
import numpy as np
import json

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from pipeline.centerline import (
    compute_vesselness, extract_centerline_seeds, clip_centerline_by_arclength,
    estimate_vessel_radii, load_seeds, VESSEL_CONFIGS
)


@pytest.fixture
def small_volume_with_vessel():
    """Create a small 20×32×32 volume with a bright tube along Z."""
    volume = np.full((20, 32, 32), -1000.0, dtype=np.float32)  # air background
    
    # Create a bright vessel tube along Z-axis
    z, y, x = np.indices(volume.shape)
    vessel_mask = (y - 16)**2 + (x - 16)**2 <= 3**2  # radius 3 voxels
    volume[vessel_mask] = 400.0  # bright contrast HU
    
    return volume


def test_compute_vesselness_shape(small_volume_with_vessel):
    """Test that vesselness output shape matches input shape."""
    spacing_mm = [1.0, 1.0, 1.0]
    vesselness = compute_vesselness(small_volume_with_vessel, spacing_mm)
    assert vesselness.shape == small_volume_with_vessel.shape


def test_compute_vesselness_range(small_volume_with_vessel):
    """Test that vesselness values are in [0, 1]."""
    spacing_mm = [1.0, 1.0, 1.0]
    vesselness = compute_vesselness(small_volume_with_vessel, spacing_mm)
    assert np.all(vesselness >= 0.0)
    assert np.all(vesselness <= 1.0)


def test_compute_vesselness_float32(small_volume_with_vessel):
    """Test that vesselness output is float32."""
    spacing_mm = [1.0, 1.0, 1.0]
    vesselness = compute_vesselness(small_volume_with_vessel, spacing_mm)
    assert vesselness.dtype == np.float32


def test_compute_vesselness_custom_sigmas(small_volume_with_vessel):
    """Test that custom sigmas work without error."""
    spacing_mm = [1.0, 1.0, 1.0]
    sigmas = [0.5, 1.0]
    vesselness = compute_vesselness(small_volume_with_vessel, spacing_mm, sigmas=sigmas)
    assert vesselness.shape == small_volume_with_vessel.shape


def test_extract_centerline_returns_ndarray(small_volume_with_vessel):
    """Test that extract_centerline returns numpy array."""
    spacing_mm = [1.0, 1.0, 1.0]
    vesselness = compute_vesselness(small_volume_with_vessel, spacing_mm)
    
    ostium_ijk = [2, 16, 16]
    waypoints_ijk = [[10, 16, 16]]
    
    centerline = extract_centerline_seeds(
        small_volume_with_vessel, vesselness, spacing_mm,
        ostium_ijk, waypoints_ijk
    )
    assert isinstance(centerline, np.ndarray)


def test_extract_centerline_shape(small_volume_with_vessel):
    """Test that centerline has shape (N, 3)."""
    spacing_mm = [1.0, 1.0, 1.0]
    vesselness = compute_vesselness(small_volume_with_vessel, spacing_mm)
    
    ostium_ijk = [2, 16, 16]
    waypoints_ijk = [[10, 16, 16]]
    
    centerline = extract_centerline_seeds(
        small_volume_with_vessel, vesselness, spacing_mm,
        ostium_ijk, waypoints_ijk
    )
    assert centerline.shape[1] == 3


def test_extract_centerline_starts_near_ostium(small_volume_with_vessel):
    """Test that first point is within 5 voxels of ostium."""
    spacing_mm = [1.0, 1.0, 1.0]
    vesselness = compute_vesselness(small_volume_with_vessel, spacing_mm)
    
    ostium_ijk = [2, 16, 16]
    waypoints_ijk = [[10, 16, 16]]
    
    centerline = extract_centerline_seeds(
        small_volume_with_vessel, vesselness, spacing_mm,
        ostium_ijk, waypoints_ijk
    )
    
    first_point = centerline[0]
    distance = np.linalg.norm(first_point - ostium_ijk)
    assert distance < 5.0


def test_extract_centerline_ends_near_waypoint(small_volume_with_vessel):
    """Test that last point is within 5 voxels of last waypoint."""
    spacing_mm = [1.0, 1.0, 1.0]
    vesselness = compute_vesselness(small_volume_with_vessel, spacing_mm)
    
    ostium_ijk = [2, 16, 16]
    waypoints_ijk = [[10, 16, 16]]
    
    centerline = extract_centerline_seeds(
        small_volume_with_vessel, vesselness, spacing_mm,
        ostium_ijk, waypoints_ijk
    )
    
    last_point = centerline[-1]
    last_waypoint = np.array(waypoints_ijk[-1])
    distance = np.linalg.norm(last_point - last_waypoint)
    assert distance < 5.0


def test_clip_centerline_length():
    """Test that clipped centerline arc-length ≈ requested length (within 10%)."""
    # Create a simple straight centerline
    centerline = np.array([[z, 0, 0] for z in range(20)])
    spacing_mm = [1.0, 1.0, 1.0]
    
    # Request 10mm length
    clipped = clip_centerline_by_arclength(centerline, spacing_mm, start_mm=0.0, length_mm=10.0)
    
    # Compute actual length
    diffs = np.diff(clipped, axis=0)
    seg_lengths = np.linalg.norm(diffs * spacing_mm, axis=1)
    actual_length = seg_lengths.sum()
    
    # Should be within 10% of requested length
    assert abs(actual_length - 10.0) < 1.0


def test_clip_centerline_start_offset():
    """Test RCA-style clip with start_mm=5.0 skips first 5mm."""
    # Create a simple straight centerline
    centerline = np.array([[z, 0, 0] for z in range(20)])
    spacing_mm = [1.0, 1.0, 1.0]
    
    # Clip with 5mm start offset
    clipped = clip_centerline_by_arclength(centerline, spacing_mm, start_mm=5.0, length_mm=10.0)
    
    # First point should be around index 5 (5mm along the line)
    first_z = clipped[0, 0]
    assert 4 <= first_z <= 6  # Allow some tolerance


def test_clip_centerline_empty_result_handled():
    """Test that if clip range is outside centerline, returns empty or short array."""
    # Create a short centerline
    centerline = np.array([[z, 0, 0] for z in range(5)])  # 5 points
    spacing_mm = [1.0, 1.0, 1.0]
    
    # Request length that's outside the centerline
    clipped = clip_centerline_by_arclength(centerline, spacing_mm, start_mm=100.0, length_mm=10.0)
    
    # Should return empty array or very short array
    assert len(clipped) <= 1


def test_estimate_vessel_radii_shape():
    """Test that radii shape matches centerline length."""
    volume = np.full((20, 32, 32), -100.0, dtype=np.float32)  # soft tissue background
    centerline = np.array([[z, 16, 16] for z in range(10)])
    spacing_mm = [1.0, 1.0, 1.0]
    
    radii = estimate_vessel_radii(volume, centerline, spacing_mm)
    assert radii.shape == (10,)


def test_estimate_vessel_radii_positive():
    """Test that all radii are positive."""
    # Create a volume with bright vessel
    volume = np.full((20, 32, 32), -100.0, dtype=np.float32)
    z, y, x = np.indices(volume.shape)
    vessel_mask = (y - 16)**2 + (x - 16)**2 <= 4**2
    volume[vessel_mask] = 400.0
    
    centerline = np.array([[z, 16, 16] for z in range(10)])
    spacing_mm = [1.0, 1.0, 1.0]
    
    radii = estimate_vessel_radii(volume, centerline, spacing_mm)
    assert np.all(radii > 0)


def test_estimate_vessel_radii_clamped():
    """Test that all radii are <= radius_search_mm param."""
    volume = np.full((20, 32, 32), -100.0, dtype=np.float32)
    centerline = np.array([[z, 16, 16] for z in range(10)])
    spacing_mm = [1.0, 1.0, 1.0]
    radius_search_mm = 5.0
    
    radii = estimate_vessel_radii(volume, centerline, spacing_mm, radius_search_mm=radius_search_mm)
    assert np.all(radii <= radius_search_mm)


def test_load_seeds_valid_json(tmp_path):
    """Test that load_seeds loads a temp JSON file and returns dict with LAD/LCX/RCA keys."""
    seeds_data = {
        "LAD": {
            "ostium_ijk": [10, 20, 30],
            "waypoints_ijk": [[15, 25, 35]],
            "segment_length_mm": 40.0
        },
        "LCX": {
            "ostium_ijk": [12, 22, 32],
            "waypoints_ijk": [[17, 27, 37]],
            "segment_length_mm": 40.0
        },
        "RCA": {
            "ostium_ijk": [14, 24, 34],
            "waypoints_ijk": [[19, 29, 39]],
            "segment_start_mm": 10.0,
            "segment_length_mm": 40.0
        }
    }
    
    seeds_file = tmp_path / "seeds.json"
    with open(seeds_file, 'w') as f:
        json.dump(seeds_data, f)
    
    loaded_seeds = load_seeds(seeds_file)
    
    assert isinstance(loaded_seeds, dict)
    assert "LAD" in loaded_seeds
    assert "LCX" in loaded_seeds
    assert "RCA" in loaded_seeds


def test_vessel_configs_present():
    """Test that VESSEL_CONFIGS has LAD, LCX, RCA keys."""
    assert "LAD" in VESSEL_CONFIGS
    assert "LCX" in VESSEL_CONFIGS
    assert "RCA" in VESSEL_CONFIGS