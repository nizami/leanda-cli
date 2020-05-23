from os import path
import json


class Config:
    web_core_api_url: str
    web_blob_api_url: str
    web_socket_url: str
    identity_server_url: str
    file_upload_limit: int
    file_download_limit: int

    def __init__(self, config_path):
        config_path = path.join(path.abspath(
            path.dirname(__file__)), config_path)

        with open(config_path, 'r') as f:
            self.__dict__ = json.load(f)


config = Config('./config.dev.json')
