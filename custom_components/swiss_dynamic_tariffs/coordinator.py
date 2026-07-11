"""Data update coordinator for Swiss Dynamic Tariffs."""

from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
)

from .const import DEFAULT_SCAN_INTERVAL
from .models import TariffPeriod
from .providers.base import BaseProvider

_LOGGER = logging.getLogger(__name__)


class SwissDynamicTariffsCoordinator(
    DataUpdateCoordinator[TariffPeriod],
):
    """Coordinator to manage tariff updates."""

    def __init__(
        self,
        hass: HomeAssistant,
        provider: BaseProvider,
    ) -> None:
        """Initialize the coordinator."""
        self.provider = provider

        super().__init__(
            hass,
            _LOGGER,
            name="Swiss Dynamic Tariffs",
            update_interval=timedelta(
                seconds=DEFAULT_SCAN_INTERVAL,
            ),
        )

    async def _async_update_data(
        self,
    ) -> TariffPeriod:
        """Fetch data from the configured provider."""
        return await self.provider.async_get_tariffs()
