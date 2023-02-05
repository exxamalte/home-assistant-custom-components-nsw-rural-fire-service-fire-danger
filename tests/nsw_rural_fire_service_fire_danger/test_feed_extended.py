"""Define tests for the NSW Rural Fire Service - Fire Danger extended feed."""
import logging
from datetime import timedelta
from http import HTTPStatus

import pytest
import respx
from homeassistant.const import (
    ATTR_ATTRIBUTION,
    ATTR_DEVICE_CLASS,
    ATTR_ICON,
    CONF_SCAN_INTERVAL,
)
from homeassistant.core import HomeAssistant
from homeassistant.setup import async_setup_component
from homeassistant.util import utcnow
from pytest_homeassistant_custom_component.common import async_fire_time_changed
from tests.nsw_rural_fire_service_fire_danger.utils import load_fixture

from custom_components.nsw_rural_fire_service_fire_danger import (
    CONF_CONVERT_NO_RATING,
    CONF_DATA_FEED,
    CONF_DISTRICT_NAME,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
)

CONFIG_EXTENDED_SYDNEY = {
    DOMAIN: {
        CONF_DISTRICT_NAME: "Greater Sydney Region",
        CONF_DATA_FEED: "extended",
        CONF_CONVERT_NO_RATING: True,
        CONF_SCAN_INTERVAL: DEFAULT_SCAN_INTERVAL.total_seconds(),
    }
}
CONFIG_EXTENDED_ACT = {
    DOMAIN: {
        CONF_DISTRICT_NAME: "ACT",
        CONF_DATA_FEED: "extended",
        CONF_CONVERT_NO_RATING: True,
        CONF_SCAN_INTERVAL: DEFAULT_SCAN_INTERVAL.total_seconds(),
    }
}

_LOGGER = logging.getLogger(__name__)


