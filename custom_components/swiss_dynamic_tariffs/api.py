"""API client for Swiss Dynamic Tariffs."""

from __future__ import annotations

from aiohttp import ClientError, ClientSession

from .const import BKW_API_URL
from .providers.bkw import parse_tariffs
from .models import TariffPeriod


class SwissDynamicTariffsApiClient:
    """Client for BKW dynamic tariff API."""

    def __init__(
        self,
        session: ClientSession,
    ) -> None:
        """Initialize API client."""

        self.session = session

    async def async_get_data(self) -> list[TariffPeriod]:
        """Fetch tariff data from BKW."""

        try:
            async with self.session.get(
                BKW_API_URL,
            ) as response:
                response.raise_for_status()

                data = await response.json()

        except ClientError as err:
            raise RuntimeError("Unable to fetch BKW tariffs") from err

        return parse_tariffs(data)
