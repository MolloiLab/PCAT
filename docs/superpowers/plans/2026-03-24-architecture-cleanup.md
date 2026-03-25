# Architecture Cleanup + UX Overhaul Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace VTK-based seed editing with 2D QPainter overlays, merge seed state/controller, separate editing from analysis, make CPR ~100ms. Match March 4 seed_editor.py UX feel.

**Architecture:** Seeds and centerlines rendered as 2D QPainter overlays on top of VTK slice views. Merged SeedEditor class handles all editing state and interaction. CPR uses fast path (~100ms) bypassing the slow `_compute_cpr_data` wrapper. "Run Pipeline" button separates editing from analysis.

**Tech Stack:** PySide6/Qt, VTK (CT slices only), QPainter (overlays), scipy CubicSpline, numpy

**Spec:** `docs/superpowers/specs/2026-03-24-architecture-cleanup-design.md`

---

## File Map

### New Files
- `pcat_workstation/models/seed_editor.py` — merged SeedEditState + SeedEditController (~450 lines)
- `pcat_workstation/widgets/overlay_painter.py` — QPainter 2D overlay for seeds + centerline (~250 lines)

### Modified Files
- `pcat_workstation/widgets/vtk_slice_view.py` — remove all VTK seed/centerline actor code, integrate OverlayPainter
- `pcat_workstation/widgets/cpr_view.py` — remove dead contour code, fix needle perpendicularity
- `pcat_workstation/app/main_window.py` — simplify signal wiring, add Run Pipeline button
- `pcat_workstation/widgets/toolbar.py` — add Run Pipeline button
- `pcat_workstation/workers/cpr_worker.py` — use fast CPR path (~100ms)

### Deleted Files
- `pcat_workstation/controllers/seed_edit_controller.py` (merged into seed_editor.py)
- `pcat_workstation/models/seed_edit_state.py` (merged into seed_editor.py)

---

## Task 1: Create SeedEditor (merged model + controller)

**Files:**
- Create: `pcat_workstation/models/seed_editor.py`
- Test: `tests/test_seed_editor.py`

This is the core data model. No UI dependencies — pure logic + Qt signals.

- [ ] **Step 1: Write test for SeedEditor basic operations**

