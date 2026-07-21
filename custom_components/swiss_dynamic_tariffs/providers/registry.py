"""Provider and tariff option registry."""

from __future__ import annotations

from dataclasses import dataclass

from aiohttp import ClientSession

from ..const import (
    PROVIDER_BKW,
    PROVIDER_CKW,
    PROVIDER_EKZ,
    PROVIDER_GROUPE_E,
    PROVIDER_PRIMEO,
)
from .base import TariffProvider
from .bkw import BKWProvider
from .ckw import CKWProvider
from .ekz import EKZProvider
from .groupe_e import GroupeEProvider
from .primeo import PrimeoProvider


@dataclass(frozen=True, slots=True)
class TariffOption:
    """A selectable provider/tariff combination."""

    key: str
    provider: str
    tariff_name: str
    title: str


PROVIDERS: dict[str, type[TariffProvider]] = {
    PROVIDER_BKW: BKWProvider,
    PROVIDER_CKW: CKWProvider,
    PROVIDER_EKZ: EKZProvider,
    PROVIDER_GROUPE_E: GroupeEProvider,
    PROVIDER_PRIMEO: PrimeoProvider,
}

TARIFF_OPTIONS: dict[str, TariffOption] = {
    "bkw": TariffOption(
        "bkw",
        PROVIDER_BKW,
        "feed_in",
        "BKW – dynamische Einspeisevergütung",
    ),
    "ckw": TariffOption("ckw", PROVIDER_CKW, "home_dynamic", "CKW – Home Dynamic"),
    "ckw_business": TariffOption(
        "ckw_business",
        PROVIDER_CKW,
        "business_dynamic",
        "CKW – Business Dynamic",
    ),
    "groupe_e": TariffOption(
        "groupe_e", PROVIDER_GROUPE_E, "VARIO", "Groupe E – Vario"
    ),
    "primeo": TariffOption(
        "primeo",
        PROVIDER_PRIMEO,
        "NetzDynamisch",
        "Primeo Energie – Netz dynamisch",
    ),
    "primeo_avag": TariffOption(
        "primeo_avag",
        PROVIDER_PRIMEO,
        "NetzDynamischAVAG",
        "Primeo Energie – Netz dynamisch (AVAG)",
    ),
    "primeo_elag": TariffOption(
        "primeo_elag",
        PROVIDER_PRIMEO,
        "NetzDynamischELAG",
        "Primeo Energie – Netz dynamisch (ELAG)",
    ),
    "ekz": TariffOption(
        "ekz",
        PROVIDER_EKZ,
        "integrated_400D",
        "EKZ – Energie Dynamisch + Netz 400D",
    ),
    "ekz_einsiedeln": TariffOption(
        "ekz_einsiedeln",
        PROVIDER_EKZ,
        "integrated_400D_E",
        "EKZ Einsiedeln – Energie Dynamisch + Netz 400D",
    ),
}


def get_provider(name: str) -> type[TariffProvider]:
    """Return provider class by name."""

    try:
        return PROVIDERS[name]
    except KeyError as err:
        raise ValueError(f"Unknown tariff provider: {name}") from err


def get_tariff_option(key: str) -> TariffOption:
    """Return a selectable tariff option by key."""

    try:
        return TARIFF_OPTIONS[key]
    except KeyError as err:
        raise ValueError(f"Unknown tariff option: {key}") from err


def create_provider(
    name: str,
    session: ClientSession,
    tariff_name: str | None = None,
) -> TariffProvider:
    """Create a configured provider instance."""

    return get_provider(name)(session, tariff_name)
