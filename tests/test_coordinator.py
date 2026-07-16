from datetime import timedelta

from homeassistant.util import dt as dt_util

from custom_components.swiss_dynamic_tariffs.models import TariffPeriod

from unittest.mock import AsyncMock, Mock

from custom_components.swiss_dynamic_tariffs.coordinator import (
    SwissDynamicTariffsCoordinator,
)

from types import SimpleNamespace


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

    from datetime import timedelta

    from homeassistant.util import dt as dt_util

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
