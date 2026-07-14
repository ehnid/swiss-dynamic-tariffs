"""Swiss Dynamic Tariffs integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN, PLATFORMS
from .coordinator import SwissDynamicTariffsCoordinator
from .providers.registry import get_provider

from homeassistant.helpers import config_validation as cv

CONFIG_SCHEMA = cv.empty_config_schema

type SwissDynamicTariffsConfigEntry = ConfigEntry[SwissDynamicTariffsCoordinator]


async def async_setup(
    hass: HomeAssistant,
    config: dict,
) -> bool:
    """Set up the integration."""

    return True


async def async_setup_entry(
    hass: HomeAssistant,
    entry: SwissDynamicTariffsConfigEntry,
) -> bool:
    """Set up Swiss Dynamic Tariffs from a config entry."""

    hass.data.setdefault(DOMAIN, {})

    provider_name = entry.data.get("provider", "bkw")

    if not isinstance(provider_name, str):
        provider_name = "bkw"

    provider_class = get_provider(provider_name)

    session = async_get_clientsession(hass)

    provider = provider_class(
        session,
    )

    coordinator = SwissDynamicTariffsCoordinator(
        hass,
        provider,
        entry,
    )

    await coordinator.async_refresh()

    if not coordinator.last_update_success:
        raise ConfigEntryNotReady

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

    hass.data[DOMAIN].pop(
        entry.entry_id,
        None,
    )

    return True
