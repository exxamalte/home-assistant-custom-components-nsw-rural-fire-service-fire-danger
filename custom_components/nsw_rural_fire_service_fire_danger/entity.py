"""NSW Rural Fire Service - Fire Danger - Entity."""
import logging
from typing import Optional

from homeassistant.const import STATE_UNKNOWN, ATTR_ATTRIBUTION
from homeassistant.core import callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity import Entity

from .const import DEFAULT_ATTRIBUTION, DEFAULT_FORCE_UPDATE, TYPES

_LOGGER = logging.getLogger(__name__)


class NswFireServiceFireDangerEntity(Entity):
    """Implementation of a generic entity."""

    def __init__(self, hass, manager, sensor_type, config_entry_unique_id):
        """Initialize the entity."""
        self._hass = hass
        self._manager = manager
        self._district_name = manager.district_name
        self._sensor_type = sensor_type
        self._config_entry_unique_id = config_entry_unique_id
        self._name = f"Fire Danger in {self._district_name} {TYPES[self._sensor_type]}"
        self._state = STATE_UNKNOWN
        self._attributes = {
            "district": self._district_name,
            ATTR_ATTRIBUTION: DEFAULT_ATTRIBUTION,
        }
        self._remove_signal_update = None

    async def async_added_to_hass(self):
        """Call when entity is added to hass."""
        _LOGGER.debug(
            f"Subscribing to: nsw_rfs_fire_danger_update_{self._district_name}"
        )
        self._remove_signal_update = async_dispatcher_connect(
            self.hass,
            f"nsw_rfs_fire_danger_update_{self._district_name}",
            self._update_callback,
        )

    async def async_will_remove_from_hass(self) -> None:
        """Call when entity will be removed from hass."""
        if self._remove_signal_update:
            self._remove_signal_update()

    @callback
    def _update_callback(self):
        """Call update method."""
        self.async_schedule_update_ha_state(True)

    async def async_update(self):
        """Update entity."""
        attributes = self._manager.attributes
        _LOGGER.debug(f"Updating from {attributes}")
        if attributes:
            self._state = attributes[self._sensor_type]
            self._attributes.update(attributes)
            # Remove the attribute equal to sensor's state.
            del self._attributes[self._sensor_type]

    @property
    def should_poll(self):
        """No polling needed."""
        return False

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def unique_id(self) -> Optional[str]:
        """Return a unique ID containing latitude/longitude and external id."""
        return f"{self._config_entry_unique_id}_{self._sensor_type}"

    @property
    def force_update(self):
        """Force update."""
        return DEFAULT_FORCE_UPDATE

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return self._attributes
