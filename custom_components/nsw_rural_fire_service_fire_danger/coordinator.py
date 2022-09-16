# NSW Rural Fire Service Fire Danger - Data Coordinators.
import logging
from abc import abstractmethod
from datetime import timedelta
from typing import Any

import xmltodict
from homeassistant.components.rest import RestData
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_SCAN_INTERVAL
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from pyexpat import ExpatError

from .const import (
    CONF_DISTRICT_NAME,
    DEFAULT_METHOD,
    DEFAULT_VERIFY_SSL,
    DOMAIN,
    SENSOR_ATTRIBUTES,
    URL_DATA,
    XML_DISTRICT,
    XML_FIRE_DANGER_MAP,
    XML_NAME,
)

_LOGGER = logging.getLogger(__name__)


class NswRfsFireDangerFeedCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Feed Entity Manager for NSW Rural Fire Service Fire Danger feed."""

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        """Initialize the Feed Entity Manager."""
        self.hass = hass
        self._district_name = config_entry.data[CONF_DISTRICT_NAME]
        self._rest = RestData(
            hass,
            DEFAULT_METHOD,
            URL_DATA[self._data_feed_type()],
            None,
            None,
            None,
            None,
            DEFAULT_VERIFY_SSL,
        )
        super().__init__(
            self.hass,
            _LOGGER,
            name=DOMAIN,
            update_method=self.async_update,
            update_interval=timedelta(seconds=config_entry.data[CONF_SCAN_INTERVAL]),
        )

    @abstractmethod
    def _data_feed_type(self) -> str:
        """Return the data feed type that this coordinator supports."""

    @property
    def district_name(self) -> str:
        """Return the district name of the coordinator."""
        return self._district_name

    @abstractmethod
    async def async_update(self) -> dict[str, str]:
        """Get the latest data from external feed and update the state."""


class NswRfsFireDangerStandardFeedCoordinator(NswRfsFireDangerFeedCoordinator):
    """Feed Entity Manager for NSW Rural Fire Service Fire Danger standard feed."""

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        """Initialize the standard Feed Entity Manager."""
        super().__init__(hass, config_entry)

    def _data_feed_type(self) -> str:
        """Return the data feed type that this coordinator supports."""
        return "standard"

    @staticmethod
    def _attribute_in_structure(obj, keys):
        """Return the attribute found under the chain of keys."""
        key = keys.pop(0)
        if key in obj:
            return (
                NswRfsFireDangerStandardFeedCoordinator._attribute_in_structure(
                    obj[key], keys
                )
                if keys
                else obj[key]
            )

    async def async_update(self) -> dict[str, str]:
        """Get the latest data from REST API and update the state."""
        _LOGGER.debug("Start updating feed")
        await self._rest.async_update()
        value = self._rest.data
        attributes = {}
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
                                break
            except ExpatError as ex:
                _LOGGER.warning("Unable to parse feed data: %s", ex)
        return attributes


class NswRfsFireDangerExtendedFeedCoordinator(NswRfsFireDangerFeedCoordinator):
    """Feed Entity Manager for NSW Rural Fire Service Fire Danger extended feed."""

    def _data_feed_type(self) -> str:
        """Return the data feed type that this coordinator supports."""
        return "extended"

    async def async_update(self) -> dict[str, str]:
        pass