```python
# tests/test_seed_editor.py
import sys
from pathlib import Path
import pytest
import numpy as np
from PySide6.QtCore import QCoreApplication

sys.path.insert(0, str(Path(__file__).parent.parent))

@pytest.fixture(scope="session")
def qapp():
    app = QCoreApplication.instance()
    if app is None:
        app = QCoreApplication(sys.argv)
    return app

@pytest.fixture
def editor(qapp):
    from pcat_workstation.models.seed_editor import SeedEditor
    return SeedEditor(
        spacing_mm=[1.0, 0.5, 0.5],
        volume_shape=(20, 64, 64),
        vessel_names=["LAD", "LCx", "RCA"],
    )

class TestSeedEditorBasic:
    def test_initial_state(self, editor):
        assert editor.current_vessel == "LAD"
        assert editor.selection is None
        for v in ["LAD", "LCx", "RCA"]:
            assert editor.seeds[v]["ostium"] is None
            assert editor.seeds[v]["waypoints"] == []

    def test_place_ostium(self, editor):
        editor.current_vessel = "LAD"
        editor.on_left_press([10, 32, 32])
        assert editor.seeds["LAD"]["ostium"] == [10, 32, 32]

    def test_add_waypoint(self, editor):
        editor.seeds["LAD"]["ostium"] = [10, 32, 32]
        editor.add_waypoint_at([15, 34, 30])
        assert len(editor.seeds["LAD"]["waypoints"]) == 1
        assert editor.seeds["LAD"]["waypoints"][0] == [15, 34, 30]

    def test_insert_waypoint_after_selected(self, editor):
        editor.seeds["LAD"]["ostium"] = [10, 32, 32]
        editor.seeds["LAD"]["waypoints"] = [[12, 33, 31], [18, 36, 28]]
        editor.select(1)  # select wp0 (flat index 1)
        editor.add_waypoint_at([15, 34, 30])
        # Should insert between wp0 and wp1
        assert len(editor.seeds["LAD"]["waypoints"]) == 3
        assert editor.seeds["LAD"]["waypoints"][1] == [15, 34, 30]
        # Selection should advance to the new point
        assert editor.selection == 2

    def test_delete_waypoint(self, editor):
        editor.seeds["LAD"]["ostium"] = [10, 32, 32]
        editor.seeds["LAD"]["waypoints"] = [[12, 33, 31], [18, 36, 28]]
        editor.select(2)  # select wp1
        editor.delete_selected()
        assert len(editor.seeds["LAD"]["waypoints"]) == 1
        assert editor.selection == 1  # clamped

    def test_delete_ostium(self, editor):
        editor.seeds["LAD"]["ostium"] = [10, 32, 32]
        editor.select(0)  # select ostium
        editor.delete_selected()
        assert editor.seeds["LAD"]["ostium"] is None
        assert editor.selection is None

    def test_cycle_seeds(self, editor):
        editor.seeds["LAD"]["ostium"] = [10, 32, 32]
        editor.seeds["LAD"]["waypoints"] = [[12, 33, 31], [18, 36, 28]]
        editor.select(0)
        editor.cycle_selection(1)
        assert editor.selection == 1
        editor.cycle_selection(1)
        assert editor.selection == 2
        editor.cycle_selection(1)  # clamp at end
        assert editor.selection == 2
        editor.cycle_selection(-1)
        assert editor.selection == 1

    def test_undo_redo(self, editor):
        editor.seeds["LAD"]["ostium"] = [10, 32, 32]
        editor.push_history()
        editor.seeds["LAD"]["ostium"] = [20, 40, 40]
        editor.push_history()
        editor.undo()
        assert editor.seeds["LAD"]["ostium"] == [10, 32, 32]
        editor.redo()
        assert editor.seeds["LAD"]["ostium"] == [20, 40, 40]

    def test_centerline_computed(self, editor):
        editor.seeds["LAD"]["ostium"] = [2, 32, 32]
        editor.seeds["LAD"]["waypoints"] = [[10, 32, 32], [17, 32, 32]]
        editor.recompute_centerline("LAD")
        cl = editor.centerlines["LAD"]
        assert cl is not None
        assert len(cl) > 10  # dense spline

    def test_get_all_seeds(self, editor):
        editor.seeds["LAD"]["ostium"] = [10, 32, 32]
        editor.seeds["LAD"]["waypoints"] = [[12, 33, 31], [18, 36, 28]]
        pts = editor.get_all_seeds("LAD")
        assert len(pts) == 3
        assert pts[0] == [10, 32, 32]  # ostium first

    def test_has_enough_seeds(self, editor):
        assert not editor.has_enough_seeds("LAD")
        editor.seeds["LAD"]["ostium"] = [10, 32, 32]
        assert not editor.has_enough_seeds("LAD")
        editor.seeds["LAD"]["waypoints"] = [[12, 33, 31]]
        assert editor.has_enough_seeds("LAD")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_seed_editor.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'pcat_workstation.models.seed_editor'`

- [ ] **Step 3: Implement SeedEditor**

Create `pcat_workstation/models/seed_editor.py`. Port logic from current `seed_edit_state.py` + `seed_edit_controller.py` into a single class. Key differences from current code:

