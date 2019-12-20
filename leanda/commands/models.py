import re
from list_items import ListItems

patt = re.compile(r'(name:\s+)(.+)?(\s)')


class ListModels(ListItems):
    """
    Allows to list models from Leanda using queries.
    """

    info = patt.sub(r'\1models\3', ListItems.info)
    FILTER = [
        ('SubType', 'eq', "'Model'"),
        # ('SubType', 'eq', "'Records'"),
        ('Status', 'eq', "'Processed'")
    ]
