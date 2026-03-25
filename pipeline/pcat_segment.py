"""
pcat_segment.py
Build the pericoronary adipose tissue (PCAT) VOI and apply FAI filtering.

Steps:
  1. Build tubular VOI mask around vessel centerline using one of two modes:
     - "crisp" (CRISP-CT): fixed gap + ring from vessel wall (Oikonomou 2018)
     - "scaled" (N×radius): outer boundary = N × mean vessel radius
  2. Subtract vessel lumen (inner boundary = vessel wall)
  3. Optionally apply HU filter for FAI: -190 to -30 HU
"""

from __future__ import annotations

from typing import List, Tuple, Dict, Any

import numpy as np
from scipy.ndimage import distance_transform_edt


# ─────────────────────────────────────────────
# Tubular VOI construction
# ─────────────────────────────────────────────

def build_tubular_voi(
    volume_shape: Tuple[int, int, int],
    centerline_ijk: np.ndarray,
    spacing_mm: List[float],
    radii_mm: np.ndarray,
    inner_margin_mm: float = 0.0,
    voi_mode: str = "crisp",
    crisp_gap_mm: float = 1.0,
    crisp_ring_mm: float = 3.0,
    radius_multiplier: float = 3.0,
) -> np.ndarray:
    """
    Build a binary tubular VOI mask around the centerline.

    Two VOI construction modes:

    **"crisp"** (CRISP-CT, Oikonomou et al. Lancet 2018):
      - inner boundary = mean_radius + crisp_gap_mm
      - outer boundary = mean_radius + crisp_gap_mm + crisp_ring_mm

    **"scaled"** (N×radius):
      - inner boundary = mean_radius + inner_margin_mm
      - outer boundary = mean_radius × radius_multiplier

    Parameters
    ----------
    volume_shape      : (Z, Y, X)
    centerline_ijk    : (N, 3) centerline voxel indices [z, y, x]
    spacing_mm        : [z, y, x]
    radii_mm          : (N,) per-point vessel radius in mm
    inner_margin_mm   : extra margin for inner boundary in "scaled" mode (default 0)
    voi_mode          : "crisp" or "scaled"
    crisp_gap_mm      : gap from vessel wall in "crisp" mode (default 1.0)
    crisp_ring_mm     : ring thickness in "crisp" mode (default 3.0)
    radius_multiplier : outer boundary multiplier in "scaled" mode (default 3.0)

    Returns
    -------
    voi_mask : (Z, Y, X) bool array — True inside the perivascular shell
    """
    sz, sy, sx = spacing_mm
    mean_radius_mm = float(np.mean(radii_mm))

    # Compute inner/outer boundaries based on VOI mode
    if voi_mode == "crisp":
        inner_mm = mean_radius_mm + crisp_gap_mm
        outer_mm = mean_radius_mm + crisp_gap_mm + crisp_ring_mm
    elif voi_mode == "scaled":
        inner_mm = mean_radius_mm + inner_margin_mm
        outer_mm = mean_radius_mm * radius_multiplier
    else:
        raise ValueError(f"Unknown voi_mode: {voi_mode!r}")

    # Determine bounding box around the centerline + max outer radius
    max_outer_mm = outer_mm
    margin_vox = np.array([
        int(np.ceil(max_outer_mm / sz)) + 2,
        int(np.ceil(max_outer_mm / sy)) + 2,
        int(np.ceil(max_outer_mm / sx)) + 2,
    ])

    lo = np.maximum(centerline_ijk.min(axis=0) - margin_vox, 0).astype(int)
    hi = np.minimum(centerline_ijk.max(axis=0) + margin_vox,
                    np.array(volume_shape) - 1).astype(int)

    # Subvolume dimensions
    sub_shape = tuple((hi - lo + 1).tolist())

    # Build binary mask of centerline points in subvolume
    cl_local = centerline_ijk - lo  # (N, 3) local coords

    cl_mask = np.zeros(sub_shape, dtype=bool)
    for pt in cl_local:
        z, y, x = int(pt[0]), int(pt[1]), int(pt[2])
        if 0 <= z < sub_shape[0] and 0 <= y < sub_shape[1] and 0 <= x < sub_shape[2]:
            cl_mask[z, y, x] = True

    # Distance transform from centerline (in mm)
    # EDT of the inverted centerline mask → each voxel's distance to nearest centerline point
    dist_mm = distance_transform_edt(~cl_mask, sampling=spacing_mm)  # mm

    # VOI: voxels between inner and outer shell
    voi_sub = (dist_mm >= inner_mm) & (dist_mm <= outer_mm)

    # Map back to full volume
    voi_full = np.zeros(volume_shape, dtype=bool)
    voi_full[lo[0]:hi[0]+1, lo[1]:hi[1]+1, lo[2]:hi[2]+1] = voi_sub

    return voi_full


