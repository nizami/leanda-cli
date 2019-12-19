# _*_ encoding: utf-8 _*_

from ..parser_helper import HandlerBase
from ..endpoint_helper import EndPoint


class Convert(HandlerBase):
    """
    leanda convert
    Convert the user to convert files.
    """
    url = 'https://api.dataledger.io/osdr/v1/api/me'
    info = '''
            name: convert
            help: Convert the user to convert files.
    '''

    def __call__(self):
        # super().__call__()
        ep = EndPoint()
        session = ep.connect()
