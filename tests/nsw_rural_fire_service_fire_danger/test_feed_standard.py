"""Define tests for the NSW Rural Fire Service - Fire Danger standard feed."""

from datetime import timedelta
from http import HTTPStatus
import logging

from homeassistant.const import (
    ATTR_ATTRIBUTION,
    ATTR_DEVICE_CLASS,
    ATTR_ICON,
    CONF_SCAN_INTERVAL,
)
from homeassistant.core import HomeAssistant
from homeassistant.setup import async_setup_component
from homeassistant.util import utcnow
import pytest
from pytest_homeassistant_custom_component.common import async_fire_time_changed
import respx

from custom_components.nsw_rural_fire_service_fire_danger import (
    CONF_CONVERT_NO_RATING,
    CONF_DATA_FEED,
    CONF_DISTRICT_NAME,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
)
from tests.nsw_rural_fire_service_fire_danger.utils import load_fixture

CONFIG_STANDARD_SYDNEY = {
    DOMAIN: {
        CONF_DISTRICT_NAME: "Greater Sydney Region",
        CONF_DATA_FEED: "standard",
        CONF_CONVERT_NO_RATING: True,
        CONF_SCAN_INTERVAL: DEFAULT_SCAN_INTERVAL.total_seconds(),
    }
}
CONFIG_STANDARD_ACT = {
    DOMAIN: {
        CONF_DISTRICT_NAME: "ACT",
        CONF_DATA_FEED: "standard",
        CONF_CONVERT_NO_RATING: True,
        CONF_SCAN_INTERVAL: DEFAULT_SCAN_INTERVAL.total_seconds(),
    }
}
CONFIG_STANDARD_FAR_WESTERN = {
    DOMAIN: {
        CONF_DISTRICT_NAME: "Far Western",
        CONF_DATA_FEED: "standard",
        CONF_CONVERT_NO_RATING: True,
        CONF_SCAN_INTERVAL: DEFAULT_SCAN_INTERVAL.total_seconds(),
    }
}
_LOGGER = logging.getLogger(__name__)


