"""Custom component to get the size of an S3 bucket."""
import logging

from homeassistant.core import HomeAssistant
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the S3 size sensor component."""
    return True

async def async_setup_entry(hass, entry):
    """Set up the S3 size sensor platform from a config entry."""
    hass.async_create_task(hass.config_entries.async_forward_entry_setup(entry, "sensor"))
    return True

async def async_unload_entry(hass, entry):
    """Unload the S3 size sensor platform."""
    await hass.config_entries.async_forward_entry_unload(entry, "sensor")
    return True
