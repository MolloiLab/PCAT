"""Merged seed editor: data model + interaction controller.

Replaces the old ``SeedEditState`` + ``SeedEditController`` pair with a
single ``SeedEditor`` class that owns seeds, selection, undo/redo history,
centerline recomputation, and mouse/key interaction logic.

Selection is a flat integer index into ``[ostium, wp0, wp1, ...]``.
"""

from __future__ import annotations

import copy
from typing import Dict, List, Optional, Tuple

import numpy as np
from PySide6.QtCore import QObject, Signal
from scipy.interpolate import CubicSpline


# Maximum number of undo snapshots to keep.
_MAX_HISTORY = 50


# ---------------------------------------------------------------------------
# Spline fitting
# ---------------------------------------------------------------------------

def _fit_spline_centerline(
    seeds_ijk: List[List[float]],
    spacing_mm: List[float],
    volume_shape: Tuple[int, int, int],
    step_mm: float = 0.5,
) -> Optional[np.ndarray]:
    """Fit a cubic spline through seed points and sample densely.

    Uses centripetal parameterization (t_i = cumulative sqrt-distance)
    which reduces overshoot compared to chord-length parameterization.

    Parameters
    ----------
    seeds_ijk : list of [z, y, x] seed points in voxel coordinates.
    spacing_mm : [sz, sy, sx] voxel spacing.
    volume_shape : (Z, Y, X) volume dimensions.
    step_mm : arc-length step for dense sampling.

    Returns
    -------
    dense_ijk : (M, 3) float64 array, or *None* if fewer than 2 points.
    """
    if len(seeds_ijk) < 2:
        return None

    pts_ijk = np.array(seeds_ijk, dtype=np.float64)
    pts_mm = pts_ijk * np.array(spacing_mm)

    # Remove duplicate points (zero-length segments).
    seg = np.linalg.norm(np.diff(pts_mm, axis=0), axis=1)
    keep = np.concatenate([[True], seg > 1e-8])
    pts_mm = pts_mm[keep]

    if len(pts_mm) < 2:
        return None

    # Centripetal parameterization: t_i = cumsum(|seg|^0.5)
    seg = np.linalg.norm(np.diff(pts_mm, axis=0), axis=1)
    t = np.concatenate([[0.0], np.cumsum(np.sqrt(seg))])
    total_t = t[-1]

    if total_t < 1e-6:
        return None

    # Total arc-length for sampling density.
    total_arc = np.sum(seg)
    n_out = max(10, int(total_arc / step_mm))

    if len(pts_mm) >= 3:
        cs = CubicSpline(t, pts_mm, bc_type="not-a-knot")
    else:
        cs = CubicSpline(t, pts_mm, bc_type="natural")

    s_vals = np.linspace(0, total_t, n_out)
    dense_mm = cs(s_vals)

    dense_ijk = dense_mm / np.array(spacing_mm)
    dense_ijk = np.clip(dense_ijk, 0, np.array(volume_shape) - 1)
    return dense_ijk


# ---------------------------------------------------------------------------
# SeedEditor
# ---------------------------------------------------------------------------

