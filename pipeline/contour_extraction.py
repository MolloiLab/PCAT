"""
contour_extraction.py

Polar-transform-based vessel wall contour extraction from cardiac CT cross-sections,
and contour-based VOI construction for PCAT analysis.

This module extracts the adventitial boundary (outer vessel wall) of coronary
arteries by sampling CT cross-sections in polar coordinates and detecting
the steepest HU gradient along each radial profile.

Key features:
  - Bishop frame (parallel transport) for stable cross-section orientation
  - Polar sampling with cubic B-spline interpolation
  - Gradient-based adventitial boundary detection
  - Chan-Vese level-set fallback for calcified/distal vessels
  - Non-circular contour preservation for accurate PCAT VOI construction
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Tuple

import numpy as np
from scipy.interpolate import CubicSpline
from scipy.ndimage import gaussian_filter1d, map_coordinates, distance_transform_edt
from scipy.signal import find_peaks


@dataclass
class ContourResult:
    """
    Result of vessel contour extraction.

    Attributes
    ----------
    contours : list of (n_angles, 3) arrays
        Cartesian contour points per centerline position in mm
    r_theta : (n_positions, n_angles) array
        Boundary radius vs angle in mm
    areas : (n_positions,) array
        Cross-section areas in mm²
    r_eq : (n_positions,) array
        Equivalent radii √(A/π) in mm
    positions_mm : (n_positions, 3) array
        Centerline mm positions
    N_frame : (n_positions, 3) array
        Normal vectors (Bishop frame)
    B_frame : (n_positions, 3) array
        Binormal vectors (Bishop frame)
    arclengths : (n_positions,) array
        Cumulative arc-lengths in mm
    fallback_mask : (n_positions,) array
        Boolean mask, True where Chan-Vese was used
    """
    contours: List[np.ndarray]
    r_theta: np.ndarray
    areas: np.ndarray
    r_eq: np.ndarray
    positions_mm: np.ndarray
    N_frame: np.ndarray
    B_frame: np.ndarray
    arclengths: np.ndarray
    fallback_mask: np.ndarray


# ─────────────────────────────────────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────────────────────────────────────

def extract_vessel_contours(
    volume: np.ndarray,
    centerline_ijk: np.ndarray,
    spacing_mm: List[float],
    vessel_name: str = "vessel",
    n_angles: int = 360,
    max_radius_mm: float = 8.0,
    min_radius_mm: float = 0.3,
    sigma_deg: float = 5.0,
) -> ContourResult:
    """
    Extract vessel wall contours from cardiac CT cross-sections.

    Main entry point for polar-transform-based contour extraction.
    Samples each cross-section in polar coordinates and detects the
    adventitial boundary as the steepest HU gradient along radial profiles.

    Parameters
    ----------
    volume : (Z, Y, X) float32
        CT HU volume
    centerline_ijk : (N, 3) float
        Centerline voxel indices [z, y, x]
    spacing_mm : [sz, sy, sx]
        Voxel spacing in mm
    vessel_name : str
        Vessel name for progress messages
    n_angles : int
        Number of angular samples (default 360)
    max_radius_mm : float
        Maximum sampling radius in mm (default 8.0)
    min_radius_mm : float
        Minimum valid boundary radius in mm (default 0.3)
    sigma_deg : float
        Gaussian smoothing sigma in degrees (default 5.0)

    Returns
    -------
    ContourResult
        Extracted contours and metadata
    """
    print(f"[contour] Extracting contours for {vessel_name}...")

    vox_size = np.array(spacing_mm, dtype=np.float64)
    n_positions = len(centerline_ijk)

    if n_positions < 2:
        raise ValueError(f"Need at least 2 centerline points, got {n_positions}")

    # Step 1: Compute Bishop frame at each centerline point
    positions_mm, N_frame, B_frame, tangents, arclengths = _compute_bishop_frame(
        centerline_ijk, spacing_mm
    )

    # Update n_positions after Bishop frame deduplication
    n_positions = len(positions_mm)

    # Step 2: Batch polar transform — sample ALL cross-sections in one map_coordinates call
    angles = np.linspace(0.0, 2.0 * np.pi, n_angles, endpoint=False)
    min_spacing = float(np.min(vox_size))
    n_radii = int(np.ceil(max_radius_mm / min_spacing)) + 1
    radii = np.linspace(0.0, max_radius_mm, n_radii)

    # Build sampling grid: (n_positions, n_angles, n_radii, 3) positions in mm
    theta_grid, r_grid = np.meshgrid(angles, radii, indexing='ij')  # (n_angles, n_radii)
    cos_theta = np.cos(theta_grid)  # (n_angles, n_radii)
    sin_theta = np.sin(theta_grid)  # (n_angles, n_radii)

    # Vectorized: positions[i] + r * (cos*N[i] + sin*B[i])
    pts_mm = (
        positions_mm[:, np.newaxis, np.newaxis, :]  # (P, 1, 1, 3)
        + r_grid[np.newaxis, :, :, np.newaxis] * (
            cos_theta[np.newaxis, :, :, np.newaxis] * N_frame[:, np.newaxis, np.newaxis, :]
            + sin_theta[np.newaxis, :, :, np.newaxis] * B_frame[:, np.newaxis, np.newaxis, :]
        )
    )  # (n_positions, n_angles, n_radii, 3)

    print(f"[contour] Sampling {n_positions * n_angles * n_radii:,} points "
          f"({n_positions} positions \u00d7 {n_angles} angles \u00d7 {n_radii} radii)...")

    # Single batched map_coordinates call using linear interpolation (order=1)
    all_polar = _sample_volume_linear(volume, vox_size, pts_mm)  # (P, n_angles, n_radii)

    # Step 3: Detect boundaries for each cross-section
    r_theta_all = np.zeros((n_positions, n_angles), dtype=np.float64)
    fallback_mask = np.zeros(n_positions, dtype=bool)

    for i in range(n_positions):
        polar_image = all_polar[i]  # (n_angles, n_radii)
        r_theta = _detect_adventitial_boundary(
            polar_image, radii, min_radius_mm=min_radius_mm
        )
        n_failed = int(np.sum(r_theta <= min_radius_mm))
        fail_fraction = n_failed / n_angles
        if fail_fraction > 0.3:
            r_theta = _chan_vese_fallback(
                volume, vox_size, positions_mm[i], N_frame[i], B_frame[i],
                polar_image, radii, angles,
                min_radius_mm=min_radius_mm,
                max_radius_mm=max_radius_mm,
            )
            fallback_mask[i] = True
        r_theta_all[i] = _smooth_contour(r_theta, sigma_deg=sigma_deg)

    # Step 4: Compute cross-section areas and equivalent radii
    areas = np.zeros(n_positions, dtype=np.float64)
    r_eq = np.zeros(n_positions, dtype=np.float64)
    contours: List[np.ndarray] = []

    for i in range(n_positions):
        r_theta = r_theta_all[i]
        N = N_frame[i]
        B = B_frame[i]
        center_mm = positions_mm[i]

        # Convert polar contour to Cartesian 3D points
        contour_pts = _contour_to_cartesian(r_theta, angles, center_mm, N, B)
        contours.append(contour_pts)

        # Compute area using shoelace formula in the (N, B) plane
        area = _compute_contour_area(r_theta, angles)
        areas[i] = area
        r_eq[i] = np.sqrt(area / np.pi)

    print(f"[contour] Extracted {n_positions} contours for {vessel_name}, "
          f"mean r_eq = {np.mean(r_eq):.2f} mm, "
          f"fallback = {np.sum(fallback_mask)} positions")

    return ContourResult(
        contours=contours,
        r_theta=r_theta_all,
        areas=areas,
        r_eq=r_eq,
        positions_mm=positions_mm,
        N_frame=N_frame,
        B_frame=B_frame,
        arclengths=arclengths,
        fallback_mask=fallback_mask,
    )


def build_contour_based_voi(
    volume_shape: Tuple[int, int, int],
    contours: List[np.ndarray],
    centerline_mm: np.ndarray,
    N_frame: np.ndarray,
    B_frame: np.ndarray,
    r_eq: np.ndarray,
    spacing_mm: List[float],
    pcat_scale: float = 3.0,
) -> np.ndarray:
    """
    Build PCAT VOI mask from extracted vessel contours.
    at each cross-section, following the actual non-circular contour shape.
    Strategy: rasterize vessel interior into 3D binary mask, then use EDT
    to get distance from vessel wall.  VOI = (dist > 0) & (dist <= d_pcat).
    This avoids per-voxel loops and runs in seconds.
    Parameters
    ----------
    volume_shape : (Z, Y, X)
        Shape of the CT volume
    contours : list of (n_angles, 3) arrays
        Cartesian contour points per centerline position in mm
    centerline_mm : (N, 3) array
        Centerline positions in mm
    N_frame : (N, 3) array
        Normal vectors
    B_frame : (N, 3) array
        Binormal vectors
    r_eq : (N,) array
        Equivalent radii in mm
    spacing_mm : [sz, sy, sx]
        Voxel spacing in mm
    pcat_scale : float
        VOI extends pcat_scale × r_eq from vessel wall (default 3.0)
    -------
    voi_mask : (Z, Y, X) bool
        PCAT VOI mask
    """
    print(f"[contour] Building contour-based VOI with pcat_scale={pcat_scale}...")
    vox_size = np.array(spacing_mm, dtype=np.float64)
    n_positions = len(centerline_mm)
    if n_positions == 0:
        return np.zeros(volume_shape, dtype=bool)

    # ── Step 1: Rasterize vessel interior into 3D mask ──────────────────
    mean_d_pcat = pcat_scale * float(np.mean(r_eq))

    # Compute overall bounding box
    centerline_vox = centerline_mm / vox_size[np.newaxis, :]
    max_outer_mm = float(np.max(r_eq)) + mean_d_pcat + float(np.max(vox_size)) * 2
    margin_vox = np.array([
        int(np.ceil(max_outer_mm / vox_size[0])) + 2,
        int(np.ceil(max_outer_mm / vox_size[1])) + 2,
        int(np.ceil(max_outer_mm / vox_size[2])) + 2,
    ])

    lo = np.maximum(np.floor(centerline_vox.min(axis=0) - margin_vox).astype(int), 0)
    hi = np.minimum(np.ceil(centerline_vox.max(axis=0) + margin_vox).astype(int),
                    np.array(volume_shape) - 1)

    sub_shape = tuple((hi - lo + 1).tolist())
    vessel_sub = np.zeros(sub_shape, dtype=bool)
    for i in range(n_positions):
        contour_pts = contours[i]  # (n_angles, 3) in mm
        center = centerline_mm[i]
        N = N_frame[i]
        B = B_frame[i]
        T = np.cross(N, B)
        T_norm = np.linalg.norm(T)
        if T_norm > 1e-8:
            T = T / T_norm
        r = r_eq[i]
        max_r = max(float(np.max(np.abs(contour_pts - center))), r) + float(np.max(vox_size))

        # Project contour onto (N, B) plane → 2D polygon
        rel_pts = contour_pts - center[np.newaxis, :]
        contour_2d = np.column_stack([rel_pts @ N, rel_pts @ B])

        # Bounding box for this cross-section
        center_vox_i = center / vox_size
        bbox_r = max_r
        z_lo_i = max(lo[0], int(np.floor(center_vox_i[0] - bbox_r / vox_size[0])) - 1)
        z_hi_i = min(hi[0], int(np.ceil(center_vox_i[0] + bbox_r / vox_size[0])) + 1)
        y_lo_i = max(lo[1], int(np.floor(center_vox_i[1] - bbox_r / vox_size[1])) - 1)
        y_hi_i = min(hi[1], int(np.ceil(center_vox_i[1] + bbox_r / vox_size[1])) + 1)
        x_lo_i = max(lo[2], int(np.floor(center_vox_i[2] - bbox_r / vox_size[2])) - 1)
        x_hi_i = min(hi[2], int(np.ceil(center_vox_i[2] + bbox_r / vox_size[2])) + 1)

        zz = np.arange(z_lo_i, z_hi_i + 1)
        yy = np.arange(y_lo_i, y_hi_i + 1)
        xx = np.arange(x_lo_i, x_hi_i + 1)
        if len(zz) == 0 or len(yy) == 0 or len(xx) == 0:
            continue

        Z, Y, X = np.meshgrid(
            zz * vox_size[0], yy * vox_size[1], xx * vox_size[2], indexing='ij'
        )

        dZ = Z - center[0]
        dY = Y - center[1]
        dX = X - center[2]

        # Tangential distance (to cross-section plane)
        t_dist = np.abs(dZ * T[0] + dY * T[1] + dX * T[2])
        t_threshold = 0.5 * float(np.max(vox_size))
        near_plane = t_dist <= t_threshold
        if not near_plane.any():
            continue

        # Project onto (N, B) plane
        n_proj = dZ * N[0] + dY * N[1] + dX * N[2]
        b_proj = dZ * B[0] + dY * B[1] + dX * B[2]

        # Point-in-polygon test
        inside = near_plane & _point_in_polygon(n_proj, b_proj, contour_2d)

        if inside.any():
            z_idx = np.broadcast_to((zz - lo[0])[:, None, None], Z.shape)
            y_idx = np.broadcast_to((yy - lo[1])[None, :, None], Y.shape)
            x_idx = np.broadcast_to((xx - lo[2])[None, None, :], X.shape)
            vessel_sub[z_idx[inside], y_idx[inside], x_idx[inside]] = True

    # ── Step 2: Distance transform from vessel boundary ────────────────
    print(f"[contour] Computing distance transform from vessel wall...")
    dist_from_wall = distance_transform_edt(~vessel_sub, sampling=spacing_mm)

    # ── Step 3: Build VOI as shell ────────────────────────────────────────
    voi_sub = (dist_from_wall > 0) & (dist_from_wall <= mean_d_pcat) & ~vessel_sub
    voi_mask = np.zeros(volume_shape, dtype=bool)
    voi_mask[lo[0]:hi[0]+1, lo[1]:hi[1]+1, lo[2]:hi[2]+1] = voi_sub

    n_voxels = int(voi_mask.sum())
    print(f"[contour] VOI built: {n_voxels:,} voxels, "
          f"vessel interior: {int(vessel_sub.sum()):,} voxels")

    return voi_mask


# ─────────────────────────────────────────────────────────────────────────────
# Internal functions
# ─────────────────────────────────────────────────────────────────────────────

def _compute_bishop_frame(
    centerline_ijk: np.ndarray,
    spacing_mm: List[float],
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Compute Bishop frame (parallel transport frame) at each centerline point.

    Unlike _sample_bezier_frame in visualize.py, this samples at the ORIGINAL
    centerline point positions (1:1 correspondence with input centerline_ijk),
    not at uniformly-spaced arc-length positions.

    Parameters
    ----------
    centerline_ijk : (N, 3) float
        Centerline voxel indices [z, y, x]
    spacing_mm : [sz, sy, sx]
        Voxel spacing in mm

    Returns
    -------
    positions_mm : (N, 3) array
        Centerline positions in mm
    N_frame : (N, 3) array
        Normal vectors (parallel-transported)
    B_frame : (N, 3) array
        Binormal vectors
    tangents : (N, 3) array
        Unit tangent vectors
    arclengths : (N,) array
        Cumulative arc-lengths in mm
    """
    vox_size = np.array(spacing_mm, dtype=np.float64)
    pts_mm = centerline_ijk.astype(np.float64) * vox_size[np.newaxis, :]
    n_pts = len(pts_mm)

    if n_pts < 2:
        raise ValueError(f"Need at least 2 points for Bishop frame, got {n_pts}")

    # Remove duplicate consecutive points
    unique = [pts_mm[0]]
    for p in pts_mm[1:]:
        if np.linalg.norm(p - unique[-1]) > 1e-6:
            unique.append(p)
    pts = np.array(unique, dtype=np.float64)
    n_unique = len(pts)

    if n_unique < 2:
        raise ValueError("Degenerate centerline — all points co-located")

    # Fit cubic spline through the points
    diffs = np.diff(pts, axis=0)
    seg_lens = np.linalg.norm(diffs, axis=1)
    s_param = np.concatenate([[0.0], np.cumsum(seg_lens)])
    total_len = float(s_param[-1])

    if total_len < 1e-3:
        raise ValueError(f"Degenerate centerline — total length {total_len:.4f} mm")

    cs = CubicSpline(s_param, pts, bc_type='not-a-knot')

    # Find arc-length parameter for each original centerline point
    # by projecting onto the spline
    positions_mm = pts.copy()  # Use original points directly

    # Compute tangents at each original point via spline derivative
    # Find the closest arc-length parameter for each point
    s_at_pts = np.zeros(n_unique, dtype=np.float64)
    for i in range(n_unique):
        # Find s that minimizes ||cs(s) - pts[i]||
        # Start with chord-length approximation
        s_at_pts[i] = s_param[i] if i < len(s_param) else total_len

    tangents_raw = cs(s_at_pts, 1)  # First derivative
    norms = np.linalg.norm(tangents_raw, axis=1, keepdims=True) + 1e-15
    tangents = tangents_raw / norms

    # Initialize normal vector
    # Choose world +Y, fallback to +X if aligned with tangent
    ref = np.array([0.0, 1.0, 0.0])
    if abs(np.dot(tangents[0], ref)) > 0.95:
        ref = np.array([1.0, 0.0, 0.0])

    n0 = np.cross(tangents[0], ref)
    n0_norm = np.linalg.norm(n0)
    if n0_norm < 1e-8:
        # Fallback: use another reference
        ref = np.array([0.0, 0.0, 1.0])
        n0 = np.cross(tangents[0], ref)
        n0_norm = np.linalg.norm(n0)
    n0 = n0 / (n0_norm + 1e-15)

    # Parallel transport (Bishop frame)
    N_frame = np.empty((n_unique, 3), dtype=np.float64)
    B_frame = np.empty((n_unique, 3), dtype=np.float64)
    N_frame[0] = n0
    b0 = np.cross(tangents[0], n0)
    b0_norm = np.linalg.norm(b0)
    B_frame[0] = b0 / (b0_norm + 1e-15) if b0_norm > 1e-8 else np.array([0.0, 0.0, 1.0])

    for i in range(1, n_unique):
        # Project previous normal onto plane perpendicular to new tangent
        ni = N_frame[i - 1] - np.dot(N_frame[i - 1], tangents[i]) * tangents[i]
        ni_norm = np.linalg.norm(ni)
        if ni_norm > 1e-8:
            N_frame[i] = ni / ni_norm
        else:
            N_frame[i] = N_frame[i - 1]
        bi = np.cross(tangents[i], N_frame[i])
        bi_norm = np.linalg.norm(bi)
        B_frame[i] = bi / (bi_norm + 1e-8) if bi_norm > 1e-8 else B_frame[i - 1]

    # Compute cumulative arc-lengths at original points
    diffs_orig = np.diff(positions_mm, axis=0)
    seg_lens_orig = np.linalg.norm(diffs_orig, axis=1)
    arclengths = np.concatenate([[0.0], np.cumsum(seg_lens_orig)])

    return positions_mm, N_frame, B_frame, tangents, arclengths


