"""Serial port management for Fardriver controllers."""

from __future__ import annotations

import logging
from typing import Optional, List

import glob
import os
import sys

try:
    import serial  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - optional dependency
    serial = None

logger = logging.getLogger(__name__)


class SerialHandler:
    def __init__(self, port: str, baudrate: int = 115200, timeout: float = 0.1):
        self.port_name = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial: Optional["serial.Serial"] = None

    def open(self) -> None:
        if serial is None:
            raise RuntimeError("pyserial is required for serial communication")
        logger.debug("Opening serial port %s", self.port_name)
        self.serial = serial.Serial(self.port_name, self.baudrate, timeout=self.timeout)

    def close(self) -> None:
        if self.serial and self.serial.is_open:
            logger.debug("Closing serial port")
            self.serial.close()
            self.serial = None

    def write(self, data: bytes) -> None:
        if not self.serial:
            raise RuntimeError("Serial port not open")
        logger.debug("Writing %s", data)
        self.serial.write(data)

    def read(self, size: int = 1) -> bytes:
        if not self.serial:
            raise RuntimeError("Serial port not open")
        data = self.serial.read(size)
        logger.debug("Read %s", data)
        return data


def list_available_ports() -> List[str]:
    """Return a list of available serial ports on the current system."""
    if sys.platform.startswith("win"):
        # Windows COM ports
        return [f"COM{i+1}" for i in range(256)]
    # Unix-like systems
    patterns = ("/dev/ttyUSB*", "/dev/ttyACM*", "/dev/tty.*")
    ports: List[str] = []
    for pattern in patterns:
        ports.extend(glob.glob(pattern))
    # Filter out entries that do not exist (in case of wildcards)
    return [p for p in ports if os.path.exists(p)]
