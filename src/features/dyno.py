"""Simple dyno testing module."""

from __future__ import annotations

import time
from typing import Callable

from .logging import Logger


class Dyno:
    def __init__(self, sampler: Callable[[], float], logger: Logger):
        self.sampler = sampler
        self.logger = logger
        self.running = False

    def start(self, duration: float) -> None:
        self.running = True
        start_time = time.time()
        while self.running and time.time() - start_time < duration:
            value = self.sampler()
            self.logger.log("dyno_sample", value)
            time.sleep(0.1)
        self.running = False

    def stop(self) -> None:
        self.running = False

