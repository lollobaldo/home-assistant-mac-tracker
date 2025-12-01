import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN
from .coordinator import MacTrackerCoordinator

_LOGGER = logging.getLogger(__name__)
PLATFORMS = ["device_tracker"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up MAC Tracker from a config entry."""

    # collect all configured devices
    devices = []
    for e in hass.config_entries.async_entries(DOMAIN):
        devices.append({
            "mac": e.data["mac"],
            "name": e.data.get("name"),
            "unique_id": e.entry_id,
            "last_ip": None,
        })

    coordinator = MacTrackerCoordinator(hass, devices)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})["coordinator"] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop("coordinator", None)
    return unload_ok
