"""Batch processing panel for multi-patient PCAT analysis."""

from __future__ import annotations

from pathlib import Path
from typing import List

from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QColor, QIcon
from PySide6.QtWidgets import (
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from pcat_workstation.workers.batch_worker import BatchWorker


class BatchPanel(QWidget):
    """Panel for queuing and processing multiple DICOM folders."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._worker = None
        self._dicom_dirs: List[Path] = []
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)

        # Header
        header = QLabel("Batch Processing")
        header.setStyleSheet("font-size: 16pt; font-weight: bold; color: #e5e5e7;")
        layout.addWidget(header)

        # Queue list
        self._queue_list = QListWidget()
        self._queue_list.setStyleSheet(
            "QListWidget { background: #1c1c1e; color: #e5e5e7; border: 1px solid #38383a; }"
            "QListWidget::item { padding: 4px 8px; }"
            "QListWidget::item:selected { background: #0a84ff; }"
        )
        layout.addWidget(self._queue_list)

        # Add/Remove buttons
        btn_row = QHBoxLayout()

        self._add_btn = QPushButton("Add Folders...")
        self._add_btn.clicked.connect(self._on_add)
        btn_row.addWidget(self._add_btn)

        self._remove_btn = QPushButton("Remove Selected")
        self._remove_btn.clicked.connect(self._on_remove)
        btn_row.addWidget(self._remove_btn)

        self._clear_btn = QPushButton("Clear All")
        self._clear_btn.clicked.connect(self._on_clear)
        btn_row.addWidget(self._clear_btn)

        layout.addLayout(btn_row)

        # Progress
        self._progress = QProgressBar()
        self._progress.setVisible(False)
        layout.addWidget(self._progress)

        self._status_label = QLabel("")
        self._status_label.setStyleSheet("color: #8e8e93;")
        layout.addWidget(self._status_label)

        # Start/Cancel buttons
        action_row = QHBoxLayout()

        self._start_btn = QPushButton("Start Batch")
        self._start_btn.setStyleSheet(
            "QPushButton { background: #30d158; color: white; border: none; "
            "border-radius: 4px; padding: 8px 20px; font-weight: bold; font-size: 14pt; }"
            "QPushButton:hover { background: #34c759; }"
            "QPushButton:disabled { background: #3a3a3c; color: #636366; }"
        )
        self._start_btn.clicked.connect(self._on_start)
        action_row.addWidget(self._start_btn)

        self._cancel_btn = QPushButton("Cancel")
        self._cancel_btn.setEnabled(False)
        self._cancel_btn.clicked.connect(self._on_cancel)
        action_row.addWidget(self._cancel_btn)

        layout.addLayout(action_row)

        # Output directory
        out_row = QHBoxLayout()
        out_row.addWidget(QLabel("Output:"))
        self._output_label = QLabel(
            str(Path.home() / ".pcat_workstation" / "batch")
        )
        self._output_label.setStyleSheet("color: #8e8e93;")
        out_row.addWidget(self._output_label, stretch=1)

        self._output_btn = QPushButton("Change...")
        self._output_btn.clicked.connect(self._on_change_output)
        out_row.addWidget(self._output_btn)

        layout.addLayout(out_row)

    # -- Queue management -------------------------------------------------

    def _on_add(self):
        dirs = QFileDialog.getExistingDirectory(
            self,
            "Select DICOM Folder",
            "",
            QFileDialog.ShowDirsOnly,
        )
        if dirs:
            path = Path(dirs)
            if path not in self._dicom_dirs:
                self._dicom_dirs.append(path)
                self._queue_list.addItem(str(path))
                self._update_status()

    def _on_remove(self):
        for item in self._queue_list.selectedItems():
            idx = self._queue_list.row(item)
            self._queue_list.takeItem(idx)
            if idx < len(self._dicom_dirs):
                self._dicom_dirs.pop(idx)
        self._update_status()

    def _on_clear(self):
        self._queue_list.clear()
        self._dicom_dirs.clear()
        self._update_status()

    def _on_change_output(self):
        d = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if d:
            self._output_label.setText(d)

    def _update_status(self):
        n = len(self._dicom_dirs)
        self._status_label.setText(f"{n} folder{'s' if n != 1 else ''} queued")
        self._start_btn.setEnabled(n > 0)

    # -- Batch execution --------------------------------------------------

    def _on_start(self):
        if not self._dicom_dirs:
            return

        output_dir = Path(self._output_label.text())
        output_dir.mkdir(parents=True, exist_ok=True)

        self._worker = BatchWorker(list(self._dicom_dirs), output_dir)
        self._worker.patient_started.connect(self._on_patient_started)
        self._worker.patient_completed.connect(self._on_patient_completed)
        self._worker.patient_failed.connect(self._on_patient_failed)
        self._worker.batch_completed.connect(self._on_batch_completed)
        self._worker.batch_progress.connect(self._on_batch_progress)

        self._progress.setVisible(True)
        self._progress.setRange(0, len(self._dicom_dirs))
        self._progress.setValue(0)
        self._start_btn.setEnabled(False)
        self._cancel_btn.setEnabled(True)
        self._add_btn.setEnabled(False)
        self._remove_btn.setEnabled(False)
        self._clear_btn.setEnabled(False)

        self._worker.start()

    def _on_cancel(self):
        if self._worker:
            self._worker.cancel()

    @Slot(int, str)
    def _on_patient_started(self, index, patient_id):
        if index < self._queue_list.count():
            item = self._queue_list.item(index)
            item.setText(f"[...] {self._dicom_dirs[index]}")

    @Slot(int, str, dict)
    def _on_patient_completed(self, index, patient_id, results):
        self._progress.setValue(index + 1)
        if index < self._queue_list.count():
            item = self._queue_list.item(index)
            n_vessels = len(results)
            item.setText(f"[OK] {patient_id} ({n_vessels} vessels)")

    @Slot(int, str, str)
    def _on_patient_failed(self, index, patient_id, error):
        self._progress.setValue(index + 1)
        if index < self._queue_list.count():
            item = self._queue_list.item(index)
            item.setText(f"[FAIL] {patient_id}: {error[:50]}")

    @Slot(int, int)
    def _on_batch_completed(self, total, succeeded):
        self._status_label.setText(
            f"Batch complete: {succeeded}/{total} succeeded"
        )
        self._start_btn.setEnabled(True)
        self._cancel_btn.setEnabled(False)
        self._add_btn.setEnabled(True)
        self._remove_btn.setEnabled(True)
        self._clear_btn.setEnabled(True)
        self._worker = None

    @Slot(str)
    def _on_batch_progress(self, message):
        self._status_label.setText(message)
