"""Economy calculations."""

from __future__ import annotations


def calculate_efficiency(power_w: float, speed_mph: float) -> float:
    """Return Wh per mile."""
    if speed_mph <= 0:
        return 0.0
    hours = 1 / speed_mph
    return power_w * hours

