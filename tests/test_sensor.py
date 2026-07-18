from datetime import datetime
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from custom_components.swiss_dynamic_tariffs.const import (
    CURRENCY_PER_KWH,
    SENSOR_AVERAGE_PRICE,
    SENSOR_CURRENT_PRICE,
    SENSOR_NEXT_PRICE,
    SENSOR_TODAY_MAX,
    SENSOR_TODAY_MIN,
)
from custom_components.swiss_dynamic_tariffs.sensor import (
    ENTITY_DESCRIPTIONS,
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

    next_period = SimpleNamespace(
        electricity=0.40,
        feed_in=0.12,
        grid=0.05,
        integrated=0.45,
        start=datetime.fromisoformat("2026-01-01T01:00:00+00:00"),
        end=datetime.fromisoformat("2026-01-01T02:00:00+00:00"),
    )

    cheapest = SimpleNamespace(
        electricity=0.05,
        feed_in=0.10,
        grid=0.05,
        integrated=0.10,
        start=datetime.fromisoformat("2026-01-01T03:00:00+00:00"),
        end=datetime.fromisoformat("2026-01-01T04:00:00+00:00"),
    )

    most_expensive = SimpleNamespace(
        electricity=0.60,
        feed_in=0.10,
        grid=0.05,
        integrated=0.65,
        start=datetime.fromisoformat("2026-01-01T05:00:00+00:00"),
        end=datetime.fromisoformat("2026-01-01T06:00:00+00:00"),
    )

    data = [current_period]

    last_update_success = True

    config_entry = SimpleNamespace(
        entry_id="test",
    )

    def cheapest_period(self, tariff_type):
        """Return the fake cheapest period, ignoring the tariff type."""
        return self.cheapest

    def most_expensive_period(self, tariff_type):
        """Return the fake most expensive period, ignoring the tariff type."""
        return self.most_expensive

    def average_price(self, tariff_type):
        """Return a fake average price, ignoring the tariff type."""
        return 0.20


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


def test_sensor_next_price():
    """Test the 'next' sensor reads from coordinator.next_period."""

    entry = Mock()
    entry.entry_id = "test"

    description = TariffSensorDescription(
        key="electricity_next_price",
        name="Electricity Next",
        tariff_type="electricity",
        kind=SENSOR_NEXT_PRICE,
        native_unit_of_measurement="CHF/kWh",
    )

    sensor = SwissDynamicTariffSensor(
        FakeCoordinator(),
        entry,
        description,
    )

    assert sensor.native_value == 0.40
    assert sensor.extra_state_attributes["start"] == FakeCoordinator.next_period.start


def test_sensor_cheapest_quarter_hour():
    """Test the 'today_min' sensor reads from coordinator.cheapest_period()."""

    entry = Mock()
    entry.entry_id = "test"

    description = TariffSensorDescription(
        key="electricity_today_min",
        name="Electricity Cheapest Quarter Hour",
        tariff_type="electricity",
        kind=SENSOR_TODAY_MIN,
        native_unit_of_measurement="CHF/kWh",
    )

    sensor = SwissDynamicTariffSensor(
        FakeCoordinator(),
        entry,
        description,
    )

    assert sensor.native_value == 0.05
    assert sensor.extra_state_attributes["start"] == FakeCoordinator.cheapest.start


def test_sensor_most_expensive_quarter_hour():
    """Test the 'today_max' sensor reads from coordinator.most_expensive_period()."""

    entry = Mock()
    entry.entry_id = "test"

    description = TariffSensorDescription(
        key="electricity_today_max",
        name="Electricity Most Expensive Quarter Hour",
        tariff_type="electricity",
        kind=SENSOR_TODAY_MAX,
        native_unit_of_measurement="CHF/kWh",
    )

    sensor = SwissDynamicTariffSensor(
        FakeCoordinator(),
        entry,
        description,
    )

    assert sensor.native_value == 0.60
    assert (
        sensor.extra_state_attributes["start"] == FakeCoordinator.most_expensive.start
    )


def test_sensor_average_price():
    """Test the 'average' sensor reads from coordinator.average_price() directly."""

    entry = Mock()
    entry.entry_id = "test"

    description = TariffSensorDescription(
        key="electricity_average_price",
        name="Electricity Average",
        tariff_type="electricity",
        kind=SENSOR_AVERAGE_PRICE,
        native_unit_of_measurement="CHF/kWh",
    )

    sensor = SwissDynamicTariffSensor(
        FakeCoordinator(),
        entry,
        description,
    )

    assert sensor.native_value == 0.20
    # An average has no single start/end quarter hour to report.
    assert sensor.extra_state_attributes is None


def test_entity_descriptions_cover_all_tariff_types_and_kinds():
    """Test that one sensor is generated per tariff component and sensor kind."""

    tariff_types = {description.tariff_type for description in ENTITY_DESCRIPTIONS}
    kinds = {description.kind for description in ENTITY_DESCRIPTIONS}

    assert tariff_types == {"electricity", "feed_in", "grid", "integrated"}
    assert kinds == {
        SENSOR_CURRENT_PRICE,
        SENSOR_NEXT_PRICE,
        SENSOR_TODAY_MIN,
        SENSOR_TODAY_MAX,
        SENSOR_AVERAGE_PRICE,
    }
    assert len(ENTITY_DESCRIPTIONS) == len(tariff_types) * len(kinds)
