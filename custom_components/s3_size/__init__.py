"""Custom component to get the size of an S3 bucket."""

import logging
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the S3 size sensor component."""
    _LOGGER.info("Setting up S3 size sensor component")
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up the S3 size sensor platform from a config entry."""
    _LOGGER.info(f"Setting up S3 size sensor platform for entry: {entry.entry_id}")
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload the S3 size sensor platform."""
    _LOGGER.info(f"Unloading S3 size sensor platform for entry: {entry.entry_id}")
    await hass.config_entries.async_forward_entry_unload(entry, "sensor")
    return True
