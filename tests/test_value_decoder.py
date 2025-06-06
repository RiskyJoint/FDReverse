from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.parsing.value_decoder import decode


def test_decode_scaling():
    assert decode(0x0002, 1234) == 123.4  # bus_voltage_v scale 0.1
    assert decode(0x0007, 500) == 5.0      # throttle_voltage_v scale 0.01
    assert decode(0x0004, 55) == 55        # motor_temp_c scale 1
    assert decode(0xFFFF, 42) == 42        # unknown param