def _polar_transform_cross_section(
    volume: np.ndarray,
    vox_size: np.ndarray,
    center_mm: np.ndarray,
    N: np.ndarray,
    B: np.ndarray,
    n_angles: int = 360,
    max_radius_mm: float = 8.0,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Sample a cross-section in polar coordinates.

    Parameters
    ----------
    volume : (Z, Y, X) float32
        CT HU volume
    vox_size : (3,) [sz, sy, sx]
        Voxel spacing in mm
    center_mm : (3,)
        Cross-section center in mm
    N : (3,)
        Normal vector (Bishop frame)
    B : (3,)
        Binormal vector (Bishop frame)
    n_angles : int
        Number of angular samples
    max_radius_mm : float
        Maximum sampling radius in mm

    Returns
    -------
    polar_image : (n_angles, n_radii) float32
        Sampled HU values in polar coordinates
    angles : (n_angles,)
        Angular coordinates in radians [0, 2π)
    radii : (n_radii,)
        Radial coordinates in mm
    """
    # Determine radial resolution based on voxel size
    min_spacing = float(np.min(vox_size))
    n_radii = int(np.ceil(max_radius_mm / min_spacing)) + 1

    angles = np.linspace(0.0, 2.0 * np.pi, n_angles, endpoint=False)
    radii = np.linspace(0.0, max_radius_mm, n_radii)

    # Build sampling grid: (n_angles, n_radii, 3) positions in mm
    # Position = center + r * (cos(θ) * N + sin(θ) * B)
    theta_grid, r_grid = np.meshgrid(angles, radii, indexing='ij')  # (n_angles, n_radii)

    cos_theta = np.cos(theta_grid)
    sin_theta = np.sin(theta_grid)

    # Compute 3D positions
    pts_mm = (
        center_mm[np.newaxis, np.newaxis, :] +
        r_grid[:, :, np.newaxis] * (
            cos_theta[:, :, np.newaxis] * N[np.newaxis, np.newaxis, :] +
            sin_theta[:, :, np.newaxis] * B[np.newaxis, np.newaxis, :]
        )
    )  # (n_angles, n_radii, 3)

    # Sample volume using cubic interpolation
    polar_image = _sample_volume_cubic(volume, vox_size, pts_mm)  # (n_angles, n_radii)

    return polar_image, angles, radii


def _detect_adventitial_boundary(
    polar_image: np.ndarray,
    radii: np.ndarray,
    min_radius_mm: float = 0.3,
) -> np.ndarray:
    """
    Detect vessel outer wall (adventitial boundary) as gradient peak.
    For each angular profile, finds the steepest HU descent that represents
    the transition from contrast-enhanced lumen (~200-400 HU) to perivascular
    tissue (~-100 to 0 HU).  Uses half-maximum descent with gradient refinement.
    Parameters
    ----------
    polar_image : (n_angles, n_radii) float32
        HU values in polar coordinates
    radii : (n_radii,)
        Radial coordinates in mm
    min_radius_mm : float
        Minimum valid boundary radius (avoid detecting noise at center)
    -------
    r_theta : (n_angles,)
        Boundary radius at each angle in mm
    """
    n_angles, n_radii = polar_image.shape
    r_theta = np.full(n_angles, 1.5, dtype=np.float64)  # default fallback
    max_radius_mm = radii[-1] * 0.9
    min_idx = max(1, int(np.searchsorted(radii, min_radius_mm)))
    max_idx = min(n_radii - 1, int(np.searchsorted(radii, max_radius_mm)))

    # Handle NaN
    polar = np.nan_to_num(polar_image, nan=-1024.0).astype(np.float64)

    # Smooth radial profiles (Gaussian sigma=1 sample ~ 1 voxel)
    polar_smooth = gaussian_filter1d(polar, sigma=1.0, axis=1)

    # Compute radial gradient
    dr = float(radii[1] - radii[0]) if n_radii > 1 else 1.0
    gradient = np.gradient(polar_smooth, dr, axis=1)  # (n_angles, n_radii)
    for a in range(n_angles):
        profile = polar_smooth[a, :]
        grad = gradient[a, :]

        # Find lumen peak HU in inner region
        inner_max_idx = min(max_idx, min_idx + max(5, (max_idx - min_idx) // 3))
        lumen_peak = float(np.max(profile[min_idx:inner_max_idx]))

        # If lumen not bright, skip (not a vessel cross-section)
        if lumen_peak < 100:
            continue

        # Transition threshold: midpoint between lumen peak and background
        bg_estimate = float(np.median(profile[max(max_idx - 5, min_idx):max_idx]))
        transition_hu = (lumen_peak + bg_estimate) / 2.0

        # Method 1: Half-maximum descent
        below_transition = np.where(profile[min_idx:max_idx] < transition_hu)[0]

        if len(below_transition) > 0:
            boundary_idx = min_idx + below_transition[0]
            # Refine: find steepest gradient near this crossing
            search_lo = max(min_idx, boundary_idx - 3)
            search_hi = min(max_idx, boundary_idx + 3)
            local_grad = grad[search_lo:search_hi]
            if len(local_grad) > 0:
                steepest = search_lo + int(np.argmin(local_grad))
                r_theta[a] = radii[steepest]
            else:
                r_theta[a] = radii[boundary_idx]
        else:
            # Method 2: Steepest negative gradient in valid range
            valid_grad = grad[min_idx:max_idx]
            if len(valid_grad) > 0:
                steepest = min_idx + int(np.argmin(valid_grad))
                if grad[steepest] < -10:
                    r_theta[a] = radii[steepest]
    return r_theta


def _smooth_contour(
    r_theta: np.ndarray,
    sigma_deg: float = 5.0,
) -> np.ndarray:
    """
    Apply 1D Gaussian smoothing to r(θ) with wrap-around.

    Parameters
    ----------
    r_theta : (n_angles,)
        Boundary radius at each angle in mm
    sigma_deg : float
        Gaussian sigma in degrees

    Returns
    -------
    r_theta_smooth : (n_angles,)
        Smoothed boundary radii
    """
    n_angles = len(r_theta)
    # Convert sigma from degrees to samples
    sigma_samples = sigma_deg / (360.0 / n_angles)

    # Apply Gaussian filter with wrap-around mode
    r_theta_smooth = gaussian_filter1d(r_theta, sigma=sigma_samples, mode='wrap')

    return r_theta_smooth


def _chan_vese_fallback(
    volume: np.ndarray,
    vox_size: np.ndarray,
    center_mm: np.ndarray,
    N: np.ndarray,
    B: np.ndarray,
    polar_image: np.ndarray,
    radii: np.ndarray,
    angles: np.ndarray,
    min_radius_mm: float = 0.3,
    max_radius_mm: float = 8.0,
) -> np.ndarray:
    """
    Chan-Vese level-set segmentation fallback for difficult cases.

    Used when gradient-based detection fails (>30% of angles), typically
    in calcified or distal vessel segments.

    Parameters
    ----------
    volume : (Z, Y, X) float32
        CT HU volume
    vox_size : (3,) [sz, sy, sx]
        Voxel spacing in mm
    center_mm : (3,)
        Cross-section center in mm
    N : (3,)
        Normal vector
    B : (3,)
        Binormal vector
    polar_image : (n_angles, n_radii) float32
        Polar-transformed cross-section
    radii : (n_radii,)
        Radial coordinates in mm
    angles : (n_angles,)
        Angular coordinates in radians
    min_radius_mm : float
        Minimum valid boundary radius
    max_radius_mm : float
        Maximum sampling radius

    Returns
    -------
    r_theta : (n_angles,)
        Boundary radius at each angle in mm
    """
    try:
        from skimage.segmentation import chan_vese
    except ImportError:
        print("[contour] Warning: skimage not available for Chan-Vese, using default radius")
        return np.full(len(angles), 1.5, dtype=np.float64)

    n_angles = len(angles)
    n_radii = len(radii)

    # Create a Cartesian image for Chan-Vese
    # Sample a 2D grid in the (N, B) plane
    grid_size = min(100, int(max_radius_mm / np.min(vox_size) * 2))
    grid_extent = max_radius_mm

    n_coords = np.linspace(-grid_extent, grid_extent, grid_size)
    b_coords = np.linspace(-grid_extent, grid_extent, grid_size)
    n_grid, b_grid = np.meshgrid(n_coords, b_coords)  # (grid_size, grid_size)

    # Build 3D sampling points
    pts_mm = (
        center_mm[np.newaxis, np.newaxis, :] +
        n_grid[:, :, np.newaxis] * N[np.newaxis, np.newaxis, :] +
        b_grid[:, :, np.newaxis] * B[np.newaxis, np.newaxis, :]
    )  # (grid_size, grid_size, 3)

    # Sample the volume
    cart_image = _sample_volume_cubic(volume, vox_size, pts_mm)

    # Handle NaN
    cart_image = np.nan_to_num(cart_image, nan=-1024.0)

    # Run Chan-Vese segmentation
    try:
        cv_result = chan_vese(
            cart_image,
            mu=0.25,
            lambda1=1.0,
            lambda2=1.0,
            max_num_iter=200,
        )
        # cv_result is boolean mask: True = inside, False = outside
        segmentation = cv_result
    except Exception as e:
        print(f"[contour] Chan-Vese failed: {e}, using default radius")
        return np.full(n_angles, 1.5, dtype=np.float64)

    # Extract boundary contour from segmentation
    # Use morphological edge detection
    from scipy.ndimage import binary_erosion
    boundary = segmentation & ~binary_erosion(segmentation)

    # Convert boundary to polar r(θ)
    r_theta = np.zeros(n_angles, dtype=np.float64)

    for a in range(n_angles):
        theta = angles[a]
        cos_t, sin_t = np.cos(theta), np.sin(theta)

        # Find boundary points along this ray
        max_r = 0.0
        for r_idx in range(n_radii):
            r = radii[r_idx]
            # Convert polar to grid coordinates
            n_val = r * cos_t
            b_val = r * sin_t

            # Map to grid indices
            n_idx = int((n_val + grid_extent) / (2 * grid_extent) * (grid_size - 1))
            b_idx = int((b_val + grid_extent) / (2 * grid_extent) * (grid_size - 1))

            if 0 <= n_idx < grid_size and 0 <= b_idx < grid_size:
                if boundary[b_idx, n_idx]:
                    max_r = max(max_r, r)

        if max_r > min_radius_mm:
            r_theta[a] = max_r
        else:
            # Fallback: use distance from center to segmentation boundary
            r_theta[a] = 1.5

    return r_theta


def _contour_to_cartesian(
    r_theta: np.ndarray,
    angles: np.ndarray,
    center_mm: np.ndarray,
    N: np.ndarray,
    B: np.ndarray,
) -> np.ndarray:
    """
    Convert polar contour to 3D Cartesian points.

    Parameters
    ----------
    r_theta : (n_angles,)
        Boundary radius at each angle in mm
    angles : (n_angles,)
        Angular coordinates in radians
    center_mm : (3,)
        Cross-section center in mm
    N : (3,)
        Normal vector
    B : (3,)
        Binormal vector

    Returns
    -------
    contour_pts : (n_angles, 3) float64
        Cartesian contour points in mm
    """
    cos_theta = np.cos(angles)  # (n_angles,)
    sin_theta = np.sin(angles)  # (n_angles,)

    # Vectorized: center + r * (cos*N + sin*B)
    contour_pts = (
        center_mm[np.newaxis, :] +
        r_theta[:, np.newaxis] * (
            cos_theta[:, np.newaxis] * N[np.newaxis, :] +
            sin_theta[:, np.newaxis] * B[np.newaxis, :]
        )
    )  # (n_angles, 3)
    return contour_pts


# ─────────────────────────────────────────────────────────────────────────────
# Helper functions
# ─────────────────────────────────────────────────────────────────────────────

def _sample_volume_cubic(
    volume: np.ndarray,
    vox_size: np.ndarray,
    pts_mm: np.ndarray,
) -> np.ndarray:
    """
    Cubic interpolation of the CT volume at arbitrary mm positions.

    Uses order=3 (cubic B-spline) for C2-smooth results.

    Parameters
    ----------
    volume : (Z, Y, X) float32
        CT HU volume
    vox_size : (3,) [sz, sy, sx]
        Voxel spacing in mm
    pts_mm : (..., 3) float64
        Sample points in DICOM mm [z, y, x]

    Returns
    -------
    vals : (...) float32
        HU values; NaN for out-of-bounds points
    """
    shape_in = pts_mm.shape[:-1]
    pts_flat = pts_mm.reshape(-1, 3)  # (M, 3)

    # Convert mm → voxel coordinates
    pts_vox = pts_flat / vox_size[np.newaxis, :]  # (M, 3)
    z_v = pts_vox[:, 0]
    y_v = pts_vox[:, 1]
    x_v = pts_vox[:, 2]

    vol_shape = np.array(volume.shape, dtype=np.float64)

    # Cubic needs 2 voxels of margin; mark anything within 1 voxel of
    # the boundary as invalid to avoid edge ringing artifacts.
    margin = 1.0
    valid = (
        (z_v >= margin) & (z_v <= vol_shape[0] - 1 - margin) &
        (y_v >= margin) & (y_v <= vol_shape[1] - 1 - margin) &
        (x_v >= margin) & (x_v <= vol_shape[2] - 1 - margin)
    )

    # order=3 = cubic B-spline interpolation (C2-smooth)
    vals = map_coordinates(
        volume,
        [z_v, y_v, x_v],
        order=3,
        mode='nearest',
        cval=0.0,
    ).astype(np.float32)

    vals[~valid] = np.nan
    return vals.reshape(shape_in)

def _sample_volume_linear(
    volume: np.ndarray,
    vox_size: np.ndarray,
    pts_mm: np.ndarray,
) -> np.ndarray:
    """
    Linear interpolation of CT volume at arbitrary mm positions.

    Faster than cubic (_sample_volume_cubic) — uses order=1 B-spline.
    Used for batched polar transforms where speed matters more than
    C2 smoothness.

    Parameters
    ----------
    volume : (Z, Y, X) float32
        CT HU volume
    vox_size : (3,) [sz, sy, sx]
        Voxel spacing in mm
    pts_mm : (..., 3) float64
        Sample points in DICOM mm [z, y, x]

    Returns
    -------
    vals : (...) float32
        HU values; NaN for out-of-bounds points
    """
    shape_in = pts_mm.shape[:-1]
    pts_flat = pts_mm.reshape(-1, 3)

    # Convert mm → voxel coordinates
    pts_vox = pts_flat / vox_size[np.newaxis, :]
    z_v, y_v, x_v = pts_vox[:, 0], pts_vox[:, 1], pts_vox[:, 2]

    vol_shape = np.array(volume.shape, dtype=np.float64)
    valid = (
        (z_v >= 0) & (z_v <= vol_shape[0] - 1) &
        (y_v >= 0) & (y_v <= vol_shape[1] - 1) &
        (x_v >= 0) & (x_v <= vol_shape[2] - 1)
    )

    vals = map_coordinates(
        volume, [z_v, y_v, x_v], order=1, mode='nearest', cval=0.0,
    ).astype(np.float32)

    vals[~valid] = np.nan
    return vals.reshape(shape_in)

def _compute_contour_area(
    r_theta: np.ndarray,
    angles: np.ndarray,
) -> float:
    """
    Compute cross-section area using shoelace formula.

    Parameters
    ----------
    r_theta : (n_angles,)
        Boundary radius at each angle in mm
    angles : (n_angles,)
        Angular coordinates in radians

    Returns
    -------
    area : float
        Cross-section area in mm²
    """
    # Convert to 2D Cartesian in the (N, B) plane
    x = r_theta * np.cos(angles)
    y = r_theta * np.sin(angles)

    # Shoelace formula: A = 0.5 * |Σ(x_i * y_{i+1} - x_{i+1} * y_i)|
    n = len(x)
    area = 0.5 * np.abs(np.sum(x * np.roll(y, -1) - np.roll(x, -1) * y))

    return float(area)


def _point_in_polygon(
    x_pts: np.ndarray,
    y_pts: np.ndarray,
    polygon: np.ndarray,
) -> np.ndarray:
    """
    Check if points are inside a polygon using ray casting.

    Parameters
    ----------
    x_pts : (H, W) array
        X coordinates of points to test
    y_pts : (H, W) array
        Y coordinates of points to test
    polygon : (N, 2) array
        Polygon vertices

    Returns
    -------
    inside : (H, W) bool
        True for points inside the polygon
    """
    n_verts = len(polygon)
    x_poly = polygon[:, 0]
    y_poly = polygon[:, 1]

    # Flatten for vectorized computation
    x_flat = x_pts.ravel()
    y_flat = y_pts.ravel()
    n_pts = len(x_flat)

    inside = np.zeros(n_pts, dtype=bool)

    # Ray casting algorithm
    j = n_verts - 1
    for i in range(n_verts):
        # Check if ray from point crosses this edge
        mask = (
            ((y_poly[i] > y_flat) != (y_poly[j] > y_flat)) &
            (x_flat < (x_poly[j] - x_poly[i]) * (y_flat - y_poly[i]) / (y_poly[j] - y_poly[i] + 1e-15) + x_poly[i])
        )
        inside ^= mask
        j = i

    return inside.reshape(x_pts.shape)
