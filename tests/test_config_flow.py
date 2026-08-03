"""Test the integration config flow."""

from unittest.mock import AsyncMock, patch

import pytest
import voluptuous as vol

from homeassistant.helpers.selector import SelectSelector, SelectSelectorMode

from custom_components.swiss_dynamic_tariffs.const import CONF_PROVIDER, DOMAIN


@pytest.fixture(autouse=True)
def bypass_provider_requests():
    """Prevent config-entry setup from making provider requests."""

    with (
        patch(
            "custom_components.swiss_dynamic_tariffs.providers.bkw.BKWProvider.async_get_tariffs",
            new=AsyncMock(return_value=[]),
        ),
        patch(
            "custom_components.swiss_dynamic_tariffs.providers.standard.StandardTariffProvider.async_get_tariffs",
            new=AsyncMock(return_value=[]),
        ),
    ):
        yield


@pytest.mark.asyncio
async def test_config_flow_single_step(hass):
    """Test the legacy BKW selection key and stored tariff name."""

    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": "user"},
        data={"provider": "bkw"},
    )

    assert result["type"] == "create_entry"
    assert result["title"] == "BKW – dynamische Einspeisevergütung"
    assert result["data"] == {"provider": "bkw", "tariff": "feed_in"}


@pytest.mark.asyncio
async def test_config_flow_starts_without_a_selected_tariff(hass):
    """Show a dropdown without implicitly choosing its first BKW option."""

    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": "user"},
    )

    assert result["type"] == "form"
    schema = result["data_schema"].schema
    provider_marker = next(
        marker for marker in schema if marker.schema == CONF_PROVIDER
    )
    provider_selector = schema[provider_marker]
    assert provider_marker.default is vol.UNDEFINED
    assert isinstance(provider_selector, SelectSelector)
    assert provider_selector.config["mode"] == SelectSelectorMode.DROPDOWN


@pytest.mark.asyncio
async def test_config_flow_already_configured(hass):
    """Test that the same provider/tariff combination cannot be configured twice."""

    await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": "user"},
        data={"provider": "bkw"},
    )

    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": "user"},
        data={"provider": "bkw"},
    )

    assert result["type"] == "abort"
    assert result["reason"] == "already_configured"


@pytest.mark.parametrize(
    ("selection", "title", "provider", "tariff"),
    [
        ("ckw", "CKW – Home Dynamic", "ckw", "home_dynamic"),
        (
            "ckw_business",
            "CKW – Business Dynamic",
            "ckw",
            "business_dynamic",
        ),
        ("groupe_e", "Groupe E – Vario", "groupe_e", "VARIO"),
        (
            "primeo",
            "Primeo Energie – Netz dynamisch",
            "primeo",
            "NetzDynamisch",
        ),
        (
            "primeo_avag",
            "Primeo Energie – Netz dynamisch (AVAG)",
            "primeo",
            "NetzDynamischAVAG",
        ),
        (
            "primeo_elag",
            "Primeo Energie – Netz dynamisch (ELAG)",
            "primeo",
            "NetzDynamischELAG",
        ),
        (
            "ekz",
            "EKZ – Energie Dynamisch + Netz 400D",
            "ekz",
            "integrated_400D",
        ),
        (
            "ekz_einsiedeln",
            "EKZ Einsiedeln – Energie Dynamisch + Netz 400D",
            "ekz",
            "integrated_400D_E",
        ),
    ],
)
@pytest.mark.asyncio
async def test_config_flow_tariff_options(
    hass,
    selection,
    title,
    provider,
    tariff,
):
    """Test every additional provider/tariff option."""

    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": "user"},
        data={"provider": selection},
    )

    assert result["type"] == "create_entry"
    assert result["title"] == title
    assert result["data"] == {"provider": provider, "tariff": tariff}


@pytest.mark.asyncio
async def test_multiple_tariffs_from_same_provider_are_allowed(hass):
    """Test that CKW home and business tariffs can coexist."""

    home = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": "user"},
        data={"provider": "ckw"},
    )
    business = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": "user"},
        data={"provider": "ckw_business"},
    )

    assert home["type"] == "create_entry"
    assert business["type"] == "create_entry"


@pytest.mark.asyncio
async def test_options_flow_restores_dashboard(hass):
    """Expose a confirmed dashboard repair action in integration options."""

    await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": "user"},
        data={"provider": "bkw"},
    )
    entry = hass.config_entries.async_entries(DOMAIN)[0]

    result = await hass.config_entries.options.async_init(entry.entry_id)
    assert result["type"] == "menu"
    assert result["menu_options"] == ["dashboard"]

    result = await hass.config_entries.options.async_configure(
        result["flow_id"],
        {"next_step_id": "dashboard"},
    )
    assert result["type"] == "form"
    assert result["step_id"] == "dashboard"

    with patch(
        "custom_components.swiss_dynamic_tariffs.config_flow."
        "async_ensure_user_dashboard",
        new=AsyncMock(),
    ) as restore_dashboard:
        result = await hass.config_entries.options.async_configure(
            result["flow_id"],
            {},
        )

    assert result["type"] == "create_entry"
    restore_dashboard.assert_awaited_once_with(hass, force=True)


@pytest.mark.asyncio
async def test_options_flow_reports_dashboard_restore_failure(hass):
    """Keep the restore form open with an actionable error on failure."""

    await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": "user"},
        data={"provider": "bkw"},
    )
    entry = hass.config_entries.async_entries(DOMAIN)[0]
    result = await hass.config_entries.options.async_init(entry.entry_id)
    result = await hass.config_entries.options.async_configure(
        result["flow_id"],
        {"next_step_id": "dashboard"},
    )

    with patch(
        "custom_components.swiss_dynamic_tariffs.config_flow."
        "async_ensure_user_dashboard",
        new=AsyncMock(side_effect=RuntimeError("unavailable")),
    ):
        result = await hass.config_entries.options.async_configure(
            result["flow_id"],
            {},
        )

    assert result["type"] == "form"
    assert result["errors"] == {"base": "dashboard_creation_failed"}