@pytest.mark.asyncio
@respx.mock
async def test_feed_standard(hass: HomeAssistant, config_entry):
    """Test standard feed setup and entities."""
    await async_setup_component(hass, "homeassistant", {})
    respx.get("http://www.rfs.nsw.gov.au/feeds/fdrToban.xml").respond(
        status_code=HTTPStatus.OK, text=load_fixture("feed-1.xml")
    )
    assert await async_setup_component(
        hass,
        DOMAIN,
        CONFIG_STANDARD_SYDNEY,
    )
    await hass.async_block_till_done()

    # Refresh the coordinator
    async_fire_time_changed(
        hass, utcnow() + timedelta(seconds=DEFAULT_SCAN_INTERVAL.total_seconds() + 1)
    )
    await hass.async_block_till_done()

    assert len(hass.states.async_all("binary_sensor")) == 2  # noqa: PLR2004

    state = hass.states.get(
        "binary_sensor.fire_danger_greater_sydney_region_fire_ban_today"
    )
    assert state.state == "off"
    assert state.name == "Fire danger Greater Sydney Region Fire ban today"
    assert state.attributes == {
        "district": "Greater Sydney Region",
        "region_number": 4,
        "councils": [
            "The Hills",
            "Blacktown",
            "Blue Mountains",
            "Burwood",
            "Camden",
            "Campbelltown",
            "Canada Bay",
            "Fairfield",
            "Hawkesbury",
            "Hornsby",
            "Hunters Hill",
            "Kogarah",
            "Ku-ring-gai",
            "Lane Cove",
            "Liverpool",
            "Mosman",
            "North Sydney",
            "Parramatta",
            "Penrith",
            "Randwick",
            "Ryde",
            "Strathfield",
            "Sutherland",
            "Sydney",
            "Waverley",
            "Willoughby",
            "Woollahra",
            "Bayside",
            "Canterbury-Bankstown",
            "Central Coast",
            "Cumberland",
            "Georges River",
            "Inner West",
            "Northern Beaches",
        ],
        "danger_level_today": "Moderate",
        "danger_level_tomorrow": "Moderate",
        "fire_ban_tomorrow": False,
        ATTR_ATTRIBUTION: "NSW Rural Fire Service",
        ATTR_DEVICE_CLASS: "safety",
        "friendly_name": "Fire danger Greater Sydney Region Fire ban today",
    }

    state = hass.states.get(
        "binary_sensor.fire_danger_greater_sydney_region_fire_ban_tomorrow"
    )
    assert state.state == "off"
    assert state.name == "Fire danger Greater Sydney Region Fire ban tomorrow"
    assert state.attributes == {
        "district": "Greater Sydney Region",
        "region_number": 4,
        "councils": [
            "The Hills",
            "Blacktown",
            "Blue Mountains",
            "Burwood",
            "Camden",
            "Campbelltown",
            "Canada Bay",
            "Fairfield",
            "Hawkesbury",
            "Hornsby",
            "Hunters Hill",
            "Kogarah",
            "Ku-ring-gai",
            "Lane Cove",
            "Liverpool",
            "Mosman",
            "North Sydney",
            "Parramatta",
            "Penrith",
            "Randwick",
            "Ryde",
            "Strathfield",
            "Sutherland",
            "Sydney",
            "Waverley",
            "Willoughby",
            "Woollahra",
            "Bayside",
            "Canterbury-Bankstown",
            "Central Coast",
            "Cumberland",
            "Georges River",
            "Inner West",
            "Northern Beaches",
        ],
        "danger_level_today": "Moderate",
        "danger_level_tomorrow": "Moderate",
        "fire_ban_today": False,
        ATTR_ATTRIBUTION: "NSW Rural Fire Service",
        ATTR_DEVICE_CLASS: "safety",
        "friendly_name": "Fire danger Greater Sydney Region Fire ban tomorrow",
    }

    assert len(hass.states.async_all("sensor")) == 2  # noqa: PLR2004

    state = hass.states.get(
        "sensor.fire_danger_greater_sydney_region_danger_level_today"
    )
    assert state.state == "Moderate"
    assert state.name == "Fire danger Greater Sydney Region Danger level today"
    assert state.attributes == {
        "district": "Greater Sydney Region",
        "region_number": 4,
        "councils": [
            "The Hills",
            "Blacktown",
            "Blue Mountains",
            "Burwood",
            "Camden",
            "Campbelltown",
            "Canada Bay",
            "Fairfield",
            "Hawkesbury",
            "Hornsby",
            "Hunters Hill",
            "Kogarah",
            "Ku-ring-gai",
            "Lane Cove",
            "Liverpool",
            "Mosman",
            "North Sydney",
            "Parramatta",
            "Penrith",
            "Randwick",
            "Ryde",
            "Strathfield",
            "Sutherland",
            "Sydney",
            "Waverley",
            "Willoughby",
            "Woollahra",
            "Bayside",
            "Canterbury-Bankstown",
            "Central Coast",
            "Cumberland",
            "Georges River",
            "Inner West",
            "Northern Beaches",
        ],
        "danger_level_tomorrow": "Moderate",
        "fire_ban_today": False,
        "fire_ban_tomorrow": False,
        ATTR_ATTRIBUTION: "NSW Rural Fire Service",
        ATTR_ICON: "mdi:speedometer-medium",
        "friendly_name": "Fire danger Greater Sydney Region Danger level today",
    }

    state = hass.states.get(
        "sensor.fire_danger_greater_sydney_region_danger_level_tomorrow"
    )
    assert state.state == "Moderate"
    assert state.name == "Fire danger Greater Sydney Region Danger level tomorrow"
    assert state.attributes == {
        "district": "Greater Sydney Region",
        "region_number": 4,
        "councils": [
            "The Hills",
            "Blacktown",
            "Blue Mountains",
            "Burwood",
            "Camden",
            "Campbelltown",
            "Canada Bay",
            "Fairfield",
            "Hawkesbury",
            "Hornsby",
            "Hunters Hill",
            "Kogarah",
            "Ku-ring-gai",
            "Lane Cove",
            "Liverpool",
            "Mosman",
            "North Sydney",
            "Parramatta",
            "Penrith",
            "Randwick",
            "Ryde",
            "Strathfield",
            "Sutherland",
            "Sydney",
            "Waverley",
            "Willoughby",
            "Woollahra",
            "Bayside",
            "Canterbury-Bankstown",
            "Central Coast",
            "Cumberland",
            "Georges River",
            "Inner West",
            "Northern Beaches",
        ],
        "danger_level_today": "Moderate",
        "fire_ban_today": False,
        "fire_ban_tomorrow": False,
        ATTR_ATTRIBUTION: "NSW Rural Fire Service",
        ATTR_ICON: "mdi:speedometer-medium",
        "friendly_name": "Fire danger Greater Sydney Region Danger level tomorrow",
    }


