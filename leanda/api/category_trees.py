from leanda.config import config
from leanda.api.http import get


def get_categories():
    url = f'{config.web_core_api_url}/CategoryTrees/tree'
    return get(url).json()
