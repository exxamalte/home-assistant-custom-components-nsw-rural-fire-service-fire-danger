"""NSW Rural Fire Service - Fire Danger - Binary Sensor."""
import logging

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    DEVICE_CLASS_SAFETY,
)

from .const import DOMAIN, BINARY_SENSOR_TYPES
from .entity import NswFireServiceFireDangerEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the NSW Rural Fire Service Fire Danger Feed platform."""
    manager = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [
            NswFireServiceFireDangerBinarySensor(hass, manager, sensor_type)
            for sensor_type in BINARY_SENSOR_TYPES
        ],
        True,
    )
    _LOGGER.debug("Sensor setup done")


class NswFireServiceFireDangerBinarySensor(
    NswFireServiceFireDangerEntity, BinarySensorEntity
):
    """Implementation of the binary sensor."""

    @property
    def is_on(self):
        """Return true if the binary sensor is on."""
        return bool(self._state)

    @property
    def device_class(self):
        """Return the class of this device."""
        return DEVICE_CLASS_SAFETY
