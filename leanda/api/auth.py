import json
import logging
import requests

from leanda.config import config
from leanda.session import session

logger = logging.getLogger('auth')


def login(username, password):
    token_url = f'{config.identity_server_url}/protocol/openid-connect/token'
    me_url = f'{config.web_core_api_url}/me'
    data = {'grant_type': 'password',
            'client_id': 'leanda_cli',
            'username': username, 'password': password, }
    try:
        res = requests.post(token_url, data=data)
    except requests.exceptions.ConnectionError as err:
        logger.exception(err)
        exit()
    assert res.ok, 'Authorization Error'

    token = '{token_type} {access_token}'.format(**res.json())
    headers = {
        'Accept': 'application/json',
        'Authorization': token
    }
    res = requests.get(me_url, headers=headers)
    owner = res.json()['id']
    info = {'token': token}
    if not session.token:
        info.update({'cwd': owner, 'owner': owner})
    session.update(info)
    logger.info('Logged in as {firstName} {lastName}'.format(**res.json()))
    return res.json()
