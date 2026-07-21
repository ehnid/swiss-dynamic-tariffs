from custom_components import swiss_dynamic_tariffs
from custom_components.swiss_dynamic_tariffs.const import DOMAIN
from homeassistant.config_entries import ConfigEntryState
from unittest.mock import AsyncMock, Mock, patch

import pytest


@pytest.mark.asyncio
async def test_setup_entry(hass):
    """Test config entry setup."""

    entry = Mock()
    entry.entry_id = "test"
    entry.domain = "swiss_dynamic_tariffs"
    entry.state = ConfigEntryState.SETUP_IN_PROGRESS
    entry.data = {
        "provider": "bkw",
    }

    with (
        patch(
            "custom_components.swiss_dynamic_tariffs.providers.bkw.BKWProvider.async_get_tariffs",
            new=AsyncMock(return_value=[]),
        ),
        patch(
            "homeassistant.config_entries.ConfigEntries.async_forward_entry_setups",
            new=AsyncMock(),
        ),
    ):
        from custom_components.swiss_dynamic_tariffs import async_setup_entry

        result = await async_setup_entry(
            hass,
            entry,
        )

    assert result is True


@pytest.mark.asyncio
async def test_setup_entry_passes_selected_tariff_to_provider(hass):
    """Test that setup creates the provider with the selected tariff."""

    entry = Mock()
    entry.entry_id = "test"
    entry.domain = DOMAIN
    entry.state = ConfigEntryState.SETUP_IN_PROGRESS
    entry.data = {
        "provider": "primeo",
        "tariff": "NetzDynamischAVAG",
    }

    with (
        patch(
            "custom_components.swiss_dynamic_tariffs.providers.standard."
            "StandardTariffProvider.async_get_tariffs",
            new=AsyncMock(return_value=[]),
        ),
        patch(
            "homeassistant.config_entries.ConfigEntries.async_forward_entry_setups",
            new=AsyncMock(),
        ),
    ):
        result = await swiss_dynamic_tariffs.async_setup_entry(hass, entry)

    assert result is True
    assert hass.data[DOMAIN][entry.entry_id].provider.tariff_name == "NetzDynamischAVAG"


@pytest.mark.asyncio
async def test_unload_entry(hass):
    """Test config entry unload."""

    entry = Mock()
    entry.entry_id = "test"

    hass.data[DOMAIN] = {
        "test": Mock(),
    }

    with patch(
        "homeassistant.config_entries.ConfigEntries.async_unload_platforms",
        new=AsyncMock(return_value=True),
    ) as unload:
        result = await swiss_dynamic_tariffs.async_unload_entry(
            hass,
            entry,
        )

    assert result is True
    assert "test" not in hass.data[DOMAIN]
    unload.assert_called_once()
