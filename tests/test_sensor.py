from datetime import datetime
import json
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

import pytest
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import UnitOfTime

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
    FORECAST_DESCRIPTION,
    SwissDynamicTariffForecastSensor,
    SwissDynamicTariffSensor,
    TariffSensorDescription,
    async_setup_entry,
)


class FakeCoordinator:
    provider = SimpleNamespace(
        name="BKW",
        attribution="Data provided by BKW",
        supported_tariff_types=("feed_in",),
    )

    current_period = SimpleNamespace(
        electricity=0.25,
        feed_in=0.10,
        grid_usage=0.04,
        grid=0.05,
        integrated=0.30,
        start=datetime.fromisoformat("2026-01-01T00:00:00+00:00"),
        end=datetime.fromisoformat("2026-01-01T01:00:00+00:00"),
    )

    next_period = SimpleNamespace(
        electricity=0.40,
        feed_in=0.12,
        grid_usage=0.04,
        grid=0.05,
        integrated=0.45,
        start=datetime.fromisoformat("2026-01-01T01:00:00+00:00"),
        end=datetime.fromisoformat("2026-01-01T02:00:00+00:00"),
    )

    cheapest = SimpleNamespace(
        electricity=0.05,
        feed_in=0.10,
        grid_usage=0.04,
        grid=0.05,
        integrated=0.10,
        start=datetime.fromisoformat("2026-01-01T03:00:00+00:00"),
        end=datetime.fromisoformat("2026-01-01T04:00:00+00:00"),
    )

    most_expensive = SimpleNamespace(
        electricity=0.60,
        feed_in=0.10,
        grid_usage=0.04,
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

    def future_periods(self, tariff_type=None):
        """Return all fake future periods, ignoring the tariff type."""
        return [self.next_period, self.cheapest, self.most_expensive]


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


def test_forecast_sensor_exposes_all_future_quarter_hours():
    """Test the dedicated forecast sensor state and price list."""

    entry = Mock()
    entry.entry_id = "test"
    coordinator = FakeCoordinator()
    coordinator.provider = SimpleNamespace(
        name="CKW",
        attribution="Data provided by CKW",
        supported_tariff_types=(
            "electricity",
            "feed_in",
            "grid_usage",
            "grid",
            "integrated",
        ),
    )
    sensor = SwissDynamicTariffForecastSensor(coordinator, entry)

    assert sensor.native_value == 3
    assert sensor.entity_description.device_class == SensorDeviceClass.DURATION
    assert sensor.entity_description.native_unit_of_measurement == UnitOfTime.HOURS
    assert sensor.extra_state_attributes == {
        "available_from": FakeCoordinator.next_period.start,
        "available_until": FakeCoordinator.most_expensive.end,
        "period_count": 3,
        "prices": [
            {
                "start": FakeCoordinator.next_period.start.isoformat(),
                "end": FakeCoordinator.next_period.end.isoformat(),
                "electricity": 0.40,
                "feed_in": 0.12,
                "grid_usage": 0.04,
                "grid": 0.05,
                "integrated": 0.45,
            },
            {
                "start": FakeCoordinator.cheapest.start.isoformat(),
                "end": FakeCoordinator.cheapest.end.isoformat(),
                "electricity": 0.05,
                "feed_in": 0.10,
                "grid_usage": 0.04,
                "grid": 0.05,
                "integrated": 0.10,
            },
            {
                "start": FakeCoordinator.most_expensive.start.isoformat(),
                "end": FakeCoordinator.most_expensive.end.isoformat(),
                "electricity": 0.60,
                "feed_in": 0.10,
                "grid_usage": 0.04,
                "grid": 0.05,
                "integrated": 0.65,
            },
        ],
    }


def test_forecast_sensor_without_future_data():
    """Test the forecast sensor when no future periods are available."""

    coordinator = FakeCoordinator()
    coordinator.future_periods = Mock(return_value=[])
    entry = Mock(entry_id="test")
    sensor = SwissDynamicTariffForecastSensor(coordinator, entry)

    assert sensor.native_value is None
    assert sensor.extra_state_attributes is None


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

    assert tariff_types == {
        "electricity",
        "feed_in",
        "grid_usage",
        "grid",
        "integrated",
    }
    assert kinds == {
        SENSOR_CURRENT_PRICE,
        SENSOR_NEXT_PRICE,
        SENSOR_TODAY_MIN,
        SENSOR_TODAY_MAX,
        SENSOR_AVERAGE_PRICE,
    }
    assert len(ENTITY_DESCRIPTIONS) == len(tariff_types) * len(kinds)
    assert all(
        description.translation_key == description.key
        for description in ENTITY_DESCRIPTIONS
    )

    current_descriptions = [
        description
        for description in ENTITY_DESCRIPTIONS
        if description.kind == SENSOR_CURRENT_PRICE
    ]
    assert all(
        description.state_class == SensorStateClass.MEASUREMENT
        for description in current_descriptions
    )


@pytest.mark.parametrize("language", ["strings", "de", "en", "fr", "it"])
def test_all_sensor_names_are_translated(language):
    """Test that every generated sensor has a name in every supported language."""

    integration_path = (
        Path(__file__).parents[1] / "custom_components" / "swiss_dynamic_tariffs"
    )
    translation_path = (
        integration_path / "strings.json"
        if language == "strings"
        else integration_path / "translations" / f"{language}.json"
    )
    translations = json.loads(translation_path.read_text(encoding="utf-8"))

    expected_translation_keys = {
        description.translation_key for description in ENTITY_DESCRIPTIONS
    }
    expected_translation_keys.add(FORECAST_DESCRIPTION.translation_key)

    assert set(translations["entity"]["sensor"]) == expected_translation_keys


@pytest.mark.asyncio
async def test_setup_only_adds_tariff_types_supported_by_provider(hass):
    """Test that BKW does not create unavailable consumption/grid sensors."""

    entry = SimpleNamespace(entry_id="test")
    hass.data.setdefault("swiss_dynamic_tariffs", {})[entry.entry_id] = (
        FakeCoordinator()
    )
    async_add_entities = Mock()

    await async_setup_entry(hass, entry, async_add_entities)

    entities = async_add_entities.call_args.args[0]
    assert len(entities) == 6
    assert all(
        entity.entity_description.tariff_type == "feed_in" for entity in entities[:-1]
    )
    assert isinstance(entities[-1], SwissDynamicTariffForecastSensor)
