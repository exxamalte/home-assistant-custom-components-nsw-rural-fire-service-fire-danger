"""Define tests for the NSW Rural Fire Service - Fire Danger config flow."""
from unittest.mock import patch

import pytest
from homeassistant import config_entries, data_entry_flow
from homeassistant.const import CONF_SCAN_INTERVAL

from custom_components.nsw_rural_fire_service_fire_danger import (
    CONF_DISTRICT_NAME,
    DOMAIN,
)


@pytest.mark.asyncio
async def test_duplicate_error(hass, config_entry):
    """Test that errors are shown when duplicates are added."""
    conf = {CONF_DISTRICT_NAME: "Greater Sydney Region"}
    config_entry.add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}, data=conf
    )
    assert result["type"] == data_entry_flow.FlowResultType.ABORT
    assert result["reason"] == "already_configured"


async def test_show_form(hass):
    """Test that the form is served with no input."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == data_entry_flow.FlowResultType.FORM
    assert result["step_id"] == "user"


async def test_step_import(hass):
    """Test that the import step works."""
    conf = {
        CONF_DISTRICT_NAME: "Greater Sydney Region",
    }

    with patch(
        "custom_components.nsw_rural_fire_service_fire_danger.coordinator.NswRfsFireDangerFeedCoordinator.async_update"
    ) as mock_coordinator_update:
        mock_coordinator_update.return_value = {
            "fire_ban_today": True,
            "fire_ban_tomorrow": False,
            "danger_level_today": "Moderate",
            "danger_level_tomorrow": "No Rating",
            "region_number": 4,
        }

        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": config_entries.SOURCE_IMPORT}, data=conf
        )
        assert result["type"] == data_entry_flow.FlowResultType.CREATE_ENTRY
        assert result["title"] == "Greater Sydney Region"
        assert result["data"] == {
            CONF_DISTRICT_NAME: "Greater Sydney Region",
            CONF_SCAN_INTERVAL: 900,
        }


async def test_step_user(hass):
    """Test that the user step works."""
    conf = {CONF_DISTRICT_NAME: "Greater Sydney Region"}

    with patch(
        "custom_components.nsw_rural_fire_service_fire_danger.coordinator.NswRfsFireDangerFeedCoordinator.async_update"
    ) as mock_coordinator_update:
        mock_coordinator_update.return_value = {
            "fire_ban_today": True,
            "fire_ban_tomorrow": False,
            "danger_level_today": "Moderate",
            "danger_level_tomorrow": "No Rating",
            "region_number": 4,
        }

        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": config_entries.SOURCE_USER}, data=conf
        )
        assert result["type"] == data_entry_flow.FlowResultType.CREATE_ENTRY
        assert result["title"] == "Greater Sydney Region"
        assert result["data"] == {
            CONF_DISTRICT_NAME: "Greater Sydney Region",
            CONF_SCAN_INTERVAL: 900,
        }
