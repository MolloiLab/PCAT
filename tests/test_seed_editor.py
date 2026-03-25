"""Tests for pcat_workstation.models.seed_editor.SeedEditor."""

from __future__ import annotations

import numpy as np
import pytest

from pcat_workstation.models.seed_editor import SeedEditor, _fit_spline_centerline


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

SPACING = [1.0, 0.5, 0.5]
SHAPE = (20, 64, 64)
VESSELS = ["LAD", "LCx", "RCA"]


@pytest.fixture
def editor():
    """Fresh SeedEditor with default vessel names."""
    return SeedEditor(spacing_mm=SPACING, volume_shape=SHAPE, vessel_names=VESSELS)


# ---------------------------------------------------------------------------
# Initial state
# ---------------------------------------------------------------------------

class TestInitialState:
    def test_empty_seeds(self, editor: SeedEditor):
        for v in VESSELS:
            assert editor.seeds[v]["ostium"] is None
            assert editor.seeds[v]["waypoints"] == []

    def test_no_selection(self, editor: SeedEditor):
        assert editor.selection is None

    def test_current_vessel_default(self, editor: SeedEditor):
        assert editor.current_vessel == "LAD"

    def test_history_empty(self, editor: SeedEditor):
        assert editor.history == []
        assert editor.redo_stack == []

    def test_get_all_seeds_empty(self, editor: SeedEditor):
        assert editor.get_all_seeds("LAD") == []

    def test_has_enough_seeds_false(self, editor: SeedEditor):
        assert not editor.has_enough_seeds("LAD")

    def test_unknown_vessel_get_all_seeds(self, editor: SeedEditor):
        assert editor.get_all_seeds("UNKNOWN") == []

    def test_unknown_vessel_has_enough(self, editor: SeedEditor):
        assert not editor.has_enough_seeds("UNKNOWN")


# ---------------------------------------------------------------------------
# Place ostium via on_left_press
# ---------------------------------------------------------------------------

class TestPlaceOstium:
    def test_place_ostium_on_empty(self, editor: SeedEditor):
        """Left-click in empty space when no ostium exists -> places ostium."""
        editor.on_left_press([5.0, 30.0, 30.0])
        assert editor.seeds["LAD"]["ostium"] is not None
        np.testing.assert_allclose(editor.seeds["LAD"]["ostium"], [5.0, 30.0, 30.0])

    def test_place_ostium_emits_seeds_changed(self, editor: SeedEditor):
        received = []
        editor.seeds_changed.connect(lambda v: received.append(v))
        editor.on_left_press([5.0, 30.0, 30.0])
        assert "LAD" in received

    def test_place_ostium_pushes_history(self, editor: SeedEditor):
        editor.on_left_press([5.0, 30.0, 30.0])
        assert len(editor.history) == 1

    def test_no_double_ostium(self, editor: SeedEditor):
        """Second click in empty space (after ostium placed) just deselects."""
        editor.on_left_press([5.0, 30.0, 30.0])
        editor.on_left_press([10.0, 40.0, 40.0])
        # Ostium should still be the first one.
        np.testing.assert_allclose(editor.seeds["LAD"]["ostium"], [5.0, 30.0, 30.0])

    def test_get_all_seeds_after_ostium(self, editor: SeedEditor):
        editor.on_left_press([5.0, 30.0, 30.0])
        seeds = editor.get_all_seeds("LAD")
        assert len(seeds) == 1
        np.testing.assert_allclose(seeds[0], [5.0, 30.0, 30.0])


# ---------------------------------------------------------------------------
# Add waypoints + insertion order
# ---------------------------------------------------------------------------

