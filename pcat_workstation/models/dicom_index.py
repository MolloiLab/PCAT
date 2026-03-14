import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional


class DicomIndex:
    """Manages recent projects and the app-level patient index.

    Stores a small JSON file tracking recently-opened sessions so the
    app can present a "recent projects" list and avoid re-importing
    DICOM directories that already have a session.
    """

    MAX_RECENT = 20

    def __init__(self, data_dir: Path = None):
        if data_dir is None:
            data_dir = Path.home() / ".pcat_workstation"
        self.data_dir: Path = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

        self._index_path: Path = self.data_dir / "recent_projects.json"
        self._recent: List[Dict] = []
        self._load()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def add_recent(
        self,
        session_dir: Path,
        patient_id: str,
        study_date: str,
        dicom_dir: Path,
        stage_summary: str = "imported",
    ) -> None:
        """Add or update an entry in the recent-projects list.

        If the session_dir already exists in the list it is moved to the
        top and its fields are updated.  The list is capped at
        MAX_RECENT entries.
        """
        session_str = str(session_dir)

        # Remove existing entry if present
        self._recent = [
            e for e in self._recent if e.get("session_dir") != session_str
        ]

        entry = {
            "session_dir": session_str,
            "patient_id": patient_id,
            "study_date": study_date,
            "last_opened": datetime.now().isoformat(),
            "stage_summary": stage_summary,
            "dicom_dir": str(dicom_dir),
        }

        # Insert at the top
        self._recent.insert(0, entry)
        self._recent = self._recent[: self.MAX_RECENT]
        self._save()

    def get_recent(self, limit: int = 10) -> List[Dict]:
        """Return the most recent entries (up to *limit*)."""
        return list(self._recent[:limit])

    def remove_recent(self, session_dir: Path) -> None:
        """Remove the entry matching *session_dir*."""
        session_str = str(session_dir)
        self._recent = [
            e for e in self._recent if e.get("session_dir") != session_str
        ]
        self._save()

    def get_session_dir_for_dicom(self, dicom_dir: Path) -> Optional[Path]:
        """Return the session_dir for an existing DICOM import, if any."""
        dicom_str = str(dicom_dir)
        for entry in self._recent:
            if entry.get("dicom_dir") == dicom_str:
                return Path(entry["session_dir"])
        return None

    def create_session_dir(self, patient_id: str, study_date: str) -> Path:
        """Create and return a new session directory.

        Format: ``{patient_id}_{study_date}_{timestamp}``
        Located under ``data_dir/sessions/``.
        """
        sessions_root = self.data_dir / "sessions"
        sessions_root.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dirname = f"{patient_id}_{study_date}_{timestamp}"
        session_dir = sessions_root / dirname
        session_dir.mkdir(parents=True, exist_ok=True)
        return session_dir

    # ------------------------------------------------------------------
    # Internal persistence
    # ------------------------------------------------------------------

    def _save(self) -> None:
        """Write the recent-projects list to disk."""
        self._index_path.write_text(
            json.dumps({"recent": self._recent}, indent=4, default=str),
            encoding="utf-8",
        )

    def _load(self) -> None:
        """Read the recent-projects list from disk.

        Handles missing or corrupt files gracefully.
        """
        if not self._index_path.exists():
            self._recent = []
            return
        try:
            data = json.loads(self._index_path.read_text(encoding="utf-8"))
            self._recent = data.get("recent", [])
        except (json.JSONDecodeError, KeyError, TypeError):
            self._recent = []
