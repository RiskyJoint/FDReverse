"""Fardriver communication protocol implementation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .crc import crc16

START_BYTE = 0xAA


@dataclass
class Packet:
    command: int
    data: bytes

    def encode(self) -> bytes:
        length = len(self.data) + 2  # command + CRC
        payload = bytes([START_BYTE, length, self.command]) + self.data
        crc = crc16(payload)
        return payload + crc.to_bytes(2, "little")


