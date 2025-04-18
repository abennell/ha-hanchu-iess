"""A demonstration 'hub' that connects several devices."""
from __future__ import annotations

# In a real implementation, this would be in an external library that's on PyPI.
# The PyPI package needs to be included in the `requirements` section of manifest.json
# See https://developers.home-assistant.io/docs/creating_integration_manifest
# for more information.
# This dummy hub always returns 3 rollers.
import asyncio
import random

from homeassistant.core import HomeAssistant


class Hub:
    manufacturer = "HANCHUESS"

    def __init__(self, hass: HomeAssistant, username: str, password: str) -> None:
        self._host = "https://iess3.hanchuess.com/"
        self._username = username
        self._password = password
        self._hass = hass
        self._name = self.manufacturer
        self._id = f"{self.manufacturer}_HUB_ADB".lower()
        self.inverters = [
            Inverter(id=f"{self._id}_1", 
                    serial_number="H016174360031",
                    brand="HANCHU",
                    model="HESS-HY-S-6.0K",
                    rated_power="6000",
                    hub=self)
        ]
        self.online = True

    @property
    def hub_id(self) -> str:
        """ID for dummy hub."""
        return self._id

    async def test_connection(self) -> bool:
        """Test connectivity to the Dummy hub is OK."""
        await asyncio.sleep(1)
        return True

class Inverter:
    """Dummy roller (device for HA) for Hello World example."""

    def __init__(self, id: str, serial_number: str, brand: str, model: str, rated_power: int, hub: Hub) -> None:
        """Init dummy roller."""
        self._id = id
        self.hub = hub
        self._serial_number = serial_number
        self._brand = brand
        self._model = model
        self._rated_power = rated_power
        self._callbacks = set()
        self._loop = asyncio.get_event_loop()
        self._target_position = 100
        self._current_position = 100
        # Reports if the roller is moving up or down.
        # >0 is up, <0 is down. This very much just for demonstration.
        self.moving = 0

        # Some static information about this device
        self.firmware_version = f"0.0.{random.randint(1, 9)}"

    @property
    def id(self) -> str:
        """Return ID for inverter."""
        return self._id
    
    @property
    def serial_number(self) -> str:
        """Return serial number for inverter."""
        return self._serial_number
    
    @property
    def brand(self) -> str:
        """Return brand for inverter."""
        return self._brand
    
    @property
    def model(self) -> str:
        """Return model for inverter."""
        return self._model

    @property
    def rated_power(self) -> str:
        """Return model for inverter."""
        return self._rated_power

    @property
    def position(self):
        """Return position for roller."""
        return self._current_position

    async def set_position(self, position: int) -> None:
        """
        Set dummy cover to the given position.

        State is announced a random number of seconds later.
        """
        self._target_position = position

        # Update the moving status, and broadcast the update
        self.moving = position - 50
        await self.publish_updates()

        self._loop.create_task(self.delayed_update())

    async def delayed_update(self) -> None:
        """Publish updates, with a random delay to emulate interaction with device."""
        await asyncio.sleep(random.randint(1, 10))
        self.moving = 0
        await self.publish_updates()

    def register_callback(self, callback: Callable[[], None]) -> None:
        """Register callback, called when Roller changes state."""
        self._callbacks.add(callback)

    def remove_callback(self, callback: Callable[[], None]) -> None:
        """Remove previously registered callback."""
        self._callbacks.discard(callback)

    # In a real implementation, this library would call it's call backs when it was
    # notified of any state changeds for the relevant device.
    async def publish_updates(self) -> None:
        """Schedule call all registered callbacks."""
        self._current_position = self._target_position
        for callback in self._callbacks:
            callback()

    @property
    def online(self) -> float:
        """Roller is online."""
        # The dummy roller is offline about 10% of the time. Returns True if online,
        # False if offline.
        return random.random() > 0.1

    @property
    def battery_level(self) -> int:
        """Battery level as a percentage."""
        return random.randint(0, 100)

    @property
    def battery_voltage(self) -> float:
        """Return a random voltage roughly that of a 12v battery."""
        return round(random.random() * 3 + 10, 2)

    @property
    def illuminance(self) -> int:
        """Return a sample illuminance in lux."""
        return random.randint(0, 500)