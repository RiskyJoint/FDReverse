import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from communication.crc import crc16


def test_crc16():
    assert crc16(b"123456789") == 0x4B37
