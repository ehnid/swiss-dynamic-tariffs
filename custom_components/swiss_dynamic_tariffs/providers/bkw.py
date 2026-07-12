"""BKW dynamic tariffs provider."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from aiohttp import ClientSession

from custom_components.swiss_dynamic_tariffs.models import TariffPeriod
from custom_components.swiss_dynamic_tariffs.const import BKW_API_URL

from .base import TariffProvider


def _parse_price_component(data: list[dict] | None) -> Decimal | None:
    """Extract first price value from API response."""

    if not data:
        return None

    return Decimal(str(data[0]["value"]))


def parse_tariffs(data: dict) -> list[TariffPeriod]:
    """Parse BKW tariff response."""

    tariffs: list[TariffPeriod] = []

    for item in data.get("prices", []):
        tariffs.append(
            TariffPeriod(
                start=datetime.fromisoformat(
                    item["start_timestamp"].replace("Z", "+00:00")
                ),
                end=datetime.fromisoformat(
                    item["end_timestamp"].replace("Z", "+00:00")
                ),
                electricity=_parse_price_component(item.get("electricity")),
                feed_in=_parse_price_component(item.get("feed_in")),
                grid=_parse_price_component(item.get("grid")),
                integrated=_parse_price_component(item.get("integrated")),
            )
        )

    return tariffs


class BkwProvider(TariffProvider):
    """BKW tariff provider."""

    API_URL = BKW_API_URL

    def __init__(self, session: ClientSession) -> None:
        """Initialize provider."""
        self._session = session

    async def async_get_tariffs(self) -> list[TariffPeriod]:
        """Fetch tariffs from BKW."""

        async with self._session.get(self.API_URL) as response:
            response.raise_for_status()
            data = await response.json()

        return parse_tariffs(data)
