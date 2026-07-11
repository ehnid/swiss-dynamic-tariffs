"""Registry for tariff providers."""

from __future__ import annotations

from .base import BaseProvider
from .bkw import BKWProvider


PROVIDERS: dict[str, type[BaseProvider]] = {
    "bkw": BKWProvider,
}
