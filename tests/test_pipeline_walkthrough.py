"""
test_pipeline_walkthrough.py
Simulate the full clinician workflow end-to-end:
  1. Create session + load synthetic volume
  2. Attempt pipeline run without seeds → expect failure message
  3. Place seeds via SeedEditState
  4. Run pipeline → seeds validation, FMM centerline, VOI, statistics
  5. Verify all signals fire and results are correct

Runs headless (no VTK) using QApplication event loop for signal delivery.
"""

import sys
import time
from pathlib import Path
from unittest.mock import MagicMock

import numpy as np
import pytest
from PySide6.QtCore import QCoreApplication, QTimer, QEventLoop

sys.path.insert(0, str(Path(__file__).parent.parent))

from pcat_workstation.models.patient_session import PatientSession, PIPELINE_STAGES
from pcat_workstation.workers.pipeline_worker import PipelineWorker


@pytest.fixture(scope="session")
def qapp():
    """Ensure a QCoreApplication exists for signal/slot delivery."""
    app = QCoreApplication.instance()
    if app is None:
        app = QCoreApplication(sys.argv)
    return app


@pytest.fixture
def synthetic_volume():
    """(20, 64, 64) volume with vessel tube at (y=32, x=32) and fat ring around it."""
    rng = np.random.default_rng(42)
    vol = np.zeros((20, 64, 64), dtype=np.float32)
    z, y, x = np.indices(vol.shape)

    # Vessel lumen: bright contrast (300-500 HU)
    vessel = (y - 32)**2 + (x - 32)**2 <= 4**2
    vol[vessel] = rng.uniform(300, 500, size=vessel.sum())

    # Perivascular fat ring: 4-8 voxels
    fat = ((y - 32)**2 + (x - 32)**2 > 4**2) & ((y - 32)**2 + (x - 32)**2 <= 8**2)
    vol[fat] = rng.uniform(-150, -60, size=fat.sum())

    # Background: soft tissue
    bg = ~vessel & ~fat
    vol[bg] = rng.normal(50, 20, size=bg.sum()).astype(np.float32)

    return vol


@pytest.fixture
def spacing():
    return [1.0, 0.5, 0.5]


@pytest.fixture
def session(tmp_path, synthetic_volume, spacing):
    """A PatientSession with volume and meta loaded, import stage complete."""
    session_dir = tmp_path / "test_session"
    session_dir.mkdir()
    s = PatientSession(session_dir)
    s._volume = synthetic_volume
    s._meta = {
        "patient_id": "TEST001",
        "study_date": "20260324",
        "spacing_mm": spacing,
        "shape": list(synthetic_volume.shape),
    }
    s.patient_id = "TEST001"
    s.study_date = "20260324"
    s.dicom_dir = tmp_path / "fake_dicom"
    s.set_stage_status("import", "complete")
    return s


def _run_worker_sync(worker, qapp, timeout_ms=30000):
    """Run a PipelineWorker and block until it finishes or times out.

    Returns dict of collected signal emissions.
    """
    collected = {
        "stage_started": [],
        "stage_completed": [],
        "stage_failed": [],
        "pipeline_completed": [],
        "pipeline_failed": [],
        "progress_messages": [],
        "seeds_ready": [],
        "centerlines_ready": [],
        "cpr_ready": [],
        "voi_masks_ready": [],
        "analysis_data_ready": [],
    }

    loop = QEventLoop()

    worker.stage_started.connect(lambda s: collected["stage_started"].append(s))
    worker.stage_completed.connect(lambda s, t: collected["stage_completed"].append((s, t)))
    worker.stage_failed.connect(lambda s, e: collected["stage_failed"].append((s, e)))
    worker.pipeline_completed.connect(lambda r: (collected["pipeline_completed"].append(r), loop.quit()))
    worker.pipeline_failed.connect(lambda e: (collected["pipeline_failed"].append(e), loop.quit()))
    worker.progress_message.connect(lambda m: collected["progress_messages"].append(m))
    worker.seeds_ready.connect(lambda d: collected["seeds_ready"].append(d))
    worker.centerlines_ready.connect(lambda d: collected["centerlines_ready"].append(d))
    worker.cpr_ready.connect(lambda v, img, ext: collected["cpr_ready"].append((v, img, ext)))
    worker.voi_masks_ready.connect(lambda d: collected["voi_masks_ready"].append(d))
    worker.analysis_data_ready.connect(lambda v, d: collected["analysis_data_ready"].append((v, d)))

    # Timeout safety
    timer = QTimer()
    timer.setSingleShot(True)
    timer.timeout.connect(loop.quit)
    timer.start(timeout_ms)

    worker.start()
    loop.exec()

    timed_out = not timer.isActive()
    timer.stop()

    collected["timed_out"] = timed_out
    return collected


# ============================================================
# Test 1: Pipeline without seeds should fail gracefully
# ============================================================

class TestPipelineWithoutSeeds:

    def test_pipeline_fails_with_no_seeds(self, session, qapp):
        """Running pipeline without seeds should emit pipeline_failed, not hang."""
        worker = PipelineWorker(session=session, resume_from="seeds")
        result = _run_worker_sync(worker, qapp, timeout_ms=5000)

        assert not result["timed_out"], "Pipeline TIMED OUT (froze!)"
        assert len(result["pipeline_failed"]) == 1
        assert "seeds" in result["pipeline_failed"][0].lower()

    def test_session_status_after_no_seeds(self, session, qapp):
        """After failed seeds stage, session should be 'failed' (not stuck in 'running')."""
        worker = PipelineWorker(session=session, resume_from="seeds")
        _run_worker_sync(worker, qapp, timeout_ms=5000)
        assert session.stage_status["seeds"] == "failed"


