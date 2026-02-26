"""
test_dicom_loader.py
Tests for dicom_loader.py module.
"""

import sys
from pathlib import Path
import pytest
import numpy as np
import pydicom
from pydicom.dataset import Dataset, FileMetaDataset
from pydicom.uid import ExplicitVRLittleEndian

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from pipeline.dicom_loader import load_dicom_series, voxel_to_world, world_to_voxel


def make_dicom_slice(z_pos: float, pixel_data: np.ndarray, out_path: Path):
    """Helper to create a minimal DICOM file for testing."""
    file_meta = FileMetaDataset()
    file_meta.MediaStorageSOPClassUID = "1.2.840.10008.5.1.4.1.1.2"  # CT Image Storage
    file_meta.MediaStorageSOPInstanceUID = pydicom.uid.generate_uid()
    file_meta.TransferSyntaxUID = ExplicitVRLittleEndian

    ds = Dataset()
    ds.file_meta = file_meta
    # Note: is_implicit_VR and is_little_endian are deprecated
    # but kept for compatibility with older pydicom versions

    ds.SOPClassUID = "1.2.840.10008.5.1.4.1.1.2"
    ds.SOPInstanceUID = pydicom.uid.generate_uid()
    ds.Modality = "CT"
    ds.Rows = pixel_data.shape[0]
    ds.Columns = pixel_data.shape[1]
    ds.PixelSpacing = [0.5, 0.5]
    ds.SliceThickness = 1.0
    ds.ImagePositionPatient = [0.0, 0.0, z_pos]
    ds.InstanceNumber = int(z_pos)
    ds.RescaleSlope = 1.0
    ds.RescaleIntercept = -1024.0
    ds.BitsAllocated = 16
    ds.BitsStored = 16
    ds.HighBit = 15
    ds.PixelRepresentation = 0  # unsigned
    ds.SamplesPerPixel = 1
    ds.PhotometricInterpretation = "MONOCHROME2"
    ds.PatientID = "TEST001"
    ds.StudyDescription = "Test CT"
    ds.SeriesDescription = "Test Series"
    ds.PixelData = pixel_data.astype(np.uint16).tobytes()

    pydicom.dcmwrite(str(out_path), ds, enforce_file_format=True)


@pytest.fixture
def dicom_dir(tmp_path):
    """Create a temporary directory with synthetic DICOM files."""
    dicom_path = tmp_path / "dicoms"
    dicom_path.mkdir()
    
    # Create 5 synthetic slices
    rng = np.random.default_rng(42)
    for i in range(5):
        pixel_data = rng.integers(0, 4096, size=(32, 32), dtype=np.uint16)
        dicom_file = dicom_path / f"slice_{i:03d}.dcm"
        make_dicom_slice(float(i), pixel_data, dicom_file)
    
    return dicom_path


@pytest.fixture
def empty_dicom_dir(tmp_path):
    """Create an empty DICOM directory for error testing."""
    empty_path = tmp_path / "empty"
    empty_path.mkdir()
    return empty_path


def test_load_returns_correct_shape(dicom_dir):
    """Test that loaded volume has expected shape."""
    volume, meta = load_dicom_series(dicom_dir)
    assert volume.shape == (5, 32, 32)


def test_load_returns_float32(dicom_dir):
    """Test that volume is float32."""
    volume, meta = load_dicom_series(dicom_dir)
    assert volume.dtype == np.float32


def test_hu_conversion_applied(dicom_dir):
    """Test that HU conversion is applied correctly."""
    volume, meta = load_dicom_series(dicom_dir)
    # Check that some values are > 0 (after adding intercept)
    assert np.any(volume > 0)
    # Check that values are in reasonable HU range
    assert np.all(volume >= -1024)  # minimum possible with intercept


def test_spacing_mm_extracted(dicom_dir):
    """Test that spacing_mm is extracted correctly."""
    volume, meta = load_dicom_series(dicom_dir)
    expected_spacing = [1.0, 0.5, 0.5]  # [z, y, x]
    np.testing.assert_array_almost_equal(meta["spacing_mm"], expected_spacing)


def test_meta_keys_present(dicom_dir):
    """Test that all required metadata keys are present."""
    volume, meta = load_dicom_series(dicom_dir)
    required_keys = [
        "patient_dir", "patient_id", "study_description", "series_description",
        "n_slices", "rows", "cols", "spacing_mm", "origin_mm", "orientation",
        "rescale_intercept", "rescale_slope", "z_positions", "shape"
    ]
    for key in required_keys:
        assert key in meta


def test_z_positions_sorted(dicom_dir):
    """Test that z_positions are monotonically increasing."""
    volume, meta = load_dicom_series(dicom_dir)
    z_positions = meta["z_positions"]
    assert all(z_positions[i] <= z_positions[i+1] for i in range(len(z_positions)-1))


def test_no_dcm_files_raises(empty_dicom_dir):
    """Test that FileNotFoundError is raised for empty directory."""
    with pytest.raises(FileNotFoundError):
        load_dicom_series(empty_dicom_dir)


def test_voxel_to_world_roundtrip(dicom_dir):
    """Test roundtrip conversion between voxel and world coordinates."""
    volume, meta = load_dicom_series(dicom_dir)
    
    # Test a few sample points
    test_points = [
        [1, 10, 15],
        [3, 20, 25],
        [0, 5, 30]
    ]
    
    for pt in test_points:
        world_pt = voxel_to_world(pt, meta)
        voxel_pt = world_to_voxel(world_pt, meta)
        
        # Allow 1 voxel tolerance due to rounding
        np.testing.assert_array_less(np.abs(voxel_pt - pt), 1.5)


def test_voxel_to_world_shape_single(dicom_dir):
    """Test that single point conversion returns (3,) shape, not (1, 3)."""
    volume, meta = load_dicom_series(dicom_dir)
    world_pt = voxel_to_world([1, 10, 15], meta)
    assert world_pt.shape == (3,)


def test_voxel_to_world_shape_multiple(dicom_dir):
    """Test that multiple points conversion preserves shape."""
    volume, meta = load_dicom_series(dicom_dir)
    test_points = [[1, 10, 15], [3, 20, 25]]
    world_pts = voxel_to_world(test_points, meta)
    assert world_pts.shape == (2, 3)


def test_world_to_voxel_shape_single(dicom_dir):
    """Test that single point conversion returns (3,) shape, not (1, 3)."""
    volume, meta = load_dicom_series(dicom_dir)
    voxel_pt = world_to_voxel([0.0, 5.0, 7.5], meta)
    assert voxel_pt.shape == (3,)


def test_world_to_voxel_shape_multiple(dicom_dir):
    """Test that multiple points conversion preserves shape."""
    volume, meta = load_dicom_series(dicom_dir)
    test_points = [[0.0, 5.0, 7.5], [2.0, 10.0, 12.5]]
    voxel_pts = world_to_voxel(test_points, meta)
    assert voxel_pts.shape == (2, 3)


def test_patient_id_extraction(dicom_dir):
    """Test that patient ID is extracted correctly."""
    volume, meta = load_dicom_series(dicom_dir)
    assert meta["patient_id"] == "TEST001"


def test_study_series_description(dicom_dir):
    """Test that study and series descriptions are extracted."""
    volume, meta = load_dicom_series(dicom_dir)
    assert meta["study_description"] == "Test CT"
    assert meta["series_description"] == "Test Series"