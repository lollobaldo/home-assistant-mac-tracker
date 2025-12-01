from datetime import timedelta
import logging
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.components.device_tracker.config_entry import TrackerEntity
from homeassistant.core import HomeAssistant
from .scanner import scan_network, is_mac_online
from .const import DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)

class MacTrackerEntity(TrackerEntity):
    def __init__(self, coordinator, device):
        self.coordinator = coordinator
        self.device = device
        self._attr_unique_id = device.get("unique_id") or device["mac"]
        self._attr_name = device["name"]
        self._mac = device["mac"]

    async def async_added_to_hass(self):
        """Called when entity is added to HA."""
        self.coordinator.async_add_listener(self._handle_coordinator_update)
        # optionally force an immediate refresh of state
        self._handle_coordinator_update()

    def _handle_coordinator_update(self):
        self.async_write_ha_state()
