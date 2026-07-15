from datetime import datetime
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from custom_components.swiss_dynamic_tariffs.const import (
    CURRENCY_PER_KWH,
)

from custom_components.swiss_dynamic_tariffs.sensor import (
    SwissDynamicTariffSensor,
    TariffSensorDescription,
)


class FakeCoordinator:
    current_period = SimpleNamespace(
        electricity=0.25,
        feed_in=0.10,
        grid=0.05,
        integrated=0.30,
        start=datetime.fromisoformat("2026-01-01T00:00:00+00:00"),
        end=datetime.fromisoformat("2026-01-01T01:00:00+00:00"),
    )

    data = [current_period]

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
    coordinator.current_period = None
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


def test_sensor_attributes():
    """Test sensor attributes."""

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

    attrs = sensor.extra_state_attributes

    assert attrs is not None
    assert "start" in attrs
    assert "end" in attrs
    assert sensor.entity_description.native_unit_of_measurement == CURRENCY_PER_KWH
    assert sensor.entity_description.suggested_display_precision == 4
