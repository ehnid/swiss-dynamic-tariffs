from unittest.mock import AsyncMock, Mock

from custom_components.swiss_dynamic_tariffs.coordinator import (
    SwissDynamicTariffsCoordinator,
)


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
