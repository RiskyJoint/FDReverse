"""Decode raw values into engineering units."""

from __future__ import annotations

from typing import Any

from .parameter_map import PARAMETERS


SCALE = {
    "motor_speed_rpm": 1,
    "bus_voltage_v": 0.1,
    "bus_current_a": 0.1,
}


def decode(param_id: int, raw_value: int) -> Any:
    name = PARAMETERS.get(param_id, f"param_{param_id:04X}")
    scale = SCALE.get(name, 1)
    return raw_value * scale

