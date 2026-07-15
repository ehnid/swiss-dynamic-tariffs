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

from .const import CURRENCY_PER_KWH, DOMAIN
from .coordinator import SwissDynamicTariffsCoordinator
from .entity import SwissDynamicTariffsEntity

TariffType = Literal[
    "electricity",
    "feed_in",
    "grid",
    "integrated",
]


@dataclass(frozen=True, kw_only=True)
class TariffSensorDescription(SensorEntityDescription):
    """Description of a tariff sensor."""

    tariff_type: TariffType
    suggested_display_precision: int = 4


ENTITY_DESCRIPTIONS: tuple[TariffSensorDescription, ...] = (
    TariffSensorDescription(
        key="electricity",
        name="Electricity",
        tariff_type="electricity",
        native_unit_of_measurement=CURRENCY_PER_KWH,
        icon="mdi:flash",
        suggested_display_precision=4,
    ),
    TariffSensorDescription(
        key="feed_in",
        name="Feed-in",
        tariff_type="feed_in",
        native_unit_of_measurement=CURRENCY_PER_KWH,
        icon="mdi:transmission-tower-export",
        suggested_display_precision=4,
    ),
    TariffSensorDescription(
        key="grid",
        name="Grid",
        tariff_type="grid",
        native_unit_of_measurement=CURRENCY_PER_KWH,
        icon="mdi:transmission-tower",
        suggested_display_precision=4,
    ),
    TariffSensorDescription(
        key="integrated",
        name="Integrated",
        tariff_type="integrated",
        native_unit_of_measurement=CURRENCY_PER_KWH,
        icon="mdi:sigma",
        suggested_display_precision=4,
    ),
)


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
    """Sensor showing current tariff value."""

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

        self._attr_unique_id = (
            f"{DOMAIN}_{self.config_entry.entry_id}_{description.key}"
        )

        self._attr_has_entity_name = True

    # @property
    # def extra_state_attributes(self):
    #     """Return tariff metadata."""

    #     if not isinstance(self.coordinator.data, list):
    #         return None

    #     if not self.coordinator.data:
    #         return None

    #     tariff = self.coordinator.data[0]

    #     return getattr(
    #         tariff,
    #         self._tariff_type,
    #         None,
    #     )

    @property
    def native_value(self) -> float | None:
        """Return the current tariff."""

        tariff = self.coordinator.current_period

        if tariff is None:
            return None

        return getattr(
            tariff,
            self.entity_description.tariff_type,
            None,
        )

    @property
    def extra_state_attributes(self) -> dict[str, object] | None:
        """Return additional tariff information."""

        tariff = self.coordinator.current_period

        if tariff is None:
            return None

        return {
            "start": tariff.start,
            "end": tariff.end,
        }