class TestAddWaypoints:
    def test_add_waypoint_appends_when_no_selection(self, editor: SeedEditor):
        editor.seeds["LAD"]["ostium"] = [5.0, 30.0, 30.0]
        editor.add_waypoint_at([7.0, 32.0, 32.0])

        wps = editor.seeds["LAD"]["waypoints"]
        assert len(wps) == 1
        np.testing.assert_allclose(wps[0], [7.0, 32.0, 32.0])

    def test_add_multiple_waypoints_order(self, editor: SeedEditor):
        editor.seeds["LAD"]["ostium"] = [5.0, 30.0, 30.0]
        editor.add_waypoint_at([7.0, 32.0, 32.0])
        editor.add_waypoint_at([9.0, 34.0, 34.0])
        editor.add_waypoint_at([11.0, 36.0, 36.0])

        wps = editor.seeds["LAD"]["waypoints"]
        # Each insert goes after the previously inserted (selection advances).
        assert len(wps) == 3
        np.testing.assert_allclose(wps[0], [7.0, 32.0, 32.0])
        np.testing.assert_allclose(wps[1], [9.0, 34.0, 34.0])
        np.testing.assert_allclose(wps[2], [11.0, 36.0, 36.0])

    def test_insert_after_selected(self, editor: SeedEditor):
        """Selecting an earlier waypoint and adding inserts right after it."""
        editor.seeds["LAD"]["ostium"] = [5.0, 30.0, 30.0]
        editor.add_waypoint_at([7.0, 32.0, 32.0])   # wp0
        editor.add_waypoint_at([9.0, 34.0, 34.0])   # wp1 (after wp0)
        # Select wp0 (flat index 1 because ostium is 0).
        editor.select(1)
        editor.add_waypoint_at([8.0, 33.0, 33.0])   # insert after wp0

        wps = editor.seeds["LAD"]["waypoints"]
        assert len(wps) == 3
        np.testing.assert_allclose(wps[0], [7.0, 32.0, 32.0])  # original wp0
        np.testing.assert_allclose(wps[1], [8.0, 33.0, 33.0])  # newly inserted
        np.testing.assert_allclose(wps[2], [9.0, 34.0, 34.0])  # original wp1

    def test_insert_after_ostium(self, editor: SeedEditor):
        """Selecting ostium (flat 0) and adding inserts as first waypoint."""
        editor.seeds["LAD"]["ostium"] = [5.0, 30.0, 30.0]
        editor.add_waypoint_at([9.0, 34.0, 34.0])   # wp0
        editor.select(0)  # select ostium
        editor.add_waypoint_at([6.0, 31.0, 31.0])

        wps = editor.seeds["LAD"]["waypoints"]
        assert len(wps) == 2
        np.testing.assert_allclose(wps[0], [6.0, 31.0, 31.0])  # inserted first
        np.testing.assert_allclose(wps[1], [9.0, 34.0, 34.0])  # original wp0

    def test_selection_advances_after_add(self, editor: SeedEditor):
        editor.seeds["LAD"]["ostium"] = [5.0, 30.0, 30.0]
        editor.add_waypoint_at([7.0, 32.0, 32.0])
        # Selection should now point at the new waypoint (flat 1).
        assert editor.selection == 1

    def test_has_enough_seeds_true(self, editor: SeedEditor):
        editor.seeds["LAD"]["ostium"] = [5.0, 30.0, 30.0]
        editor.add_waypoint_at([7.0, 32.0, 32.0])
        assert editor.has_enough_seeds("LAD")

    def test_has_enough_seeds_ostium_only(self, editor: SeedEditor):
        editor.seeds["LAD"]["ostium"] = [5.0, 30.0, 30.0]
        assert not editor.has_enough_seeds("LAD")


# ---------------------------------------------------------------------------
# Delete
# ---------------------------------------------------------------------------

class TestDeleteSelected:
    def test_delete_waypoint(self, editor: SeedEditor):
        editor.seeds["LAD"]["ostium"] = [5.0, 30.0, 30.0]
        editor.add_waypoint_at([7.0, 32.0, 32.0])
        editor.add_waypoint_at([9.0, 34.0, 34.0])
        # Select wp0 (flat 1) and delete.
        editor.select(1)
        editor.delete_selected()

        wps = editor.seeds["LAD"]["waypoints"]
        assert len(wps) == 1
        np.testing.assert_allclose(wps[0], [9.0, 34.0, 34.0])

    def test_delete_ostium(self, editor: SeedEditor):
        editor.seeds["LAD"]["ostium"] = [5.0, 30.0, 30.0]
        editor.add_waypoint_at([7.0, 32.0, 32.0])
        # Select ostium (flat 0).
        editor.select(0)
        editor.delete_selected()

        assert editor.seeds["LAD"]["ostium"] is None
        # Waypoint should still be there.
        assert len(editor.seeds["LAD"]["waypoints"]) == 1

    def test_delete_nothing_selected(self, editor: SeedEditor):
        """delete_selected is a no-op when nothing is selected."""
        editor.seeds["LAD"]["ostium"] = [5.0, 30.0, 30.0]
        editor.clear_selection()
        editor.delete_selected()
        assert editor.seeds["LAD"]["ostium"] is not None

    def test_delete_clamps_selection(self, editor: SeedEditor):
        """After deleting last seed, selection clamps or goes to None."""
        editor.seeds["LAD"]["ostium"] = [5.0, 30.0, 30.0]
        editor.add_waypoint_at([7.0, 32.0, 32.0])
        # Select the only waypoint (flat 1), delete it.
        editor.select(1)
        editor.delete_selected()
        # Only ostium remains -> selection clamped to 0.
        assert editor.selection == 0

    def test_delete_all_gives_none_selection(self, editor: SeedEditor):
        editor.on_left_press([5.0, 30.0, 30.0])  # place ostium
        # Select ostium and delete.
        editor.select(0)
        editor.delete_selected()
        assert editor.selection is None


