"""Export CPR views as DICOM Secondary Capture images."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

import numpy as np


def export_cpr_as_dicom(
    cpr_image: np.ndarray,
    output_path: Path,
    patient_id: str = "",
    study_date: str = "",
    series_description: str = "CPR",
    vessel_name: str = "",
    window: float = 800.0,
    level: float = 200.0,
    study_instance_uid: str = "",
) -> None:
    """Export a CPR image as a DICOM Secondary Capture.

    Parameters
    ----------
    cpr_image : (rows, cols) float32 HU values
    output_path : path for the output .dcm file
    patient_id, study_date : patient metadata
    series_description : DICOM series description
    vessel_name : vessel name for annotation
    window, level : display window/level
    """
    try:
        import pydicom
        from pydicom.dataset import FileDataset
        from pydicom.uid import generate_uid, ExplicitVRLittleEndian
    except ImportError:
        raise RuntimeError(
            "pydicom is required for DICOM export. Install with: pip install pydicom"
        )

    # Apply window/level to get uint16 pixel data
    low = level - window / 2.0
    high = level + window / 2.0
    scaled = np.clip((cpr_image - low) / (high - low), 0.0, 1.0)
    pixel_data = (scaled * 65535).astype(np.uint16)

    rows, cols = pixel_data.shape

    # Create DICOM dataset
    file_meta = pydicom.Dataset()
    file_meta.MediaStorageSOPClassUID = "1.2.840.10008.5.1.4.1.1.7"  # SC
    file_meta.MediaStorageSOPInstanceUID = generate_uid()
    file_meta.TransferSyntaxUID = ExplicitVRLittleEndian

    ds = FileDataset(
        str(output_path), {}, file_meta=file_meta, preamble=b"\x00" * 128
    )

    # Patient
    ds.PatientName = patient_id
    ds.PatientID = patient_id

    # Study
    ds.StudyDate = study_date.replace("-", "")
    ds.StudyTime = ""
    ds.StudyInstanceUID = study_instance_uid or generate_uid()
    ds.StudyDescription = "PCAT Analysis"

    # Series
    ds.SeriesInstanceUID = generate_uid()
    ds.SeriesDescription = (
        f"{series_description} - {vessel_name}"
        if vessel_name
        else series_description
    )
    ds.SeriesNumber = 9000
    ds.Modality = "OT"  # Other

    # Instance
    ds.SOPClassUID = "1.2.840.10008.5.1.4.1.1.7"
    ds.SOPInstanceUID = file_meta.MediaStorageSOPInstanceUID
    ds.InstanceNumber = 1

    # Image
    ds.Rows = rows
    ds.Columns = cols
    ds.BitsAllocated = 16
    ds.BitsStored = 16
    ds.HighBit = 15
    ds.SamplesPerPixel = 1
    ds.PhotometricInterpretation = "MONOCHROME2"
    ds.PixelRepresentation = 0  # unsigned
    ds.PixelData = pixel_data.tobytes()

    # W/L
    ds.WindowCenter = str(int(level))
    ds.WindowWidth = str(int(window))

    # Content date/time
    now = datetime.now()
    ds.ContentDate = now.strftime("%Y%m%d")
    ds.ContentTime = now.strftime("%H%M%S")

    ds.save_as(str(output_path))


def export_cpr_series(
    cpr_images: Dict[str, np.ndarray],
    output_dir: Path,
    patient_id: str = "",
    study_date: str = "",
    window: float = 800.0,
    level: float = 200.0,
) -> list:
    """Export all vessel CPR images as DICOM files.

    Returns list of output file paths.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Share a single StudyInstanceUID so PACS groups all vessels together
    try:
        from pydicom.uid import generate_uid
        shared_study_uid = generate_uid()
    except ImportError:
        shared_study_uid = ""

    paths = []
    for vessel, img in cpr_images.items():
        if img is None:
            continue
        out_path = output_dir / f"CPR_{vessel}.dcm"
        export_cpr_as_dicom(
            img,
            out_path,
            patient_id=patient_id,
            study_date=study_date,
            vessel_name=vessel,
            window=window,
            level=level,
            study_instance_uid=shared_study_uid,
        )
        paths.append(out_path)

    return paths
