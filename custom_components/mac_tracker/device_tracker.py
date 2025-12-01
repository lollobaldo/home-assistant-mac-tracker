from homeassistant.components.device_tracker.config_entry import TrackerEntity
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

    async def async_added_to_hass(self):
        self.coordinator.async_add_listener(self._handle_coordinator_update)
        self._handle_coordinator_update()

    def _handle_coordinator_update(self):
        if self.hass is None:
            return
        self.async_write_ha_state()

    @property
    def is_connected(self):
        return self.coordinator.data.get(self._mac.lower(), False)

    @property
    def extra_state_attributes(self):  # type: ignore
        return {"ip": self.device.get("last_ip")}
