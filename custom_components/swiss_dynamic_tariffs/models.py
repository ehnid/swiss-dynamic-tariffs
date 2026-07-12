"""Data models for Swiss Dynamic Tariffs."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass
class TariffPeriod:
    """A single tariff interval."""

    start: datetime
    end: datetime

    electricity: Decimal | None = None
    feed_in: Decimal | None = None
    grid: Decimal | None = None
    integrated: Decimal | None = None
