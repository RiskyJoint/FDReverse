"""Application entry point for Fardriver Dashboard 2.0."""

from __future__ import annotations

import sys
from pathlib import Path

from PySide6 import QtWidgets

from ui.dashboard import Dashboard


def main() -> int:
    app = QtWidgets.QApplication(sys.argv)
    ui_path = Path(__file__).parent / "ui" / "NEWDASH.ui"
    window = Dashboard(ui_path)
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())

