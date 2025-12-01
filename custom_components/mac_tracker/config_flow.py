from __future__ import annotations
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN, CONF_PERSON, CONF_NAME, CONF_MAC

class MacTrackerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            # Default name if not provided
            if not user_input.get(CONF_NAME):
                user_input[CONF_NAME] = f"{user_input[CONF_PERSON]}'s phone"
            return self.async_create_entry(
                title=user_input[CONF_NAME],
                data=user_input
            )

        persons = self._get_persons()
        schema = vol.Schema({
            vol.Required(CONF_PERSON): vol.In(persons),
            vol.Required(CONF_MAC): cv.string,
            vol.Optional(CONF_NAME): cv.string,
        })
        return self.async_show_form(step_id="user", data_schema=schema)

    def _get_persons(self):
        """Return dict of person name -> entity_id."""
        return {
            state.name: state.entity_id
            for state in self.hass.states.async_all()
            if state.domain == "person"
        }

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return MacTrackerOptionsFlow(config_entry)


class MacTrackerOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, entry):
        self.entry = entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        schema = vol.Schema({
            vol.Required("mac", default=self.entry.options.get("mac", self.entry.data[CONF_MAC])): cv.string
        })
        return self.async_show_form(step_id="init", data_schema=schema)
