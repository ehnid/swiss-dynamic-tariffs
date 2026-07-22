"""Sensor platform for Swiss Dynamic Tariffs."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTime
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    CURRENCY_PER_KWH,
    DOMAIN,
    SENSOR_AVERAGE_PRICE,
    SENSOR_CURRENT_PRICE,
    SENSOR_NEXT_PRICE,
    SENSOR_TODAY_MAX,
    SENSOR_TODAY_MIN,
)
from .coordinator import SwissDynamicTariffsCoordinator
from .entity import SwissDynamicTariffsEntity
from .models import TariffPeriod, TariffType

SensorKind = Literal[
    "current_price",
    "next_price",
    "today_min",
    "today_max",
    "average_price",
]

# Tariff components a provider can report. User-facing names are supplied
# through Home Assistant's entity translation system.
TARIFF_TYPES: tuple[tuple[TariffType, str], ...] = (
    ("electricity", "mdi:flash"),
    ("feed_in", "mdi:transmission-tower-export"),
    ("grid_usage", "mdi:transmission-tower-import"),
    ("grid", "mdi:transmission-tower"),
    ("integrated", "mdi:sigma"),
)

# One sensor per tariff component is generated for each of these kinds.
SENSOR_KINDS: tuple[SensorKind, ...] = (
    SENSOR_CURRENT_PRICE,
    SENSOR_NEXT_PRICE,
    SENSOR_TODAY_MIN,
    SENSOR_TODAY_MAX,
    SENSOR_AVERAGE_PRICE,
)


@dataclass(frozen=True, kw_only=True)
class TariffSensorDescription(SensorEntityDescription):
    """Description of a tariff sensor."""

    tariff_type: TariffType
    kind: SensorKind = SENSOR_CURRENT_PRICE
    suggested_display_precision: int = 4


def _build_entity_descriptions() -> tuple[TariffSensorDescription, ...]:
    """Build one sensor description per tariff component and sensor kind."""

    descriptions: list[TariffSensorDescription] = []

    for tariff_type, icon in TARIFF_TYPES:
        for kind in SENSOR_KINDS:
            key = f"{tariff_type}_{kind}"
            descriptions.append(
                TariffSensorDescription(
                    key=key,
                    translation_key=key,
                    tariff_type=tariff_type,
                    kind=kind,
                    native_unit_of_measurement=CURRENCY_PER_KWH,
                    state_class=(
                        SensorStateClass.MEASUREMENT
                        if kind == SENSOR_CURRENT_PRICE
                        else None
                    ),
                    icon=icon,
                )
            )

    return tuple(descriptions)


ENTITY_DESCRIPTIONS: tuple[TariffSensorDescription, ...] = _build_entity_descriptions()

FORECAST_DESCRIPTION = SensorEntityDescription(
    key="forecast",
    translation_key="forecast",
    device_class=SensorDeviceClass.DURATION,
    native_unit_of_measurement=UnitOfTime.HOURS,
    suggested_display_precision=2,
    icon="mdi:chart-timeline-variant",
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up tariff sensors."""

    coordinator: SwissDynamicTariffsCoordinator = hass.data[DOMAIN][entry.entry_id]

    supported_types = coordinator.provider.supported_tariff_types
    entities = [
        SwissDynamicTariffSensor(
            coordinator,
            entry,
            description,
        )
        for description in ENTITY_DESCRIPTIONS
        if description.tariff_type in supported_types
    ]
    entities.append(
        SwissDynamicTariffForecastSensor(
            coordinator,
            entry,
        )
    )

    async_add_entities(entities)


class SwissDynamicTariffSensor(
    SwissDynamicTariffsEntity,
    SensorEntity,
):
    """Sensor for a tariff value (current, next, cheapest, most expensive, average)."""

    def __init__(
        self,
        coordinator: SwissDynamicTariffsCoordinator,
        config_entry,
        description: TariffSensorDescription,
    ) -> None:
        """Initialize sensor."""

        super().__init__(
            coordinator,
            config_entry,
        )

        self.entity_description = description

        self._attr_unique_id = f"{DOMAIN}_{self._entry.entry_id}_{description.key}"

        self._attr_has_entity_name = True

    def _reference_period(self) -> TariffPeriod | None:
        """Return the tariff period this sensor's value is derived from.

        Not applicable for the "average" kind, which is computed across
        several periods rather than read from a single one.
        """

        kind = self.entity_description.kind

        if kind == SENSOR_CURRENT_PRICE:
            return self.coordinator.current_period

        if kind == SENSOR_NEXT_PRICE:
            return self.coordinator.next_period

        if kind == SENSOR_TODAY_MIN:
            return self.coordinator.cheapest_period(self.entity_description.tariff_type)

        if kind == SENSOR_TODAY_MAX:
            return self.coordinator.most_expensive_period(
                self.entity_description.tariff_type
            )

        return None

    @property
    def native_value(self) -> float | None:
        """Return the tariff value for this sensor."""

        if self.entity_description.kind == SENSOR_AVERAGE_PRICE:
            return self.coordinator.average_price(self.entity_description.tariff_type)

        period = self._reference_period()

        if period is None:
            return None

        return getattr(
            period,
            self.entity_description.tariff_type,
            None,
        )

    @property
    def extra_state_attributes(self) -> dict[str, object] | None:
        """Return the start/end of the quarter hour this value refers to."""

        period = self._reference_period()

        if period is None:
            return None

        return {
            "start": period.start,
            "end": period.end,
        }


class SwissDynamicTariffForecastSensor(
    SwissDynamicTariffsEntity,
    SensorEntity,
):
    """Sensor exposing all published future quarter-hour prices."""

    entity_description = FORECAST_DESCRIPTION
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: SwissDynamicTariffsCoordinator,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the tariff forecast sensor."""

        super().__init__(coordinator, config_entry)
        self._attr_unique_id = f"{DOMAIN}_{self._entry.entry_id}_forecast"

    @property
    def native_value(self) -> float | None:
        """Return the duration covered by future prices in hours."""

        periods = self.coordinator.future_periods()

        if not periods:
            return None

        return (
            sum((period.end - period.start).total_seconds() for period in periods)
            / 3600
        )

    @property
    def extra_state_attributes(self) -> dict[str, object] | None:
        """Return every future period and all provider-supported prices."""

        periods = self.coordinator.future_periods()

        if not periods:
            return None

        tariff_types = self.coordinator.provider.supported_tariff_types
        prices: list[dict[str, object]] = []

        for period in periods:
            price: dict[str, object] = {
                "start": period.start.isoformat(),
                "end": period.end.isoformat(),
            }
            price.update(
                {
                    tariff_type: value
                    for tariff_type in tariff_types
                    if (value := getattr(period, tariff_type, None)) is not None
                }
            )
            prices.append(price)

        return {
            "available_from": periods[0].start,
            "available_until": periods[-1].end,
            "period_count": len(periods),
            "prices": prices,
        }
