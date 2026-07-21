"""CKW dynamic tariffs provider."""

from __future__ import annotations

from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo

from aiohttp import ClientError, ClientResponseError, ClientSession, ClientTimeout

from ..const import CKW_API_URL, REQUEST_TIMEOUT
from ..exceptions import (
    ProviderAuthenticationError,
    ProviderConnectionError,
)
from ..models import TariffPeriod
from .base import TariffProvider
from .parser import parse_tariff_response

SWISS_TIME_ZONE = ZoneInfo("Europe/Zurich")


class CKWProvider(TariffProvider):
    """CKW tariff provider for the home_dynamic product."""

    name = "CKW"
    attribution = "Data provided by CKW"
    supported_tariff_types = (
        "electricity",
        "grid_usage",
        "grid",
        "integrated",
    )

    def __init__(self, session: ClientSession) -> None:
        """Initialize CKW provider."""

        self.session = session

    async def async_get_tariffs(self) -> list[TariffPeriod]:
        """Fetch today's and tomorrow's home dynamic tariffs from CKW."""

        params = _request_params()

        try:
            async with self.session.get(
                CKW_API_URL,
                params=params,
                timeout=ClientTimeout(total=REQUEST_TIMEOUT),
            ) as response:
                response.raise_for_status()
                data = await response.json()
        except ClientResponseError as err:
            if err.status in (401, 403):
                raise ProviderAuthenticationError(
                    "CKW rejected the API request"
                ) from err
            raise ProviderConnectionError(
                f"CKW API returned HTTP status {err.status}"
            ) from err
        except (ClientError, TimeoutError) as err:
            raise ProviderConnectionError("Unable to reach the CKW API") from err

        return self.validate_periods(
            parse_tariff_response(data, self.supported_tariff_types)
        )


def _request_params(now: datetime | None = None) -> dict[str, str]:
    """Build a Swiss-local query window covering today and tomorrow."""

    local_now = now or datetime.now(SWISS_TIME_ZONE)
    start = datetime.combine(local_now.date(), time.min, tzinfo=SWISS_TIME_ZONE)
    end = start + timedelta(days=2)

    return {
        "tariff_name": "home_dynamic",
        "start_timestamp": start.isoformat(timespec="seconds"),
        "end_timestamp": end.isoformat(timespec="seconds"),
    }
