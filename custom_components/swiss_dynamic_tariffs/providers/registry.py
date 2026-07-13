"""Provider registry."""

from __future__ import annotations

from .base import TariffProvider
from .bkw import BKWProvider


PROVIDERS: dict[str, type[TariffProvider]] = {
    "bkw": BKWProvider,
}


def get_provider(name: str) -> type[TariffProvider]:
    """Return provider class by name."""

    try:
        return PROVIDERS[name]
    except KeyError as err:
        raise ValueError(f"Unknown tariff provider: {name}") from err
