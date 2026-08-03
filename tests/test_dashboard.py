"""Tests for the user-managed Lovelace dashboard."""

from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch

import pytest

from homeassistant.components import websocket_api
from homeassistant.components.lovelace import dashboard as lovelace_dashboard
from homeassistant.components.lovelace.const import LOVELACE_DATA
from homeassistant.setup import async_setup_component

from custom_components.swiss_dynamic_tariffs.const import (
    DASHBOARD_CARD_TYPE,
    DASHBOARD_LAYOUT_VERSION,
    DASHBOARD_STRATEGY_TYPE,
    DASHBOARD_URL_PATH,
)
from custom_components.swiss_dynamic_tariffs.dashboard import (
    _DASHBOARDS_LIST_COMMAND,
    _active_dashboards_collection,
    _automatic_dashboard_config,
    async_ensure_user_dashboard,
)


def test_active_dashboard_collection_uses_registered_websocket_handler(hass):
    """Use the live collection whose listeners power dashboard management."""

    collection = lovelace_dashboard.DashboardsCollection.__new__(
        lovelace_dashboard.DashboardsCollection
    )
    handler_owner = SimpleNamespace(storage_collection=collection)

    def list_dashboards():
        return None

    handler_owner.list_dashboards = list_dashboards
    # Bind a method so the implementation can recover its owning websocket
    # collection exactly as it does with Home Assistant's registered handler.
    handler = list_dashboards.__get__(handler_owner)
    hass.data[websocket_api.DOMAIN] = {_DASHBOARDS_LIST_COMMAND: (handler, None)}

    assert _active_dashboards_collection(hass) is collection


@pytest.mark.asyncio
async def test_dashboard_can_be_deleted_through_live_lovelace_collection(hass):
    """Create and delete the dashboard through Home Assistant's real collection."""

    assert await async_setup_component(hass, "lovelace", {"lovelace": {}})

    await async_ensure_user_dashboard(hass)

    collection = _active_dashboards_collection(hass)
    assert collection is not None
    item = next(
        item
        for item in collection.async_items()
        if item["url_path"] == DASHBOARD_URL_PATH
    )
    config = (
        await hass.data[LOVELACE_DATA].dashboards[DASHBOARD_URL_PATH].async_load(False)
    )
    assert config == _automatic_dashboard_config()

    await collection.async_delete_item(item["id"])

    assert DASHBOARD_URL_PATH not in hass.data[LOVELACE_DATA].dashboards

    await async_ensure_user_dashboard(hass)

    assert all(
        item["url_path"] != DASHBOARD_URL_PATH for item in collection.async_items()
    )


