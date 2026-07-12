"""Base classes for tariff providers."""

from __future__ import annotations

from abc import ABC, abstractmethod

from custom_components.swiss_dynamic_tariffs.models import TariffPeriod


class TariffProvider(ABC):
    """Abstract base class for tariff providers."""

    @abstractmethod
    async def async_get_tariffs(self) -> list[TariffPeriod]:
        """Return tariff periods."""
