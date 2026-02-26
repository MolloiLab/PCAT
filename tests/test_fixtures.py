"""
test_fixtures.py
Additional test fixtures to avoid pytest discovery issues.
"""

import numpy as np
import pytest


@pytest.fixture
def simple_centerline():
    """Simple straight centerline along Z-axis through vessel center."""
    return np.array([[z, 32, 32] for z in range(2, 18)])


@pytest.fixture
def simple_radii():
    """Simple radii array with 2mm radius at each centerline point."""
    return np.full(16, 2.0)


@pytest.fixture
def simple_voi_mask(small_volume, simple_centerline):
    """Create a simple VOI mask - a ring around the centerline."""
    from pipeline.pcat_segment import build_tubular_voi
    spacing_mm = [1.0, 0.5, 0.5]
    radii = np.full(len(simple_centerline), 2.0)
    
    # Create a ring-shaped VOI around the centerline
    return build_tubular_voi(small_volume.shape, simple_centerline, spacing_mm, radii)