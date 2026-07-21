"""Test BKW provider."""

from unittest.mock import AsyncMock, Mock

import pytest

from custom_components.swiss_dynamic_tariffs.const import (
    BKW_API_URL,
    REQUEST_TIMEOUT,
)
from custom_components.swiss_dynamic_tariffs.exceptions import ProviderDataError
from custom_components.swiss_dynamic_tariffs.providers.bkw import (
    BKWProvider,
    parse_tariffs,
)


@pytest.fixture
def bkw_response():
    """Sample BKW API response."""

    return {
        "publication_timestamp": "2026-07-12T10:00:00Z",
        "prices": [
            {
                "start_timestamp": "2026-07-12T10:00:00Z",
                "end_timestamp": "2026-07-12T10:15:00Z",
                "electricity": [
                    {
                        "unit": "CHF_kWh",
                        "value": 0.25,
                    }
                ],
                "feed_in": [
                    {
                        "unit": "CHF_kWh",
                        "value": 0.08,
                    }
                ],
                "grid": [
                    {
                        "unit": "CHF_kWh",
                        "value": 0.12,
                    }
                ],
                "integrated": [
                    {
                        "unit": "CHF_kWh",
                        "value": 0.37,
                    }
                ],
            }
        ],
    }


def test_parse_tariffs(bkw_response):
    """Test parsing BKW response."""

    tariffs = parse_tariffs(bkw_response)

    assert len(tariffs) == 1

    tariff = tariffs[0]

    assert tariff.electricity is None
    assert tariff.feed_in == 0.08
    assert tariff.grid is None
    assert tariff.integrated is None


@pytest.mark.asyncio
async def test_bkw_provider_fetches_data(bkw_response):
    """Test BKW API request."""

    response = Mock()
    response.json = AsyncMock(return_value=bkw_response)
    response.raise_for_status = Mock()

    session = Mock()
    session.get.return_value.__aenter__ = AsyncMock(return_value=response)
    session.get.return_value.__aexit__ = AsyncMock(return_value=None)

    provider = BKWProvider(session)

    tariffs = await provider.async_get_tariffs()

    assert len(tariffs) == 1

    session.get.assert_called_once()
    args, kwargs = session.get.call_args

    assert args == (BKW_API_URL,)
    assert kwargs["timeout"].total == REQUEST_TIMEOUT


def test_parse_tariffs_with_real_bkw_feed_in_shape():
    """Test the feed-in-only response currently returned by BKW."""

    tariffs = parse_tariffs(
        {
            "publication_timestamp": "2026-07-21T20:50:00Z",
            "prices": [
                {
                    "start_timestamp": "2026-07-21T22:00:00Z",
                    "end_timestamp": "2026-07-21T22:15:00Z",
                    "feed_in": [{"unit": "CHF_kWh", "value": 0.145}],
                }
            ],
        }
    )

    assert tariffs[0].feed_in == 0.145
    assert tariffs[0].electricity is None


@pytest.mark.parametrize(
    "response",
    [
        {},
        {"prices": "not-a-list"},
        {
            "prices": [
                {
                    "start_timestamp": "2026-07-21T22:00:00Z",
                    "end_timestamp": "2026-07-21T22:15:00Z",
                    "feed_in": [{"unit": "EUR_kWh", "value": 0.145}],
                }
            ]
        },
    ],
)
def test_parse_tariffs_rejects_invalid_data(response):
    """Test that malformed or incompatible API data is rejected."""

    with pytest.raises(ProviderDataError):
        parse_tariffs(response)
