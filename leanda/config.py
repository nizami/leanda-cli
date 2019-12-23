# _*_ encoding: utf-8 _*_
import os
from os.path import exists, expanduser
import pickle

def get_or_update_config(dict = None):
    config = {}
    leanda_dir = '{}/.leanda'.format(expanduser('~'))
    config_path = '{}/config'.format(leanda_dir)
    if exists(config_path):
        with open(config_path, "rb") as f:
            config = pickle.load(f)
            if dict: config.update(dict)
    with open(config_path, "wb") as f:
        pickle.dump(config, f)
    return config

DEBUG = True
if 'OAUTHLIB_INSECURE_TRANSPORT' not in os.environ.keys():
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

config = get_or_update_config()
WEB_API_URL = config['WEB_API_URL'] or 'http://localhost:28611/api'
WEB_STORAGE_API_URL = config['WEB_STORAGE_API_URL'] or 'http://localhost/blob/v1/api'
WEB_SOCKET_URL = config['WEB_SOCKET_URL'] or 'ws://localhost/core-api/v1'
IDENTITY_SERVER_URL = config['IDENTITY_SERVER_URL'] or 'https://id.leanda.io/auth/realms/OSDR'

TOKEN_URL = '{}/protocol/openid-connect/token'.format(IDENTITY_SERVER_URL)
ME_URL = '%s/me' % WEB_API_URL

SIGNALR_URL = '%s/signalr' % WEB_SOCKET_URL

NODE = '%s/nodes/{}' % WEB_API_URL
CONTENTS = '%s/nodes/{}/nodes' % WEB_API_URL
BROWSE_CONTENTS = '%s/nodes/{cwd}/nodes?PageNumber={page}&PageSize={size}' % WEB_API_URL

DOWNLOAD = '%s/entities/files/{file_id}/blobs/{id}' % WEB_API_URL
UPLOAD = '%s/blobs/{id}' % WEB_STORAGE_API_URL
REMOVE = '%s/nodecollections' % WEB_API_URL

TRAIN = '%s/machinelearning/models' % WEB_API_URL
PREDICT = '%s/machinelearning/predictions' % WEB_API_URL

LIST_MODELS = '%s/entities/files' % WEB_API_URL

FILE = 'File'
FOLDER = 'Folder'

MACHINE_LEARNING_MODEL = {'FileType': 'MachineLearningModel', }

ID_PATTERN = r'([0-9a-f]){8}-([0-9a-f]){4}-([0-9a-f]){4}-([0-9a-f]){4}-([0-9a-f]){12}'

LAST_UPDATED = '.updated.leanda'

REMOVE_DATA = '''
              [{"value": [{"id": "%s", "type": "File"}],
                "path": "/deleted",
                "op": "add",
              }]
              '''