# ---------------------------------------------------------------------------
# Cycle selection (arrow keys)
# ---------------------------------------------------------------------------

class TestCycleSelection:
    def test_cycle_from_none_selects_first(self, editor: SeedEditor):
        editor.seeds["LAD"]["ostium"] = [5.0, 30.0, 30.0]
        editor.add_waypoint_at([7.0, 32.0, 32.0])
        editor.clear_selection()
        editor.cycle_selection(+1)
        assert editor.selection == 0

    def test_cycle_forward(self, editor: SeedEditor):
        editor.seeds["LAD"]["ostium"] = [5.0, 30.0, 30.0]
        editor.add_waypoint_at([7.0, 32.0, 32.0])
        editor.add_waypoint_at([9.0, 34.0, 34.0])
        editor.select(0)
        editor.cycle_selection(+1)
        assert editor.selection == 1

    def test_cycle_backward(self, editor: SeedEditor):
        editor.seeds["LAD"]["ostium"] = [5.0, 30.0, 30.0]
        editor.add_waypoint_at([7.0, 32.0, 32.0])
        editor.select(1)
        editor.cycle_selection(-1)
        assert editor.selection == 0

    def test_cycle_clamp_at_end(self, editor: SeedEditor):
        editor.seeds["LAD"]["ostium"] = [5.0, 30.0, 30.0]
        editor.add_waypoint_at([7.0, 32.0, 32.0])
        editor.select(1)
        editor.cycle_selection(+1)
        # Should stay at 1 (clamped).
        assert editor.selection == 1

    def test_cycle_clamp_at_start(self, editor: SeedEditor):
        editor.seeds["LAD"]["ostium"] = [5.0, 30.0, 30.0]
        editor.select(0)
        editor.cycle_selection(-1)
        assert editor.selection == 0

    def test_cycle_empty_vessel_noop(self, editor: SeedEditor):
        editor.cycle_selection(+1)
        assert editor.selection is None


# ---------------------------------------------------------------------------
# Undo / Redo
# ---------------------------------------------------------------------------

class TestUndoRedo:
    def test_undo_restores_previous_state(self, editor: SeedEditor):
        editor.on_left_press([5.0, 30.0, 30.0])  # places ostium, pushes history
        assert editor.seeds["LAD"]["ostium"] is not None
        editor.undo()
        assert editor.seeds["LAD"]["ostium"] is None

    def test_redo_restores_undone_state(self, editor: SeedEditor):
        editor.on_left_press([5.0, 30.0, 30.0])
        editor.undo()
        editor.redo()
        assert editor.seeds["LAD"]["ostium"] is not None
        np.testing.assert_allclose(editor.seeds["LAD"]["ostium"], [5.0, 30.0, 30.0])

    def test_undo_empty_noop(self, editor: SeedEditor):
        """Undo with no history should be a no-op."""
        editor.undo()  # should not raise
        assert editor.seeds["LAD"]["ostium"] is None

    def test_redo_empty_noop(self, editor: SeedEditor):
        editor.redo()  # should not raise

    def test_push_history_clears_redo(self, editor: SeedEditor):
        editor.on_left_press([5.0, 30.0, 30.0])
        editor.undo()
        assert len(editor.redo_stack) == 1
        # New action clears redo.
        editor.on_left_press([6.0, 31.0, 31.0])
        assert len(editor.redo_stack) == 0

    def test_multiple_undo(self, editor: SeedEditor):
        editor.on_left_press([5.0, 30.0, 30.0])
        editor.add_waypoint_at([7.0, 32.0, 32.0])
        editor.add_waypoint_at([9.0, 34.0, 34.0])
        # Undo twice -> back to ostium-only state.
        editor.undo()
        editor.undo()
        assert len(editor.seeds["LAD"]["waypoints"]) == 0
        assert editor.seeds["LAD"]["ostium"] is not None


# ---------------------------------------------------------------------------
# Centerline computation
# ---------------------------------------------------------------------------

