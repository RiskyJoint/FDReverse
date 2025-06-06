"""Main window controller."""

from __future__ import annotations

from pathlib import Path

from PySide6 import QtWidgets, QtUiTools, QtCore


class Dashboard(QtWidgets.QMainWindow):
    def __init__(self, ui_path: Path):
        super().__init__()
        loader = QtUiTools.QUiLoader()
        ui_file = QtCore.QFile(str(ui_path))
        ui_file.open(QtCore.QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()
        self.setCentralWidget(self.ui)

