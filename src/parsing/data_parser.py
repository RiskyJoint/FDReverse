"""Message parsing logic for Fardriver controllers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any

from ..communication.protocol import START_BYTE
from ..communication.crc import crc16


@dataclass
class ParsedMessage:
    command: int
    payload: bytes


class DataParser:
    def parse(self, message: bytes) -> ParsedMessage:
        if len(message) < 4:
            raise ValueError("Message too short")
        if message[0] != START_BYTE:
            raise ValueError("Invalid start byte")
        length = message[1]
        if length != len(message) - 2:
            raise ValueError("Invalid length")
        command = message[2]
        payload = message[3:-2]
        crc_expected = int.from_bytes(message[-2:], "little")
        crc_actual = crc16(message[:-2])
        if crc_expected != crc_actual:
            raise ValueError("CRC mismatch")
        return ParsedMessage(command, payload)

