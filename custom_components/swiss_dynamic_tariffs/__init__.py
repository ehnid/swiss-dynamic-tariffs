"""Swiss Dynamic Tariffs integration."""

from __future__ import annotations

from pathlib import Path

from homeassistant.components import frontend as ha_frontend
from homeassistant.components.http import StaticPathConfig
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import (
    CONF_PROVIDER,
    CONF_TARIFF,
    DOMAIN,
    FRONTEND_URL,
    PLATFORMS,
    PROVIDER_BKW,
    VERSION,
)
from .coordinator import SwissDynamicTariffsCoordinator
from .providers.registry import create_provider

CONFIG_SCHEMA = cv.empty_config_schema(DOMAIN)

type SwissDynamicTariffsConfigEntry = ConfigEntry[SwissDynamicTariffsCoordinator]

FRONTEND_PATH = Path(__file__).parent / "frontend" / "swiss-dynamic-tariffs.js"


async def async_setup(
    hass: HomeAssistant,
    config: dict,
) -> bool:
    """Set up the integration."""

    await hass.http.async_register_static_paths(
        [
            StaticPathConfig(
                FRONTEND_URL,
                str(FRONTEND_PATH),
                cache_headers=True,
            )
        ]
    )
    ha_frontend.add_extra_js_url(hass, f"{FRONTEND_URL}?v={VERSION}")

    return True


async def async_setup_entry(
    hass: HomeAssistant,
    entry: SwissDynamicTariffsConfigEntry,
) -> bool:
    """Set up Swiss Dynamic Tariffs from a config entry."""

    hass.data.setdefault(DOMAIN, {})

    provider_name = entry.data.get(CONF_PROVIDER, PROVIDER_BKW)
    tariff_name = entry.data.get(CONF_TARIFF)

    session = async_get_clientsession(hass)

    provider = create_provider(provider_name, session, tariff_name)

    coordinator = SwissDynamicTariffsCoordinator(
        hass,
        provider,
        entry,
    )

    try:
        await coordinator.async_config_entry_first_refresh()
    except Exception as err:
        raise ConfigEntryNotReady(f"Initial tariff fetch failed: {err}") from err

    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(
        entry,
        PLATFORMS,
    )

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: SwissDynamicTariffsConfigEntry,
) -> bool:
    """Unload a config entry."""

    unload_ok = await hass.config_entries.async_unload_platforms(
        entry,
        PLATFORMS,
    )

    if unload_ok:
        hass.data[DOMAIN].pop(
            entry.entry_id,
            None,
        )

    return unload_ok
