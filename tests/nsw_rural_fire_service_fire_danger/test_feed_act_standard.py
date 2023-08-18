"""Define tests for the ACT Emergency Services Agency - Fire Danger standard feed."""
import logging
from datetime import datetime, timedelta, timezone
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

CONFIG_ACT_STANDARD_ACT = {
    DOMAIN: {
        CONF_DISTRICT_NAME: "ACT",
        CONF_DATA_FEED: "act_standard",
        CONF_CONVERT_NO_RATING: True,
        CONF_SCAN_INTERVAL: DEFAULT_SCAN_INTERVAL.total_seconds(),
    }
}

_LOGGER = logging.getLogger(__name__)


@pytest.mark.asyncio
@respx.mock
async def test_feed_standard_act(hass: HomeAssistant, config_entry):
    """Test act_standard feed setup and entities."""
    await async_setup_component(hass, "homeassistant", {})
    respx.get("https://esa.act.gov.au/feeds/firedangerrating.xml").respond(
        status_code=HTTPStatus.OK, text=load_fixture("feed-act-1.xml")
    )
    assert await async_setup_component(
        hass,
        DOMAIN,
        CONFIG_ACT_STANDARD_ACT,
    )
    await hass.async_block_till_done()

    # Refresh the coordinator
    async_fire_time_changed(
        hass, utcnow() + timedelta(seconds=DEFAULT_SCAN_INTERVAL.total_seconds() + 1)
    )
    await hass.async_block_till_done()

    assert len(hass.states.async_all("binary_sensor")) == 2

    state = hass.states.get("binary_sensor.fire_danger_act_esa_fire_ban_today")
    assert state.state == "off"
    assert state.name == "Fire danger ACT (ESA) Fire ban today"
    assert state.attributes == {
        "district": "ACT (ESA)",
        "region_number": 8,
        "danger_level_today": "No Rating",
        "danger_level_tomorrow": "No Rating",
        "fire_ban_tomorrow": False,
        ATTR_ATTRIBUTION: "ACT Emergency Services Agency",
        ATTR_DEVICE_CLASS: "safety",
        "friendly_name": "Fire danger ACT (ESA) Fire ban today",
        "last_build_date": datetime(
            2023, 8, 13, 10, 24, 5, tzinfo=timezone(timedelta(seconds=36000))
        ),
        "publish_date": datetime(
            2023, 8, 13, 10, 24, 5, tzinfo=timezone(timedelta(seconds=36000))
        ),
    }

    state = hass.states.get("binary_sensor.fire_danger_act_esa_fire_ban_tomorrow")
    assert state.state == "off"
    assert state.name == "Fire danger ACT (ESA) Fire ban tomorrow"
    assert state.attributes == {
        "district": "ACT (ESA)",
        "region_number": 8,
        "danger_level_today": "No Rating",
        "danger_level_tomorrow": "No Rating",
        "fire_ban_today": False,
        ATTR_ATTRIBUTION: "ACT Emergency Services Agency",
        ATTR_DEVICE_CLASS: "safety",
        "friendly_name": "Fire danger ACT (ESA) Fire ban tomorrow",
        "last_build_date": datetime(
            2023, 8, 13, 10, 24, 5, tzinfo=timezone(timedelta(seconds=36000))
        ),
        "publish_date": datetime(
            2023, 8, 13, 10, 24, 5, tzinfo=timezone(timedelta(seconds=36000))
        ),
    }

    assert len(hass.states.async_all("sensor")) == 2

    state = hass.states.get("sensor.fire_danger_act_esa_danger_level_today")
    assert state.state == "No Rating"
    assert state.name == "Fire danger ACT (ESA) Danger level today"
    assert state.attributes == {
        "district": "ACT (ESA)",
        "region_number": 8,
        "danger_level_tomorrow": "No Rating",
        "fire_ban_today": False,
        "fire_ban_tomorrow": False,
        ATTR_ATTRIBUTION: "ACT Emergency Services Agency",
        ATTR_ICON: "mdi:speedometer-medium",
        "friendly_name": "Fire danger ACT (ESA) Danger level today",
        "last_build_date": datetime(
            2023, 8, 13, 10, 24, 5, tzinfo=timezone(timedelta(seconds=36000))
        ),
        "publish_date": datetime(
            2023, 8, 13, 10, 24, 5, tzinfo=timezone(timedelta(seconds=36000))
        ),
    }

    state = hass.states.get("sensor.fire_danger_act_esa_danger_level_tomorrow")
    assert state.state == "No Rating"
    assert state.name == "Fire danger ACT (ESA) Danger level tomorrow"
    assert state.attributes == {
        "district": "ACT (ESA)",
        "region_number": 8,
        "danger_level_today": "No Rating",
        "fire_ban_today": False,
        "fire_ban_tomorrow": False,
        ATTR_ATTRIBUTION: "ACT Emergency Services Agency",
        ATTR_ICON: "mdi:speedometer-medium",
        "friendly_name": "Fire danger ACT (ESA) Danger level tomorrow",
        "last_build_date": datetime(
            2023, 8, 13, 10, 24, 5, tzinfo=timezone(timedelta(seconds=36000))
        ),
        "publish_date": datetime(
            2023, 8, 13, 10, 24, 5, tzinfo=timezone(timedelta(seconds=36000))
        ),
    }


# Commented out until I can work out if this is something we do

# @pytest.mark.asyncio
# @respx.mock
# async def test_feed_standard_missing_data(hass: HomeAssistant, config_entry):
#     """Test standard feed setup and entities."""
#     await async_setup_component(hass, "homeassistant", {})
#     respx.get("https://esa.act.gov.au/feeds/firedangerrating.xml").respond(
#         status_code=HTTPStatus.OK, text=load_fixture("feed-1.xml")
#     )
#     assert await async_setup_component(
#         hass,
#         DOMAIN,
#         CONFIG_ACT_STANDARD_ACT,
#     )
#     await hass.async_block_till_done()

#     # Refresh the coordinator
#     async_fire_time_changed(
#         hass, utcnow() + timedelta(seconds=DEFAULT_SCAN_INTERVAL.total_seconds() + 1)
#     )
#     await hass.async_block_till_done()

#     state = hass.states.get("binary_sensor.fire_danger_act_esa_fire_ban_today")
#     assert state.state == "off"
#     state = hass.states.get("binary_sensor.fire_danger_act_esa_fire_ban_tomorrow")
#     assert state.state == "unknown"
#     state = hass.states.get("sensor.fire_danger_act_esa_danger_level_today")
#     assert state.state == "No Rating"
#     state = hass.states.get("sensor.fire_danger_act_esa_danger_level_tomorrow")
#     assert state.state == "unknown"


@pytest.mark.asyncio
@respx.mock
async def test_feed_standard_invalid(hass: HomeAssistant, config_entry):
    """Test standard feed setup and entities."""
    await async_setup_component(hass, "homeassistant", {})
    respx.get("https://esa.act.gov.au/feeds/firedangerrating.xml").respond(
        status_code=HTTPStatus.OK, text="NOT XML"
    )
    assert await async_setup_component(
        hass,
        DOMAIN,
        CONFIG_ACT_STANDARD_ACT,
    )
    await hass.async_block_till_done()

    # Refresh the coordinator
    async_fire_time_changed(
        hass, utcnow() + timedelta(seconds=DEFAULT_SCAN_INTERVAL.total_seconds() + 1)
    )
    await hass.async_block_till_done()

    state = hass.states.get("binary_sensor.fire_danger_act_esa_fire_ban_today")
    assert state.state == "unknown"
