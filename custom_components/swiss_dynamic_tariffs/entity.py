"""Base entity for Swiss Dynamic Tariffs."""

from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import ATTRIBUTION, DOMAIN, NAME, VERSION
from .coordinator import SwissDynamicTariffsCoordinator


class SwissDynamicTariffsEntity(CoordinatorEntity[SwissDynamicTariffsCoordinator]):
    """Base entity for Swiss Dynamic Tariffs."""

    def __init__(
        self,
        coordinator: SwissDynamicTariffsCoordinator,
        config_entry,
    ) -> None:
        """Initialize the entity."""
        super().__init__(coordinator)
        # Home Assistant's own `Entity.config_entry` is a read-only property
        # populated automatically once the entity is added to hass, so we
        # keep the config entry we were constructed with under our own name
        # instead of assigning to that property (which raises AttributeError
        # on current Home Assistant versions).
        self._entry = config_entry

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._entry.entry_id)},
            name=NAME,
            manufacturer=NAME,
            model=VERSION,
        )

    @property
    def extra_state_attributes(self) -> dict[str, str]:
        """Return common state attributes."""
        return {
            "attribution": ATTRIBUTION,
            "integration": DOMAIN,
        }
