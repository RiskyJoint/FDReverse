from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.communication.protocol import Packet, START_BYTE
from src.communication.crc import crc16


def test_packet_encode_format_and_crc():
    pkt = Packet(command=0x55, data=b"\x01\x02")
    encoded = pkt.encode()
    # Start byte
    assert encoded[0] == START_BYTE
    # Length should equal data length + 3
    assert encoded[1] == len(pkt.data) + 3
    # Command byte
    assert encoded[2] == 0x55
    # Data bytes
    assert encoded[3:5] == b"\x01\x02"
    # CRC should match crc16 over payload (start,length,command,data)
    expected_crc = crc16(encoded[:-2])
    assert encoded[-2:] == expected_crc.to_bytes(2, "little")
