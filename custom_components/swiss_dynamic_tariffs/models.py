from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class TariffPeriod:
    """Single tariff period."""

    start: datetime
    end: datetime
    electricity: float | None = None
    feed_in: float | None = None
    grid: float | None = None
    integrated: float | None = None
