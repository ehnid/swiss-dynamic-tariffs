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
            always_update=False,
        )

    async def _async_update_data(
        self,
    ) -> list[TariffPeriod]:
        """Fetch data from the configured provider."""
        _LOGGER.debug("Fetching tariff data")

        try:
            fresh_data = await self.provider.async_get_tariffs()
        except Exception as err:
            _LOGGER.exception("Unable to fetch tariff data.")
            raise UpdateFailed(f"Unable to fetch tariffs: {err}") from err

        data = self._merge_tariff_periods(fresh_data)

        _LOGGER.debug("Received %d tariff periods", len(data))

        return data

    def _merge_tariff_periods(
        self,
        fresh_data: list[TariffPeriod],
    ) -> list[TariffPeriod]:
        """Merge new periods with still-relevant data from the previous update.

        BKW switches its response to the next day's values after publication.
        Keeping periods that have not ended prevents the current price from
        disappearing for a continuously running Home Assistant instance.
        """

        now = dt_util.now()
        previous_data = getattr(self, "data", None) or []
        periods = {
            (period.start, period.end): period
            for period in previous_data
            if period.end > now
        }
        periods.update({(period.start, period.end): period for period in fresh_data})

        return sorted(periods.values(), key=lambda period: period.start)

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

    @property
    def next_period(self) -> TariffPeriod | None:
        """Return the tariff period directly following the current one."""

        if not self.data:
            return None

        now = dt_util.now()
        current = self.current_period

        if current is not None:
            upcoming = [period for period in self.data if period.start >= current.end]
        else:
            upcoming = [period for period in self.data if period.start > now]

        if not upcoming:
            return None

        return min(upcoming, key=lambda period: period.start)

    def cheapest_period(self, tariff_type: str) -> TariffPeriod | None:
        """Return the upcoming quarter-hour with the lowest price for a tariff type."""

        candidates = self._periods_with_value(tariff_type)

        if not candidates:
            return None

        return min(candidates, key=lambda period: getattr(period, tariff_type))

    def most_expensive_period(self, tariff_type: str) -> TariffPeriod | None:
        """Return the upcoming quarter-hour with the highest price for a tariff type."""

        candidates = self._periods_with_value(tariff_type)

        if not candidates:
            return None

        return max(candidates, key=lambda period: getattr(period, tariff_type))

    def average_price(self, tariff_type: str) -> float | None:
        """Return the average upcoming price for a tariff type."""

        values = [
            getattr(period, tariff_type)
            for period in self._periods_with_value(tariff_type)
        ]

        if not values:
            return None

        return sum(values) / len(values)

    def _upcoming_periods(self) -> list[TariffPeriod]:
        """Return periods that are still active or lie in the future.

        This covers the remainder of today plus tomorrow once the provider
        has published the next day's prices, which is what "cheapest" and
        "most expensive" should be computed over - a period that has
        already ended is no longer actionable.
        """

        if not self.data:
            return []

        now = dt_util.now()

        return [period for period in self.data if period.end > now]

    def _periods_with_value(self, tariff_type: str) -> list[TariffPeriod]:
        """Return upcoming periods that have a value for the given tariff type."""

        return [
            period
            for period in self._upcoming_periods()
            if getattr(period, tariff_type, None) is not None
        ]
