"""Test provider registry."""

from custom_components.swiss_dynamic_tariffs.providers.bkw import (
    BKWProvider,
)
from custom_components.swiss_dynamic_tariffs.providers.ckw import CKWProvider
from custom_components.swiss_dynamic_tariffs.providers.registry import (
    get_provider,
)


def test_get_bkw_provider():
    """Test BKW provider lookup."""

    provider = get_provider("bkw")

    assert provider is BKWProvider


def test_get_ckw_provider():
    """Test CKW provider lookup."""

    provider = get_provider("ckw")

    assert provider is CKWProvider
