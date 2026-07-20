"""Swiss Dynamic Tariffs integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN, PLATFORMS
from .coordinator import SwissDynamicTariffsCoordinator
from .providers.registry import get_provider

CONFIG_SCHEMA = cv.empty_config_schema(DOMAIN)

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

    provider_class = get_provider(provider_name)

    session = async_get_clientsession(hass)

    provider = provider_class(session)

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
