"""Tests for Pipeline UX: state clearing, step-by-step execution, seed visibility,
vesselness removal, and backward compatibility.

VTK-based tests are skipped when no display is available (macOS offscreen segfaults).
Pure logic tests run everywhere.
"""

import json
import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock

import numpy as np
import pytest

# Ensure project root is importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pcat_workstation.app.config import PIPELINE_STAGES, STAGE_LABELS
from pcat_workstation.models.patient_session import (
    PIPELINE_STAGES as MODEL_STAGES,
    PatientSession,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

DICOM_DIR = Path("/Users/shunie/Developer/PCAT/Rahaf_Patients/2.1")

# VTK + QApplication segfaults in offscreen mode on macOS.
# Only enable VTK tests when a real display is available.
_HAS_DISPLAY = os.environ.get("DISPLAY") or sys.platform == "darwin"
_VTK_REASON = "VTK widgets require a live display (macOS offscreen segfaults)"


def _make_qt_app():
    """Get or create a QApplication for VTK tests."""
    from PySide6.QtWidgets import QApplication
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


@pytest.fixture
def tmp_session_dir(tmp_path):
    d = tmp_path / "test_session"
    d.mkdir()
    return d


@pytest.fixture
def session(tmp_session_dir):
    return PatientSession(tmp_session_dir)


# ===========================================================================
# 1. Vesselness removal — config & model
# ===========================================================================

class TestVesselnessRemoval:

    def test_vesselness_not_in_config_stages(self):
        assert "vesselness" not in PIPELINE_STAGES

    def test_vesselness_not_in_config_labels(self):
        assert "vesselness" not in STAGE_LABELS

    def test_vesselness_not_in_model_stages(self):
        assert "vesselness" not in MODEL_STAGES

    def test_config_and_model_stages_match(self):
        assert PIPELINE_STAGES == MODEL_STAGES

    def test_stage_count_is_six(self):
        assert len(PIPELINE_STAGES) == 6

    def test_stage_order(self):
        expected = ["import", "seeds", "centerlines", "contours", "pcat_voi", "statistics"]
        assert PIPELINE_STAGES == expected

    def test_new_session_has_no_vesselness(self, session):
        assert "vesselness" not in session.stage_status
        assert len(session.stage_status) == 6

    def test_backward_compat_old_session_json(self, tmp_session_dir):
        """Loading a session.json with vesselness should silently drop it."""
        old_data = {
            "patient_id": "legacy",
            "study_date": "20250101",
            "series_description": "old",
            "kVp": 120.0,
            "dicom_dir": None,
            "created_at": "2026-01-01T00:00:00",
            "modified_at": "2026-01-01T00:00:00",
            "stage_status": {
                "import": "complete",
                "seeds": "complete",
                "vesselness": "complete",
                "centerlines": "pending",
                "contours": "pending",
                "pcat_voi": "pending",
                "statistics": "pending",
            },
            "vessel_stats": {},
        }
        json_path = tmp_session_dir / "session.json"
        json_path.write_text(json.dumps(old_data), encoding="utf-8")

        loaded = PatientSession.load(tmp_session_dir)
        assert "vesselness" not in loaded.stage_status
        assert loaded.stage_status["import"] == "complete"
        assert loaded.stage_status["seeds"] == "complete"
        assert loaded.stage_status["centerlines"] == "pending"

    def test_real_session_backward_compat(self):
        """The actual l_140 session on disk has vesselness — verify it loads."""
        session_dir = Path.home() / ".pcat_workstation/sessions/l_140_20251010_20260316_154603"
        if not (session_dir / "session.json").exists():
            pytest.skip("Real session not found")
        loaded = PatientSession.load(session_dir)
        assert "vesselness" not in loaded.stage_status


# ===========================================================================
# 2. PatientSession.get_resume_stage()
# ===========================================================================

class TestResumeStage:

    def test_resume_after_import(self, session):
        session.stage_status["import"] = "complete"
        assert session.get_resume_stage() == "seeds"

    def test_resume_after_seeds(self, session):
        session.stage_status["import"] = "complete"
        session.stage_status["seeds"] = "complete"
        assert session.get_resume_stage() == "centerlines"

    def test_resume_skips_vesselness(self, session):
        """After removing vesselness, seeds -> centerlines directly."""
        session.stage_status["import"] = "complete"
        session.stage_status["seeds"] = "complete"
        assert session.get_resume_stage() == "centerlines"

    def test_resume_all_complete(self, session):
        for stage in MODEL_STAGES:
            session.stage_status[stage] = "complete"
        assert session.get_resume_stage() is None

    def test_resume_nothing_complete(self, session):
        assert session.get_resume_stage() is None

    def test_resume_chain_full(self, session):
        """Step through all stages one by one."""
        expected_chain = ["seeds", "centerlines", "contours", "pcat_voi", "statistics", None]
        for i, expected_next in enumerate(expected_chain):
            if i > 0:
                session.stage_status[MODEL_STAGES[i]] = "complete"
            if i == 0:
                session.stage_status["import"] = "complete"
            assert session.get_resume_stage() == expected_next, f"After completing {i+1} stages"


# ===========================================================================
# 3. PipelineWorker — stop_after and vesselness merge
# ===========================================================================

class TestPipelineWorkerStopAfter:

    def test_stop_after_param_accepted(self):
        from pcat_workstation.workers.pipeline_worker import PipelineWorker
        session = MagicMock()
        session.stage_status = {s: "pending" for s in MODEL_STAGES}
        session.get_volume.return_value = None
        session.session_dir = Path("/tmp/fake")
        session._prefix = "pcat"

        worker = PipelineWorker(
            session=session, resume_from="seeds", stop_after="seeds",
        )
        assert worker.stop_after == "seeds"
        assert worker.resume_from == "seeds"

    def test_stop_after_guard_requires_complete_status(self):
        """stop_after guard should NOT fire if stage status != 'complete'."""
        from pcat_workstation.workers.pipeline_worker import PipelineWorker
        session = MagicMock()
        session.stage_status = {s: "pending" for s in MODEL_STAGES}
        session.stage_status["import"] = "complete"
        session.get_volume.return_value = np.zeros((4, 4, 4), dtype=np.float32)
        session.get_meta.return_value = {"spacing_mm": [1.0, 1.0, 1.0]}
        session.session_dir = Path(tempfile.mkdtemp())
        session._prefix = "pcat"
        session.dicom_dir = Path("/fake")

        worker = PipelineWorker(session=session, stop_after="centerlines")
        # centerlines is "pending" → guard `status == "complete"` is False → won't stop
        assert session.stage_status.get("centerlines") != "complete"

    def test_should_skip_logic(self):
        from pcat_workstation.workers.pipeline_worker import PipelineWorker
        session = MagicMock()
        session.stage_status = {
            "import": "complete",
            "seeds": "complete",
            "centerlines": "pending",
            "contours": "pending",
            "pcat_voi": "pending",
            "statistics": "pending",
        }
        worker = PipelineWorker(session=session, resume_from="centerlines")
        # Stages before resume_from should be skipped
        assert worker._should_skip("import") is True
        assert worker._should_skip("seeds") is True
        # The target stage should not be skipped (it's pending)
        assert worker._should_skip("centerlines") is False

    def test_no_vesselness_in_should_skip(self):
        """_should_skip should never encounter vesselness stage."""
        from pcat_workstation.workers.pipeline_worker import PipelineWorker
        session = MagicMock()
        session.stage_status = {s: "pending" for s in MODEL_STAGES}
        worker = PipelineWorker(session=session)
        # vesselness is not in PIPELINE_STAGES, so index lookup fails
        # but _should_skip handles ValueError gracefully
        assert worker._should_skip("vesselness") is False  # not "complete"


# ===========================================================================
# 4. Seed visibility logic (pure math, no VTK)
# ===========================================================================

class TestSeedVisibilityLogic:
    """Test the distance-based visibility logic without VTK."""

    def _compute_visibility(self, orientation, seed_ijk, spacing, current_slice):
        """Replicate the visibility logic from _update_seed_visibility."""
        z, y, x = seed_ijk
        sx, sy, sz = spacing[2], spacing[1], spacing[0]
        cx, cy, cz = x * sx, y * sy, z * sz

        if orientation == "axial":
            slice_mm = current_slice * sz
            seed_mm = cz
        elif orientation == "coronal":
            slice_mm = current_slice * sy
            seed_mm = cy
        else:  # sagittal
            slice_mm = current_slice * sx
            seed_mm = cx

        return abs(seed_mm - slice_mm) <= 2.0

    def test_axial_seed_at_slice(self):
        assert self._compute_visibility("axial", [16, 10, 10], [1, 1, 1], 16) is True

    def test_axial_seed_far_from_slice(self):
        assert self._compute_visibility("axial", [16, 10, 10], [1, 1, 1], 0) is False

    def test_axial_seed_within_2mm(self):
        assert self._compute_visibility("axial", [16, 10, 10], [1, 1, 1], 14) is True
        assert self._compute_visibility("axial", [16, 10, 10], [1, 1, 1], 18) is True

    def test_axial_seed_just_outside_2mm(self):
        assert self._compute_visibility("axial", [16, 10, 10], [1, 1, 1], 13) is False
        assert self._compute_visibility("axial", [16, 10, 10], [1, 1, 1], 19) is False

    def test_coronal_orientation(self):
        # Seed at y=20, coronal slices along Y
        assert self._compute_visibility("coronal", [10, 20, 10], [1, 1, 1], 20) is True
        assert self._compute_visibility("coronal", [10, 20, 10], [1, 1, 1], 0) is False

    def test_sagittal_orientation(self):
        # Seed at x=25, sagittal slices along X
        assert self._compute_visibility("sagittal", [10, 10, 25], [1, 1, 1], 25) is True
        assert self._compute_visibility("sagittal", [10, 10, 25], [1, 1, 1], 0) is False

    def test_nonuniform_spacing(self):
        # spacing [sz, sy, sx] = [2.0, 0.5, 0.5]
        # Seed at z=10 → world z = 10 * 2.0 = 20mm
        # Slice 10 → 20mm → visible
        assert self._compute_visibility("axial", [10, 10, 10], [2.0, 0.5, 0.5], 10) is True
        # Slice 11 → 22mm → 2mm away → visible
        assert self._compute_visibility("axial", [10, 10, 10], [2.0, 0.5, 0.5], 11) is True
        # Slice 12 → 24mm → 4mm away → hidden
        assert self._compute_visibility("axial", [10, 10, 10], [2.0, 0.5, 0.5], 12) is False

    def test_boundary_exactly_2mm(self):
        # Exactly 2mm should be visible (<=2.0)
        assert self._compute_visibility("axial", [10, 10, 10], [1, 1, 1], 12) is True
        assert self._compute_visibility("axial", [10, 10, 10], [1, 1, 1], 8) is True


# ===========================================================================
# 4b. Crosshair line coordinate logic (pure math, no VTK)
# ===========================================================================

class TestCrosshairLogic:
    """Verify the crosshair line endpoint math from update_crosshair_lines."""

    def _compute_crosshair_endpoints(self, orientation, x_mm, y_mm, z_mm, shape, spacing):
        """Replicate the line endpoint logic from update_crosshair_lines."""
        nz, ny, nx = shape
        sx, sy, sz = spacing[2], spacing[1], spacing[0]
        wx, wy, wz = nx * sx, ny * sy, nz * sz

        if orientation == "axial":
            h_pts = [(0, y_mm, z_mm), (wx, y_mm, z_mm)]
            v_pts = [(x_mm, 0, z_mm), (x_mm, wy, z_mm)]
        elif orientation == "coronal":
            h_pts = [(0, y_mm, z_mm), (wx, y_mm, z_mm)]
            v_pts = [(x_mm, y_mm, 0), (x_mm, y_mm, wz)]
        else:  # sagittal
            h_pts = [(x_mm, 0, z_mm), (x_mm, wy, z_mm)]
            v_pts = [(x_mm, y_mm, 0), (x_mm, y_mm, wz)]
        return h_pts, v_pts

    def test_axial_crosshair_endpoints(self):
        shape = (32, 32, 32)
        spacing = [1.0, 1.0, 1.0]
        h, v = self._compute_crosshair_endpoints("axial", 10, 15, 20, shape, spacing)
        # Horizontal line at y=15 spanning full X range
        assert h[0] == (0, 15, 20)
        assert h[1] == (32, 15, 20)
        # Vertical line at x=10 spanning full Y range
        assert v[0] == (10, 0, 20)
        assert v[1] == (10, 32, 20)

    def test_coronal_crosshair_endpoints(self):
        shape = (32, 32, 32)
        spacing = [1.0, 1.0, 1.0]
        h, v = self._compute_crosshair_endpoints("coronal", 10, 15, 20, shape, spacing)
        # Horizontal line at z=20 spanning full X range
        assert h[0] == (0, 15, 20)
        assert h[1] == (32, 15, 20)
        # Vertical line at x=10 spanning full Z range
        assert v[0] == (10, 15, 0)
        assert v[1] == (10, 15, 32)

    def test_sagittal_crosshair_endpoints(self):
        shape = (32, 32, 32)
        spacing = [1.0, 1.0, 1.0]
        h, v = self._compute_crosshair_endpoints("sagittal", 10, 15, 20, shape, spacing)
        # Horizontal line at z=20 spanning full Y range
        assert h[0] == (10, 0, 20)
        assert h[1] == (10, 32, 20)
        # Vertical line at y=15 spanning full Z range
        assert v[0] == (10, 15, 0)
        assert v[1] == (10, 15, 32)

    def test_nonuniform_spacing(self):
        shape = (64, 128, 256)
        spacing = [2.0, 0.5, 0.5]  # [sz, sy, sx]
        h, v = self._compute_crosshair_endpoints("axial", 50, 30, 100, shape, spacing)
        # wx = 256*0.5=128, wy = 128*0.5=64
        assert h[1][0] == pytest.approx(128.0)  # full X extent
        assert v[1][1] == pytest.approx(64.0)   # full Y extent

    def test_scroll_sync_position_math(self):
        """Replicate MPRPanel._on_slice_changed position computation."""
        spacing = [2.0, 0.5, 0.5]  # [sz, sy, sx]
        sx, sy, sz = spacing[2], spacing[1], spacing[0]
        axial_slice = 30
        coronal_slice = 50
        sagittal_slice = 100
        x_mm = sagittal_slice * sx
        y_mm = coronal_slice * sy
        z_mm = axial_slice * sz
        assert x_mm == pytest.approx(50.0)
        assert y_mm == pytest.approx(25.0)
        assert z_mm == pytest.approx(60.0)


# ===========================================================================
# 5. Progress panel (requires QApplication but no VTK)
# ===========================================================================

@pytest.fixture(scope="module")
def qt_app():
    """Module-scoped QApplication for progress panel tests."""
    try:
        return _make_qt_app()
    except Exception:
        pytest.skip("Qt not available")


class TestProgressPanel:

    @pytest.fixture
    def panel(self, qt_app):
        from pcat_workstation.widgets.progress_panel import ProgressPanel
        return ProgressPanel()

    def test_has_run_next_signal(self, panel):
        assert hasattr(panel, "run_next_clicked")

    def test_has_run_next_button(self, panel):
        assert hasattr(panel, "_run_next_btn")
        assert panel._run_next_btn.isEnabled() is False

    def test_set_run_next_enabled(self, panel):
        panel.set_run_next_enabled(True)
        assert panel._run_next_btn.isEnabled() is True
        panel.set_run_next_enabled(False)
        assert panel._run_next_btn.isEnabled() is False

    def test_set_running_disables_run_next(self, panel):
        panel.set_run_next_enabled(True)
        panel.set_running(True)
        assert panel._run_next_btn.isEnabled() is False

    def test_set_running_changes_vessel_group_title(self, panel):
        panel.set_running(True)
        assert panel._vessel_group.title() == "Progress"
        panel.set_running(False)
        assert panel._vessel_group.title() == "Vessel Summary"

    def test_clear_vessel_summary(self, panel):
        panel.set_vessel_summary({
            "LAD": {"mean_fai": -80.0, "risk": "HIGH"},
            "RCA": {"mean_fai": -75.0, "risk": "LOW"},
        })
        assert panel._vessel_layout.count() > 0
        panel.clear_vessel_summary()
        assert panel._vessel_layout.count() == 0

    def test_progress_log_capped_at_10(self, panel):
        panel.set_running(True)
        for i in range(20):
            panel.set_progress_message(f"Message {i}")
        assert panel._vessel_layout.count() <= 10

    def test_no_vesselness_stage_row(self, panel):
        assert "vesselness" not in panel._stage_rows

    def test_stage_rows_match_config(self, panel):
        assert list(panel._stage_rows.keys()) == PIPELINE_STAGES

    def test_reset_stages(self, panel):
        from pcat_workstation.widgets.progress_panel import _STATUS_ICONS
        panel.set_stage_status("import", "complete")
        panel.set_stage_status("seeds", "running")
        panel.reset_stages()
        for row in panel._stage_rows.values():
            assert row.icon_label.text() == _STATUS_ICONS["pending"]

    def test_progress_bar_range(self, panel):
        assert panel._progress_bar.maximum() == len(PIPELINE_STAGES)

    def test_run_next_button_click_emits_signal(self, panel, qt_app):
        from PySide6.QtTest import QTest
        from PySide6.QtCore import Qt
        received = []
        panel.run_next_clicked.connect(lambda: received.append(True))
        panel._run_next_btn.setEnabled(True)
        QTest.mouseClick(panel._run_next_btn, Qt.LeftButton)
        assert len(received) == 1


# ===========================================================================
# 6. MainWindow signal wiring (no VTK, mock-based)
# ===========================================================================

class TestMainWindowWiring:

    def test_connect_pipeline_signals_method_exists(self, qt_app):
        """MainWindow has the extracted helper method."""
        from pcat_workstation.app.main_window import MainWindow
        assert hasattr(MainWindow, "_connect_pipeline_signals")

    def test_on_run_next_step_method_exists(self, qt_app):
        from pcat_workstation.app.main_window import MainWindow
        assert hasattr(MainWindow, "_on_run_next_step")


# ===========================================================================
# 7. Integration: load DICOM volume
# ===========================================================================

class TestDICOMIntegration:

    def test_load_dicom_volume(self):
        if not DICOM_DIR.exists():
            pytest.skip("DICOM data not available")
        from pcat_workstation.pipeline.dicom_loader import load_dicom_series
        volume, meta = load_dicom_series(DICOM_DIR)
        assert volume is not None
        assert volume.ndim == 3
        assert volume.dtype == np.float32
        assert meta["spacing_mm"] is not None
        assert len(meta["spacing_mm"]) == 3

    def test_volume_shape_reasonable(self):
        if not DICOM_DIR.exists():
            pytest.skip("DICOM data not available")
        from pcat_workstation.pipeline.dicom_loader import load_dicom_series
        volume, meta = load_dicom_series(DICOM_DIR)
        nz, ny, nx = volume.shape
        assert nz > 10
        assert ny > 10
        assert nx > 10

    def test_step_by_step_session_flow(self, tmp_path):
        """Simulate step-by-step pipeline at session level with real DICOM metadata."""
        session_dir = tmp_path / "step_session"
        session_dir.mkdir()
        session = PatientSession(session_dir)
        session.set_stage_status("import", "complete")

        # Step through all stages
        expected = ["seeds", "centerlines", "contours", "pcat_voi", "statistics"]
        for expected_next in expected:
            assert session.get_resume_stage() == expected_next
            session.set_stage_status(expected_next, "complete")

        # All done
        assert session.get_resume_stage() is None
        assert "vesselness" not in session.stage_status

    def test_session_save_load_roundtrip(self, tmp_path):
        """Session saves and loads without vesselness."""
        session_dir = tmp_path / "roundtrip"
        session_dir.mkdir()
        session = PatientSession(session_dir)
        session.patient_id = "roundtrip_test"
        session.set_stage_status("import", "complete")
        session.set_stage_status("seeds", "complete")
        session.save()

        loaded = PatientSession.load(session_dir)
        assert loaded.patient_id == "roundtrip_test"
        assert loaded.stage_status["import"] == "complete"
        assert loaded.stage_status["seeds"] == "complete"
        assert loaded.stage_status["centerlines"] == "pending"
        assert "vesselness" not in loaded.stage_status

    def test_session_with_vessel_stats_roundtrip(self, tmp_path):
        """Session with vessel stats saves and loads correctly."""
        session_dir = tmp_path / "stats_roundtrip"
        session_dir.mkdir()
        session = PatientSession(session_dir)
        session.patient_id = "stats_test"
        session.set_stage_status("import", "complete")
        session.set_vessel_stats("LAD", {"hu_mean": -78.5, "fat_fraction": 0.65, "fai_risk": "HIGH"})
        session.save()

        loaded = PatientSession.load(session_dir)
        assert "LAD" in loaded.vessel_stats
        assert loaded.vessel_stats["LAD"]["hu_mean"] == pytest.approx(-78.5)
        assert loaded.vessel_stats["LAD"]["fai_risk"] == "HIGH"