@pytest.mark.asyncio
@respx.mock
async def test_feed_extended(hass: HomeAssistant, config_entry):
    """Test extended feed setup and entities."""
    await async_setup_component(hass, "homeassistant", {})
    respx.get(
        "https://www.rfs.nsw.gov.au/_designs/xml/fire-danger-ratings/fire-danger-ratings-v2"
    ).respond(status_code=HTTPStatus.OK, text=load_fixture("feed-1.json"))
    assert await async_setup_component(
        hass,
        DOMAIN,
        CONFIG_EXTENDED_SYDNEY,
    )
    await hass.async_block_till_done()

    # Refresh the coordinator
    async_fire_time_changed(
        hass, utcnow() + timedelta(seconds=DEFAULT_SCAN_INTERVAL.total_seconds() + 1)
    )
    await hass.async_block_till_done()

    assert len(hass.states.async_all("binary_sensor")) == 4

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
            " Blacktown",
            " Blue Mountains",
            " Burwood",
            " Camden",
            " Campbelltown",
            " Canada Bay",
            " Fairfield",
            " Hawkesbury",
            " Hornsby",
            " Hunters Hill",
            " Kogarah",
            " Ku-ring-gai",
            " Lane Cove",
            " Liverpool",
            " Mosman",
            " North Sydney",
            " Parramatta",
            " Penrith",
            " Randwick",
            " Ryde",
            " Strathfield",
            " Sutherland",
            " Sydney",
            " Waverley",
            " Willoughby",
            " Woollahra",
            " Bayside",
            " Canterbury-Bankstown",
            " Central Coast",
            " Cumberland",
            " Georges River",
            " Inner West",
            " Northern Beaches",
        ],
        "danger_level_today": "Moderate",
        "danger_level_tomorrow": "Moderate",
        "danger_level_day3": "Moderate",
        "danger_level_day4": "No Rating",
        "fire_ban_tomorrow": False,
        "fire_ban_day3": False,
        "fire_ban_day4": False,
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
            " Blacktown",
            " Blue Mountains",
            " Burwood",
            " Camden",
            " Campbelltown",
            " Canada Bay",
            " Fairfield",
            " Hawkesbury",
            " Hornsby",
            " Hunters Hill",
            " Kogarah",
            " Ku-ring-gai",
            " Lane Cove",
            " Liverpool",
            " Mosman",
            " North Sydney",
            " Parramatta",
            " Penrith",
            " Randwick",
            " Ryde",
            " Strathfield",
            " Sutherland",
            " Sydney",
            " Waverley",
            " Willoughby",
            " Woollahra",
            " Bayside",
            " Canterbury-Bankstown",
            " Central Coast",
            " Cumberland",
            " Georges River",
            " Inner West",
            " Northern Beaches",
        ],
        "danger_level_today": "Moderate",
        "danger_level_tomorrow": "Moderate",
        "danger_level_day3": "Moderate",
        "danger_level_day4": "No Rating",
        "fire_ban_today": False,
        "fire_ban_day3": False,
        "fire_ban_day4": False,
        ATTR_ATTRIBUTION: "NSW Rural Fire Service",
        ATTR_DEVICE_CLASS: "safety",
        "friendly_name": "Fire danger Greater Sydney Region Fire ban tomorrow",
    }

    assert len(hass.states.async_all("sensor")) == 4

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
            " Blacktown",
            " Blue Mountains",
            " Burwood",
            " Camden",
            " Campbelltown",
            " Canada Bay",
            " Fairfield",
            " Hawkesbury",
            " Hornsby",
            " Hunters Hill",
            " Kogarah",
            " Ku-ring-gai",
            " Lane Cove",
            " Liverpool",
            " Mosman",
            " North Sydney",
            " Parramatta",
            " Penrith",
            " Randwick",
            " Ryde",
            " Strathfield",
            " Sutherland",
            " Sydney",
            " Waverley",
            " Willoughby",
            " Woollahra",
            " Bayside",
            " Canterbury-Bankstown",
            " Central Coast",
            " Cumberland",
            " Georges River",
            " Inner West",
            " Northern Beaches",
        ],
        "danger_level_tomorrow": "Moderate",
        "danger_level_day3": "Moderate",
        "danger_level_day4": "No Rating",
        "fire_ban_today": False,
        "fire_ban_tomorrow": False,
        "fire_ban_day3": False,
        "fire_ban_day4": False,
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
            " Blacktown",
            " Blue Mountains",
            " Burwood",
            " Camden",
            " Campbelltown",
            " Canada Bay",
            " Fairfield",
            " Hawkesbury",
            " Hornsby",
            " Hunters Hill",
            " Kogarah",
            " Ku-ring-gai",
            " Lane Cove",
            " Liverpool",
            " Mosman",
            " North Sydney",
            " Parramatta",
            " Penrith",
            " Randwick",
            " Ryde",
            " Strathfield",
            " Sutherland",
            " Sydney",
            " Waverley",
            " Willoughby",
            " Woollahra",
            " Bayside",
            " Canterbury-Bankstown",
            " Central Coast",
            " Cumberland",
            " Georges River",
            " Inner West",
            " Northern Beaches",
        ],
        "danger_level_today": "Moderate",
        "danger_level_day3": "Moderate",
        "danger_level_day4": "No Rating",
        "fire_ban_today": False,
        "fire_ban_tomorrow": False,
        "fire_ban_day3": False,
        "fire_ban_day4": False,
        ATTR_ATTRIBUTION: "NSW Rural Fire Service",
        ATTR_ICON: "mdi:speedometer-medium",
        "friendly_name": "Fire danger Greater Sydney Region Danger level tomorrow",
    }


@pytest.mark.asyncio
@respx.mock
async def test_feed_standard_act(hass: HomeAssistant, config_entry):
    """Test standard feed setup and entities."""
    await async_setup_component(hass, "homeassistant", {})
    respx.get(
        "https://www.rfs.nsw.gov.au/_designs/xml/fire-danger-ratings/fire-danger-ratings-v2"
    ).respond(status_code=HTTPStatus.OK, text=load_fixture("feed-1.json"))
    assert await async_setup_component(
        hass,
        DOMAIN,
        CONFIG_EXTENDED_ACT,
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
        "councils": [""],
        "region_number": 8,
        "danger_level_today": "Moderate",
        "danger_level_tomorrow": "Moderate",
        "danger_level_day3": "Moderate",
        "danger_level_day4": "Moderate",
        "fire_ban_tomorrow": False,
        "fire_ban_day3": False,
        "fire_ban_day4": False,
        ATTR_ATTRIBUTION: "NSW Rural Fire Service",
        ATTR_DEVICE_CLASS: "safety",
        "friendly_name": "Fire danger ACT Fire ban today",
    }
