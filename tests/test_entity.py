"""Test entity base class."""

from types import SimpleNamespace

from custom_components.swiss_dynamic_tariffs.entity import (
    SwissDynamicTariffsEntity,
)


class FakeCoordinator:
    """Fake coordinator for entity tests."""

    data = []
    last_update_success = True


def test_entity_device_info():
    """Test device information."""

    entry = SimpleNamespace(
        entry_id="test",
    )

    entity = SwissDynamicTariffsEntity(
        FakeCoordinator(),
        entry,
    )

    device_info = entity.device_info

    assert device_info["identifiers"] == {
        (
            "swiss_dynamic_tariffs",
            "test",
        )
    }

    assert "name" in device_info
    assert "model" in device_info
    assert "manufacturer" in device_info


def test_entity_extra_attributes():
    """Test extra attributes."""

    entry = SimpleNamespace(
        entry_id="test",
    )

    entity = SwissDynamicTariffsEntity(
        FakeCoordinator(),
        entry,
    )

    attributes = entity.extra_state_attributes

    assert "integration" in attributes
    assert attributes["integration"] == "swiss_dynamic_tariffs"
