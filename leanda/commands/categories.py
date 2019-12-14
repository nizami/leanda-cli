# _*_ encoding: utf-8 _*_

from leanda.parser_helper import HandlerBase
from leanda.endpoint_helper import EndPoint
from leanda.config import CONTENTS
import os
import json
from leanda.config import (WEB_API_URL)
from leanda.api import Api


class Categories(HandlerBase):
    """
    Allows download a  file from Leanda BLOB store.
    leanda download {remote-id} [{metadata}]
    Command: download
    """
    info = '''
            name: categories
            help: Create categories
            params:
                -
                    names:
                        - -rm
                        - --remove
                    action: store_true
                    help: Remove all categories
                -
                    names:
                        - -i
                        - --init
                    action: store_true
                    help: Initialize categories from categories.json file data
    '''
    api: Api

    def __call__(self):
        self.api = Api()
        url = '{}/CategoryTrees/tree'.format(WEB_API_URL)
        get_resp = self.api.get(url)
        if self.init:
            if not len(get_resp.json()):
                with open('categories.json') as categories_json:
                    categories_data = json.load(categories_json)
                    resp = self.api.post(url, categories_data)
                    print(resp)
            else:
                print('Can\'t create a tree. It is already exists')
        elif self.remove:
            for node in get_resp.json():
                resp = self.api.delete(
                    url+'/{id}?version={version}'.format(**node))
                print(resp)
        else:
            print(json.dumps(get_resp.json(), indent=4))
