"""Groupe E VARIO dynamic tariffs provider."""

from __future__ import annotations

from ..const import GROUPE_E_API_URL
from .standard import StandardTariffProvider


class GroupeEProvider(StandardTariffProvider):
    """Groupe E provider for the VARIO tariff."""

    name = "Groupe E"
    attribution = "Data provided by Groupe E"
    api_url = GROUPE_E_API_URL
    allowed_tariff_names = ("VARIO",)
    default_tariff_name = "VARIO"
    include_tariff_name = False
    supported_tariff_types = ("grid", "integrated")
