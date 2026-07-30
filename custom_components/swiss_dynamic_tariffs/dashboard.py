"""Provision the optional user-managed Lovelace dashboard."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components import websocket_api
from homeassistant.components.lovelace import dashboard as lovelace_dashboard
from homeassistant.components.lovelace.const import (
    CONF_ICON,
    CONF_REQUIRE_ADMIN,
    CONF_SHOW_IN_SIDEBAR,
    CONF_TITLE,
    CONF_URL_PATH,
    LOVELACE_DATA,
)
from homeassistant.const import CONF_ID
from homeassistant.core import HomeAssistant
from homeassistant.helpers.storage import Store

from .const import (
    DASHBOARD_STORAGE_KEY,
    DASHBOARD_STORAGE_VERSION,
    DASHBOARD_STRATEGY_TYPE,
    DASHBOARD_URL_PATH,
    NAME,
)

_LOGGER = logging.getLogger(__name__)

_DASHBOARDS_LIST_COMMAND = "lovelace/dashboards/list"
_DASHBOARD_ICON = "mdi:chart-timeline-variant"


def _active_dashboards_collection(
    hass: HomeAssistant,
) -> lovelace_dashboard.DashboardsCollection | None:
    """Return the collection backing Home Assistant's dashboard UI.

    Home Assistant does not currently expose a public Python function for
    creating a storage dashboard. Its registered list command is deliberately
    used to obtain the already-loaded collection instead of opening a second
    collection over the same storage file. Using the active instance is
    essential: its listeners immediately register the sidebar panel and keep
    rename, reorder and delete operations in sync.
    """

    registered = hass.data.get(websocket_api.DOMAIN, {}).get(_DASHBOARDS_LIST_COMMAND)
    if not isinstance(registered, tuple) or not registered:
        return None

    handler_owner = getattr(registered[0], "__self__", None)
    collection = getattr(handler_owner, "storage_collection", None)
    if not isinstance(collection, lovelace_dashboard.DashboardsCollection):
        return None

    return collection


def _matching_dashboard(items: list[dict[str, Any]]) -> dict[str, Any] | None:
    """Find an existing dashboard that should remain under user ownership."""

    return next(
        (
            item
            for item in items
            if item.get(CONF_URL_PATH) == DASHBOARD_URL_PATH
            or item.get(CONF_TITLE) == NAME
        ),
        None,
    )


async def async_ensure_user_dashboard(hass: HomeAssistant) -> None:
    """Create the tariff dashboard once and leave later ownership to the user."""

    marker_store = Store[dict[str, bool]](
        hass,
        DASHBOARD_STORAGE_VERSION,
        DASHBOARD_STORAGE_KEY,
    )
    marker = await marker_store.async_load()
    collection = _active_dashboards_collection(hass)
    if collection is None:
        raise RuntimeError("Active Lovelace dashboard collection is unavailable")

    existing = _matching_dashboard(collection.async_items())
    if existing is not None:
        if not marker:
            await marker_store.async_save({"provisioned": True})
        return

    # A retained marker with no matching dashboard means that the user deleted
    # it. Do not recreate it and thereby undo an explicit UI action.
    if marker and marker.get("provisioned"):
        return

    item = await collection.async_create_item(
        {
            CONF_ICON: _DASHBOARD_ICON,
            CONF_REQUIRE_ADMIN: False,
            CONF_SHOW_IN_SIDEBAR: True,
            CONF_TITLE: NAME,
            CONF_URL_PATH: DASHBOARD_URL_PATH,
        }
    )

    try:
        config = hass.data[LOVELACE_DATA].dashboards[DASHBOARD_URL_PATH]
        await config.async_save({"strategy": {"type": DASHBOARD_STRATEGY_TYPE}})
    except Exception:
        # Roll back the item created above instead of leaving a blank dashboard.
        await collection.async_delete_item(item[CONF_ID])
        raise

    await marker_store.async_save({"provisioned": True})
    _LOGGER.info("Created user-managed Swiss Dynamic Tariffs dashboard")
