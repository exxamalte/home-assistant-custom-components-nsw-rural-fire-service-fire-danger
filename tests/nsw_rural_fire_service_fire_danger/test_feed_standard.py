"""Define tests for the NSW Rural Fire Service - Fire Danger general setup."""
import logging
from http import HTTPStatus

import pytest
import respx
from homeassistant.const import CONF_SCAN_INTERVAL
from homeassistant.core import HomeAssistant
from homeassistant.setup import async_setup_component
from tests.nsw_rural_fire_service_fire_danger.utils import load_fixture

from custom_components.nsw_rural_fire_service_fire_danger import (
    CONF_CONVERT_NO_RATING,
    CONF_DATA_FEED,
    CONF_DISTRICT_NAME,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
)

CONFIG = {
    DOMAIN: {
        CONF_DISTRICT_NAME: "Greater Sydney Region",
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
        CONFIG,
    )
    await hass.async_block_till_done()
    assert len(hass.states.async_all("sensor")) == 2
    assert (
        hass.states.get(
            "sensor.fire_danger_greater_sydney_region_danger_level_today"
        ).state
        == "Moderate"
    )
    assert (
        hass.states.get(
            "sensor.fire_danger_greater_sydney_region_danger_level_tomorrow"
        ).state
        == "Moderate"
    )
    assert len(hass.states.async_all("binary_sensor")) == 2
    assert (
        hass.states.get(
            "binary_sensor.fire_danger_greater_sydney_region_fire_ban_today"
        ).state
        == "off"
    )
    assert (
        hass.states.get(
            "binary_sensor.fire_danger_greater_sydney_region_fire_ban_tomorrow"
        ).state
        == "off"
    )


#         state = hass.states.get("binary_sensor.fire_danger_greater_sydney_region_fire_ban_today")
#         assert state is not None
#
#         assert state.name == "Fire danger Greater Sydney Region Fire ban today"
#         assert state.attributes == {
#             "district": "Greater Sydney Region",
#             "region_number": 4,
#             "councils": ["The Hills", " Blacktown", " Blue Mountains", " Burwood", " Camden", " Campbelltown", " Canada Bay", " Fairfield", " Hawkesbury", " Hornsby", " Hunters Hill", " Kogarah", " Ku-ring-gai", " Lane Cove", " Liverpool", " Mosman", " North Sydney", " Parramatta", " Penrith", " Randwick", " Ryde", " Strathfield", " Sutherland", " Sydney", " Waverley", " Willoughby", " Woollahra", " Bayside", " Canterbury-Bankstown", " Central Coast", " Cumberland", " Georges River", " Inner West", " Northern Beaches"],
#             "danger_level_today": "Moderate",
#             "danger_level_tomorrow": "Moderate",
#             "fire_ban_tomorrow": False,
#             ATTR_ATTRIBUTION: "NSW Rural Fire Service",
#             ATTR_DEVICE_CLASS: "safety",
#             "friendly_name": "Fire danger Greater Sydney Region Fire ban today",
#         }