- Single `selection` integer (flat index into all_seeds list) instead of separate vessel/type/index
- `on_left_press(voxel_ijk)` handles: place ostium if none, select seed if near one, start drag if already selected
- `on_left_drag(voxel_ijk)` moves seed + recomputes spline, NO signal emission
- `on_left_release()` pushes history + emits `centerline_changed`
- `add_waypoint_at(voxel_ijk)` inserts after selection, advances selection
- `delete_selected()` works for both ostium and waypoints
- `_fit_spline_centerline()` uses centripetal parameterization (from current seed_edit_state.py)
- `save_to_session(session)` persists to PatientSession

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_seed_editor.py -v`
Expected: all tests PASS

- [ ] **Step 5: Commit**

```bash
git add pcat_workstation/models/seed_editor.py tests/test_seed_editor.py
git commit -m "feat: SeedEditor — merged seed state + controller"
```

---

## Task 2: Create OverlayPainter (2D QPainter overlay)

**Files:**
- Create: `pcat_workstation/widgets/overlay_painter.py`
- Test: `tests/test_overlay_painter.py`

Transparent QWidget that sits on top of the VTK widget and draws seeds, centerline, and crosshair using QPainter.

- [ ] **Step 1: Write test for coordinate conversion**

```python
# tests/test_overlay_painter.py
import numpy as np
import pytest

def test_voxel_to_screen_axial():
    """Axial view: voxel [z,y,x] → screen pixel at (x*sx, y*sy) position."""
    from pcat_workstation.widgets.overlay_painter import voxel_to_screen
    # Simple case: spacing=[1,1,1], widget 512x512, volume 20x64x64
    # Axial view at slice z=10: shows X-Y plane
    screen = voxel_to_screen(
        ijk=[10, 32, 32],
        orientation="axial",
        current_slice=10,
        spacing=[1.0, 1.0, 1.0],
        volume_shape=(20, 64, 64),
        widget_size=(512, 512),
        parallel_scale=32.0,  # half-height in world coords
    )
    # Should map to center of widget
    assert screen is not None
    assert abs(screen[0] - 256) < 20  # x near center
    assert abs(screen[1] - 256) < 20  # y near center

