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


class StreamingDataParser:
    """Incrementally parse incoming bytes into :class:`ParsedMessage` objects."""

    def __init__(self) -> None:
        self._buffer = bytearray()
        self._parser = DataParser()

    def feed(self, data: bytes) -> list[ParsedMessage]:
        """Feed raw bytes and return any complete messages parsed."""
        self._buffer.extend(data)
        messages: list[ParsedMessage] = []
        while True:
            if len(self._buffer) < 4:
                break
            if self._buffer[0] != START_BYTE:
                self._buffer.pop(0)
                continue
            length = self._buffer[1]
            total = length + 2
            if len(self._buffer) < total:
                break
            packet = bytes(self._buffer[:total])
            try:
                msg = self._parser.parse(packet)
            except ValueError:
                self._buffer.pop(0)
                continue
            messages.append(msg)
            del self._buffer[:total]
        return messages