def build_pcat_voi(
    volume_shape: Tuple[int, int, int],
    centerline_ijk: np.ndarray,
    spacing_mm: List[float],
    radii_mm: np.ndarray,
    pcat_scale: float = 3.0,
    inner_margin_mm: float = 0.0,
    voi_mode: str = "scaled",
    crisp_gap_mm: float = 1.0,
    crisp_ring_mm: float = 3.0,
) -> np.ndarray:
    """Build PCAT VOI — delegates to build_tubular_voi with appropriate mode."""
    return build_tubular_voi(
        volume_shape=volume_shape,
        centerline_ijk=centerline_ijk,
        spacing_mm=spacing_mm,
        radii_mm=radii_mm,
        inner_margin_mm=inner_margin_mm,
        voi_mode=voi_mode,
        crisp_gap_mm=crisp_gap_mm,
        crisp_ring_mm=crisp_ring_mm,
        radius_multiplier=pcat_scale,
    )


def build_vessel_mask(
    volume_shape: Tuple[int, int, int],
    centerline_ijk: np.ndarray,
    spacing_mm: List[float],
    radii_mm: np.ndarray,
) -> np.ndarray:
    """
    Build binary mask of the vessel lumen (inner tube, radius = mean_radius).
    Useful for visualization overlays.
    """
    sz, sy, sx = spacing_mm
    mean_radius_mm = float(np.mean(radii_mm))

    margin_vox = np.array([
        int(np.ceil(mean_radius_mm / sz)) + 2,
        int(np.ceil(mean_radius_mm / sy)) + 2,
        int(np.ceil(mean_radius_mm / sx)) + 2,
    ])
    lo = np.maximum(centerline_ijk.min(axis=0) - margin_vox, 0).astype(int)
    hi = np.minimum(centerline_ijk.max(axis=0) + margin_vox,
                    np.array(volume_shape) - 1).astype(int)
    sub_shape = tuple((hi - lo + 1).tolist())

    cl_local = centerline_ijk - lo
    cl_mask = np.zeros(sub_shape, dtype=bool)
    for pt in cl_local:
        z, y, x = int(pt[0]), int(pt[1]), int(pt[2])
        if 0 <= z < sub_shape[0] and 0 <= y < sub_shape[1] and 0 <= x < sub_shape[2]:
            cl_mask[z, y, x] = True

    dist_mm = distance_transform_edt(~cl_mask, sampling=spacing_mm)
    vessel_sub = dist_mm <= mean_radius_mm

    vessel_full = np.zeros(volume_shape, dtype=bool)
    vessel_full[lo[0]:hi[0]+1, lo[1]:hi[1]+1, lo[2]:hi[2]+1] = vessel_sub
    return vessel_full


# ─────────────────────────────────────────────
# FAI filtering (HU masking for fat)
# ─────────────────────────────────────────────

FAI_HU_MIN = -190.0
FAI_HU_MAX = -30.0
# FAI risk threshold — Oikonomou et al. Lancet 2018, validated in CRISP-CT (n=1,872)
# FAI > -70.1 HU → high cardiac mortality risk (HR = 9.04 for cardiac death)
FAI_RISK_THRESHOLD = -70.1

