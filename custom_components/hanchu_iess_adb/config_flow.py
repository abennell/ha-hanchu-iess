from homeassistant import config_entries
import voluptuous as vol
from homeassistant.helpers.selector import (
    TextSelector,
    TextSelectorConfig,
    TextSelectorType,
)
from .const import DOMAIN  # pylint:disable=unused-import
import logging

_LOGGER = logging.getLogger(__name__)


class IntegrationConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 0
    MINOR_VERSION = 1
    
    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            # Validate user input
            
            valid = True
            if valid:
                # See next section on create entry usage
                return self.async_create_entry(
                    title="Hanchu IESS ADB",
                    data={
                        "username": user_input["username"],
                        "password": user_input["password"]
                    }
                )

            errors["base"] = "auth_error"
            
        # Specify items in the order they are to be displayed in the UI
        data_schema = {
            vol.Required("username"): TextSelector(
                TextSelectorConfig(type=TextSelectorType.EMAIL, autocomplete="username")
            ),
            vol.Required("password"): TextSelector(
                TextSelectorConfig(
                    type=TextSelectorType.PASSWORD, autocomplete="current-password"
                )
            ),
        }

        return self.async_show_form(step_id="user", data_schema=vol.Schema(data_schema), errors=errors)