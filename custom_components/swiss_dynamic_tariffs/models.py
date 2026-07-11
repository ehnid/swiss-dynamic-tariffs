"""Data models for Swiss Dynamic Tariffs."""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass(frozen=True)
class TariffPrice:
    """Represents a single electricity tariff price."""

    timestamp: datetime
    price: Decimal
    currency: str = "CHF"
    unit: str = "kWh"


@dataclass(frozen=True)
class TariffPeriod:
    """Represents a tariff period with multiple prices."""

    prices: list[TariffPrice]

    @property
    def latest(self) -> TariffPrice | None:
        """Return the latest available price."""
        if not self.prices:
            return None

        return max(
            self.prices,
            key=lambda item: item.timestamp,
        )
