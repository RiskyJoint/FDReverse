"""Parameter modification functionality."""

from __future__ import annotations

from ..communication.protocol import Packet
from ..communication.serial_handler import SerialHandler


class Tuner:
    def __init__(self, serial: SerialHandler):
        self.serial = serial

    def set_parameter(self, param_id: int, value: int) -> None:
        packet = Packet(command=0x10, data=param_id.to_bytes(2, "little") + value.to_bytes(2, "little"))
        self.serial.write(packet.encode())

