from types import SimpleNamespace

import pytest

from custom_components.swiss_dynamic_tariffs.sensor import (
    SwissDynamicTariffSensor,
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

    sensor = SwissDynamicTariffSensor(
        FakeCoordinator(),
        "electricity",
    )

    assert sensor.native_value == 0.25


def test_sensor_without_data():
    coordinator = FakeCoordinator()
    coordinator.data = []

    sensor = SwissDynamicTariffSensor(
        coordinator,
        "electricity",
    )

    assert sensor.native_value is None
