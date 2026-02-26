"""
conftest.py
Shared pytest fixtures for synthetic CT data and test utilities.
"""

import numpy as np
import pytest
from pathlib import Path


@pytest.fixture
def small_volume():
    """Create a (20, 64, 64) float32 numpy array with synthetic CT data."""
    rng = np.random.default_rng(42)
    volume = np.zeros((20, 64, 64), dtype=np.float32)
    
    # Fill background with muscle/soft tissue: N(50, 20) HU
    volume[:] = rng.normal(50, 20, size=volume.shape)
    
    # Create coordinates
    z, y, x = np.indices(volume.shape)
    
    # Vessel tube along Z-axis: centered at (y=32, x=32), radius 4 voxels
    # Fill with bright contrast HU (300-500 HU)
    vessel_mask = (y - 32)**2 + (x - 32)**2 <= 4**2
    volume[vessel_mask] = rng.uniform(300, 500, size=vessel_mask.sum())
    
    # Perivascular fat ring: 4-8 voxels from center, fill with fat HU [-150, -60]
    fat_mask = ((y - 32)**2 + (x - 32)**2 > 4**2) & ((y - 32)**2 + (x - 32)**2 <= 8**2)
    volume[fat_mask] = rng.uniform(-150, -60, size=fat_mask.sum())
    
    # Set background air at -1000 HU
    background_mask = ~vessel_mask & ~fat_mask
    volume[background_mask] = -1000.0
    
    return volume


@pytest.fixture
def small_meta():
    """Metadata dict matching the small_volume fixture."""
    return {
        "patient_dir": "/tmp/test_patient",
        "patient_id": "TEST001",
        "study_description": "Test CT",
        "series_description": "Test Series",
        "n_slices": 20,
        "rows": 64,
        "cols": 64,
        "spacing_mm": [1.0, 0.5, 0.5],   # [z, y, x]
        "origin_mm": [0.0, 0.0, 0.0],
        "orientation": [1, 0, 0, 0, 1, 0],
        "rescale_intercept": -1024.0,
        "rescale_slope": 1.0,
        "z_positions": list(np.arange(20) * 1.0),   # [0.0, 1.0, ..., 19.0]
        "shape": [20, 64, 64],
    }


@pytest.fixture
def simple_centerline():
    """Simple straight centerline along Z-axis through vessel center."""
    return np.array([[z, 32, 32] for z in range(2, 18)])


@pytest.fixture
def simple_radii():
    """Simple radii array with 2mm radius at each centerline point."""
    return np.full(16, 2.0)


@pytest.fixture
def tmp_output_dir(tmp_path):
    """A tmp_path-based fixture returning a Path."""
    return tmp_path