def test_voxel_outside_slab_returns_none():
    from pcat_workstation.widgets.overlay_painter import voxel_to_screen
    screen = voxel_to_screen(
        ijk=[5, 32, 32],  # z=5, far from current slice z=10
        orientation="axial",
        current_slice=10,
        spacing=[1.0, 1.0, 1.0],
        volume_shape=(20, 64, 64),
        widget_size=(512, 512),
        parallel_scale=32.0,
        slab_mm=2.0,  # ±1mm = ±1 voxel
    )
    assert screen is None  # outside slab
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_overlay_painter.py -v`

- [ ] **Step 3: Implement OverlayPainter**

Create `pcat_workstation/widgets/overlay_painter.py`:

- `voxel_to_screen()` function: converts [z,y,x] voxel to (px, py) screen coordinates for a given orientation, current slice, spacing, and camera parallel scale. Returns None if outside slab.
- `OverlayPainter(QWidget)` class:
  - Transparent widget (`setAttribute(Qt.WA_TransparentForMouseEvents)`) sized to match the VTK widget
  - `set_data(seed_editor, vessel_colors)` — stores reference to SeedEditor
  - `paintEvent()` calls QPainter to draw:
    - Crosshair lines (thin white dashed)
    - Seed markers (square for ostium, circle for waypoints, with white edge + vessel color fill)
    - Selected seed highlight (yellow ring, larger)
    - Centerline spline (vessel-colored polyline, slab-filtered with NaN breaks)
  - `update_view_params(orientation, current_slice, spacing, volume_shape, parallel_scale, camera_focal_point)` — called when view changes

- [ ] **Step 4: Run tests**

Run: `pytest tests/test_overlay_painter.py -v`

- [ ] **Step 5: Commit**

```bash
git add pcat_workstation/widgets/overlay_painter.py tests/test_overlay_painter.py
git commit -m "feat: OverlayPainter — QPainter 2D overlay for seeds + centerline"
```

---

## Task 3: Integrate OverlayPainter into VTKSliceView

**Files:**
- Modify: `pcat_workstation/widgets/vtk_slice_view.py`
- Modify: `pcat_workstation/widgets/mpr_panel.py`

Wire the OverlayPainter into VTKSliceView. The overlay sits on top of the VTK widget and redraws when the slice, zoom, or seeds change.

- [ ] **Step 1: Add OverlayPainter to VTKSliceView**

In `vtk_slice_view.py`:
- Import `OverlayPainter`
- In `__init__`, create overlay as child widget, sized to match VTK widget
- In `set_slice()`, call `self._overlay.update_view_params(...)` + `self._overlay.update()`
- In `_on_ctrl_scroll()` (zoom), update overlay params
- Add `set_seed_editor(editor)` method that passes the SeedEditor reference to the overlay
- Wire mouse events: left press/drag/release → `editor.on_left_press/drag/release(voxel)`
- Wire key events: → `editor.on_key(key, modifiers)`

- [ ] **Step 2: Remove old VTK seed/centerline actor code**

Remove from `vtk_slice_view.py`:
- `set_seed_overlay_extended()` (~60 lines)
- `set_seed_overlay()` (~20 lines)
- `_create_sphere_marker()` (~40 lines)
- `_create_cube_marker()` (~40 lines)
- `update_single_seed_position()` (~20 lines)
- `set_selection_highlight()` (~30 lines)
- `clear_selection_highlight()` (~15 lines)
- `set_centerline_overlay()` (~80 lines)
- `_update_centerline_clip()` (~20 lines)
- `set_contour_overlay()` (~50 lines)
- `_update_seed_visibility()` (~20 lines)
- `_seed_actor_info` list and `_centerline_mappers` list
- All VTK imports only needed for seeds (vtkCubeSource, vtkSphereSource, vtkDiskSource, vtkPlaneSource, vtkPlane, etc.)

This removes ~400 lines of VTK actor management code.

- [ ] **Step 3: Update mpr_panel.py**

In `mpr_panel.py`:
- Remove `set_seed_overlay()`, `set_centerline_overlay()`, `set_contour_overlay()`, `set_contour_data()` delegate methods
- Add `set_seed_editor(editor)` that calls `view.set_seed_editor(editor)` on all 3 views
- Add `refresh_overlays()` that calls `view._overlay.update()` on all 3 views

- [ ] **Step 4: Test manually**

Run: `python -m pcat_workstation.main`
- Import DICOM → volume loads
- Click to place ostium → should see square marker on all 3 views
- Enter to add waypoints → circles appear, spline line connects them
- Drag a seed → spline follows in real-time
- Scroll → markers only visible near current slice

- [ ] **Step 5: Commit**

```bash
git add pcat_workstation/widgets/vtk_slice_view.py pcat_workstation/widgets/mpr_panel.py pcat_workstation/widgets/overlay_painter.py
git commit -m "feat: integrate QPainter overlay, remove VTK seed/centerline actors"
```

---

## Task 4: Simplify MainWindow signal wiring

**Files:**
- Modify: `pcat_workstation/app/main_window.py`
- Delete: `pcat_workstation/controllers/seed_edit_controller.py`
- Delete: `pcat_workstation/models/seed_edit_state.py`

Replace the old seed editing setup with the new SeedEditor.

- [ ] **Step 1: Replace _enable_seed_editing with SeedEditor**

In `main_window.py`:
- Remove import of `SeedEditState`, `SeedEditController`
- Import `SeedEditor` from `pcat_workstation.models.seed_editor`
- Replace `_enable_seed_editing()` method: create `SeedEditor`, call `self._mpr_panel.set_seed_editor(editor)`, connect signals:
  - `editor.centerline_changed` → dispatch CPRWorker
  - `editor.save_requested` → save to session
- Remove `_on_edit_centerline_changed()` — handled by direct signal connection
- Remove `_on_seeds_edited()` — no longer needed (CPR auto-updates)
- Remove `_on_contours_ready()` if still present
- Simplify `_on_run_pipeline()` — `editor.save_to_session(session)` before run

- [ ] **Step 2: Delete old files**

```bash
git rm pcat_workstation/controllers/seed_edit_controller.py
git rm pcat_workstation/models/seed_edit_state.py
```

- [ ] **Step 3: Update imports everywhere**

Search for `seed_edit_state` and `seed_edit_controller` imports in all files:
- `pipeline_worker.py` imports `_fit_spline_centerline` from `seed_edit_state` → update to import from `seed_editor`
- `main_window.py` → already updated
- Any test files → update imports

- [ ] **Step 4: Run tests**

Run: `pytest tests/ -v --tb=short -k "not test_stage_rows"`
Expected: All existing tests pass (may need import path updates)

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "refactor: simplify MainWindow, delete old seed_edit_state + controller"
```

