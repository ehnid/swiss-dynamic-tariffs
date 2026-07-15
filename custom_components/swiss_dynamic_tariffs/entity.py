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
        self.config_entry = config_entry

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, self.config_entry.entry_id)},
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
