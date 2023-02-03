"""Configuration for NSW Rural Fire Service - Fire Danger tests."""
import pytest
from homeassistant import loader
from homeassistant.const import CONF_SCAN_INTERVAL
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.nsw_rural_fire_service_fire_danger.const import (
    CONF_CONVERT_NO_RATING,
    CONF_DATA_FEED,
    CONF_DISTRICT_NAME,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
)


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    yield


@pytest.fixture
def enable_custom_integrations(hass):
    """Enable custom integrations defined in the test dir."""
    hass.data.pop(loader.DATA_CUSTOM_COMPONENTS)


@pytest.fixture
def config_entry():
    """Create a mock NSW Rural Fire Service Feeds Events config entry."""
    return MockConfigEntry(
        domain=DOMAIN,
        data={
            CONF_DISTRICT_NAME: "Greater Sydney Region",
            CONF_DATA_FEED: "standard",
            CONF_CONVERT_NO_RATING: True,
            CONF_SCAN_INTERVAL: DEFAULT_SCAN_INTERVAL.total_seconds(),
        },
        title="Greater Sydney Region",
        unique_id="Greater Sydney Region",
    )
