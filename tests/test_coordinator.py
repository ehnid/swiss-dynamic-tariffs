from datetime import timedelta
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

import pytest
from homeassistant.util import dt as dt_util

from custom_components.swiss_dynamic_tariffs.coordinator import (
    SwissDynamicTariffsCoordinator,
)
from custom_components.swiss_dynamic_tariffs.models import TariffPeriod


async def test_coordinator_update(hass):
    """Test coordinator update."""

    provider = Mock()
    provider.async_get_tariffs = AsyncMock(return_value=[])

    entry = Mock()
    entry.entry_id = "test"
    entry.async_on_unload = Mock()

    coordinator = SwissDynamicTariffsCoordinator(
        hass,
        provider,
        entry,
    )

    await coordinator.async_refresh()

    assert coordinator.last_update_success
    assert coordinator.data == []

    provider.async_get_tariffs.assert_awaited_once()


def test_current_period():
    """Test selecting the active tariff period."""

    now = dt_util.now()

    coordinator = SwissDynamicTariffsCoordinator.__new__(SwissDynamicTariffsCoordinator)

    coordinator.data = [
        TariffPeriod(
            start=now - timedelta(hours=1),
            end=now + timedelta(hours=1),
            electricity=0.25,
            feed_in=0.10,
            grid=0.05,
            integrated=0.30,
        )
    ]

    assert coordinator.current_period is coordinator.data[0]


def test_current_period_without_data(hass):
    """Test current period when no tariff data exists."""

    provider = Mock()

    entry = SimpleNamespace(
        entry_id="test",
        async_on_unload=lambda callback: None,
    )

    coordinator = SwissDynamicTariffsCoordinator(
        hass,
        provider,
        entry,
    )

    coordinator.data = []

    assert coordinator.current_period is None


def test_current_period_returns_first_period(hass):
    """Test current period selection."""

    provider = Mock()

    entry = SimpleNamespace(
        entry_id="test",
        async_on_unload=lambda callback: None,
    )

    coordinator = SwissDynamicTariffsCoordinator(
        hass,
        provider,
        entry,
    )

    now = dt_util.now()

    first = SimpleNamespace(
        electricity=0.25,
        start=now - timedelta(minutes=30),
        end=now + timedelta(minutes=30),
    )

    second = SimpleNamespace(
        electricity=0.30,
        start=now + timedelta(minutes=30),
        end=now + timedelta(hours=1),
    )

    coordinator.data = [
        first,
        second,
    ]

    assert coordinator.current_period == first


def _build_quarter_hours(now):
    """Build four quarter-hour periods spanning the last hour to the next two hours."""

    return [
        TariffPeriod(
            start=now - timedelta(minutes=15),
            end=now,
            electricity=0.20,
            feed_in=0.05,
        ),
        TariffPeriod(
            start=now,
            end=now + timedelta(minutes=15),
            electricity=0.30,
            feed_in=0.10,
        ),
        TariffPeriod(
            start=now + timedelta(minutes=15),
            end=now + timedelta(minutes=30),
            electricity=0.10,
            feed_in=0.20,
        ),
        TariffPeriod(
            start=now + timedelta(minutes=30),
            end=now + timedelta(minutes=45),
            electricity=0.50,
            feed_in=0.02,
        ),
    ]


def test_next_period():
    """Test that next_period returns the period right after the current one."""

    now = dt_util.now()

    coordinator = SwissDynamicTariffsCoordinator.__new__(SwissDynamicTariffsCoordinator)
    coordinator.data = _build_quarter_hours(now)

    assert coordinator.next_period == coordinator.data[2]


def test_cheapest_and_most_expensive_period():
    """Test identifying the cheapest and most expensive upcoming quarter hour."""

    now = dt_util.now()

    coordinator = SwissDynamicTariffsCoordinator.__new__(SwissDynamicTariffsCoordinator)
    coordinator.data = _build_quarter_hours(now)

    # The period that already ended (electricity=0.20) must not be considered.
    assert coordinator.cheapest_period("electricity") == coordinator.data[2]
    assert coordinator.most_expensive_period("electricity") == coordinator.data[3]

    assert coordinator.cheapest_period("feed_in") == coordinator.data[3]
    assert coordinator.most_expensive_period("feed_in") == coordinator.data[2]


def test_average_price():
    """Test computing the average upcoming price for a tariff type."""

    now = dt_util.now()

    coordinator = SwissDynamicTariffsCoordinator.__new__(SwissDynamicTariffsCoordinator)
    coordinator.data = _build_quarter_hours(now)

    # Only the three upcoming periods (0.30, 0.10, 0.50) count.
    assert coordinator.average_price("electricity") == pytest.approx(0.30)


def test_cheapest_period_without_data():
    """Test that cheapest/most expensive/average handle an empty dataset."""

    coordinator = SwissDynamicTariffsCoordinator.__new__(SwissDynamicTariffsCoordinator)
    coordinator.data = []

    assert coordinator.cheapest_period("electricity") is None
    assert coordinator.most_expensive_period("electricity") is None
    assert coordinator.average_price("electricity") is None
    assert coordinator.next_period is None