@pytest.mark.asyncio
async def test_dashboard_is_created_once_with_static_panel_card(hass):
    """Create a normal storage dashboard with the stable overview card."""

    collection = Mock()
    collection.async_items.return_value = []
    collection.async_create_item = AsyncMock(return_value={"id": DASHBOARD_URL_PATH})
    dashboard_config = Mock(async_save=AsyncMock())
    hass.data[LOVELACE_DATA] = SimpleNamespace(
        dashboards={DASHBOARD_URL_PATH: dashboard_config}
    )
    load_marker = AsyncMock(return_value=None)
    save_marker = AsyncMock()

    with (
        patch(
            "custom_components.swiss_dynamic_tariffs.dashboard.Store.async_load",
            new=load_marker,
        ),
        patch(
            "custom_components.swiss_dynamic_tariffs.dashboard.Store.async_save",
            new=save_marker,
        ),
        patch(
            "custom_components.swiss_dynamic_tariffs.dashboard."
            "_active_dashboards_collection",
            return_value=collection,
        ),
    ):
        await async_ensure_user_dashboard(hass)

    collection.async_create_item.assert_awaited_once()
    dashboard_config.async_save.assert_awaited_once_with(_automatic_dashboard_config())
    save_marker.assert_awaited_once_with(
        {
            "provisioned": True,
            "layout_version": DASHBOARD_LAYOUT_VERSION,
        }
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("marker", [None, {"provisioned": True}])
async def test_legacy_strategy_dashboard_is_migrated(hass, marker):
    """Replace only the strategy-only layout provisioned by older releases."""

    collection = Mock()
    collection.async_items.return_value = [
        {
            "id": DASHBOARD_URL_PATH,
            "url_path": DASHBOARD_URL_PATH,
            "title": "Swiss Dynamic Tariffs",
        }
    ]
    dashboard_config = Mock(
        async_load=AsyncMock(
            return_value={"strategy": {"type": DASHBOARD_STRATEGY_TYPE}}
        ),
        async_save=AsyncMock(),
    )
    hass.data[LOVELACE_DATA] = SimpleNamespace(
        dashboards={DASHBOARD_URL_PATH: dashboard_config}
    )
    save_marker = AsyncMock()

    with (
        patch(
            "custom_components.swiss_dynamic_tariffs.dashboard.Store.async_load",
            new=AsyncMock(return_value=marker),
        ),
        patch(
            "custom_components.swiss_dynamic_tariffs.dashboard.Store.async_save",
            new=save_marker,
        ),
        patch(
            "custom_components.swiss_dynamic_tariffs.dashboard."
            "_active_dashboards_collection",
            return_value=collection,
        ),
    ):
        await async_ensure_user_dashboard(hass)

    dashboard_config.async_save.assert_awaited_once_with(_automatic_dashboard_config())
    assert _automatic_dashboard_config()["views"][0]["cards"] == [
        {"type": DASHBOARD_CARD_TYPE}
    ]
    save_marker.assert_awaited_once_with(
        {
            "provisioned": True,
            "layout_version": DASHBOARD_LAYOUT_VERSION,
        }
    )


@pytest.mark.asyncio
async def test_user_modified_legacy_dashboard_is_not_migrated(hass):
    """Preserve user content even when its integration marker is outdated."""

    collection = Mock()
    collection.async_items.return_value = [
        {
            "id": DASHBOARD_URL_PATH,
            "url_path": DASHBOARD_URL_PATH,
            "title": "Swiss Dynamic Tariffs",
        }
    ]
    dashboard_config = Mock(
        async_load=AsyncMock(return_value={"views": [{"title": "My view"}]}),
        async_save=AsyncMock(),
    )
    hass.data[LOVELACE_DATA] = SimpleNamespace(
        dashboards={DASHBOARD_URL_PATH: dashboard_config}
    )
    save_marker = AsyncMock()

    with (
        patch(
            "custom_components.swiss_dynamic_tariffs.dashboard.Store.async_load",
            new=AsyncMock(return_value={"provisioned": True}),
        ),
        patch(
            "custom_components.swiss_dynamic_tariffs.dashboard.Store.async_save",
            new=save_marker,
        ),
        patch(
            "custom_components.swiss_dynamic_tariffs.dashboard."
            "_active_dashboards_collection",
            return_value=collection,
        ),
    ):
        await async_ensure_user_dashboard(hass)

    dashboard_config.async_save.assert_not_awaited()
    save_marker.assert_awaited_once_with(
        {
            "provisioned": True,
            "layout_version": DASHBOARD_LAYOUT_VERSION,
        }
    )


@pytest.mark.asyncio
async def test_deleted_dashboard_is_not_recreated(hass):
    """Treat a retained marker without a dashboard as an explicit deletion."""

    collection = Mock()
    collection.async_items.return_value = []
    collection.async_create_item = AsyncMock()
    load_marker = AsyncMock(return_value={"provisioned": True})
    save_marker = AsyncMock()

    with (
        patch(
            "custom_components.swiss_dynamic_tariffs.dashboard.Store.async_load",
            new=load_marker,
        ),
        patch(
            "custom_components.swiss_dynamic_tariffs.dashboard.Store.async_save",
            new=save_marker,
        ),
        patch(
            "custom_components.swiss_dynamic_tariffs.dashboard."
            "_active_dashboards_collection",
            return_value=collection,
        ),
    ):
        await async_ensure_user_dashboard(hass)

    collection.async_create_item.assert_not_awaited()
    save_marker.assert_not_awaited()


@pytest.mark.asyncio
async def test_existing_user_dashboard_is_never_overwritten(hass):
    """Adopt an existing matching dashboard without changing its config."""

    collection = Mock()
    collection.async_items.return_value = [
        {
            "id": DASHBOARD_URL_PATH,
            "url_path": DASHBOARD_URL_PATH,
            "title": "Renamed by user",
        }
    ]
    collection.async_create_item = AsyncMock()
    dashboard_config = Mock(
        async_load=AsyncMock(return_value={"views": [{"title": "My dashboard"}]}),
        async_save=AsyncMock(),
    )
    hass.data[LOVELACE_DATA] = SimpleNamespace(
        dashboards={DASHBOARD_URL_PATH: dashboard_config}
    )
    load_marker = AsyncMock(return_value=None)
    save_marker = AsyncMock()

    with (
        patch(
            "custom_components.swiss_dynamic_tariffs.dashboard.Store.async_load",
            new=load_marker,
        ),
        patch(
            "custom_components.swiss_dynamic_tariffs.dashboard.Store.async_save",
            new=save_marker,
        ),
        patch(
            "custom_components.swiss_dynamic_tariffs.dashboard."
            "_active_dashboards_collection",
            return_value=collection,
        ),
    ):
        await async_ensure_user_dashboard(hass)

    collection.async_create_item.assert_not_awaited()
    dashboard_config.async_save.assert_not_awaited()
    save_marker.assert_awaited_once_with(
        {
            "provisioned": True,
            "layout_version": DASHBOARD_LAYOUT_VERSION,
        }
    )
