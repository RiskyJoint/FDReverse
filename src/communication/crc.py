"""CRC calculation methods for Fardriver protocol."""

from typing import Iterable


def crc16(data: Iterable[int]) -> int:
    """Compute CRC-16-IBM."""
    crc = 0xFFFF
    for b in data:
        crc ^= b
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
    return crc & 0xFFFF