def apply_fai_filter(
    volume: np.ndarray,
    voi_mask: np.ndarray,
    hu_min: float = FAI_HU_MIN,
    hu_max: float = FAI_HU_MAX,
) -> np.ndarray:
    """
    Apply fat HU range filter within the VOI.

    Returns a float32 array where:
      - voxels in VOI AND in fat HU range → their HU value
      - all other voxels → NaN

    Parameters
    ----------
    volume   : (Z, Y, X) HU float32
    voi_mask : (Z, Y, X) bool — tubular VOI
    hu_min   : lower HU threshold for fat
    hu_max   : upper HU threshold for fat

    Returns
    -------
    fai_volume : (Z, Y, X) float32 with NaN outside fat region
    """
    fat_mask = (volume >= hu_min) & (volume <= hu_max) & voi_mask

    fai_volume = np.full(volume.shape, np.nan, dtype=np.float32)
    fai_volume[fat_mask] = volume[fat_mask]

    return fai_volume


# ─────────────────────────────────────────────
# Statistics
# ─────────────────────────────────────────────

def compute_pcat_stats(
    volume: np.ndarray,
    voi_mask: np.ndarray,
    vessel_name: str,
    hu_min: float = FAI_HU_MIN,
    hu_max: float = FAI_HU_MAX,
) -> Dict[str, Any]:
    """
    Compute PCAT statistics for a vessel VOI.

    Returns dict with:
      vessel, n_voi_voxels, n_fat_voxels, fat_fraction,
      hu_mean, hu_std, hu_median, hu_min, hu_max, hu_percentiles
    """
    hu_in_voi = volume[voi_mask]
    fat_voxels = hu_in_voi[(hu_in_voi >= hu_min) & (hu_in_voi <= hu_max)]
    hu_mean = float(np.mean(fat_voxels)) if len(fat_voxels) > 0 else float("nan")

    # FAI risk classification (Oikonomou 2018, CRISP-CT): > -70.1 HU = high risk
    if len(fat_voxels) > 0 and not np.isnan(hu_mean):
        fai_risk = "HIGH" if hu_mean > FAI_RISK_THRESHOLD else "LOW"
    else:
        fai_risk = "UNKNOWN"
    stats = {
        "vessel": vessel_name,
        "n_voi_voxels": int(voi_mask.sum()),
        "n_fat_voxels": int(len(fat_voxels)),
        "fat_fraction": float(len(fat_voxels) / max(voi_mask.sum(), 1)),
        "hu_mean": hu_mean,
        "hu_std": float(np.std(fat_voxels)) if len(fat_voxels) > 0 else float("nan"),
        "hu_median": float(np.median(fat_voxels)) if len(fat_voxels) > 0 else float("nan"),
        "hu_min_measured": float(np.min(fat_voxels)) if len(fat_voxels) > 0 else float("nan"),
        "hu_max_measured": float(np.max(fat_voxels)) if len(fat_voxels) > 0 else float("nan"),
        "hu_p25": float(np.percentile(fat_voxels, 25)) if len(fat_voxels) > 0 else float("nan"),
        "hu_p75": float(np.percentile(fat_voxels, 75)) if len(fat_voxels) > 0 else float("nan"),
        "FAI_HU_range": [hu_min, hu_max],
        "fai_risk_threshold_hu": FAI_RISK_THRESHOLD,
        "fai_risk": fai_risk,
        "fai_risk_note": "FAI > -70.1 HU = HIGH cardiac mortality risk (HR=9.04, Oikonomou 2018 / CRISP-CT)",
    }
    return stats


# ─────────────────────────────────────────────
# Angular asymmetry (per-octant FAI)
# ─────────────────────────────────────────────

_SECTOR_LABELS_8 = [
    "Anterior", "Anterior-Right", "Right", "Posterior-Right",
    "Posterior", "Posterior-Left", "Left", "Anterior-Left",
]


