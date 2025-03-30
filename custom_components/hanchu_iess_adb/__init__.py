from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

DOMAIN = "hanchu_iess_adb"


async def async_setup(hass: HomeAssistant, config) -> bool:
    hass.states.async_set('hello_world_async.Hello_World', 'Works!')

    # Return boolean to indicate that initialization was successful.
    return True