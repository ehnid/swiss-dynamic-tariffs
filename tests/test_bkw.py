"""Test BKW provider."""

from unittest.mock import AsyncMock, Mock

import pytest

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
                        "unit": "CHF/kWh",
                        "value": 0.25,
                    }
                ],
                "feed_in": [
                    {
                        "unit": "CHF/kWh",
                        "value": 0.08,
                    }
                ],
                "grid": [
                    {
                        "unit": "CHF/kWh",
                        "value": 0.12,
                    }
                ],
                "integrated": [
                    {
                        "unit": "CHF/kWh",
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

    assert tariff.electricity == 0.25
    assert tariff.feed_in == 0.08
    assert tariff.grid == 0.12
    assert tariff.integrated == 0.37


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

    session.get.assert_called_once_with("https://api.bkw.ch/api/dyntariffs/v1/tariffs/")
