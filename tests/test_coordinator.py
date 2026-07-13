"""Test coordinator."""

from unittest.mock import AsyncMock, Mock

from custom_components.swiss_dynamic_tariffs.coordinator import (
    SwissDynamicTariffsCoordinator,
)


async def test_coordinator_update(hass):
    """Test coordinator update."""

    provider = Mock()
    provider.async_get_tariffs = AsyncMock(return_value=[])

    coordinator = SwissDynamicTariffsCoordinator(
        hass,
        provider,
    )

    await coordinator.async_refresh()

    assert coordinator.data == []
