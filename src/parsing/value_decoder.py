"""Decode raw values into engineering units."""

from __future__ import annotations

from typing import Any

from .parameter_map import PARAMETERS


SCALE = {
    "motor_speed_rpm": 1,
    "bus_voltage_v": 0.1,
    "bus_current_a": 0.1,
    "motor_temp_c": 1,
    "id_out_a": 0.1,
    "iq_out_a": 0.1,
    "throttle_voltage_v": 0.01,
    "brake_voltage_v": 0.01,
    "rpm_divisor": 1,
}


def decode(param_id: int, raw_value: int) -> Any:
    name = PARAMETERS.get(param_id, f"param_{param_id:04X}")
    scale = SCALE.get(name, 1)
    return raw_value * scale

