"""Shared parsing helpers for tariff provider responses."""

from __future__ import annotations

from datetime import datetime
import math

from ..exceptions import ProviderDataError
from ..models import TariffPeriod, TariffType


def _parse_price_component(data: object) -> float | None:
    """Extract and validate the CHF/kWh value from a component."""

    if data is None or data == []:
        return None

    if not isinstance(data, list) or not all(
        isinstance(component, dict) for component in data
    ):
        raise ProviderDataError("Invalid price component")

    component = next(
        (
            component
            for component in data
            if component.get("unit") in ("CHF_kWh", "CHF/kWh")
        ),
        None,
    )

    if component is None:
        units = ", ".join(str(item.get("unit")) for item in data)
        raise ProviderDataError(f"Unsupported price unit(s): {units}")

    try:
        value = float(component["value"])
    except (KeyError, TypeError, ValueError) as err:
        raise ProviderDataError("Invalid price value") from err

    if not math.isfinite(value):
        raise ProviderDataError("Price value must be finite")

    return value


def _parse_timestamp(value: object) -> datetime:
    """Parse and validate an ISO 8601 timestamp."""

    if not isinstance(value, str):
        raise ProviderDataError("Invalid tariff timestamp")

    try:
        timestamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as err:
        raise ProviderDataError("Invalid tariff timestamp") from err

    if timestamp.tzinfo is None:
        raise ProviderDataError("Tariff timestamp must include a timezone")

    return timestamp


def parse_tariff_response(
    data: object,
    supported_types: tuple[TariffType, ...],
) -> list[TariffPeriod]:
    """Parse the common Swiss dynamic-tariff response shape."""

    if not isinstance(data, dict) or not isinstance(data.get("prices"), list):
        raise ProviderDataError("Invalid tariff API response")

    tariffs: list[TariffPeriod] = []

    for item in data["prices"]:
        if not isinstance(item, dict):
            raise ProviderDataError("Invalid tariff period")

        tariffs.append(
            TariffPeriod(
                start=_parse_timestamp(item.get("start_timestamp")),
                end=_parse_timestamp(item.get("end_timestamp")),
                electricity=(
                    _parse_price_component(item.get("electricity"))
                    if "electricity" in supported_types
                    else None
                ),
                feed_in=(
                    _parse_price_component(item.get("feed_in"))
                    if "feed_in" in supported_types
                    else None
                ),
                grid_usage=(
                    _parse_price_component(item.get("grid_usage"))
                    if "grid_usage" in supported_types
                    else None
                ),
                grid=(
                    _parse_price_component(item.get("grid"))
                    if "grid" in supported_types
                    else None
                ),
                integrated=(
                    _parse_price_component(item.get("integrated"))
                    if "integrated" in supported_types
                    else None
                ),
            )
        )

    return tariffs
