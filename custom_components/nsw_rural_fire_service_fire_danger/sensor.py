"""NSW Rural Fire Service - Fire Danger - Sensor."""
import logging

from .const import DOMAIN, SENSOR_TYPES
from .entity import NswFireServiceFireDangerEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the NSW Rural Fire Service Fire Danger Feed platform."""
    manager = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [
            NswFireServiceFireDangerSensor(hass, manager, sensor_type)
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
