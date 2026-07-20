"""BKW dynamic tariffs provider."""

from __future__ import annotations

from datetime import datetime

from aiohttp import ClientSession

from .base import TariffProvider
from ..models import TariffPeriod


BKW_API_URL = "https://api.bkw.ch/api/dyntariffs/v1/tariffs/"


class BKWProvider(TariffProvider):
    """BKW tariff provider."""

    def __init__(
        self,
        session: ClientSession,
    ) -> None:
        """Initialize BKW provider."""

        self.session = session

    async def async_get_tariffs(
        self,
    ) -> list[TariffPeriod]:
        """Fetch tariffs from BKW."""

        async with self.session.get(
            "https://api.bkw.ch/api/dyntariffs/v1/tariffs/"
        ) as response:
            response.raise_for_status()

            data = await response.json()

        return self.validate_periods(parse_tariffs(data))


def _parse_price_component(
    data: list[dict] | None,
) -> float | None:
    """Extract first price value from API response."""

    if not data:
        return None

    return float(data[0]["value"])


def parse_tariffs(
    data: dict,
) -> list[TariffPeriod]:
    """Parse BKW response."""

    tariffs = []

    for item in data.get("prices", []):
        tariffs.append(
            TariffPeriod(
                start=datetime.fromisoformat(
                    item["start_timestamp"].replace(
                        "Z",
                        "+00:00",
                    )
                ),
                end=datetime.fromisoformat(
                    item["end_timestamp"].replace(
                        "Z",
                        "+00:00",
                    )
                ),
                electricity=_parse_price_component(item.get("electricity")),
                feed_in=_parse_price_component(item.get("feed_in")),
                grid=_parse_price_component(item.get("grid")),
                integrated=_parse_price_component(item.get("integrated")),
            )
        )

    return tariffs
