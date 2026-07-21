"""BKW dynamic tariffs provider."""

from __future__ import annotations

from aiohttp import ClientError, ClientResponseError, ClientSession, ClientTimeout

from ..const import BKW_API_URL, REQUEST_TIMEOUT
from ..exceptions import (
    ProviderAuthenticationError,
    ProviderConnectionError,
)
from ..models import TariffPeriod
from .base import TariffProvider
from .parser import parse_tariff_response


class BKWProvider(TariffProvider):
    """BKW tariff provider."""

    name = "BKW"
    attribution = "Data provided by BKW"
    supported_tariff_types = ("feed_in",)

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

        try:
            async with self.session.get(
                BKW_API_URL,
                timeout=ClientTimeout(total=REQUEST_TIMEOUT),
            ) as response:
                response.raise_for_status()

                data = await response.json()
        except ClientResponseError as err:
            if err.status in (401, 403):
                raise ProviderAuthenticationError(
                    "BKW rejected the API request"
                ) from err
            raise ProviderConnectionError(
                f"BKW API returned HTTP status {err.status}"
            ) from err
        except (ClientError, TimeoutError) as err:
            raise ProviderConnectionError("Unable to reach the BKW API") from err

        return self.validate_periods(parse_tariffs(data))


def parse_tariffs(
    data: object,
) -> list[TariffPeriod]:
    """Parse BKW response."""

    return parse_tariff_response(
        data,
        BKWProvider.supported_tariff_types,
    )
