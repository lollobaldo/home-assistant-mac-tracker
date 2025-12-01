import logging
from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.core import HomeAssistant
from .scanner import scan_network, is_mac_online
from .const import DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)

class MacTrackerCoordinator(DataUpdateCoordinator):
    """Coordinator that scans network and updates all devices."""

    def __init__(self, hass: HomeAssistant, devices: list[dict]):
        super().__init__(
            hass,
            _LOGGER,
            name="MAC Tracker Coordinator",
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )
        self.devices = devices
        self.scan_results = {}

    async def _async_update_data(self):
        results = await self.hass.async_add_executor_job(scan_network)
        self.scan_results = {mac: ip for mac, ip in results}

        online_status = {}
        for device in self.devices:
            mac = device["mac"].lower()
            online, ip = is_mac_online(mac, results)
            device["last_ip"] = ip
            online_status[mac] = online
            _LOGGER.debug("Device %s online: %s, IP: %s", device["name"], online, ip)

        return online_status
