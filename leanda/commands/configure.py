# _*_ encoding: utf-8 _*_
import os
import json

from parser_helper import HandlerBase
from endpoint_helper import EndPoint
from config import CONTENTS, get_or_update_config


class Configure(HandlerBase):
    """
    Allows download enter configuration information
    """
    info = '''
            name: configure
            help: Set leanda-cli configuration
    '''
    def __call__(self):
        params = ['WEB_API_URL', 'WEB_STORAGE_API_URL', 'WEB_SOCKET_URL', 'IDENTITY_SERVER_URL']
        config = get_or_update_config() 

        print('Set the following parameters or leave empty to skip:')
        for param in params:
            config[param] = input(param + ': ') or param in config and config[param] or ''
        
        config = get_or_update_config(config)
        print('Configuration saved as:\n', json.dumps(config, indent=4))
