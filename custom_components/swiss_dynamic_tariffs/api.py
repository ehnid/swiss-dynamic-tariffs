"""BKW Dynamic Tariffs API client."""

from __future__ import annotations

from aiohttp import ClientSession

from .const import BKW_API_URL
from .models import TariffPeriod
from .providers.bkw import parse_tariffs


class SwissDynamicTariffsApiClient:
    """Client for the BKW Dynamic Tariffs API."""

    def __init__(
        self,
        session: ClientSession,
    ) -> None:
        """Initialize the client."""
        self.session = session

    async def async_get_tariffs(self) -> list[TariffPeriod]:
        """Fetch tariffs from BKW."""
        async with self.session.get(
            BKW_API_URL,
        ) as response:
            response.raise_for_status()

            data = await response.json()

        return parse_tariffs(data)
