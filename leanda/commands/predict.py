# _*_ encoding: utf-8 _*_

import json
from ..parser_helper import HandlerBase
from ..endpoint_helper import EndPoint
from ..config import CONTENTS, NODE, PREDICT


class Predict(HandlerBase):
    """
    leanda predict
    Allows to run Machine Learning command predict.
    """
    url = 'https://api.dataledger.io/osdr/v1/api/me'
    info = '''
            name: predict
            help: Allows to run Machine Learning command predict.
            params:
                -
                    names:
                        - -f
                        - --folder-name
                    dest: folder
                    required: True
                    help: Output folder name
                -
                    names:
                        - -m
                        - --model
                    required: True
                    help: Leanda model's file id.
                -
                    names:
                        - -r
                        - --recordset
                    required: True
                    help: Leanda recordsets's file id.
    '''

    def __call__(self):
        ep = EndPoint()
        session = ep.connect()
        list_url = CONTENTS.format(session['cwd'])

        # Container 
        records = ep.get_containers(list_url)
        try:
            ep.get_uniq_container(records, self.folder)
            raise RuntimeError(
                "Model container '{}' already exists".format(self.folder))
        except AssertionError:
            pass

        # Recordset
        resp = ep.get(NODE.format(self.recordset))
        recordset = resp.json()
        assert recordset['subType'] == 'Records'

        # Model
        resp = ep.get(NODE.format(self.model))
        model = resp.json()
        assert model['subType'] == 'Model'

        query = {
            'UserId': session['owner'],
            'ParentId': session['cwd'],
            'FolderName': self.folder,
            'DatasetBlobId': recordset['blob']['id'],
            'DatasetBucket': recordset['blob']['bucket'],
            'ModelBlobId': model['blob']['id'],
            'ModelBucket': model['blob']['bucket'],
        }
        # print(query)

        resp = ep.post(PREDICT, data=query)
        result = resp.json()
        assert result['modelFolderId'], \
            "Error training model '{}'".format(model_name)
