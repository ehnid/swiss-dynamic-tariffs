"""Base classes for tariff providers."""

from __future__ import annotations

from abc import ABC, abstractmethod

from ..models import TariffPeriod


class TariffProvider(ABC):
    """Abstract base class for tariff providers."""

    @abstractmethod
    async def async_get_tariffs(self) -> list[TariffPeriod]:
        """Return tariff periods."""
