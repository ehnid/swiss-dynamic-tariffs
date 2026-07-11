"""BKW tariff provider."""

from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal

from ..models import TariffPeriod, TariffPrice
from .base import BaseProvider


class BKWProvider(BaseProvider):
    """Provider for BKW dynamic tariffs."""

    @property
    def name(self) -> str:
        """Return provider name."""
        return "BKW"

    async def async_get_tariffs(self) -> TariffPeriod:
        """Fetch tariff data from BKW."""

        # Temporary test data.
        # This will be replaced by the real BKW data source.

        return TariffPeriod(
            prices=[
                TariffPrice(
                    timestamp=datetime.now(timezone.utc),
                    price=Decimal("0.28"),
                )
            ]
        )