# ============================================================
# Test 2: Pipeline with seeds should complete
# ============================================================

class TestSeedEditStateIntegration:
    """Test that SeedEditState.save_to_session format is readable by pipeline."""

    def test_extended_format_parsed(self, session, qapp):
        """Pipeline worker should parse the {flat: ..., extended: ...} format."""
        # This is how SeedEditState.save_to_session stores seeds
        session.seeds_data = {
            "flat": {"LAD": [2, 32, 32]},
            "extended": {
                "LAD": {
                    "ostium": [2, 32, 32],
                    "waypoints": [[10, 32, 32], [17, 32, 32]],
                },
            },
        }
        worker = PipelineWorker(session=session, resume_from="seeds", stop_after="seeds")
        result = _run_worker_sync(worker, qapp, timeout_ms=5000)
        assert not result["timed_out"]
        assert len(result["pipeline_failed"]) == 0, f"Failed: {result['pipeline_failed']}"
        assert len(result["seeds_ready"]) == 1
        assert "LAD" in result["seeds_ready"][0]


class TestPipelineWithSeeds:

    @pytest.fixture
    def session_with_seeds(self, session):
        """Add ostium seeds at the vessel center (SeedEditState extended format)."""
        session.seeds_data = {
            "flat": {"LAD": [2, 32, 32]},
            "extended": {
                "LAD": {
                    "ostium": [2, 32, 32],
                    "waypoints": [[10, 32, 32], [17, 32, 32]],
                },
            },
        }
        return session

    def test_seeds_stage_validates(self, session_with_seeds, qapp):
        """Seeds stage should validate and emit seeds_ready."""
        worker = PipelineWorker(
            session=session_with_seeds,
            resume_from="seeds",
            stop_after="seeds",
        )
        result = _run_worker_sync(worker, qapp, timeout_ms=5000)

        assert not result["timed_out"], "Seeds stage TIMED OUT"
        assert len(result["pipeline_failed"]) == 0, f"Failed: {result['pipeline_failed']}"
        assert len(result["seeds_ready"]) == 1
        assert "LAD" in result["seeds_ready"][0]

    def test_centerlines_stage(self, session_with_seeds, qapp):
        """Centerlines stage should extract centerline via FMM and emit signals."""
        worker = PipelineWorker(
            session=session_with_seeds,
            resume_from="seeds",
            stop_after="centerlines",
        )
        result = _run_worker_sync(worker, qapp, timeout_ms=60000)

        assert not result["timed_out"], "Centerlines stage TIMED OUT"
        if result["pipeline_failed"]:
            pytest.fail(f"Pipeline failed: {result['pipeline_failed']}")

        # Should have completed seeds and centerlines
        completed_stages = [s for s, t in result["stage_completed"]]
        assert "seeds" in completed_stages
        assert "centerlines" in completed_stages

        # Centerlines and CPR should be emitted
        assert len(result["centerlines_ready"]) == 1
        # CPR may or may not succeed on synthetic data

    def test_full_pipeline(self, session_with_seeds, qapp):
        """Full pipeline: seeds → centerlines → VOI → statistics."""
        worker = PipelineWorker(
            session=session_with_seeds,
            resume_from="seeds",
        )
        result = _run_worker_sync(worker, qapp, timeout_ms=120000)

        assert not result["timed_out"], "Full pipeline TIMED OUT (froze!)"
        if result["pipeline_failed"]:
            # Print progress messages for debugging
            print("\n--- Progress messages ---")
            for msg in result["progress_messages"]:
                print(f"  {msg}")
            print("---")
            pytest.fail(f"Pipeline failed: {result['pipeline_failed']}")

        # All stages should complete
        completed_stages = [s for s, t in result["stage_completed"]]
        assert "seeds" in completed_stages
        assert "centerlines" in completed_stages
        assert "pcat_voi" in completed_stages
        assert "statistics" in completed_stages

        # Pipeline completed signal should fire
        assert len(result["pipeline_completed"]) == 1

        # Results should have vessel stats
        results = result["pipeline_completed"][0]
        assert "vessels" in results


# ============================================================
# Test 3: Session stage_status consistency
# ============================================================

class TestSessionStageConsistency:

    def test_new_session_has_five_stages(self, tmp_path):
        s = PatientSession(tmp_path / "s")
        assert len(s.stage_status) == 5
        assert "contours" not in s.stage_status
        assert list(s.stage_status.keys()) == PIPELINE_STAGES

    def test_old_session_contours_removed(self, tmp_path):
        """Loading an old session with contours stage should drop it."""
        import json
        d = tmp_path / "old"
        d.mkdir()
        (d / "session.json").write_text(json.dumps({
            "patient_id": "OLD",
            "study_date": "",
            "series_description": "",
            "kVp": 120.0,
            "dicom_dir": None,
            "created_at": "2026-01-01T00:00:00",
            "modified_at": "2026-01-01T00:00:00",
            "stage_status": {
                "import": "complete",
                "seeds": "complete",
                "centerlines": "pending",
                "contours": "pending",
                "pcat_voi": "pending",
                "statistics": "pending",
            },
            "vessel_stats": {},
        }))
        loaded = PatientSession.load(d)
        assert "contours" not in loaded.stage_status
        assert "vesselness" not in loaded.stage_status
        assert loaded.get_resume_stage() == "centerlines"


# Test 4 (Progress panel stages) is in test_pipeline_ux.py::TestProgressPanel
