from __future__ import annotations

from homeassistant.components.device_tracker.config_entry import TrackerEntity
from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.core import callback
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, CONF_NAME, CONF_PERSON, CONF_MAC

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([MacPresenceEntity(coordinator)])


class MacPresenceEntity(TrackerEntity):
    def __init__(self, coordinator):
        self.coordinator = coordinator
        self._attr_unique_id = f"mac_presence_{coordinator.mac}"

        self._person = coordinator.entry.data.get(CONF_PERSON)
        self._name = coordinator.entry.data.get(CONF_NAME)
        self._mac = coordinator.mac

        self._attr_name = self._name

    @property
    def is_connected(self) -> bool:
        return self.coordinator.data

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self._attr_unique_id)},
            name=self._name,
            model="MAC Presence Tracker",
            manufacturer="Custom",
            entry_type=DeviceEntryType.SERVICE,
        )

    @callback
    def _handle_coordinator_update(self):
        self.async_write_ha_state()