---

## Task 5: Fast CPR path (~100ms)

**Files:**
- Modify: `pcat_workstation/workers/cpr_worker.py`

Replace the slow `_compute_cpr_data` wrapper (30s!) with direct calls to the fast building blocks.

- [ ] **Step 1: Write benchmark test**

```python
# tests/test_cpr_speed.py
import time
import numpy as np
import pytest

def test_fast_cpr_under_500ms():
    """CPR generation should complete in < 500ms for live editing."""
    from pcat_workstation.workers.cpr_worker import build_cpr_fast
    # Synthetic volume
    vol = np.random.default_rng(42).normal(0, 100, (20, 64, 64)).astype(np.float32)
    cl = np.array([[z, 32, 32] for z in range(2, 18)], dtype=np.float64)
    spacing = [1.0, 0.5, 0.5]

    t0 = time.perf_counter()
    result = build_cpr_fast(vol, cl, spacing)
    dt = time.perf_counter() - t0

    assert result is not None
    assert dt < 0.5  # 500ms max
```

- [ ] **Step 2: Implement fast CPR path in cpr_worker.py**

Add `build_cpr_fast()` function that calls:
1. `_bezier_fit_centerline(cl_mm)` — <1ms
2. `_sample_bezier_frame(cs, total_len, n_wide)` — ~8ms
3. `_build_cpr_image_fast(vol, spacing, positions, normals, binormals, ...)` — ~93ms

Total: ~100ms. No aorta prepend, no rotation handling (that stays in the full pipeline path).

Update `CPRWorker.run()` to use `build_cpr_fast()` instead of `_compute_cpr_data()`.

Also return the Bishop frame (N_frame, B_frame, positions, arclengths) for cross-section sampling.

- [ ] **Step 3: Run benchmark**

Run: `pytest tests/test_cpr_speed.py -v`
Expected: PASS (< 500ms)

- [ ] **Step 4: Commit**

```bash
git add pcat_workstation/workers/cpr_worker.py tests/test_cpr_speed.py
git commit -m "perf: fast CPR path ~100ms (bypass slow _compute_cpr_data wrapper)"
```

---

## Task 6: Clean up cpr_view.py

**Files:**
- Modify: `pcat_workstation/widgets/cpr_view.py`

Remove dead contour code and fix needle perpendicularity.

- [ ] **Step 1: Remove dead contour code**

Remove from `cpr_view.py`:
- `_VesselData.contour_result` field (line 109, 123)
- `_draw_wall_boundaries()` method (lines 320-353)
- `_draw_pcat_boundary()` method (lines 355-395)
- Calls to these in `paintEvent` (lines 259, 262)
- `set_contour_data()` method (lines 881-902)
- All `contour_result` references in `_on_needle_moved`, `_n_positions`, `_refresh_all_cs`
- `_y_for_index` / `_index_for_y` aliases (lines 227-228)

- [ ] **Step 2: Fix needle lines to be perpendicular to vessel tangent**

In `_CPRPanel.paintEvent()`, the needle lines are currently vertical:
```python
p.drawLine(QPointF(nx, rect.top()), QPointF(nx, rect.bottom()))
```

For a straightened CPR (vessel horizontal), vertical IS perpendicular. This is correct. But add a comment explaining why:
```python
# In straightened CPR, vessel runs horizontally (left→right),
# so perpendicular = vertical. In stretched mode, the vessel
# curves and needles would need to follow the local normal.
```

- [ ] **Step 3: Test**

