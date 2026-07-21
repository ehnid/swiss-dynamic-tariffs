"""Provider registry."""

from __future__ import annotations

from ..const import PROVIDER_BKW, PROVIDER_CKW
from .base import TariffProvider
from .bkw import BKWProvider
from .ckw import CKWProvider


PROVIDERS: dict[str, type[TariffProvider]] = {
    PROVIDER_BKW: BKWProvider,
    PROVIDER_CKW: CKWProvider,
}


def get_provider(name: str) -> type[TariffProvider]:
    """Return provider class by name."""

    try:
        return PROVIDERS[name]
    except KeyError as err:
        raise ValueError(f"Unknown tariff provider: {name}") from err
