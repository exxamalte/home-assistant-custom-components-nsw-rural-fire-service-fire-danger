# NSW Rural Fire Service Fire Danger.
import asyncio
from datetime import timedelta
import logging
from pyexpat import ExpatError

import voluptuous as vol
import xmltodict
from homeassistant.components.rest.data import RestData

from homeassistant.config_entries import SOURCE_IMPORT
from homeassistant.const import CONF_SCAN_INTERVAL, STATE_OK, STATE_UNKNOWN
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.dispatcher import async_dispatcher_send
from homeassistant.helpers.event import async_track_time_interval

from .config_flow import configured_instances
from .const import (
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    CONF_DISTRICT_NAME,
    DEFAULT_METHOD,
    URL,
    DEFAULT_VERIFY_SSL,
    XML_FIRE_DANGER_MAP,
    XML_DISTRICT,
    XML_NAME,
    SENSOR_ATTRIBUTES,
)

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_DISTRICT_NAME): cv.string,
                vol.Optional(
                    CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL
                ): cv.time_period,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)


async def async_setup(hass, config):
    """Set up the NSW Rural Fire Service Fire Danger component."""
    if DOMAIN not in config:
        return True

    conf = config[DOMAIN]

    district_name = conf.get[CONF_DISTRICT_NAME]
    scan_interval = conf[CONF_SCAN_INTERVAL]

    identifier = f"{district_name}"
    if identifier in configured_instances(hass):
        return True

    hass.async_create_task(
        hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": SOURCE_IMPORT},
            data={CONF_DISTRICT_NAME: district_name, CONF_SCAN_INTERVAL: scan_interval},
        )
    )

    return True


async def async_setup_entry(hass, config_entry):
    """Set up the NSW Rural Fire Service Fire Danger component as config entry."""
    hass.data.setdefault(DOMAIN, {})
    # Create feed entity manager for all platforms.
    manager = NswRfsFireDangerFeedEntityManager(hass, config_entry)
    hass.data[DOMAIN][config_entry.entry_id] = manager
    _LOGGER.debug("Feed entity manager added for %s", config_entry.entry_id)
    await manager.async_init()
    return True


async def async_unload_entry(hass, config_entry):
    """Unload an NSW Rural Fire Service Fire Danger component config entry."""
    manager = hass.data[DOMAIN].pop(config_entry.entry_id)
    await manager.async_stop()
    await asyncio.wait(
        [hass.config_entries.async_forward_entry_unload(config_entry, "sensor")]
    )
    return True


class NswRfsFireDangerFeedEntityManager:
    """Feed Entity Manager for NSW Rural Fire Service Fire Danger feed."""

    def __init__(self, hass, config_entry):
        """Initialize the Feed Entity Manager."""
        self._hass = hass
        self._config_entry = config_entry
        self._district_name = config_entry.data[CONF_DISTRICT_NAME]
        # websession = aiohttp_client.async_get_clientsession(hass)
        # self._feed_manager = GeonetnzVolcanoFeedManager(
        #     websession,
        #     self._generate_entity,
        #     self._update_entity,
        #     self._remove_entity,
        #     coordinates,
        #     filter_radius=radius_in_km,
        # )
        self._config_entry_id = config_entry.entry_id
        self._scan_interval = timedelta(seconds=config_entry.data[CONF_SCAN_INTERVAL])
        self._track_time_remove_callback = None
        self.listeners = []
        self._rest = RestData(DEFAULT_METHOD, URL, None, None, None, DEFAULT_VERIFY_SSL)

    @property
    def district_name(self):
        """Return the district name of the manager."""
        return self._district_name

    async def async_init(self):
        """Schedule initial and regular updates based on configured time interval."""

        self._hass.async_create_task(
            self._hass.config_entries.async_forward_entry_setup(
                self._config_entry, "sensor"
            )
        )

        async def update(event_time):
            """Update."""
            await self.async_update()

        # Trigger updates at regular intervals.
        self._track_time_remove_callback = async_track_time_interval(
            self._hass, update, self._scan_interval
        )

        _LOGGER.debug("Feed entity manager initialized")

    # async def async_update(self):
    #     """Refresh data."""
    #     # await self._feed_manager.update()
    #     _LOGGER.debug("Feed entity manager updated")

    @staticmethod
    def _attribute_in_structure(obj, keys):
        """Return the attribute found under the chain of keys."""
        key = keys.pop(0)
        if key in obj:
            return (
                NswRfsFireDangerFeedEntityManager._attribute_in_structure(
                    obj[key], keys
                )
                if keys
                else obj[key]
            )

    async def async_update(self):
        """Get the latest data from REST API and update the state."""
        await self._rest.async_update()
        value = self._rest.data
        attributes = {
            # "district": self._district_name,
            # ATTR_ATTRIBUTION: DEFAULT_ATTRIBUTION,
        }
        self._state = STATE_UNKNOWN
        if value:
            try:
                value = xmltodict.parse(value)
                districts = self._attribute_in_structure(
                    value, [XML_FIRE_DANGER_MAP, XML_DISTRICT]
                )
                if districts and isinstance(districts, list):
                    for district in districts:
                        if XML_NAME in district:
                            district_name = district.get(XML_NAME)
                            if district_name == self._district_name:
                                # Found it.
                                for key in SENSOR_ATTRIBUTES:
                                    if key in district:
                                        text_value = district.get(key)
                                        conversion = SENSOR_ATTRIBUTES[key][1]
                                        if conversion:
                                            text_value = conversion(text_value)
                                        attributes[
                                            SENSOR_ATTRIBUTES[key][0]
                                        ] = text_value
                                self._state = STATE_OK
                                # Dispatch to sensors.
                                async_dispatcher_send(
                                    self._hass,
                                    f"nsw_rfs_fire_danger_update_{self._district_name}_fire_ban_today",
                                    SENSOR_ATTRIBUTES["FireBanToday"],
                                    attributes,
                                )
                                async_dispatcher_send(
                                    self._hass,
                                    f"nsw_rfs_fire_danger_update_{self._district_name}_fire_ban_tomorrow",
                                    SENSOR_ATTRIBUTES["FireBanTomorrow"],
                                    attributes,
                                )
                                break
            except ExpatError as ex:
                _LOGGER.warning("Unable to parse XML data: %s", ex)
        self._attributes = attributes

    async def async_stop(self):
        """Stop this feed entity manager from refreshing."""
        for unsub_dispatcher in self.listeners:
            unsub_dispatcher()
        self.listeners = []
        if self._track_time_remove_callback:
            self._track_time_remove_callback()
        _LOGGER.debug("Feed entity manager stopped")