@pytest.mark.asyncio
@respx.mock
async def test_feed_standard_act(hass: HomeAssistant, config_entry):
    """Test standard feed setup and entities."""
    await async_setup_component(hass, "homeassistant", {})
    respx.get("http://www.rfs.nsw.gov.au/feeds/fdrToban.xml").respond(
        status_code=HTTPStatus.OK, text=load_fixture("feed-1.xml")
    )
    assert await async_setup_component(
        hass,
        DOMAIN,
        CONFIG_STANDARD_ACT,
    )
    await hass.async_block_till_done()

    # Refresh the coordinator
    async_fire_time_changed(
        hass, utcnow() + timedelta(seconds=DEFAULT_SCAN_INTERVAL.total_seconds() + 1)
    )
    await hass.async_block_till_done()

    state = hass.states.get("binary_sensor.fire_danger_act_fire_ban_today")
    assert state.state == "off"
    assert state.name == "Fire danger ACT Fire ban today"
    assert state.attributes == {
        "district": "ACT",
        "region_number": 8,
        "danger_level_today": "Moderate",
        "danger_level_tomorrow": "Moderate",
        "fire_ban_tomorrow": False,
        ATTR_ATTRIBUTION: "NSW Rural Fire Service",
        ATTR_DEVICE_CLASS: "safety",
        "friendly_name": "Fire danger ACT Fire ban today",
    }


@pytest.mark.asyncio
@respx.mock
async def test_feed_standard_missing_data(hass: HomeAssistant, config_entry):
    """Test standard feed setup and entities."""
    await async_setup_component(hass, "homeassistant", {})
    respx.get("http://www.rfs.nsw.gov.au/feeds/fdrToban.xml").respond(
        status_code=HTTPStatus.OK, text=load_fixture("feed-1.xml")
    )
    assert await async_setup_component(
        hass,
        DOMAIN,
        CONFIG_STANDARD_FAR_WESTERN,
    )
    await hass.async_block_till_done()

    # Refresh the coordinator
    async_fire_time_changed(
        hass, utcnow() + timedelta(seconds=DEFAULT_SCAN_INTERVAL.total_seconds() + 1)
    )
    await hass.async_block_till_done()

    state = hass.states.get("binary_sensor.fire_danger_far_western_fire_ban_today")
    assert state.state == "off"
    state = hass.states.get("binary_sensor.fire_danger_far_western_fire_ban_tomorrow")
    assert state.state == "unknown"
    state = hass.states.get("sensor.fire_danger_far_western_danger_level_today")
    assert state.state == "Moderate"
    state = hass.states.get("sensor.fire_danger_far_western_danger_level_tomorrow")
    assert state.state == "unknown"


@pytest.mark.asyncio
@respx.mock
async def test_feed_standard_invalid(hass: HomeAssistant, config_entry):
    """Test standard feed setup and entities."""
    await async_setup_component(hass, "homeassistant", {})
    respx.get("http://www.rfs.nsw.gov.au/feeds/fdrToban.xml").respond(
        status_code=HTTPStatus.OK, text="NOT XML"
    )
    assert await async_setup_component(
        hass,
        DOMAIN,
        CONFIG_STANDARD_SYDNEY,
    )
    await hass.async_block_till_done()

    # Refresh the coordinator
    async_fire_time_changed(
        hass, utcnow() + timedelta(seconds=DEFAULT_SCAN_INTERVAL.total_seconds() + 1)
    )
    await hass.async_block_till_done()

    state = hass.states.get(
        "binary_sensor.fire_danger_greater_sydney_region_fire_ban_today"
    )
    assert state.state == "unknown"
