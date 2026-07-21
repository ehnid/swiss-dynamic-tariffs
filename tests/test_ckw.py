"""Test CKW provider."""

from datetime import datetime
from unittest.mock import AsyncMock, Mock

import pytest

from custom_components.swiss_dynamic_tariffs.const import (
    CKW_API_URL,
    REQUEST_TIMEOUT,
)
from custom_components.swiss_dynamic_tariffs.providers.ckw import (
    CKWProvider,
    _request_params,
)


@pytest.fixture
def ckw_response():
    """Return a response matching CKW API version 0.2."""

    return {
        "publication_timestamp": "2026-07-21T11:18:52.634354+02:00",
        "prices": [
            {
                "start_timestamp": "2026-07-21T00:00+02:00",
                "end_timestamp": "2026-07-21T00:15+02:00",
                "grid": [{"unit": "CHF_kWh", "value": 0.1363}],
                "electricity": [{"unit": "CHF_kWh", "value": 0.12}],
                "integrated": [{"unit": "CHF_kWh", "value": 0.2563}],
                "grid_usage": [{"unit": "CHF_kWh", "value": 0.106}],
            }
        ],
    }


@pytest.mark.asyncio
async def test_ckw_provider_fetches_and_parses_data(ckw_response):
    """Test the CKW request and supported tariff components."""

    response = Mock()
    response.json = AsyncMock(return_value=ckw_response)
    response.raise_for_status = Mock()

    session = Mock()
    session.get.return_value.__aenter__ = AsyncMock(return_value=response)
    session.get.return_value.__aexit__ = AsyncMock(return_value=None)

    tariffs = await CKWProvider(session).async_get_tariffs()

    assert len(tariffs) == 1
    assert tariffs[0].electricity == 0.12
    assert tariffs[0].grid_usage == 0.106
    assert tariffs[0].grid == 0.1363
    assert tariffs[0].integrated == 0.2563
    assert tariffs[0].feed_in is None

    args, kwargs = session.get.call_args
    assert args == (CKW_API_URL,)
    assert kwargs["params"]["tariff_name"] == "home_dynamic"
    assert kwargs["timeout"].total == REQUEST_TIMEOUT


def test_request_params_cover_today_and_tomorrow():
    """Test CKW query boundaries in the Swiss time zone."""

    params = _request_params(datetime.fromisoformat("2026-07-21T14:00:00+02:00"))

    assert params["start_timestamp"] == "2026-07-21T00:00:00+02:00"
    assert params["end_timestamp"] == "2026-07-23T00:00:00+02:00"
