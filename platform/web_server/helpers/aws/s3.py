import boto3
import logging
from PIL import Image

from web_server.settings import (
    AWS_ACCESS_KEY_ID,
    AWS_LOCATION,
    AWS_SECRET_ACCESS_KEY,
    AWS_STORAGE_BUCKET_NAME,
)


logger = logging.getLogger(__name__)


s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)


# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html
def upload_image(source_filename: str, file_path: str) -> str:
    location = f"{AWS_LOCATION}/{file_path}"
    try:
        s3_client.upload_file(source_filename, AWS_STORAGE_BUCKET_NAME, location)
    except ValueError as e:
        logger.error(f"error trying to upload from {source_filename} {location} to s3: {e}")
        raise(e)
    return f"https://gamers-service.s3.us-west-1.amazonaws.com/{location}"
