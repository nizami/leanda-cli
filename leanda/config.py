import humanfriendly
import json
import logging
import os
import sys

from dotenv import load_dotenv
from os import path
from pathlib import Path

from leanda import logger

logger.initialize()
logger = logging.getLogger('config')

env_path = Path('.') / 'environments/dev.env'
load_dotenv(dotenv_path=env_path)


class Config:
    web_core_api_url = os.getenv("LEANDA_WEB_CORE_API_URL")
    web_blob_api_url = os.getenv("LEANDA_WEB_BLOB_API_URL")
    web_socket_url = os.getenv("LEANDA_WEB_SOCKET_URL")
    identity_server_url = os.getenv("LEANDA_IDENTITY_SERVER_URL")
    file_upload_limit = os.getenv("LEANDA_FILE_UPLOAD_LIMIT")
    file_upload_limit_int = humanfriendly.parse_size(
        os.getenv("LEANDA_FILE_UPLOAD_LIMIT") or '50MB', binary=True)
    file_download_limit = os.getenv("LEANDA_FILE_DOWNLOAD_LIMIT")
    file_download_limit_int = humanfriendly.parse_size(
        os.getenv("LEANDA_FILE_DOWNLOAD_LIMIT") or '50MB', binary=True)


config = Config()
logger.debug(config)
