from custom_components import swiss_dynamic_tariffs
from custom_components.swiss_dynamic_tariffs.const import (
    DOMAIN,
    FRONTEND_URL,
    NAME,
    PANEL_COMPONENT_NAME,
    PANEL_URL_PATH,
    VERSION,
)
from homeassistant.config_entries import ConfigEntryState
from unittest.mock import AsyncMock, Mock, patch

import pytest


@pytest.mark.asyncio
async def test_setup_registers_frontend_module(hass):
    """Test that setup registers the bundled tariff card."""

    register_static_paths = AsyncMock()
    hass.http = Mock(async_register_static_paths=register_static_paths)

    with (
        patch(
            "custom_components.swiss_dynamic_tariffs.ha_frontend.add_extra_js_url",
        ) as add_extra_js_url,
        patch(
            "custom_components.swiss_dynamic_tariffs.panel_custom.async_register_panel",
            new=AsyncMock(),
        ) as register_panel,
    ):
        result = await swiss_dynamic_tariffs.async_setup(hass, {})

    assert result is True
    register_static_paths.assert_awaited_once()
    static_path = register_static_paths.await_args.args[0][0]
    assert static_path.url_path == FRONTEND_URL
    assert static_path.path.endswith("frontend/swiss-dynamic-tariffs.js")
    assert static_path.cache_headers is True
    add_extra_js_url.assert_called_once_with(
        hass,
        f"{FRONTEND_URL}?v={VERSION}",
    )
    register_panel.assert_awaited_once_with(
        hass,
        frontend_url_path=PANEL_URL_PATH,
        webcomponent_name=PANEL_COMPONENT_NAME,
        sidebar_title=NAME,
        sidebar_icon="mdi:chart-timeline-variant",
        module_url=f"{FRONTEND_URL}?v={VERSION}",
    )


@pytest.mark.asyncio
async def test_setup_survives_dashboard_url_collision(hass):
    """Test that a conflicting user panel does not break the integration."""

    hass.http = Mock(async_register_static_paths=AsyncMock())

    with (
        patch(
            "custom_components.swiss_dynamic_tariffs.ha_frontend.add_extra_js_url",
        ),
        patch(
            "custom_components.swiss_dynamic_tariffs.panel_custom.async_register_panel",
            new=AsyncMock(side_effect=ValueError("URL already used")),
        ),
    ):
        result = await swiss_dynamic_tariffs.async_setup(hass, {})

    assert result is True


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
