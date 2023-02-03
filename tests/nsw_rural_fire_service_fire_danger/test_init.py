"""Define tests for the NSW Rural Fire Service - Fire Danger general setup."""
from unittest.mock import patch

from homeassistant.config_entries import ConfigEntryState
from homeassistant.core import HomeAssistant

from custom_components.nsw_rural_fire_service_fire_danger.const import DOMAIN


async def test_component_unload_config_entry(hass: HomeAssistant, config_entry):
    """Test that loading and unloading of a config entry works."""
    config_entry.add_to_hass(hass)
    with patch(
        "custom_components.nsw_rural_fire_service_fire_danger.coordinator.NswRfsFireDangerFeedCoordinator.async_update"
    ) as mock_coordinator_update:
        mock_coordinator_update.return_value = {"a": "x", "b": "y"}
        # Load config entry.
        assert await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()
        assert mock_coordinator_update.call_count == 1
        assert hass.data[DOMAIN][config_entry.entry_id] is not None
        # Unload config entry.
        assert await hass.config_entries.async_unload(config_entry.entry_id)
        await hass.async_block_till_done()
        assert hass.data[DOMAIN].get(config_entry.entry_id) is None
        assert config_entry.state is ConfigEntryState.NOT_LOADED
