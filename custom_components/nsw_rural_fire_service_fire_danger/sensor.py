"""NSW Rural Fire Service - Fire Danger - Sensor."""
import logging

from .const import DOMAIN, SENSOR_TYPES
from .entity import NswFireServiceFireDangerEntity

_LOGGER = logging.getLogger(__name__)

# An update of this entity is not making a web request, but uses internal data only.
PARALLEL_UPDATES = 0


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the NSW Rural Fire Service Fire Danger Feed platform."""
    manager = hass.data[DOMAIN][entry.entry_id]
    config_entry_unique_id = entry.unique_id

    async_add_entities(
        [
            NswFireServiceFireDangerSensor(
                hass, manager, sensor_type, config_entry_unique_id
            )
            for sensor_type in SENSOR_TYPES
        ],
        True,
    )
    _LOGGER.debug("Sensor setup done")


class NswFireServiceFireDangerSensor(NswFireServiceFireDangerEntity):
    """Implementation of the sensor."""

    @property
    def state(self):
        """Return the state of the device."""
        return self._state
