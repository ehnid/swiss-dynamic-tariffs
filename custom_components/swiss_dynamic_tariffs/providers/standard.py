"""Base provider for the Swiss dynamic-tariff API standard."""

from __future__ import annotations

from datetime import datetime, time, timedelta
from typing import ClassVar
from zoneinfo import ZoneInfo

from aiohttp import ClientError, ClientResponseError, ClientSession, ClientTimeout

from ..const import REQUEST_TIMEOUT
from ..exceptions import (
    ProviderAuthenticationError,
    ProviderConnectionError,
)
from ..models import TariffPeriod
from .base import TariffProvider
from .parser import parse_tariff_response

SWISS_TIME_ZONE = ZoneInfo("Europe/Zurich")


def build_request_params(
    tariff_name: str | None,
    now: datetime | None = None,
) -> dict[str, str]:
    """Build a Swiss-local query window covering today and tomorrow."""

    local_now = now or datetime.now(SWISS_TIME_ZONE)
    start = datetime.combine(local_now.date(), time.min, tzinfo=SWISS_TIME_ZONE)
    end = start + timedelta(days=2)
    params = {
        "start_timestamp": start.isoformat(timespec="seconds"),
        "end_timestamp": end.isoformat(timespec="seconds"),
    }

    if tariff_name is not None:
        params["tariff_name"] = tariff_name

    return params


class StandardTariffProvider(TariffProvider):
    """Provider using the VSE/SmartGridready-style tariff response."""

    api_url: ClassVar[str]
    allowed_tariff_names: ClassVar[tuple[str, ...]]
    default_tariff_name: ClassVar[str]
    include_tariff_name: ClassVar[bool] = True

    def __init__(
        self,
        session: ClientSession,
        tariff_name: str | None = None,
    ) -> None:
        """Initialize a standard tariff provider."""

        selected_tariff = tariff_name or self.default_tariff_name

        if selected_tariff not in self.allowed_tariff_names:
            raise ValueError(f"Unsupported {self.name} tariff: {selected_tariff}")

        self.session = session
        self.tariff_name = selected_tariff

    async def async_get_tariffs(self) -> list[TariffPeriod]:
        """Fetch and parse today's and tomorrow's tariffs."""

        query_tariff = self.tariff_name if self.include_tariff_name else None
        params = build_request_params(query_tariff)

        try:
            async with self.session.get(
                self.api_url,
                params=params,
                timeout=ClientTimeout(total=REQUEST_TIMEOUT),
            ) as response:
                response.raise_for_status()
                data = await response.json()
        except ClientResponseError as err:
            if err.status in (401, 403):
                raise ProviderAuthenticationError(
                    f"{self.name} rejected the API request"
                ) from err
            raise ProviderConnectionError(
                f"{self.name} API returned HTTP status {err.status}"
            ) from err
        except (ClientError, TimeoutError) as err:
            raise ProviderConnectionError(
                f"Unable to reach the {self.name} API"
            ) from err

        return self.validate_periods(
            parse_tariff_response(data, self.supported_tariff_types)
        )
