# _*_ encoding: utf-8 _*_

from leanda.parser_helper import HandlerBase
from leanda.endpoint_helper import EndPoint
from leanda.config import LIST_MODELS
import json
import yaml
from clint.textui import colored
from urllib.parse import quote


class ListItems(HandlerBase):
    """
    Allows to list contents of Leanda using queries.
    """
    url = 'https://api.dataledger.io/osdr/v1/api/me'
    info = '''
            name: items
            help: Allows to list contents of Leanda using queries.
            params:
                -
                    names:
                        - -q
                        - --query
                    help: Filter models by subquery

                -
                    names:
                        - -n
                        - --name
                    help: Filter models by substring

                -
                    names:
                        - -s
                        - --short-notation
                    help: |
                        Path to yaml file with list of short notations
                        Example - p.radius:
                            MachineLearningModelInfo.Fingerprints.Radius
                -
                    names:
                        - -v
                        - --verbosity
                    default: 0
                    action: count
                    help: >
                        Set verbosity level. 
                        -v - display query string,
                        -vv - display records,
                -
                    names:
                        - -f
                        - --format
                    choices:
                        - json
                        - yaml
                    default:
                    help: Set model verbosity output format

    '''
    OPS = "".maketrans({'>': 'gt', '<': 'lt', '=': 'eq'})
    QUOTES = "".maketrans('', '', "'\"")

    FILTER = [
                ('Status',  'eq', "'Processed'")
            ]

    HIDE_FIELDS = ['createdBy', 'createdDateTime', 'images', 'ownedBy', 'parentId',
                   'updatedBy', 'updatedDateTime', 'status', 'version', 'blob',
                   ]

    def _valid_rec(self, record):
        return True

    def _get_subquery(self, subquery):
        ops = []
        for item in subquery.split(','):
            for op in '<>=':
                opset = item.partition(op)
                opset = list(opset)
                if all(opset):
                    opset[1] = opset[1].translate(self.OPS)
                    try:
                        int(opset[2])
                    except ValueError:
                        opset[2] = opset[2].translate(self.QUOTES)
                        opset[2] = "'{}'".format(opset[2])
                    ops.append(list(opset))
        for idx, item in enumerate(ops):
            pname = self.TRAIN_PARAMS.get(item[0].strip().lower())
            if not pname:
                continue
            ops[idx][0] = pname

        return ops

    def __call__(self):
        if self.short_notation:
            self.TRAIN_PARAMS = yaml.load(open(self.short_notation))
            if self.query:
                self.FILTER.extend(self._get_subquery(self.query))

        query = [' '.join(qitem) for qitem in self.FILTER]
        query = " and ".join(query)

        if self.query and not self.short_notation:
            query += ' and ' + self.query

        if self.verbosity > 0: print(query)
        if self.verbosity > 2: self.HIDE_FIELDS.remove('blob')

        ep = EndPoint()
        session = ep.connect()

        url = "{0}?$filter={1}".format(LIST_MODELS, quote(query))
        resp = ep.get(url)
        # pprint.pprint(resp)
        assert resp.ok, 'Error getting data'
        models = resp.json()
        ids = [rec['id'] for rec in models]
        # pprint.pprint(ids)

        if self.name:
            self.name = self.name.casefold()

        for id in ids:
            recs = filter(lambda x: x['id'] == id, models)
            recs = list(recs)
            rec = recs[0]
            if not self._valid_rec(rec):
                continue

            if self.name:
                has_substring = [self.name in rec.get('name', '').casefold(),
                                 self.name in rec.get('className', '').casefold(),
                                 self.name in rec.get('method', '').casefold(),
                                 ]
                if not any(has_substring):
                    continue

            path, _ = ep.get_full_path(id)
            if not path: continue
            mf = "{id}\t{path}".format(path=path, id=id)
            print(colored.green(mf))
            if self.verbosity > 1:
                # print(url)
                for key in self.HIDE_FIELDS:
                    if key in rec:
                        del rec[key]
                if self.format == 'json':
                    print(json.dumps(rec))
                else:
                    print(yaml.dump(rec))
