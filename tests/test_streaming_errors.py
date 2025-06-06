from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.communication.protocol import Packet
from src.parsing.data_parser import StreamingDataParser


def test_streaming_parser_bad_crc_then_valid():
    valid = Packet(command=0x01, data=b"\x02").encode()
    # Corrupt last byte of CRC
    bad = bytearray(valid)
    bad[-1] ^= 0xFF
    parser = StreamingDataParser()
    # Feeding invalid packet should yield no messages
    assert parser.feed(bytes(bad)) == []
    # Now feed a valid packet
    msgs = parser.feed(valid)
    assert len(msgs) == 1
    assert msgs[0].command == 0x01
    assert msgs[0].payload == b"\x02"


def test_streaming_parser_bad_length_then_valid():
    valid = Packet(command=0x05, data=b"\x01\x02").encode()
    bad = bytearray(valid)
    # Decrease length field so it does not match actual length
    bad[1] -= 1
    parser = StreamingDataParser()
    assert parser.feed(bytes(bad)) == []
    msgs = parser.feed(valid)
    assert len(msgs) == 1
    assert msgs[0].command == 0x05
    assert msgs[0].payload == b"\x01\x02"
