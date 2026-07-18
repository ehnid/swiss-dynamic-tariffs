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


class _ReadOnlyConfigEntryBase:
    """Stand-in mimicking Home Assistant's Entity.config_entry.

    On current Home Assistant versions, Entity.config_entry is a read-only
    property populated automatically by the entity platform. Assigning to it
    directly (as older integration code sometimes does) raises AttributeError
    and prevents the whole platform from loading.
    """

    @property
    def config_entry(self):
        """Return the config entry (read-only, like the real Entity class)."""
        return None


class _EntityWithReadOnlyConfigEntry(
    _ReadOnlyConfigEntryBase,
    SwissDynamicTariffsEntity,
):
    """SwissDynamicTariffsEntity built on top of the read-only stand-in."""


def test_entity_does_not_write_to_config_entry_property():
    """Test that constructing the entity never assigns to `.config_entry`."""

    entry = SimpleNamespace(entry_id="test")

    # This must not raise AttributeError: property 'config_entry' has no setter.
    entity = _EntityWithReadOnlyConfigEntry(
        FakeCoordinator(),
        entry,
    )

    assert entity.device_info["identifiers"] == {("swiss_dynamic_tariffs", "test")}
