# _*_ encoding: utf-8 _*_

from parser_helper import HandlerBase
from endpoint_helper import EndPoint
from config import CONTENTS
import os
import json
from config import (WEB_API_URL)

class Categories(HandlerBase):
    """
    Allows download a  file from OSDR BLOB store.
    osdr download {remote-id} [{metadata}]
    Command: download
    """
    info = '''
            name: categories
            help: Create categories
            params:
                -
                    names:
                        - -f
                        - --folder-name
                    dest: folder
                    required: False
                    help: Output folder name
    '''

    def __call__(self):
        # super().__call__()
        ep = EndPoint()
        session = ep.connect()
        with open('categories.json') as categories_json:
            categories_data = json.load(categories_json)
            print(categories_data)
            url = '{}/CategoryTrees/tree'.format(WEB_API_URL)
            print(url)
            resp = ep.post(url, categories_data)
            print(resp)