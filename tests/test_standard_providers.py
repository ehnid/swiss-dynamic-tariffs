"""Test providers based on the Swiss standard tariff API."""

from unittest.mock import AsyncMock, Mock

import pytest

from custom_components.swiss_dynamic_tariffs.const import (
    EKZ_API_URL,
    GROUPE_E_API_URL,
    PRIMEO_API_URL,
    REQUEST_TIMEOUT,
)
from custom_components.swiss_dynamic_tariffs.providers.ekz import EKZProvider
from custom_components.swiss_dynamic_tariffs.providers.groupe_e import (
    GroupeEProvider,
)
from custom_components.swiss_dynamic_tariffs.providers.primeo import PrimeoProvider


def _mock_session(response_data):
    """Return a session mock yielding the supplied JSON response."""

    response = Mock()
    response.json = AsyncMock(return_value=response_data)
    response.raise_for_status = Mock()

    session = Mock()
    session.get.return_value.__aenter__ = AsyncMock(return_value=response)
    session.get.return_value.__aexit__ = AsyncMock(return_value=None)
    return session


def _response(**components):
    """Build a one-period standard tariff response."""

    return {
        "publication_timestamp": "2026-07-21T18:00:00+02:00",
        "prices": [
            {
                "start_timestamp": "2026-07-22T00:00:00+02:00",
                "end_timestamp": "2026-07-22T00:15:00+02:00",
                **components,
            }
        ],
    }


@pytest.mark.asyncio
async def test_groupe_e_vario_provider():
    """Test Groupe E's grid and integrated VARIO components."""

    session = _mock_session(
        _response(
            grid=[{"unit": "CHF_kWh", "value": 0.1039}],
            integrated=[{"unit": "CHF_kWh", "value": 0.2234}],
        )
    )

    tariffs = await GroupeEProvider(session, "VARIO").async_get_tariffs()

    assert tariffs[0].grid == 0.1039
    assert tariffs[0].integrated == 0.2234
    args, kwargs = session.get.call_args
    assert args == (GROUPE_E_API_URL,)
    assert "tariff_name" not in kwargs["params"]
    assert kwargs["timeout"].total == REQUEST_TIMEOUT


@pytest.mark.asyncio
async def test_primeo_tariff_variant():
    """Test Primeo's AVAG option and all price components."""

    session = _mock_session(
        _response(
            electricity=[{"unit": "CHF_kWh", "value": 0.13}],
            grid_usage=[{"unit": "CHF_kWh", "value": 0.1}],
            grid=[{"unit": "CHF_kWh", "value": 0.1303}],
            integrated=[{"unit": "CHF_kWh", "value": 0.2603}],
        )
    )

    tariffs = await PrimeoProvider(session, "NetzDynamischAVAG").async_get_tariffs()

    assert tariffs[0].electricity == 0.13
    assert tariffs[0].grid_usage == 0.1
    assert tariffs[0].grid == 0.1303
    assert tariffs[0].integrated == 0.2603
    args, kwargs = session.get.call_args
    assert args == (PRIMEO_API_URL,)
    assert kwargs["params"]["tariff_name"] == "NetzDynamischAVAG"


@pytest.mark.asyncio
async def test_ekz_selects_kwh_value_after_monthly_charge():
    """Test EKZ parsing when CHF/month precedes CHF/kWh."""

    session = _mock_session(
        _response(
            integrated=[
                {"unit": "CHF_m", "value": 3.0},
                {"unit": "CHF_kWh", "value": 0.20368},
            ]
        )
    )

    tariffs = await EKZProvider(session, "integrated_400D").async_get_tariffs()

    assert tariffs[0].integrated == 0.20368
    args, kwargs = session.get.call_args
    assert args == (EKZ_API_URL,)
    assert kwargs["params"]["tariff_name"] == "integrated_400D"


@pytest.mark.parametrize(
    ("provider_class", "tariff_name"),
    [
        (GroupeEProvider, "not_vario"),
        (PrimeoProvider, "unknown"),
        (EKZProvider, "integrated_unknown"),
    ],
)
def test_standard_provider_rejects_unknown_tariff(provider_class, tariff_name):
    """Test that invalid tariff configurations cannot be instantiated."""

    with pytest.raises(ValueError, match="Unsupported"):
        provider_class(Mock(), tariff_name)
