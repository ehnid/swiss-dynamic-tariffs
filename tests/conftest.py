"""Global fixtures for Swiss Dynamic Tariffs integration."""

from unittest.mock import patch

from homeassistant.components.frontend import DATA_EXTRA_MODULE_URL
import pytest
from pytest_homeassistant_custom_component.common import mock_component

pytest_plugins = [
    "pytest_homeassistant_custom_component",
]


@pytest.fixture(autouse=True)
def enable_custom_integrations(enable_custom_integrations):
    """Enable custom integrations."""
    return


@pytest.fixture(autouse=True)
def mock_frontend_fixture(hass):
    """Provide the frontend state omitted from the lightweight test install."""
    mock_component(hass, "frontend")
    hass.data[DATA_EXTRA_MODULE_URL] = set()


# This fixture is used to prevent HomeAssistant from attempting to create and dismiss persistent
# notifications. These calls would fail without this fixture since the persistent_notification
# integration is never loaded during a test.
@pytest.fixture(name="skip_notifications", autouse=True)
def skip_notifications_fixture():
    """Skip notification calls."""
    with (
        patch("homeassistant.components.persistent_notification.async_create"),
        patch("homeassistant.components.persistent_notification.async_dismiss"),
    ):
        yield


# This fixture, when used, will result in calls to the BKW provider returning an empty
# list of tariffs instead of making a real HTTP request.
@pytest.fixture(name="bypass_get_data")
def bypass_get_data_fixture():
    """Skip calls to get data from the BKW provider."""
    with patch(
        "custom_components.swiss_dynamic_tariffs.providers.bkw.BKWProvider.async_get_tariffs",
        return_value=[],
    ):
        yield


# In this fixture, we are forcing calls to the BKW provider to raise an Exception. This is
# useful for exception handling.
@pytest.fixture(name="error_on_get_data")
def error_get_data_fixture():
    """Simulate error when retrieving data from the BKW provider."""
    with patch(
        "custom_components.swiss_dynamic_tariffs.providers.bkw.BKWProvider.async_get_tariffs",
        side_effect=Exception,
    ):
        yield
