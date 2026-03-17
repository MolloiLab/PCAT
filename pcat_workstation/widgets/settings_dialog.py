"""Settings dialog for PCAT Workstation configuration."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QComboBox, QDoubleSpinBox, QSpinBox, QLabel,
    QPushButton, QGroupBox, QDialogButtonBox,
)
from PySide6.QtCore import Qt

from pcat_workstation.app.config import (
    DATA_DIR, VOI_MODE, CRISP_GAP_MM, CRISP_RING_MM,
    DEFAULT_PCAT_SCALE, FAI_HU_MIN, FAI_HU_MAX,
    DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_LEVEL,
)

_CONFIG_PATH = Path(DATA_DIR) / "config.json"


def load_config() -> Dict[str, Any]:
    """Load settings from config.json, falling back to defaults."""
    defaults = {
        "voi_mode": VOI_MODE,
        "crisp_gap_mm": CRISP_GAP_MM,
        "crisp_ring_mm": CRISP_RING_MM,
        "pcat_scale": DEFAULT_PCAT_SCALE,
        "fai_hu_min": FAI_HU_MIN,
        "fai_hu_max": FAI_HU_MAX,
        "default_window": DEFAULT_WINDOW_WIDTH,
        "default_level": DEFAULT_WINDOW_LEVEL,
        "lad_length_mm": 40.0,
        "lcx_length_mm": 40.0,
        "rca_length_mm": 40.0,
        "rca_start_mm": 10.0,
    }
    if _CONFIG_PATH.exists():
        try:
            saved = json.loads(_CONFIG_PATH.read_text())
            defaults.update(saved)
        except Exception:
            pass
    return defaults


def save_config(config: Dict[str, Any]) -> None:
    """Save settings to config.json."""
    _CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    _CONFIG_PATH.write_text(json.dumps(config, indent=2))


class SettingsDialog(QDialog):
    """Modal settings dialog."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("PCAT Workstation Settings")
        self.setMinimumWidth(450)
        self._config = load_config()
        self._build_ui()
        self._populate()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        # VOI Geometry group
        voi_group = QGroupBox("VOI Geometry")
        voi_form = QFormLayout()

        self._voi_mode = QComboBox()
        self._voi_mode.addItems(["crisp", "scaled"])
        self._voi_mode.currentTextChanged.connect(self._on_voi_mode_changed)
        voi_form.addRow("VOI Mode:", self._voi_mode)

        self._crisp_gap = QDoubleSpinBox()
        self._crisp_gap.setRange(0.0, 10.0)
        self._crisp_gap.setSingleStep(0.5)
        self._crisp_gap.setSuffix(" mm")
        voi_form.addRow("CRISP-CT Gap:", self._crisp_gap)

        self._crisp_ring = QDoubleSpinBox()
        self._crisp_ring.setRange(0.5, 20.0)
        self._crisp_ring.setSingleStep(0.5)
        self._crisp_ring.setSuffix(" mm")
        voi_form.addRow("CRISP-CT Ring Width:", self._crisp_ring)

        self._pcat_scale = QDoubleSpinBox()
        self._pcat_scale.setRange(1.0, 10.0)
        self._pcat_scale.setSingleStep(0.5)
        self._pcat_scale.setSuffix("\u00d7 r_eq")
        voi_form.addRow("Scaled VOI Factor:", self._pcat_scale)

        voi_group.setLayout(voi_form)
        layout.addWidget(voi_group)

        # Segment Lengths group
        seg_group = QGroupBox("Vessel Segment Lengths")
        seg_form = QFormLayout()

        self._lad_length = QDoubleSpinBox()
        self._lad_length.setRange(10.0, 100.0)
        self._lad_length.setSuffix(" mm")
        seg_form.addRow("LAD Length:", self._lad_length)

        self._lcx_length = QDoubleSpinBox()
        self._lcx_length.setRange(10.0, 100.0)
        self._lcx_length.setSuffix(" mm")
        seg_form.addRow("LCx Length:", self._lcx_length)

        self._rca_length = QDoubleSpinBox()
        self._rca_length.setRange(10.0, 100.0)
        self._rca_length.setSuffix(" mm")
        seg_form.addRow("RCA Length:", self._rca_length)

        self._rca_start = QDoubleSpinBox()
        self._rca_start.setRange(0.0, 50.0)
        self._rca_start.setSuffix(" mm")
        seg_form.addRow("RCA Start Offset:", self._rca_start)

        seg_group.setLayout(seg_form)
        layout.addWidget(seg_group)

        # HU Thresholds group
        hu_group = QGroupBox("HU Thresholds")
        hu_form = QFormLayout()

        self._fai_min = QDoubleSpinBox()
        self._fai_min.setRange(-500.0, 0.0)
        self._fai_min.setSuffix(" HU")
        hu_form.addRow("FAI Min:", self._fai_min)

        self._fai_max = QDoubleSpinBox()
        self._fai_max.setRange(-100.0, 100.0)
        self._fai_max.setSuffix(" HU")
        hu_form.addRow("FAI Max:", self._fai_max)

        hu_group.setLayout(hu_form)
        layout.addWidget(hu_group)

        # Display Defaults group
        disp_group = QGroupBox("Display Defaults")
        disp_form = QFormLayout()

        self._def_window = QDoubleSpinBox()
        self._def_window.setRange(1.0, 4000.0)
        self._def_window.setSuffix(" HU")
        disp_form.addRow("Default Window:", self._def_window)

        self._def_level = QDoubleSpinBox()
        self._def_level.setRange(-1000.0, 2000.0)
        self._def_level.setSuffix(" HU")
        disp_form.addRow("Default Level:", self._def_level)

        disp_group.setLayout(disp_form)
        layout.addWidget(disp_group)

        # Buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self._on_accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def _populate(self):
        self._voi_mode.setCurrentText(self._config["voi_mode"])
        self._crisp_gap.setValue(self._config["crisp_gap_mm"])
        self._crisp_ring.setValue(self._config["crisp_ring_mm"])
        self._pcat_scale.setValue(self._config["pcat_scale"])
        self._lad_length.setValue(self._config["lad_length_mm"])
        self._lcx_length.setValue(self._config["lcx_length_mm"])
        self._rca_length.setValue(self._config["rca_length_mm"])
        self._rca_start.setValue(self._config["rca_start_mm"])
        self._fai_min.setValue(self._config["fai_hu_min"])
        self._fai_max.setValue(self._config["fai_hu_max"])
        self._def_window.setValue(self._config["default_window"])
        self._def_level.setValue(self._config["default_level"])
        self._on_voi_mode_changed(self._config["voi_mode"])

    def _on_voi_mode_changed(self, mode: str):
        is_crisp = mode == "crisp"
        self._crisp_gap.setEnabled(is_crisp)
        self._crisp_ring.setEnabled(is_crisp)
        self._pcat_scale.setEnabled(not is_crisp)

    def _on_accept(self):
        self._config.update({
            "voi_mode": self._voi_mode.currentText(),
            "crisp_gap_mm": self._crisp_gap.value(),
            "crisp_ring_mm": self._crisp_ring.value(),
            "pcat_scale": self._pcat_scale.value(),
            "lad_length_mm": self._lad_length.value(),
            "lcx_length_mm": self._lcx_length.value(),
            "rca_length_mm": self._rca_length.value(),
            "rca_start_mm": self._rca_start.value(),
            "fai_hu_min": self._fai_min.value(),
            "fai_hu_max": self._fai_max.value(),
            "default_window": self._def_window.value(),
            "default_level": self._def_level.value(),
        })
        save_config(self._config)
        self.accept()

    def get_config(self) -> Dict[str, Any]:
        return dict(self._config)
