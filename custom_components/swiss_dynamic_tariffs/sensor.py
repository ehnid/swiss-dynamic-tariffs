"""Sensor platform for Swiss Dynamic Tariffs."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
# from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import SwissDynamicTariffsCoordinator

from .entity import SwissDynamicTariffsEntity

from typing import Literal

TariffType = Literal[
    "electricity",
    "feed_in",
    "grid",
    "integrated",
]


async def async_setup_entry(
    hass,
    entry,
    async_add_entities,
) -> None:
    """Set up tariff sensors."""

    coordinator: SwissDynamicTariffsCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [
            SwissDynamicTariffSensor(
                coordinator,
                "electricity",
            ),
            SwissDynamicTariffSensor(
                coordinator,
                "feed_in",
            ),
            SwissDynamicTariffSensor(
                coordinator,
                "grid",
            ),
            SwissDynamicTariffSensor(
                coordinator,
                "integrated",
            ),
        ]
    )


class SwissDynamicTariffSensor(
    SwissDynamicTariffsEntity,
    SensorEntity,
):
    """Sensor showing current tariff value."""

    def __init__(
        self,
        coordinator: SwissDynamicTariffsCoordinator,
        tariff_type: TariffType,
    ) -> None:
        """Initialize sensor."""

        super().__init__(coordinator)

        self._tariff_type = tariff_type

        self._attr_unique_id = (
            f"{DOMAIN}_{coordinator.config_entry.entry_id}_{tariff_type}"
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

        print("DATA:", self.coordinator.data)
        print("TYPE:", type(self.coordinator.data))

        if not self.coordinator.data:
            return None

        tariff = self.coordinator.data[0]

        print("TARIFF:", tariff)

        return getattr(
            tariff,
            self._tariff_type,
            None,
        )
