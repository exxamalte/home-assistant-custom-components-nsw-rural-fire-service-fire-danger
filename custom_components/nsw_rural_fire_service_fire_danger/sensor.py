"""NSW Rural Fire Service - Fire Danger - Sensor."""
import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, SENSOR_TYPES
from .entity import NswFireServiceFireDangerEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the NSW Rural Fire Service Fire Danger Feed platform."""
    manager = hass.data[DOMAIN][config_entry.entry_id]
    config_entry_unique_id = config_entry.unique_id

    async_add_entities(
        [
            NswFireServiceFireDangerSensor(manager, sensor_type, config_entry_unique_id)
            for sensor_type in SENSOR_TYPES
        ],
        True,
    )
    _LOGGER.debug("Sensor setup done")


class NswFireServiceFireDangerSensor(NswFireServiceFireDangerEntity, SensorEntity):
    """Implementation of the sensor."""

    _attr_icon = "mdi:speedometer-medium"
