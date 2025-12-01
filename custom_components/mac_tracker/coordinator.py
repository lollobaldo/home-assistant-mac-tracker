from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from .const import CONF_MAC, DEFAULT_SCAN_INTERVAL
from .scanner import ping_mac

_LOGGER = logging.getLogger(__name__)

class MacPresenceCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry):
        super().__init__(
            hass,
            _LOGGER,
            name=f"MAC Presence {entry.title}",
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )
        self.entry = entry
        self.mac = entry.data[CONF_MAC]

    async def _async_update_data(self):
        return await self.hass.async_add_executor_job(ping_mac, self.mac)
