from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Literal


type TariffType = Literal[
    "electricity",
    "feed_in",
    "grid_usage",
    "grid",
    "integrated",
]


@dataclass(frozen=True, slots=True)
class TariffPeriod:
    """Single tariff period."""

    start: datetime
    end: datetime
    electricity: float | None = None
    feed_in: float | None = None
    grid_usage: float | None = None
    grid: float | None = None
    integrated: float | None = None