def compute_angular_asymmetry(
    volume: np.ndarray,
    centerline_ijk: np.ndarray,
    radii_mm: np.ndarray,
    spacing_mm: List[float],
    n_sectors: int = 8,
    hu_min: float = FAI_HU_MIN,
    hu_max: float = FAI_HU_MAX,
    voi_mode: str = "crisp",
    crisp_gap_mm: float = 1.0,
    crisp_ring_mm: float = 3.0,
    radius_multiplier: float = 3.0,
) -> dict:
    """Compute per-octant FAI along the vessel.

    For each cross-section position along the centerline, divides the
    pericoronary ring into n_sectors angular sectors. Computes mean HU
    in each sector.

    Parameters
    ----------
    volume          : (Z, Y, X) CT volume in HU
    centerline_ijk  : (N, 3) centerline voxel indices [z, y, x]
    radii_mm        : (N,) per-point vessel radius in mm
    spacing_mm      : [sz, sy, sx] voxel spacing
    n_sectors       : number of angular sectors (default 8 = octants)
    hu_min, hu_max  : FAI HU range
    voi_mode        : "crisp" or "scaled"
    crisp_gap_mm    : gap from vessel wall (crisp mode)
    crisp_ring_mm   : ring width (crisp mode)
    radius_multiplier: outer boundary multiplier (scaled mode)

    Returns
    -------
    dict with keys:
        "sectors"       : list of dicts, each with "angle_deg", "hu_mean",
                          "hu_std", "n_voxels", "fai_risk"
        "sector_labels" : list of str, human-readable labels
        "per_position"  : (N_positions, n_sectors) array of mean HU per
                          sector per position (for heatmap)
    """
    spacing = np.asarray(spacing_mm, dtype=np.float64)
    centerline_mm = centerline_ijk.astype(np.float64) * spacing

    n_pts = len(centerline_ijk)
    mean_radius = float(np.mean(radii_mm))

    # --- inner / outer radii (same logic as build_tubular_voi) ---
    if voi_mode == "crisp":
        inner_mm = mean_radius + crisp_gap_mm
        outer_mm = mean_radius + crisp_gap_mm + crisp_ring_mm
    elif voi_mode == "scaled":
        inner_mm = mean_radius
        outer_mm = mean_radius * radius_multiplier
    else:
        raise ValueError(f"Unknown voi_mode: {voi_mode!r}")

    # --- angular sampling setup ---
    n_angular = max(n_sectors * 4, 32)  # 4× oversampling per sector
    n_radial = 5
    angles = np.linspace(0, 2 * np.pi, n_angular, endpoint=False)
    radial_steps = np.linspace(inner_mm, outer_mm, n_radial)
    sector_width = 2 * np.pi / n_sectors
    # Pre-compute sector index for each angular sample
    sector_idx = (angles / sector_width).astype(int) % n_sectors

    # --- subsample centerline positions for efficiency ---
    step = max(1, n_pts // 60)  # ~60 cross-sections max
    sample_indices = np.arange(0, n_pts, step)
    n_positions = len(sample_indices)

    # Per-position, per-sector accumulators
    per_pos_hu = np.full((n_positions, n_sectors), np.nan, dtype=np.float64)
    # Global accumulators across all positions
    global_sector_vals: List[List[float]] = [[] for _ in range(n_sectors)]

    vol_shape = np.array(volume.shape, dtype=np.float64)

    for pos_i, ci in enumerate(sample_indices):
        pt_mm = centerline_mm[ci]

        # --- local coordinate frame via finite differences ---
        if ci == 0:
            tangent = centerline_mm[min(ci + 1, n_pts - 1)] - centerline_mm[ci]
        elif ci == n_pts - 1:
            tangent = centerline_mm[ci] - centerline_mm[ci - 1]
        else:
            tangent = centerline_mm[ci + 1] - centerline_mm[ci - 1]

        t_len = np.linalg.norm(tangent)
        if t_len < 1e-12:
            continue
        T = tangent / t_len

        # Stable normal: cross T with reference, fallback if near-parallel
        ref = np.array([0.0, 0.0, 1.0])
        if abs(np.dot(T, ref)) > 0.9:
            ref = np.array([0.0, 1.0, 0.0])
        N = np.cross(T, ref)
        n_len = np.linalg.norm(N)
        if n_len < 1e-12:
            continue
        N /= n_len
        B = np.cross(T, N)
        # B is already unit length (T and N are orthonormal)

        # --- sample ring voxels ---
        # Build all (angle, radius) sample points in the N-B plane
        # Shape: (n_angular, n_radial, 3) in mm
        cos_a = np.cos(angles)  # (n_angular,)
        sin_a = np.sin(angles)  # (n_angular,)

        # offsets_mm: (n_angular, n_radial, 3)
        # For each angle and radius: r * cos(a) * N + r * sin(a) * B
        # N_comp: (n_angular, 1, 3), R_comp: (n_angular, 1, 3)
        N_comp = cos_a[:, None, None] * N[None, None, :]  # (n_angular, 1, 3)
        B_comp = sin_a[:, None, None] * B[None, None, :]  # (n_angular, 1, 3)
        r_vals = radial_steps[None, :, None]              # (1, n_radial, 1)
        sample_mm = pt_mm + r_vals * (N_comp + B_comp)    # (n_angular, n_radial, 3)

        # Convert to voxel indices
        sample_ijk = sample_mm / spacing[None, None, :]   # (n_angular, n_radial, 3)
        sample_ijk_int = np.round(sample_ijk).astype(int)

        # Bounds check
        in_bounds = (
            (sample_ijk_int[:, :, 0] >= 0) & (sample_ijk_int[:, :, 0] < volume.shape[0]) &
            (sample_ijk_int[:, :, 1] >= 0) & (sample_ijk_int[:, :, 1] < volume.shape[1]) &
            (sample_ijk_int[:, :, 2] >= 0) & (sample_ijk_int[:, :, 2] < volume.shape[2])
        )  # (n_angular, n_radial)

        # Sector accumulation for this position
        sector_sums = np.zeros(n_sectors, dtype=np.float64)
        sector_counts = np.zeros(n_sectors, dtype=np.int64)

        for ai in range(n_angular):
            si = sector_idx[ai]
            for ri in range(n_radial):
                if not in_bounds[ai, ri]:
                    continue
                z, y, x = sample_ijk_int[ai, ri]
                hu = float(volume[z, y, x])
                if hu_min <= hu <= hu_max:
                    sector_sums[si] += hu
                    sector_counts[si] += 1
                    global_sector_vals[si].append(hu)

        # Per-position mean HU per sector
        for si in range(n_sectors):
            if sector_counts[si] > 0:
                per_pos_hu[pos_i, si] = sector_sums[si] / sector_counts[si]

    # --- aggregate global sector statistics ---
    sector_labels = (
        _SECTOR_LABELS_8 if n_sectors == 8
        else [f"Sector {i}" for i in range(n_sectors)]
    )
    sectors: List[Dict[str, Any]] = []
    for si in range(n_sectors):
        vals = np.array(global_sector_vals[si], dtype=np.float64)
        n_vox = len(vals)
        if n_vox > 0:
            mean_hu = float(np.mean(vals))
            std_hu = float(np.std(vals))
            risk = "HIGH" if mean_hu > FAI_RISK_THRESHOLD else "LOW"
        else:
            mean_hu = float("nan")
            std_hu = float("nan")
            risk = "UNKNOWN"
        angle_center = (si + 0.5) * (360.0 / n_sectors)
        sectors.append({
            "angle_deg": angle_center,
            "hu_mean": mean_hu,
            "hu_std": std_hu,
            "n_voxels": n_vox,
            "fai_risk": risk,
        })

    return {
        "sectors": sectors,
        "sector_labels": sector_labels,
        "per_position": per_pos_hu,
    }