Run: `python -m pcat_workstation.main`
- Verify CPR still works, no errors about contour_result
- Verify cross-sections still show

- [ ] **Step 4: Commit**

```bash
git add pcat_workstation/widgets/cpr_view.py
git commit -m "refactor: remove dead contour code from cpr_view.py (~200 lines)"
```

---

## Task 7: "Run Pipeline" button in toolbar

**Files:**
- Modify: `pcat_workstation/widgets/toolbar.py`
- Modify: `pcat_workstation/app/main_window.py`

Add a prominent "Run Pipeline" button matching the "Import DICOM" visual style.

- [ ] **Step 1: Add button to toolbar**

In `toolbar.py`, add a "Run Pipeline" button with the same blue styling as "Import DICOM" in the DICOM browser. Place it after the vessel selector buttons.

```python
self._run_pipeline_btn = QPushButton("▶ Run Pipeline")
self._run_pipeline_btn.setFixedHeight(36)
self._run_pipeline_btn.setCursor(Qt.PointingHandCursor)
self._run_pipeline_btn.setEnabled(False)
self._run_pipeline_btn.setStyleSheet("""
    QPushButton { background-color: #0a84ff; color: white; border: none;
                  border-radius: 4px; font-size: 13pt; font-weight: bold; padding: 0 16px; }
    QPushButton:hover { background-color: #0070e0; }
    QPushButton:disabled { background-color: #3a3a3c; color: #636366; }
""")
self._run_pipeline_btn.clicked.connect(self.run_pipeline_clicked)
```

Add signal: `run_pipeline_clicked = Signal()`

- [ ] **Step 2: Wire in MainWindow**

- Connect `toolbar.run_pipeline_clicked` → `_on_run_pipeline`
- In `_on_run_pipeline`: save seeds from editor → run pipeline
- Enable/disable the button based on whether any vessel has ostium + waypoints:
  - Connect `editor.seeds_changed` → check and enable/disable
- After pipeline completes: enable FAI overlay, show analysis

- [ ] **Step 3: Remove the old "Run All" button logic if redundant**

Keep the progress panel's "Run" button (Ctrl+R) for step-by-step execution.
The new toolbar button runs the full pipeline.

- [ ] **Step 4: Test**

Run app → place seeds → verify "Run Pipeline" button becomes active → click → pipeline runs → FAI overlay appears

- [ ] **Step 5: Commit**

```bash
git add pcat_workstation/widgets/toolbar.py pcat_workstation/app/main_window.py
git commit -m "feat: Run Pipeline button in toolbar (same style as Import DICOM)"
```

---

## Task 8: Final integration test + cleanup

**Files:**
- Modify: `tests/test_pipeline_walkthrough.py`

- [ ] **Step 1: Update walkthrough test**

Update `test_pipeline_walkthrough.py` to use the new `SeedEditor` instead of old `SeedEditState`. Ensure the full workflow test still passes:
1. Create session + load volume
2. Create SeedEditor, place seeds
3. Run pipeline → verify all stages complete
4. Verify FAI stats are computed

- [ ] **Step 2: Run full test suite**

Run: `pytest tests/ -v --tb=short`
Expected: All tests pass

- [ ] **Step 3: Manual walkthrough**

Full clinician workflow:
1. Launch app → both sidebars hidden, full image area
2. Ctrl+1 → show DICOM browser → Import DICOM folder
3. Volume loads → edit mode active, seed markers visible
4. Click LAD ostium → square marker appears
5. Enter to add waypoints → circles, spline line
6. Arrow keys to navigate seeds, drag to adjust
7. CPR updates on mouse release (~100ms)
8. Ctrl+S to save
9. Click "Run Pipeline" → stages progress → FAI overlay appears
10. Switch vessels → analysis dashboard updates
11. Ctrl+2 → check vessel results

- [ ] **Step 4: Final commit**

```bash
git add -A
git commit -m "test: update walkthrough tests for new architecture"
git push origin master
```
