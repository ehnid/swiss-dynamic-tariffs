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
    DASHBOARD_CARD_TYPE,
    DASHBOARD_LAYOUT_VERSION,
    DASHBOARD_STORAGE_KEY,
    DASHBOARD_STORAGE_VERSION,
    DASHBOARD_STRATEGY_TYPE,
    DASHBOARD_URL_PATH,
    NAME,
)

_LOGGER = logging.getLogger(__name__)

_DASHBOARDS_LIST_COMMAND = "lovelace/dashboards/list"
_DASHBOARD_ICON = "mdi:chart-timeline-variant"


def _automatic_dashboard_config() -> dict[str, Any]:
    """Return the self-updating dashboard without a strategy dependency."""

    return {
        "views": [
            {
                "title": NAME,
                "path": "tariffs",
                "icon": _DASHBOARD_ICON,
                "type": "panel",
                "cards": [{"type": DASHBOARD_CARD_TYPE}],
            }
        ]
    }


def _legacy_strategy_config() -> dict[str, Any]:
    """Return the exact configuration provisioned before layout version 2."""

    return {"strategy": {"type": DASHBOARD_STRATEGY_TYPE}}


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


async def async_ensure_user_dashboard(
    hass: HomeAssistant,
    *,
    force: bool = False,
) -> None:
    """Create the tariff dashboard while preserving user-owned content.

    ``force`` only overrides the retained deletion marker. It deliberately
    does not replace or edit an existing dashboard, so the options-flow repair
    action remains safe for user-customized layouts.
    """

    marker_store = Store[dict[str, bool | int]](
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
        current_marker = {
            "provisioned": True,
            "layout_version": DASHBOARD_LAYOUT_VERSION,
        }
        if not marker or marker.get("layout_version", 1) < DASHBOARD_LAYOUT_VERSION:
            dashboard_path = existing.get(CONF_URL_PATH, DASHBOARD_URL_PATH)
            config = hass.data[LOVELACE_DATA].dashboards.get(dashboard_path)
            stored_config = (
                await config.async_load(False) if config is not None else None
            )
            # Only replace the exact strategy-only layout created by earlier
            # integration versions. Any user edit makes the dashboard theirs
            # and must remain untouched.
            if config is not None and stored_config == _legacy_strategy_config():
                await config.async_save(_automatic_dashboard_config())
                _LOGGER.info(
                    "Migrated Swiss Dynamic Tariffs dashboard to a static layout"
                )

        if marker != current_marker:
            await marker_store.async_save(current_marker)
        return

    # A current marker with no matching dashboard means that the user deleted
    # the static dashboard and it must stay deleted. An older marker can also
    # remain after the user removed the strategy-based dashboard because it no
    # longer loaded. Recreate that legacy case once so the fixed layout is not
    # permanently suppressed by stale provisioning state.
    if (
        marker
        and marker.get("provisioned")
        and marker.get("layout_version", 1) >= DASHBOARD_LAYOUT_VERSION
        and not force
    ):
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
        await config.async_save(_automatic_dashboard_config())
    except Exception:
        # Roll back the item created above instead of leaving a blank dashboard.
        await collection.async_delete_item(item[CONF_ID])
        raise

    await marker_store.async_save(
        {
            "provisioned": True,
            "layout_version": DASHBOARD_LAYOUT_VERSION,
        }
    )
    _LOGGER.info("Created user-managed Swiss Dynamic Tariffs dashboard")
