"""Constants for Swiss Dynamic Tariffs."""

import json
from pathlib import Path
from typing import Final

DOMAIN: Final = "swiss_dynamic_tariffs"

NAME: Final = "Swiss Dynamic Tariffs"

VERSION: Final = json.loads(
    (Path(__file__).parent / "manifest.json").read_text(encoding="utf-8")
)["version"]

DEFAULT_SCAN_INTERVAL: Final = 900
REQUEST_TIMEOUT: Final = 30

PLATFORMS: list[str] = ["sensor"]

CURRENCY_PER_KWH = "CHF/kWh"
FRONTEND_URL: Final = f"/{DOMAIN}/swiss-dynamic-tariffs.js"
PANEL_COMPONENT_NAME: Final = f"swiss-dynamic-tariffs-panel-{VERSION.replace('.', '-')}"
DASHBOARD_URL_PATH: Final = "swiss-dynamic-tariffs"
DASHBOARD_STRATEGY_TYPE: Final = "custom:swiss-dynamic-tariffs"
DASHBOARD_STORAGE_KEY: Final = f"{DOMAIN}.dashboard"
DASHBOARD_STORAGE_VERSION: Final = 1


# Configuration keys

CONF_PROVIDER: Final = "provider"
CONF_TARIFF: Final = "tariff"
CONF_API_URL: Final = "api_url"
CONF_API_KEY: Final = "api_key"


# Supported providers

PROVIDER_BKW: Final = "bkw"
PROVIDER_CKW: Final = "ckw"
PROVIDER_EKZ: Final = "ekz"
PROVIDER_GROUPE_E: Final = "groupe_e"
PROVIDER_PRIMEO: Final = "primeo"
BKW_API_URL: Final = "https://api.bkw.ch/api/dyntariffs/v1/tariffs/"
CKW_API_URL: Final = (
    "https://e-ckw-public-data.de-c1.eu1.cloudhub.io/api/v1/"
    "netzinformationen/energie/dynamische-preise"
)
EKZ_API_URL: Final = "https://api.tariffs.ekz.ch/v1/tariffs"
GROUPE_E_API_URL: Final = "https://api.tariffs.groupe-e.ch/v2/tariffs/"
PRIMEO_API_URL: Final = "https://tarife.primeo-energie.ch/api/v1/tariffs"

# Sensor types

SENSOR_CURRENT_PRICE: Final = "current_price"
SENSOR_NEXT_PRICE: Final = "next_price"
SENSOR_TODAY_MIN: Final = "today_min"
SENSOR_TODAY_MAX: Final = "today_max"
SENSOR_AVERAGE_PRICE: Final = "average_price"


STARTUP_MESSAGE: Final = f"""
{NAME}
Version: {VERSION}
"""
