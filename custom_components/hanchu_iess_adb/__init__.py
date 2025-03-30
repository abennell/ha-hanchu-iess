from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN  # pylint:disable=unused-import



async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    hass.states.async_set('hello_world_async.Hello_World', 'Works!')

    # Return boolean to indicate that initialization was successful.
    return True