class TestCenterlineComputation:
    def test_centerline_none_with_insufficient_points(self, editor: SeedEditor):
        editor.seeds["LAD"]["ostium"] = [5.0, 30.0, 30.0]
        editor.recompute_centerline("LAD")
        assert editor.centerlines.get("LAD") is None

    def test_centerline_computed_with_two_points(self, editor: SeedEditor):
        editor.seeds["LAD"]["ostium"] = [2.0, 32.0, 32.0]
        editor.seeds["LAD"]["waypoints"] = [[10.0, 32.0, 32.0]]
        editor.recompute_centerline("LAD")
        cl = editor.centerlines.get("LAD")
        assert cl is not None
        assert cl.shape[1] == 3
        assert cl.shape[0] >= 10  # should have dense sampling

    def test_centerline_starts_and_ends_near_seeds(self, editor: SeedEditor):
        editor.seeds["LAD"]["ostium"] = [2.0, 32.0, 32.0]
        editor.seeds["LAD"]["waypoints"] = [[10.0, 32.0, 32.0]]
        editor.recompute_centerline("LAD")
        cl = editor.centerlines["LAD"]
        np.testing.assert_allclose(cl[0], [2.0, 32.0, 32.0], atol=0.5)
        np.testing.assert_allclose(cl[-1], [10.0, 32.0, 32.0], atol=0.5)

    def test_centerline_clipped_to_volume(self, editor: SeedEditor):
        """Centerline points should be within volume bounds."""
        editor.seeds["LAD"]["ostium"] = [0.0, 0.0, 0.0]
        editor.seeds["LAD"]["waypoints"] = [[19.0, 63.0, 63.0]]
        editor.recompute_centerline("LAD")
        cl = editor.centerlines["LAD"]
        assert np.all(cl >= 0)
        assert np.all(cl[:, 0] <= 19)
        assert np.all(cl[:, 1] <= 63)
        assert np.all(cl[:, 2] <= 63)

    def test_centerline_with_three_points(self, editor: SeedEditor):
        editor.seeds["LAD"]["ostium"] = [2.0, 32.0, 32.0]
        editor.seeds["LAD"]["waypoints"] = [[6.0, 32.0, 32.0], [10.0, 32.0, 32.0]]
        editor.recompute_centerline("LAD")
        cl = editor.centerlines["LAD"]
        assert cl is not None
        assert cl.shape[0] >= 10


# ---------------------------------------------------------------------------
# get_all_seeds flat list
# ---------------------------------------------------------------------------

class TestGetAllSeeds:
    def test_empty(self, editor: SeedEditor):
        assert editor.get_all_seeds("LAD") == []

    def test_ostium_only(self, editor: SeedEditor):
        editor.seeds["LAD"]["ostium"] = [5.0, 30.0, 30.0]
        seeds = editor.get_all_seeds("LAD")
        assert len(seeds) == 1

    def test_ostium_plus_waypoints(self, editor: SeedEditor):
        editor.seeds["LAD"]["ostium"] = [5.0, 30.0, 30.0]
        editor.seeds["LAD"]["waypoints"] = [[7.0, 32.0, 32.0], [9.0, 34.0, 34.0]]
        seeds = editor.get_all_seeds("LAD")
        assert len(seeds) == 3
        np.testing.assert_allclose(seeds[0], [5.0, 30.0, 30.0])
        np.testing.assert_allclose(seeds[1], [7.0, 32.0, 32.0])
        np.testing.assert_allclose(seeds[2], [9.0, 34.0, 34.0])

    def test_waypoints_only_no_ostium(self, editor: SeedEditor):
        editor.seeds["LAD"]["waypoints"] = [[7.0, 32.0, 32.0]]
        seeds = editor.get_all_seeds("LAD")
        assert len(seeds) == 1
        np.testing.assert_allclose(seeds[0], [7.0, 32.0, 32.0])


# ---------------------------------------------------------------------------
# find_nearest_seed
# ---------------------------------------------------------------------------

class TestFindNearestSeed:
    def test_find_ostium(self, editor: SeedEditor):
        editor.seeds["LAD"]["ostium"] = [5.0, 30.0, 30.0]
        idx = editor.find_nearest_seed("LAD", [5.0, 30.0, 30.0])
        assert idx == 0

    def test_find_waypoint(self, editor: SeedEditor):
        editor.seeds["LAD"]["ostium"] = [5.0, 30.0, 30.0]
        editor.seeds["LAD"]["waypoints"] = [[10.0, 32.0, 32.0]]
        idx = editor.find_nearest_seed("LAD", [10.0, 32.0, 32.0])
        assert idx == 1  # flat: ostium=0, wp0=1

    def test_none_when_too_far(self, editor: SeedEditor):
        editor.seeds["LAD"]["ostium"] = [5.0, 30.0, 30.0]
        idx = editor.find_nearest_seed("LAD", [5.0, 30.0, 30.0], max_dist_vox=0.0)
        # distance == 0, which is not < 0 threshold, so None
        assert idx is None

    def test_none_on_empty(self, editor: SeedEditor):
        assert editor.find_nearest_seed("LAD", [5.0, 30.0, 30.0]) is None


