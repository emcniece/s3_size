import logging
import boto3
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    CONF_BUCKET_NAME,
    CONF_ACCESS_KEY_ID,
    CONF_SECRET_ACCESS_KEY,
    CONF_REGION_NAME,
    CONF_ENDPOINT_URL,
    DEFAULT_REGION_NAME,
    DEFAULT_ENDPOINT_URL,
    ATTR_BUCKET_NAME,
    ATTR_OBJECT_COUNT,
    ATTR_TOTAL_SIZE,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


class S3SizeSensor(RestoreEntity):
    """Representation of an S3 size sensor."""

    def __init__(self, aws_config: dict, bucket_name: str):
        """Initialize the sensor."""
        self._bucket_name = bucket_name
        self._s3 = boto3.client("s3", **aws_config)
        self._object_count = None
        self._total_size = None
        self._state = None
        self._attributes = {}

    @property
    def bucket_name(self) -> str:
        """Return the bucket name."""
        return self._bucket_name

    @property
    def s3_client(self):
        """Return the S3 client."""
        return self._s3

    async def async_added_to_hass(self):
        """Register services and restore last state."""
        _LOGGER.info("Adding S3 size sensor to Home Assistant")
        self.hass.services.async_register(DOMAIN, "s3_size_update", self.s3_size_update)
        last_state = await self.async_get_last_state()
        if last_state is not None:
            self._state = last_state.state
            self._attributes = dict(last_state.attributes)

    async def async_will_remove_from_hass(self):
        """Unregister services."""
        _LOGGER.info("Removing S3 size sensor from Home Assistant")
        self.hass.services.async_remove(DOMAIN, "s3_size_update")

    async def s3_size_update(self, call):
        """Update the sensor."""
        total_size = 0
        object_count = 0
        continuation_token = None

        while True:
            list_objects_args = {}
            if continuation_token:
                list_objects_args["ContinuationToken"] = continuation_token

            objects = await self.hass.async_add_executor_job(
                lambda: self._s3.list_objects_v2(
                    Bucket=self._bucket_name, **list_objects_args
                )
            )

            contents = objects.get("Contents", [])
            total_size += sum(obj["Size"] for obj in contents)
            object_count += len(contents)
            if objects.get("IsTruncated"):
                continuation_token = objects.get("NextContinuationToken")
            else:
                break

        self._object_count = object_count
        self._total_size = total_size

        if self._total_size is None:
            self._state = None
        else:
            self._state = round(self._total_size / 1_000_000_000, 2)

        self._attributes = {
            ATTR_BUCKET_NAME: self._bucket_name,
            ATTR_OBJECT_COUNT: self._object_count,
            ATTR_TOTAL_SIZE: self._total_size,
        }

        self.async_write_ha_state()

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return f"S3 Size ({self._bucket_name})"

    @property
    def unique_id(self) -> str:
        """Return the unique ID of the sensor."""
        return f"s3_size_{self._bucket_name}"

    @property
    def state(self) -> float:
        """Return the current size of the bucket in GB."""
        return self._state

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement of the sensor."""
        return "GB"

    @property
    def device_class(self) -> str:
        """Return the device class of the sensor."""
        return "storage"

    @property
    def state_attributes(self) -> dict:
        """Return the state attributes of the sensor."""
        return self._attributes


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
):
    """Set up the S3 size sensor."""
    aws_config = {
        "region_name": entry.data.get(CONF_REGION_NAME, DEFAULT_REGION_NAME),
        "aws_access_key_id": entry.data[CONF_ACCESS_KEY_ID],
        "aws_secret_access_key": entry.data[CONF_SECRET_ACCESS_KEY],
        "endpoint_url": entry.data.get(CONF_ENDPOINT_URL, DEFAULT_ENDPOINT_URL),
    }

    sensor = S3SizeSensor(aws_config, entry.data[CONF_BUCKET_NAME])
    async_add_entities([sensor])
