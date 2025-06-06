from pathlib import Path
import sys

# Add repository root so that 'src' package can be imported
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.communication.protocol import Packet
from src.parsing.data_parser import DataParser, StreamingDataParser


def test_data_parser_roundtrip():
    packet = Packet(command=0x01, data=b"\x02\x03")
    encoded = packet.encode()
    parser = DataParser()
    parsed = parser.parse(encoded)
    assert parsed.command == 0x01
    assert parsed.payload == b"\x02\x03"


def test_streaming_parser_multiple_packets():
    pkt1 = Packet(command=0x01, data=b"\x01")
    pkt2 = Packet(command=0x02, data=b"\x03\x04")
    enc1 = pkt1.encode()
    enc2 = pkt2.encode()
    stream = StreamingDataParser()

    # feed partial first packet
    assert stream.feed(enc1[:2]) == []
    msgs = stream.feed(enc1[2:] + enc2)
    assert len(msgs) == 2
    assert msgs[0].command == pkt1.command
    assert msgs[0].payload == b"\x01"
    assert msgs[1].command == pkt2.command
    assert msgs[1].payload == b"\x03\x04"
