from unittest.mock import AsyncMock, Mock, patch

import pytest


@pytest.mark.asyncio
async def test_setup_entry(hass):
    """Test config entry setup."""

    entry = Mock()
    entry.entry_id = "test"
    entry.domain = "swiss_dynamic_tariffs"
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
