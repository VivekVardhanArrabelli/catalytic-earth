"""Explicit sources of time and randomness for deterministic new code."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Callable


@dataclass(frozen=True)
class ExecutionContext:
    seed: int
    now: Callable[[], datetime]

    def __post_init__(self) -> None:
        if not isinstance(self.seed, int) or isinstance(self.seed, bool) or self.seed < 0:
            raise ValueError("seed must be a non-negative integer")

    def now_utc_iso(self) -> str:
        value = self.now()
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("injected clock must return a timezone-aware datetime")
        return value.astimezone().isoformat(timespec="seconds").replace("+00:00", "Z")
