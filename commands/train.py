# _*_ encoding: utf-8 _*_

from parser_helper import HandlerBase
from endpoint_helper import EndPoint
from config import CONTENTS, TRAIN
import os
import pprint


class Train(HandlerBase):
    """
    leanda train
    Allows to run Machine Learning command train.
    """
    url = 'https://api.dataledger.io/osdr/v1/api/me'
    info = '''
            name: train
            help: Allows to run Machine Learning command train.
            params:
                -
                    names:
                        - container
                    help: >
                          Remote Leanda SDF file id.
                          Leanda file can be choosed by its
                          full id system wide or by substring in
                          current Leanda folder.
                          Substring compared to filename starting
                          from the beggining or to file id ending.
                -
                    names:
                        - -m
                        - --meta
                    dest: path
                    required: True
                    help: Model metadata in json or yaml formats
                -
                    names:
                        - -f
                        - --folder-name
                    dest: name
                    help: Output folder name

   '''

    def __set_model_meta(self, file_name):
        assert os.path.isfile(self.path), \
            "File '{path}' does not exists.".format(path=self.path)
        model_meta = self.get_meta(filepath=self.path)
        if self.name:
            model_meta.update({'modelName': self.name, })

        if not model_meta.get('modelName'):
            name = file_name[:file_name.lower().rindex('.sdf')]
            model_meta.update({'modelName': "{}.model".format(name), })

        model_meta.update({'sourceFileName': file_name, })
        self.model_meta = model_meta

        return self.model_meta['modelName']

    def __call__(self):
        ep = EndPoint()
        session = ep.connect()

        # get c sdf file
        list_url = CONTENTS.format(session['cwd'])
        record = ep.get_container_by_id(self.container)
        if not record:
            records = ep.get_containers(list_url)
            record = ep.get_uniq_container(records, self.container)

        assert record.get('status') == 'Processed', \
            "File '{}' has not been processed yet".format(record['name'])

        assert record['name'].lower().endswith('sdf'), \
            "Unsupported file format"

        model_name = self.__set_model_meta(record['name'])

        # check folder name
        records = ep.get_containers(list_url)
        try:
            ep.get_uniq_container(records, model_name)
            raise RuntimeError(
                "Model container '{}' already exists".format(model_name))
        except AssertionError:
            pass

        placement = {"parentId": session['cwd'],
                     "userId": session['owner'],
                     "sourceBlobId": record['blob']['id'],
                     "sourceBucket": record['blob']['bucket'],
                     }

        self.model_meta.update(placement)
        pprint.pprint(self.model_meta)

        url = TRAIN
        resp = ep.post(url, self.model_meta)
        result = resp.json()
