from list_items import ListItems
import re

patt = re.compile(r'(name:\s+)(.+)?(\s)')


class ListRecordsets(ListItems):
    """
    Allows to list recordsets from Leanda using queries.
    """

    info = patt.sub(r'\1recordsets\3', ListItems.info)

    FILTER = [
        # ('SubType', 'eq', "'Model'"),
        ('SubType', 'eq', "'Records'"),
        ('Status', 'eq', "'Processed'")
    ]

    def _valid_rec(self, record):
        try:
            return len(record['properties']['chemicalProperties']) > 1 \
                   and len(record['properties']['fields']) > 1
        except KeyError:
            return False
