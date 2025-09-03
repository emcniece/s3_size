"""Constants for the S3 size sensor platform."""

DOMAIN = "s3_size"

CONF_BUCKET_NAME = "bucket_name"
CONF_ACCESS_KEY_ID = "aws_access_key_id"
CONF_SECRET_ACCESS_KEY = "aws_secret_access_key"
CONF_REGION_NAME = "region_name"
CONF_ENDPOINT_URL = "endpoint_url"

ATTR_BUCKET_NAME = "bucket_name"
ATTR_OBJECT_COUNT = "object_count"
ATTR_TOTAL_SIZE = "total_size"

DEFAULT_REGION_NAME = "us-east-1"
DEFAULT_ENDPOINT_URL = "https://s3.us-east-1.amazonaws.com"
