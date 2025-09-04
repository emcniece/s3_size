""" Config Flow for S3 Size Integration """

import logging
import boto3
import botocore.exceptions
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant import config_entries
from .const import (
    CONF_BUCKET_NAME,
    CONF_ACCESS_KEY_ID,
    CONF_SECRET_ACCESS_KEY,
    CONF_REGION_NAME,
    CONF_ENDPOINT_URL,
    DEFAULT_REGION_NAME,
    DEFAULT_ENDPOINT_URL,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_BUCKET_NAME): cv.string,
        vol.Required(CONF_ACCESS_KEY_ID): cv.string,
        vol.Required(CONF_SECRET_ACCESS_KEY): cv.string,
        vol.Optional(CONF_REGION_NAME, default=DEFAULT_REGION_NAME): cv.string,
        vol.Optional(CONF_ENDPOINT_URL, default=DEFAULT_ENDPOINT_URL): cv.string,
    }
)


async def validate_credentials(
    hass, aws_access_key_id: str, aws_secret_access_key: str, region_name: str, endpoint_url: str
) -> bool:
    """Validate AWS credentials."""
    try:
        aws_config = {
            CONF_REGION_NAME: region_name,
            CONF_ACCESS_KEY_ID: aws_access_key_id,
            CONF_SECRET_ACCESS_KEY: aws_secret_access_key,
            CONF_ENDPOINT_URL: endpoint_url,
        }
        s3 = boto3.client("s3", **aws_config)

        # Run list_buckets in a separate thread
        await hass.async_add_executor_job(s3.list_buckets)

        return True
    except botocore.exceptions.BotoCoreError as e:
        _LOGGER.error("Invalid AWS credentials: %s", e)
        return False


class S3SizeFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for the S3 size sensor platform."""

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            bucket_name = user_input[CONF_BUCKET_NAME]
            aws_access_key_id = user_input[CONF_ACCESS_KEY_ID]
            aws_secret_access_key = user_input[CONF_SECRET_ACCESS_KEY]
            region_name = user_input[CONF_REGION_NAME]
            endpoint_url = user_input[CONF_ENDPOINT_URL]
            valid_credentials = await validate_credentials(
                self.hass,  # add this
                aws_access_key_id,
                aws_secret_access_key,
                region_name,
                endpoint_url,
            )
            if not valid_credentials:
                errors["base"] = "invalid_credentials"
            else:
                return self.async_create_entry(title=bucket_name, data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=DATA_SCHEMA,
            errors=errors,
        )
