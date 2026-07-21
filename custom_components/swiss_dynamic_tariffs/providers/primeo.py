"""Primeo Energie dynamic tariffs provider."""

from __future__ import annotations

from ..const import PRIMEO_API_URL
from .standard import StandardTariffProvider


class PrimeoProvider(StandardTariffProvider):
    """Primeo provider for its dynamic network tariff areas."""

    name = "Primeo Energie"
    attribution = "Data provided by Primeo Energie"
    api_url = PRIMEO_API_URL
    allowed_tariff_names = (
        "NetzDynamisch",
        "NetzDynamischAVAG",
        "NetzDynamischELAG",
    )
    default_tariff_name = "NetzDynamisch"
    supported_tariff_types = (
        "electricity",
        "grid_usage",
        "grid",
        "integrated",
    )
