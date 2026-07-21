from datetime import timedelta
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch

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

    frozen_now = dt_util.now()

    coordinator = SwissDynamicTariffsCoordinator.__new__(SwissDynamicTariffsCoordinator)

    coordinator.data = [
        TariffPeriod(
            start=frozen_now - timedelta(hours=1),
            end=frozen_now + timedelta(hours=1),
            electricity=0.25,
            feed_in=0.10,
            grid=0.05,
            integrated=0.30,
        )
    ]

    with patch(
        "custom_components.swiss_dynamic_tariffs.coordinator.dt_util.now",
        return_value=frozen_now,
    ):
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

    frozen_now = dt_util.now()

    first = SimpleNamespace(
        electricity=0.25,
        start=frozen_now - timedelta(minutes=30),
        end=frozen_now + timedelta(minutes=30),
    )

    second = SimpleNamespace(
        electricity=0.30,
        start=frozen_now + timedelta(minutes=30),
        end=frozen_now + timedelta(hours=1),
    )

    coordinator.data = [
        first,
        second,
    ]

    with patch(
        "custom_components.swiss_dynamic_tariffs.coordinator.dt_util.now",
        return_value=frozen_now,
    ):
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


def _frozen_quarter_hours():
    """Build four quarter-hour periods anchored to one fixed reference time.

    The reference time is returned alongside the periods so tests can patch
    coordinator.dt_util.now() to that exact same instant. Without this, the
    test would build periods around one call to dt_util.now() and then let
    the coordinator make its own, separate call to dt_util.now() - any real
    time passing between the two (CI scheduling delays, a slow worker, ...)
    can shift which periods count as "past" vs. "upcoming" and make the test
    flaky, exactly as seen in CI.
    """

    frozen_now = dt_util.now()

    return frozen_now, _build_quarter_hours(frozen_now)


def test_next_period():
    """Test that next_period returns the period right after the current one."""

    frozen_now, periods = _frozen_quarter_hours()

    coordinator = SwissDynamicTariffsCoordinator.__new__(SwissDynamicTariffsCoordinator)
    coordinator.data = periods

    with patch(
        "custom_components.swiss_dynamic_tariffs.coordinator.dt_util.now",
        return_value=frozen_now,
    ):
        assert coordinator.next_period == coordinator.data[2]


def test_next_period_without_current_period():
    """Test that the first future period is returned when none is active."""

    frozen_now, periods = _frozen_quarter_hours()
    coordinator = SwissDynamicTariffsCoordinator.__new__(SwissDynamicTariffsCoordinator)
    coordinator.data = periods[2:]

    with patch(
        "custom_components.swiss_dynamic_tariffs.coordinator.dt_util.now",
        return_value=frozen_now,
    ):
        assert coordinator.next_period == periods[2]


def test_merge_keeps_active_periods_when_provider_publishes_next_day():
    """Test that still-active old data survives a provider response rollover."""

    frozen_now = dt_util.now()
    active = TariffPeriod(
        start=frozen_now - timedelta(minutes=5),
        end=frozen_now + timedelta(minutes=10),
        feed_in=0.10,
    )
    expired = TariffPeriod(
        start=frozen_now - timedelta(minutes=20),
        end=frozen_now - timedelta(minutes=5),
        feed_in=0.09,
    )
    future = TariffPeriod(
        start=frozen_now + timedelta(hours=1),
        end=frozen_now + timedelta(hours=1, minutes=15),
        feed_in=0.11,
    )
    coordinator = SwissDynamicTariffsCoordinator.__new__(SwissDynamicTariffsCoordinator)
    coordinator.data = [expired, active]

    with patch(
        "custom_components.swiss_dynamic_tariffs.coordinator.dt_util.now",
        return_value=frozen_now,
    ):
        merged = coordinator._merge_tariff_periods([future])

    assert merged == [active, future]


def test_cheapest_and_most_expensive_period():
    """Test identifying the cheapest and most expensive upcoming quarter hour."""

    frozen_now, periods = _frozen_quarter_hours()

    coordinator = SwissDynamicTariffsCoordinator.__new__(SwissDynamicTariffsCoordinator)
    coordinator.data = periods

    with patch(
        "custom_components.swiss_dynamic_tariffs.coordinator.dt_util.now",
        return_value=frozen_now,
    ):
        # The period that already ended (electricity=0.20) must not be considered.
        assert coordinator.cheapest_period("electricity") == coordinator.data[2]
        assert coordinator.most_expensive_period("electricity") == coordinator.data[3]

        assert coordinator.cheapest_period("feed_in") == coordinator.data[3]
        assert coordinator.most_expensive_period("feed_in") == coordinator.data[2]


def test_average_price():
    """Test computing the average upcoming price for a tariff type."""

    frozen_now, periods = _frozen_quarter_hours()

    coordinator = SwissDynamicTariffsCoordinator.__new__(SwissDynamicTariffsCoordinator)
    coordinator.data = periods

    with patch(
        "custom_components.swiss_dynamic_tariffs.coordinator.dt_util.now",
        return_value=frozen_now,
    ):
        # Only the three upcoming periods (0.30, 0.10, 0.50) count.
        assert coordinator.average_price("electricity") == pytest.approx(0.30)


def test_future_periods_returns_all_future_prices():
    """Test returning every future quarter hour for one tariff component."""

    frozen_now, periods = _frozen_quarter_hours()
    coordinator = SwissDynamicTariffsCoordinator.__new__(SwissDynamicTariffsCoordinator)
    coordinator.data = periods

    with patch(
        "custom_components.swiss_dynamic_tariffs.coordinator.dt_util.now",
        return_value=frozen_now,
    ):
        assert coordinator.future_periods("electricity") == periods[2:]


def test_future_periods_omits_missing_tariff_values():
    """Test that future periods without the selected component are omitted."""

    frozen_now, periods = _frozen_quarter_hours()
    periods[2] = TariffPeriod(
        start=periods[2].start,
        end=periods[2].end,
        feed_in=periods[2].feed_in,
    )
    coordinator = SwissDynamicTariffsCoordinator.__new__(SwissDynamicTariffsCoordinator)
    coordinator.data = periods

    with patch(
        "custom_components.swiss_dynamic_tariffs.coordinator.dt_util.now",
        return_value=frozen_now,
    ):
        assert coordinator.future_periods("electricity") == [periods[3]]


def test_cheapest_period_without_data():
    """Test that cheapest/most expensive/average handle an empty dataset."""

    coordinator = SwissDynamicTariffsCoordinator.__new__(SwissDynamicTariffsCoordinator)
    coordinator.data = []

    assert coordinator.cheapest_period("electricity") is None
    assert coordinator.most_expensive_period("electricity") is None
    assert coordinator.average_price("electricity") is None
    assert coordinator.next_period is None
    assert coordinator.future_periods("electricity") == []
