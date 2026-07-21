"""Test provider and tariff option registry."""

from unittest.mock import Mock

from custom_components.swiss_dynamic_tariffs.providers.bkw import BKWProvider
from custom_components.swiss_dynamic_tariffs.providers.ckw import CKWProvider
from custom_components.swiss_dynamic_tariffs.providers.ekz import EKZProvider
from custom_components.swiss_dynamic_tariffs.providers.groupe_e import (
    GroupeEProvider,
)
from custom_components.swiss_dynamic_tariffs.providers.primeo import PrimeoProvider
from custom_components.swiss_dynamic_tariffs.providers.registry import (
    TARIFF_OPTIONS,
    create_provider,
    get_provider,
    get_tariff_option,
)


def test_provider_lookup():
    """Test all registered provider classes."""

    assert get_provider("bkw") is BKWProvider
    assert get_provider("ckw") is CKWProvider
    assert get_provider("ekz") is EKZProvider
    assert get_provider("groupe_e") is GroupeEProvider
    assert get_provider("primeo") is PrimeoProvider


def test_tariff_options_are_complete():
    """Test selectable option titles and exact tariff names."""

    assert len(TARIFF_OPTIONS) == 9
    assert get_tariff_option("ckw_business").title == "CKW – Business Dynamic"
    assert get_tariff_option("primeo_avag").tariff_name == "NetzDynamischAVAG"
    assert (
        get_tariff_option("ekz_einsiedeln").title
        == "EKZ Einsiedeln – Energie Dynamisch + Netz 400D"
    )


def test_create_provider_passes_selected_tariff():
    """Test provider construction with an explicit tariff name."""

    provider = create_provider("ckw", Mock(), "business_dynamic")

    assert isinstance(provider, CKWProvider)
    assert provider.tariff_name == "business_dynamic"
