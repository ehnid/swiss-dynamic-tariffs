"""Constants for Swiss Dynamic Tariffs."""

from typing import Final

DOMAIN: Final = "swiss_dynamic_tariffs"

NAME: Final = "Swiss Dynamic Tariffs"

VERSION: Final = "0.1.0"

DEFAULT_SCAN_INTERVAL: Final = 900
REQUEST_TIMEOUT: Final = 30

PLATFORMS: list[str] = ["sensor"]

CURRENCY_PER_KWH = "CHF/kWh"


# Configuration keys

CONF_PROVIDER: Final = "provider"
CONF_API_URL: Final = "api_url"
CONF_API_KEY: Final = "api_key"


# Supported providers

PROVIDER_BKW: Final = "bkw"
PROVIDER_CKW: Final = "ckw"
BKW_API_URL: Final = "https://api.bkw.ch/api/dyntariffs/v1/tariffs/"
CKW_API_URL: Final = (
    "https://e-ckw-public-data.de-c1.eu1.cloudhub.io/api/v1/"
    "netzinformationen/energie/dynamische-preise"
)

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
