import pytest

from custom_components.swiss_dynamic_tariffs.const import DOMAIN


@pytest.mark.asyncio
async def test_config_flow_single_step(hass):
    """Test provider selection flow."""

    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={
            "source": "user",
        },
        data={
            "provider": "bkw",
        },
    )

    assert result["type"] == "create_entry"
    assert result["data"] == {
        "provider": "bkw",
    }


@pytest.mark.asyncio
async def test_config_flow_already_configured(hass):
    """Test that the same provider cannot be configured twice."""

    await hass.config_entries.flow.async_init(
        DOMAIN,
        context={
            "source": "user",
        },
        data={
            "provider": "bkw",
        },
    )

    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={
            "source": "user",
        },
        data={
            "provider": "bkw",
        },
    )

    assert result["type"] == "abort"
    assert result["reason"] == "already_configured"


@pytest.mark.asyncio
async def test_config_flow_ckw(hass):
    """Test configuring CKW as a second supported provider."""

    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": "user"},
        data={"provider": "ckw"},
    )

    assert result["type"] == "create_entry"
    assert result["title"] == "CKW Dynamic Tariffs"
    assert result["data"] == {"provider": "ckw"}
