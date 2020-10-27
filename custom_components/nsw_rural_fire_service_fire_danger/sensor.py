"""NSW Rural Fire Service - Fire Danger - Sensor."""
import logging

from homeassistant.core import callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect

from .const import (
    DEFAULT_ATTRIBUTION,
    DEFAULT_FORCE_UPDATE,
    DOMAIN,
    SENSOR_TYPES,
)
from homeassistant.const import ATTR_ATTRIBUTION, STATE_UNKNOWN
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the NSW Rural Fire Service Fire Danger Feed platform."""
    manager = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [
            NswFireServiceFireDangerSensor(hass, manager.district_name, sensor_type)
            for sensor_type in SENSOR_TYPES
        ],
        True,
    )
    _LOGGER.debug("Sensor setup done")


class NswFireServiceFireDangerSensor(Entity):
    """Implementation of the sensor."""

    def __init__(self, hass, district_name, sensor_type):
        """Initialize the sensor."""
        self._hass = hass
        self._district_name = district_name
        self._sensor_type = sensor_type
        # TODO: Generate proper name
        self._name = district_name
        self._state = STATE_UNKNOWN
        self._attributes = {
            "district": district_name,
            ATTR_ATTRIBUTION: DEFAULT_ATTRIBUTION,
        }
        self._remove_signal_update = None

    async def async_added_to_hass(self):
        """Call when entity is added to hass."""
        self._remove_signal_update = async_dispatcher_connect(
            self.hass,
            f"nsw_rfs_fire_danger_update_{self._district_name}_{self._sensor_type}",
            self._update_callback,
        )

    async def async_will_remove_from_hass(self) -> None:
        """Call when entity will be removed from hass."""
        if self._remove_signal_update:
            self._remove_signal_update()

    @callback
    def _update_callback(self, state, attributes):
        """Call update method."""
        self._state = state
        self._attributes.update(attributes)
        self.async_schedule_update_ha_state(True)

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the device."""
        return self._state

    @property
    def force_update(self):
        """Force update."""
        return DEFAULT_FORCE_UPDATE

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return self._attributes
