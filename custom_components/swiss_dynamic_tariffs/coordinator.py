"""Data update coordinator for Swiss Dynamic Tariffs."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.util import dt as dt_util

from datetime import (
    timedelta,
)

import logging

from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)


from .const import DEFAULT_SCAN_INTERVAL, NAME
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
        entry: ConfigEntry,
    ) -> None:
        """Initialize the coordinator."""
        self.provider = provider

        super().__init__(
            hass,
            _LOGGER,
            name=NAME,
            update_interval=timedelta(
                seconds=DEFAULT_SCAN_INTERVAL,
            ),
            config_entry=entry,
        )

    async def _async_update_data(
        self,
    ) -> list[TariffPeriod]:
        """Fetch data from the configured provider."""
        _LOGGER.debug("Fetching tariff data")

        try:
            data = await self.provider.async_get_tariffs()
        except Exception as err:
            _LOGGER.exception("Unable to fetch tariff data.")
            raise UpdateFailed(f"Unable to fetch tariffs: {err}") from err

        _LOGGER.debug("Received tariff data: %s", data)

        return data

    @property
    def current_period(self) -> TariffPeriod | None:
        """Return the currently active tariff period."""

        if not self.data:
            return None

        now = dt_util.now()

        for period in self.data:
            if period.start <= now < period.end:
                return period

        return None
