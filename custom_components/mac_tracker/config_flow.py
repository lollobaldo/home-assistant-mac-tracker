from __future__ import annotations

import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant import config_entries
from homeassistant.core import callback

from .const import DOMAIN, CONF_PERSON, CONF_NAME, CONF_MAC

class MacPresenceConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
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
        person_comp = self.hass.data.get("person")
        if not person_comp:
            return []
        return {p["name"]: p["id"] for p in person_comp.persons}

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return MacPresenceOptionsFlow(config_entry)


class MacPresenceOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, entry):
        self.entry = entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        schema = vol.Schema({
            vol.Required(CONF_MAC, default=self.entry.options.get(CONF_MAC, self.entry.data[CONF_MAC])): cv.string
        })

        return self.async_show_form(step_id="init", data_schema=schema)
