"""Base class for tariff providers."""

from __future__ import annotations

from abc import ABC, abstractmethod

from custom_components.swiss_dynamic_tariffs.models import TariffPeriod


class BaseProvider(ABC):
    """Abstract base class for all tariff providers."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the provider name."""

    @abstractmethod
    async def async_get_tariffs(self) -> TariffPeriod:
        """Fetch tariff data from the provider."""