class SeedEditor(QObject):
    """Unified seed editor — owns data, selection, history, and interaction.

    Seed storage::

        {vessel: {"ostium": [z, y, x] | None, "waypoints": [[z,y,x], ...]}}

    Selection is a **flat index** into the list
    ``[ostium, wp0, wp1, ...]`` (0 = ostium when present).
    ``None`` means nothing is selected.
    """

    seeds_changed = Signal(str)       # vessel name
    centerline_changed = Signal(str)  # vessel name
    selection_changed = Signal()
    save_requested = Signal()

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(
        self,
        spacing_mm: list,
        volume_shape: tuple,
        vessel_names: Optional[List[str]] = None,
        parent=None,
    ):
        super().__init__(parent)

        if vessel_names is None:
            vessel_names = ["LAD", "LCx", "RCA"]

        self.spacing_mm: List[float] = list(spacing_mm)
        self.volume_shape: Tuple[int, int, int] = tuple(volume_shape)  # type: ignore[assignment]

        # Seed data — extended format per vessel.
        self.seeds: Dict[str, Dict] = {
            v: {"ostium": None, "waypoints": []} for v in vessel_names
        }
        self.centerlines: Dict[str, Optional[np.ndarray]] = {}
        self.current_vessel: str = vessel_names[0] if vessel_names else ""

        # Selection — flat index into get_all_seeds() or None.
        self.selection: Optional[int] = None

        # Undo / redo.
        self.history: List[dict] = []
        self.redo_stack: List[dict] = []

        # Drag state.
        self._dragging: bool = False
        self._drag_flat_index: int = 0

    # ------------------------------------------------------------------
    # Seed accessors
    # ------------------------------------------------------------------

    def get_all_seeds(self, vessel: str) -> list:
        """Return flat list ``[ostium, wp0, wp1, ...]`` for *vessel*.

        Ostium is included only when it is not None.
        """
        entry = self.seeds.get(vessel)
        if entry is None:
            return []
        pts: list = []
        if entry["ostium"] is not None:
            pts.append(entry["ostium"])
        pts.extend(entry.get("waypoints", []))
        return pts

    def has_enough_seeds(self, vessel: str) -> bool:
        """Return True if *vessel* has an ostium and at least one waypoint."""
        entry = self.seeds.get(vessel)
        if entry is None:
            return False
        return entry["ostium"] is not None and len(entry["waypoints"]) >= 1

    # ------------------------------------------------------------------
    # Proximity search
    # ------------------------------------------------------------------

    def find_nearest_seed(
        self,
        vessel: str,
        pos_ijk,
        max_dist_vox: float = 10.0,
    ) -> Optional[int]:
        """Find the closest seed to *pos_ijk* within *max_dist_vox*.

        Returns the flat index into ``get_all_seeds(vessel)``, or None.
        """
        all_seeds = self.get_all_seeds(vessel)
        if not all_seeds:
            return None

        pos = np.asarray(pos_ijk, dtype=np.float64)
        best_dist = max_dist_vox
        best_idx: Optional[int] = None

        for i, seed in enumerate(all_seeds):
            d = float(np.linalg.norm(np.asarray(seed, dtype=np.float64) - pos))
            if d < best_dist:
                best_dist = d
                best_idx = i

        return best_idx

    # ------------------------------------------------------------------
    # Selection
    # ------------------------------------------------------------------

    def select(self, flat_index: int) -> None:
        """Set selection to *flat_index* and emit ``selection_changed``."""
        self.selection = flat_index
        self.selection_changed.emit()

    def clear_selection(self) -> None:
        """Clear the selection and emit ``selection_changed``."""
        self.selection = None
        self.selection_changed.emit()

    def cycle_selection(self, direction: int) -> None:
        """Increment/decrement selection, clamped to bounds.

        *direction* should be +1 (right) or -1 (left).
        """
        vessel = self.current_vessel
        if not vessel:
            return
        all_seeds = self.get_all_seeds(vessel)
        if not all_seeds:
            return

        if self.selection is None:
            new_idx = 0
        else:
            new_idx = max(0, min(len(all_seeds) - 1, self.selection + direction))

        self.select(new_idx)

    # ------------------------------------------------------------------
    # Internal helpers: flat index ↔ (type, index)
    # ------------------------------------------------------------------

    def _flat_to_type_index(self, vessel: str, flat_index: int) -> Tuple[str, int]:
        """Convert flat index to ``("ostium", 0)`` or ``("waypoint", wp_idx)``."""
        has_ostium = self.seeds[vessel]["ostium"] is not None
        if has_ostium and flat_index == 0:
            return ("ostium", 0)
        wp_idx = flat_index - (1 if has_ostium else 0)
        return ("waypoint", wp_idx)

    def _type_index_to_flat(self, vessel: str, seed_type: str, index: int) -> int:
        """Convert ``("ostium"|"waypoint", index)`` to flat index."""
        has_ostium = self.seeds[vessel]["ostium"] is not None
        if seed_type == "ostium":
            return 0
        return index + (1 if has_ostium else 0)

    # ------------------------------------------------------------------
    # Mouse interaction
    # ------------------------------------------------------------------

    def on_left_press(self, voxel_ijk) -> None:
        """Handle left-press in voxel coordinates.

        * If vessel has no ostium -> place ostium.
        * If near a seed -> select it.  If *already* selected -> start drag.
        * Otherwise -> clear selection.
        """
        vessel = self.current_vessel
        if not vessel:
            return

        voxel_list = list(np.asarray(voxel_ijk, dtype=np.float64))

        hit = self.find_nearest_seed(vessel, voxel_ijk)

        if hit is not None:
            if self.selection == hit:
                # Already selected -> prepare for drag.
                self._dragging = False  # actual drag starts on on_left_drag
                self._drag_flat_index = hit
            else:
                # First click on this seed -> select, no drag.
                self.select(hit)
                self._dragging = False
                self._drag_flat_index = -1
        else:
            # Empty space: place ostium if none exists, otherwise deselect.
            entry = self.seeds.get(vessel)
            if entry is not None and entry["ostium"] is None:
                self.push_history()
                entry["ostium"] = voxel_list
                self.recompute_centerline(vessel)
                self.seeds_changed.emit(vessel)
            else:
                self.clear_selection()
            self._dragging = False
            self._drag_flat_index = -1

    def on_left_drag(self, voxel_ijk) -> None:
        """Handle left-drag: move the seed, recompute spline, NO signals."""
        if self._drag_flat_index < 0:
            return

        self._dragging = True
        vessel = self.current_vessel
        if not vessel:
            return

        voxel_list = list(np.asarray(voxel_ijk, dtype=np.float64))
        seed_type, idx = self._flat_to_type_index(vessel, self._drag_flat_index)

        entry = self.seeds[vessel]
        if seed_type == "ostium":
            entry["ostium"] = voxel_list
        else:
            if 0 <= idx < len(entry["waypoints"]):
                entry["waypoints"][idx] = voxel_list

        # Recompute spline silently (no signal).
        self.recompute_centerline(vessel, emit=False)

    def on_left_release(self) -> None:
        """Handle left-release: push history and emit signals."""
        if self._dragging and self._drag_flat_index >= 0:
            vessel = self.current_vessel
            self.push_history()
            if vessel:
                self.centerline_changed.emit(vessel)
                self.seeds_changed.emit(vessel)

        self._dragging = False
        self._drag_flat_index = -1

    # ------------------------------------------------------------------
    # Seed mutations
    # ------------------------------------------------------------------

    def add_waypoint_at(self, voxel_ijk) -> None:
        """Insert a waypoint after the selected seed, advancing selection.

        If the ostium (flat 0) is selected, insert as first waypoint.
        If a waypoint is selected, insert after it.
        If nothing selected, append at end.
        """
        vessel = self.current_vessel
        if not vessel:
            return

        self.push_history()
        voxel_list = list(np.asarray(voxel_ijk, dtype=np.float64))
        entry = self.seeds[vessel]
        wps = entry["waypoints"]
        has_ostium = entry["ostium"] is not None

        if self.selection is not None:
            seed_type, idx = self._flat_to_type_index(vessel, self.selection)
            if seed_type == "ostium":
                # Insert as first waypoint.
                wps.insert(0, voxel_list)
                # Select the new waypoint -> flat index 1 (ostium is 0).
                self.selection = 1
            else:
                # Insert after the selected waypoint.
                insert_at = max(0, min(idx + 1, len(wps)))
                wps.insert(insert_at, voxel_list)
                # Advance selection to the new waypoint.
                self.selection = self._type_index_to_flat(vessel, "waypoint", insert_at)
        else:
            # Nothing selected -> append.
            wps.append(voxel_list)
            self.selection = self._type_index_to_flat(vessel, "waypoint", len(wps) - 1)

        self.recompute_centerline(vessel)
        self.seeds_changed.emit(vessel)
        self.selection_changed.emit()

    def delete_selected(self) -> None:
        """Delete the currently selected seed (ostium or waypoint)."""
        vessel = self.current_vessel
        if not vessel or self.selection is None:
            return

        all_seeds = self.get_all_seeds(vessel)
        if self.selection < 0 or self.selection >= len(all_seeds):
            return

        self.push_history()
        seed_type, idx = self._flat_to_type_index(vessel, self.selection)
        entry = self.seeds[vessel]

        if seed_type == "ostium":
            entry["ostium"] = None
        else:
            if 0 <= idx < len(entry["waypoints"]):
                entry["waypoints"].pop(idx)

        # Clamp selection: if seeds remain, stay at same flat index or last.
        remaining = self.get_all_seeds(vessel)
        if not remaining:
            self.selection = None
        else:
            self.selection = min(self.selection, len(remaining) - 1)

        self.recompute_centerline(vessel)
        self.seeds_changed.emit(vessel)
        self.selection_changed.emit()

    # ------------------------------------------------------------------
    # Centerline fitting
    # ------------------------------------------------------------------

    def recompute_centerline(self, vessel: str, emit: bool = True) -> None:
        """Refit the spline centerline for *vessel* from its seeds.

        Parameters
        ----------
        vessel : vessel name.
        emit : if True, emit ``centerline_changed``.
               Set False during drag to avoid expensive CPR updates.
        """
        ordered = self.get_all_seeds(vessel)

        if len(ordered) < 2:
            self.centerlines[vessel] = None
        else:
            self.centerlines[vessel] = _fit_spline_centerline(
                ordered, self.spacing_mm, self.volume_shape
            )

        if emit:
            self.centerline_changed.emit(vessel)

    # ------------------------------------------------------------------
    # Undo / Redo
    # ------------------------------------------------------------------

    def push_history(self) -> None:
        """Snapshot the current seeds dict onto the undo stack."""
        self.history.append(copy.deepcopy(self.seeds))
        if len(self.history) > _MAX_HISTORY:
            self.history.pop(0)
        self.redo_stack.clear()

    def undo(self) -> None:
        """Restore the previous seeds state."""
        if not self.history:
            return
        self.redo_stack.append(copy.deepcopy(self.seeds))
        self.seeds = self.history.pop()
        self._recompute_all_centerlines()
        for vessel in self.seeds:
            self.seeds_changed.emit(vessel)

    def redo(self) -> None:
        """Re-apply an undone change."""
        if not self.redo_stack:
            return
        self.history.append(copy.deepcopy(self.seeds))
        self.seeds = self.redo_stack.pop()
        self._recompute_all_centerlines()
        for vessel in self.seeds:
            self.seeds_changed.emit(vessel)

    def _recompute_all_centerlines(self) -> None:
        """Recompute centerlines for every vessel (after undo/redo)."""
        for vessel in self.seeds:
            self.recompute_centerline(vessel)

    # ------------------------------------------------------------------
    # Session persistence
    # ------------------------------------------------------------------

    def save_to_session(self, session) -> None:
        """Persist seeds into a :class:`PatientSession`.

        Format: ``{"flat": {vessel: [z,y,x]|None}, "extended": {vessel: {...}}}``.
        """
        flat: dict = {}
        for vessel, entry in self.seeds.items():
            flat[vessel] = list(entry["ostium"]) if entry["ostium"] is not None else None

        session.seeds_data = {
            "flat": flat,
            "extended": copy.deepcopy(self.seeds),
        }
        session.save()

    def load_from_session(self, session) -> None:
        """Load seeds from a :class:`PatientSession`.

        Reads ``session.seeds_data["extended"]`` if available, falling back
        to ``session.seeds_data["flat"]`` (ostium-only).
        """
        data = getattr(session, "seeds_data", None)
        if data is None:
            return

        if isinstance(data, dict) and "extended" in data:
            raw = data["extended"]
        elif isinstance(data, dict) and "flat" in data:
            raw = data["flat"]
        else:
            raw = data

        # Normalise into extended format, preserving any vessels already in
        # self.seeds that might not be in the loaded data.
        for vessel, value in raw.items():
            if isinstance(value, dict):
                self.seeds[vessel] = {
                    "ostium": value.get("ostium"),
                    "waypoints": list(value.get("waypoints", [])),
                }
            else:
                # Flat format — treat as ostium seed.
                self.seeds[vessel] = {
                    "ostium": list(value) if value is not None else None,
                    "waypoints": [],
                }

        # Recompute all centerlines after loading.
        for vessel in self.seeds:
            self.recompute_centerline(vessel)

    # ------------------------------------------------------------------
    # Export helpers (backward compat)
    # ------------------------------------------------------------------

    def get_all_seeds_flat(self) -> dict:
        """Return ``{vessel: [z, y, x]}`` (ostium only) for pipeline use."""
        out: dict = {}
        for vessel, entry in self.seeds.items():
            out[vessel] = list(entry["ostium"]) if entry["ostium"] is not None else None
        return out
