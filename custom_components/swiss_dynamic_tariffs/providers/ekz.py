"""EKZ dynamic tariffs provider."""

from __future__ import annotations

from ..const import EKZ_API_URL
from .standard import StandardTariffProvider


class EKZProvider(StandardTariffProvider):
    """EKZ provider for the integrated dynamic tariff."""

    name = "EKZ"
    attribution = "Data provided by EKZ"
    api_url = EKZ_API_URL
    allowed_tariff_names = ("integrated_400D", "integrated_400D_E")
    default_tariff_name = "integrated_400D"
    supported_tariff_types = ("integrated",)
