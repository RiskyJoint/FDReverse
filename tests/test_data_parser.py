from pathlib import Path
import sys

# Add repository root so that 'src' package can be imported
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.communication.protocol import Packet
from src.parsing.data_parser import DataParser


def test_data_parser_roundtrip():
    packet = Packet(command=0x01, data=b"\x02\x03")
    encoded = packet.encode()
    parser = DataParser()
    parsed = parser.parse(encoded)
    assert parsed.command == 0x01
    assert parsed.payload == b"\x02\x03"
