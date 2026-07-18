"""Sensor platform for Swiss Dynamic Tariffs."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
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
from .models import TariffPeriod

TariffType = Literal[
    "electricity",
    "feed_in",
    "grid",
    "integrated",
]

SensorKind = Literal[
    "current_price",
    "next_price",
    "today_min",
    "today_max",
    "average_price",
]

# Tariff components a provider can report. "electricity" is what the
# customer pays for consumption, "feed_in" is the compensation for
# feeding electricity back into the grid (Rueckspeisung), "grid" is the
# grid-usage fee (Netznutzung) and "integrated" is a provider-specific
# all-in price that already combines multiple components.
TARIFF_TYPES: tuple[tuple[TariffType, str, str], ...] = (
    ("electricity", "Electricity", "mdi:flash"),
    ("feed_in", "Feed-in", "mdi:transmission-tower-export"),
    ("grid", "Grid", "mdi:transmission-tower"),
    ("integrated", "Integrated", "mdi:sigma"),
)

# One sensor per tariff component is generated for each of these kinds.
SENSOR_KINDS: tuple[tuple[SensorKind, str], ...] = (
    (SENSOR_CURRENT_PRICE, "Current"),
    (SENSOR_NEXT_PRICE, "Next"),
    (SENSOR_TODAY_MIN, "Cheapest Quarter Hour"),
    (SENSOR_TODAY_MAX, "Most Expensive Quarter Hour"),
    (SENSOR_AVERAGE_PRICE, "Average"),
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

    for tariff_type, tariff_name, icon in TARIFF_TYPES:
        for kind, kind_name in SENSOR_KINDS:
            descriptions.append(
                TariffSensorDescription(
                    key=f"{tariff_type}_{kind}",
                    name=f"{tariff_name} {kind_name}",
                    tariff_type=tariff_type,
                    kind=kind,
                    native_unit_of_measurement=CURRENCY_PER_KWH,
                    icon=icon,
                )
            )

    return tuple(descriptions)


ENTITY_DESCRIPTIONS: tuple[TariffSensorDescription, ...] = _build_entity_descriptions()


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up tariff sensors."""

    coordinator: SwissDynamicTariffsCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities = [
        SwissDynamicTariffSensor(
            coordinator,
            entry,
            description,
        )
        for description in ENTITY_DESCRIPTIONS
    ]

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
