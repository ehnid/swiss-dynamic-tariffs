"""CKW dynamic tariffs provider."""

from __future__ import annotations

from datetime import datetime

from ..const import CKW_API_URL
from .standard import StandardTariffProvider, build_request_params


class CKWProvider(StandardTariffProvider):
    """CKW tariff provider."""

    name = "CKW"
    attribution = "Data provided by CKW"
    api_url = CKW_API_URL
    allowed_tariff_names = ("home_dynamic", "business_dynamic")
    default_tariff_name = "home_dynamic"
    supported_tariff_types = (
        "electricity",
        "grid_usage",
        "grid",
        "integrated",
    )


def _request_params(now: datetime | None = None) -> dict[str, str]:
    """Build CKW's default request parameters (compatibility helper)."""

    return build_request_params(CKWProvider.default_tariff_name, now)
