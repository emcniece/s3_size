import logging
import boto3
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant import config_entries
from .const import (
    CONF_BUCKET_NAME,
    CONF_ACCESS_KEY_ID,
    CONF_SECRET_ACCESS_KEY,
    CONF_REGION_NAME,
    DEFAULT_REGION_NAME,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_BUCKET_NAME): cv.string,
        vol.Required(CONF_ACCESS_KEY_ID): cv.string,
        vol.Required(CONF_SECRET_ACCESS_KEY): cv.string,
        vol.Optional(CONF_REGION_NAME, default=DEFAULT_REGION_NAME): cv.string,
    }
)

async def validate_credentials(
    aws_access_key_id: str, aws_secret_access_key: str, region_name: str
) -> bool:
    """Validate AWS credentials."""
    try:
        aws_config = {
            CONF_REGION_NAME: region_name,
            CONF_ACCESS_KEY_ID: aws_access_key_id,
            CONF_SECRET_ACCESS_KEY: aws_secret_access_key,
        }
        s3 = boto3.client("s3", **aws_config)
        await s3.list_buckets()
        return True
    except Exception:
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
            await validate_credentials(aws_access_key_id, aws_secret_access_key, region_name)
            return self.async_create_entry(title=bucket_name, data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=DATA_SCHEMA,
            errors=errors,
        )
