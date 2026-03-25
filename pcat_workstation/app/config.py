"""Configuration constants for PCAT Workstation."""

import os

# FAI thresholds (Antonopoulos et al., Sci Transl Med 2017)
FAI_HU_MIN = -190.0
FAI_HU_MAX = -30.0

# Risk threshold (Oikonomou et al., Lancet 2018, CRISP-CT)
FAI_RISK_THRESHOLD = -70.1  # HU, above this = HIGH risk (HR=9.04)

# Vessel segment definitions
VESSEL_CONFIGS = {
    "LAD": {"start_mm": 0.0, "length_mm": 40.0, "color": "#ff453a", "key": "1"},
    "LCx": {"start_mm": 0.0, "length_mm": 40.0, "color": "#0a84ff", "key": "2"},
    "RCA": {"start_mm": 10.0, "length_mm": 40.0, "color": "#30d158", "key": "3"},
}

# PCAT VOI geometry
DEFAULT_PCAT_SCALE = 3.0  # x mean vessel radius

# CRISP-CT VOI geometry (Oikonomou et al., Lancet 2018)
VOI_MODE = "crisp"  # "crisp" (fixed 1mm+3mm) or "scaled" (pcat_scale × r_eq)
CRISP_GAP_MM = 1.0   # gap from outer vessel wall
CRISP_RING_MM = 3.0   # ring width
N_ANGULAR_SECTORS = 8          # octants for asymmetry analysis

# CT display defaults (vascular window for coronary artery work)
DEFAULT_WINDOW_WIDTH = 800
DEFAULT_WINDOW_LEVEL = 200

# Pipeline stages (ordered)
PIPELINE_STAGES = [
    "import",
    "seeds",          # manual ostium placement (no auto)
    "centerlines",    # FMM + vesselness auto-trace
    "pcat_voi",       # tubular VOI (CRISP-CT or N×radius)
    "statistics",     # FAI + angular asymmetry
]

STAGE_LABELS = {
    "import": "Loading volume",
    "seeds": "Manual seed placement",
    "centerlines": "Fitting centerlines (spline through seeds)",
    "pcat_voi": "Building PCAT VOI",
    "statistics": "Computing FAI + angular asymmetry",
}

# Paths
DATA_DIR = os.path.expanduser("~/.pcat_workstation")
RECENT_PROJECTS_FILE = os.path.join(DATA_DIR, "recent_projects.json")
