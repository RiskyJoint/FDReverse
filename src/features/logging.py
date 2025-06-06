"""CSV logging functionality."""

from __future__ import annotations

import csv
import datetime
from pathlib import Path
from typing import Dict


class Logger:
    def __init__(self, path: Path):
        self.path = path
        self.file = open(self.path, "w", newline="")
        self.writer = csv.writer(self.file)
        self.writer.writerow(["timestamp", "parameter", "value"])

    def log(self, parameter: str, value: float) -> None:
        timestamp = datetime.datetime.utcnow().isoformat()
        self.writer.writerow([timestamp, parameter, value])
        self.file.flush()

    def close(self) -> None:
        self.file.close()

