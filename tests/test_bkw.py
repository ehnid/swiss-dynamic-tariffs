"""Tests for BKW provider."""

from datetime import UTC, datetime
from decimal import Decimal

from custom_components.swiss_dynamic_tariffs.providers.bkw import parse_tariffs


def test_parse_bkw_tariffs():
    """Test parsing BKW tariff response."""

    data = {
        "publication_timestamp": "2026-07-11T20:00:00Z",
        "prices": [
            {
                "start_timestamp": "2026-07-11T22:00:00Z",
                "end_timestamp": "2026-07-11T22:15:00Z",
                "feed_in": [
                    {
                        "unit": "CHF_kWh",
                        "value": 0.129,
                    }
                ],
            }
        ],
    }

    tariffs = parse_tariffs(data)

    assert len(tariffs) == 1

    tariff = tariffs[0]

    assert tariff.start == datetime(2026, 7, 11, 22, 0, tzinfo=UTC)

    assert tariff.end == datetime(2026, 7, 11, 22, 15, tzinfo=UTC)

    assert tariff.feed_in == Decimal("0.129")
    assert tariff.electricity is None
    assert tariff.grid is None
    assert tariff.integrated is None
