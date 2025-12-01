from homeassistant.components.device_tracker.config_entry import TrackerEntity
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.device_registry import DeviceEntryType
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN]["coordinator"]
    async_add_entities([MacTrackerEntity(coordinator, device) for device in coordinator.devices])

class MacTrackerEntity(TrackerEntity):
    def __init__(self, coordinator, device):
        self.coordinator = coordinator
        self.device = device
        self._attr_unique_id = device.get("unique_id") or device["mac"]
        self._attr_name = device["name"]
        self._mac = device["mac"]

        self.coordinator.async_add_listener(self._handle_coordinator_update)

    @property
    def is_connected(self):
        return self.coordinator.data.get(self._mac.lower(), False)

    @property
    def extra_state_attributes(self):
        return {"ip": self.device.get("last_ip")}

    def _handle_coordinator_update(self):
        self.async_write_ha_state()

    async def async_update(self):
        """Force update from coordinator."""
        await self.coordinator.async_request_refresh()
