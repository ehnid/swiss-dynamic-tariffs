from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from custom_components.swiss_dynamic_tariffs.sensor import (
    SwissDynamicTariffSensor,
    TariffSensorDescription,
)


class FakeCoordinator:
    data = [
        SimpleNamespace(
            electricity=0.25,
        )
    ]

    last_update_success = True

    config_entry = SimpleNamespace(
        entry_id="test",
    )


@pytest.mark.asyncio
async def test_sensor_value():
    """Test sensor returns tariff value."""

    entry = Mock()
    entry.entry_id = "test"

    description = TariffSensorDescription(
        key="electricity",
        name="Electricity",
        tariff_type="electricity",
        native_unit_of_measurement="CHF/kWh",
    )

    sensor = SwissDynamicTariffSensor(
        FakeCoordinator(),
        entry,
        description,
    )

    assert sensor.native_value == 0.25


def test_sensor_without_data():
    coordinator = FakeCoordinator()
    coordinator.data = []

    entry = Mock()
    entry.entry_id = "test"

    description = TariffSensorDescription(
        key="electricity",
        name="Electricity",
        tariff_type="electricity",
        native_unit_of_measurement="CHF/kWh",
    )

    sensor = SwissDynamicTariffSensor(
        coordinator,
        entry,
        description,
    )

    assert sensor.native_value is None
