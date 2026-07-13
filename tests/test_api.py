"""Test API client."""

from unittest.mock import AsyncMock, Mock

import pytest

from aiohttp import ClientResponseError

from custom_components.swiss_dynamic_tariffs.api import (
    SwissDynamicTariffsApiClient,
)


@pytest.mark.asyncio
async def test_get_data():
    """Test API data retrieval."""

    session = Mock()

    response = Mock()
    response.raise_for_status = Mock()

    async def json():
        return {"prices": []}

    response.json = json

    context_manager = Mock()
    context_manager.__aenter__ = AsyncMock(return_value=response)
    context_manager.__aexit__ = AsyncMock(return_value=None)

    session.get.return_value = context_manager

    client = SwissDynamicTariffsApiClient(
        session,
    )

    result = await client.async_get_data()

    assert result == []


@pytest.mark.asyncio
async def test_get_data_http_error():
    """Test API error handling."""

    session = Mock()

    response = Mock()

    response.raise_for_status.side_effect = ClientResponseError(
        request_info=Mock(),
        history=(),
        status=500,
        message="Server error",
    )

    context_manager = Mock()

    context_manager.__aenter__ = AsyncMock(return_value=response)

    context_manager.__aexit__ = AsyncMock(return_value=None)

    session.get.return_value = context_manager

    client = SwissDynamicTariffsApiClient(
        session,
    )

    with pytest.raises(RuntimeError):
        await client.async_get_data()
