"""Base classes for tariff providers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import ClassVar

from ..models import TariffPeriod, TariffType


class TariffProvider(ABC):
    """Abstract base class for tariff providers."""

    name: ClassVar[str] = "Dynamic tariffs"
    attribution: ClassVar[str] = ""
    tariff_name: str | None = None
    supported_tariff_types: ClassVar[tuple[TariffType, ...]] = (
        "electricity",
        "feed_in",
        "grid_usage",
        "grid",
        "integrated",
    )

    @abstractmethod
    async def async_get_tariffs(
        self,
    ) -> list[TariffPeriod]:
        """Return tariff periods."""

    @staticmethod
    def validate_periods(
        periods: list[TariffPeriod],
    ) -> list[TariffPeriod]:
        """Validate returned tariff periods."""

        valid_periods = [period for period in periods if period.start < period.end]

        return sorted(valid_periods, key=lambda period: period.start)