# ---------------------------------------------------------------------------
# Drag interaction
# ---------------------------------------------------------------------------

class TestDragInteraction:
    def test_drag_moves_seed(self, editor: SeedEditor):
        """Select-then-drag model: first click selects, second click+drag moves."""
        editor.on_left_press([5.0, 30.0, 30.0])  # place ostium
        # First click near ostium -> select.
        editor.on_left_press([5.0, 30.0, 30.0])
        assert editor.selection == 0
        # Second click on same (already selected) -> prepares drag.
        editor.on_left_press([5.0, 30.0, 30.0])
        editor.on_left_drag([6.0, 31.0, 31.0])
        editor.on_left_release()
        np.testing.assert_allclose(editor.seeds["LAD"]["ostium"], [6.0, 31.0, 31.0])

    def test_drag_pushes_history_on_release(self, editor: SeedEditor):
        editor.on_left_press([5.0, 30.0, 30.0])  # place ostium (1 history entry)
        editor.on_left_press([5.0, 30.0, 30.0])  # select
        editor.on_left_press([5.0, 30.0, 30.0])  # prepare drag
        history_before = len(editor.history)
        editor.on_left_drag([6.0, 31.0, 31.0])
        editor.on_left_release()
        assert len(editor.history) == history_before + 1


# ---------------------------------------------------------------------------
# Session persistence
# ---------------------------------------------------------------------------

class TestSessionPersistence:
    def test_save_and_load(self, editor: SeedEditor):
        editor.seeds["LAD"]["ostium"] = [5.0, 30.0, 30.0]
        editor.seeds["LAD"]["waypoints"] = [[7.0, 32.0, 32.0]]

        # Mock session.
        class MockSession:
            seeds_data = None
            def save(self):
                pass

        session = MockSession()
        editor.save_to_session(session)

        # Verify saved format.
        assert "flat" in session.seeds_data
        assert "extended" in session.seeds_data
        np.testing.assert_allclose(session.seeds_data["flat"]["LAD"], [5.0, 30.0, 30.0])

        # Load into a fresh editor.
        editor2 = SeedEditor(spacing_mm=SPACING, volume_shape=SHAPE, vessel_names=VESSELS)
        editor2.load_from_session(session)
        np.testing.assert_allclose(editor2.seeds["LAD"]["ostium"], [5.0, 30.0, 30.0])
        assert len(editor2.seeds["LAD"]["waypoints"]) == 1

    def test_load_from_flat_format(self, editor: SeedEditor):
        """Backward compat: load from flat-only format."""
        class MockSession:
            seeds_data = {
                "flat": {"LAD": [5.0, 30.0, 30.0], "LCx": None, "RCA": None}
            }
            def save(self):
                pass

        editor.load_from_session(MockSession())
        np.testing.assert_allclose(editor.seeds["LAD"]["ostium"], [5.0, 30.0, 30.0])
        assert editor.seeds["LCx"]["ostium"] is None

    def test_load_none_noop(self, editor: SeedEditor):
        class MockSession:
            seeds_data = None
        editor.load_from_session(MockSession())
        # Should not raise; seeds unchanged.
        assert editor.seeds["LAD"]["ostium"] is None


# ---------------------------------------------------------------------------
# _fit_spline_centerline unit tests
# ---------------------------------------------------------------------------

class TestFitSplineCenterline:
    def test_less_than_two_points(self):
        result = _fit_spline_centerline([[1, 2, 3]], [1, 1, 1], (10, 10, 10))
        assert result is None

    def test_empty_list(self):
        result = _fit_spline_centerline([], [1, 1, 1], (10, 10, 10))
        assert result is None

    def test_two_points(self):
        pts = [[0, 0, 0], [9, 9, 9]]
        result = _fit_spline_centerline(pts, [1, 1, 1], (10, 10, 10))
        assert result is not None
        assert result.shape[1] == 3
        assert result.shape[0] >= 10

    def test_duplicate_points_removed(self):
        pts = [[0, 0, 0], [0, 0, 0], [9, 9, 9]]
        result = _fit_spline_centerline(pts, [1, 1, 1], (10, 10, 10))
        assert result is not None

    def test_all_duplicates(self):
        pts = [[5, 5, 5], [5, 5, 5]]
        result = _fit_spline_centerline(pts, [1, 1, 1], (10, 10, 10))
        assert result is None
