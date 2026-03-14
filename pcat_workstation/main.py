"""PCAT Workstation entry point."""

import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from pcat_workstation.app.style import get_stylesheet
from pcat_workstation.app.main_window import MainWindow


def main():
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    app = QApplication(sys.argv)
    app.setApplicationName("PCAT Workstation")
    app.setOrganizationName("Molloi Lab")
    app.setStyleSheet(get_stylesheet())

    window = MainWindow()
    window.showMaximized()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
