"""Sensor platform for Swiss Dynamic Tariffs."""

from __future__ import annotations

from .const import DOMAIN
from .coordinator import SwissDynamicTariffsCoordinator

from .entity import SwissDynamicTariffsEntity

from typing import Literal

from dataclasses import dataclass

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
)

TariffType = Literal[
    "electricity",
    "feed_in",
    "grid",
    "integrated",
]


@dataclass(frozen=True, kw_only=True)
class TariffSensorDescription(SensorEntityDescription):
    """Description of a tariff sensor."""

    tariff_type: str


SENSORS: tuple[TariffSensorDescription, ...] = (
    TariffSensorDescription(
        key="electricity",
        name="Electricity",
        tariff_type="electricity",
        native_unit_of_measurement="CHF/kWh",
        icon="mdi:flash",
    ),
    TariffSensorDescription(
        key="feed_in",
        name="Feed-in",
        tariff_type="feed_in",
        native_unit_of_measurement="CHF/kWh",
        icon="mdi:transmission-tower-export",
    ),
    TariffSensorDescription(
        key="grid",
        name="Grid",
        tariff_type="grid",
        native_unit_of_measurement="CHF/kWh",
        icon="mdi:transmission-tower",
    ),
    TariffSensorDescription(
        key="integrated",
        name="Integrated",
        tariff_type="integrated",
        native_unit_of_measurement="CHF/kWh",
        icon="mdi:sigma",
    ),
)


async def async_setup_entry(
    hass,
    entry,
    async_add_entities,
) -> None:
    """Set up tariff sensors."""

    coordinator: SwissDynamicTariffsCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        SwissDynamicTariffSensor(
            coordinator,
            entry,
            description,
        )
        for description in SENSORS
    )


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

        self._attr_native_unit_of_measurement = "CHF/kWh"

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
    def native_value(self):
        """Return current tariff."""

        if not self.coordinator.data:
            return None

        tariff = self.coordinator.data[0]

        return getattr(
            tariff,
            self.entity_description.tariff_type,
            None,
        )
