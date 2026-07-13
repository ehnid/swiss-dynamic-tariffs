"""Data update coordinator for Swiss Dynamic Tariffs."""

from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from homeassistant.config_entries import ConfigEntry

from .const import DEFAULT_SCAN_INTERVAL
from .models import TariffPeriod
from .providers.base import TariffProvider

_LOGGER = logging.getLogger(__name__)


class SwissDynamicTariffsCoordinator(
    DataUpdateCoordinator[list[TariffPeriod]],
):
    """Coordinator to manage tariff updates."""

    def __init__(
        self,
        hass: HomeAssistant,
        provider: TariffProvider,
        entry: ConfigEntry | None = None,
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
            config_entry=entry,
        )

    async def _async_update_data(
        self,
    ) -> list[TariffPeriod]:
        """Fetch data from the configured provider."""
        try:
            return await self.provider.async_get_tariffs()
        except Exception as err:
            raise UpdateFailed(f"Unable to fetch tariffs: {err}") from err
