# _*_ encoding: utf-8 _*_

from parser_helper import HandlerBase
from endpoint_helper import EndPoint
import os
import json
import yaml
from config import UPLOAD, MACHINE_LEARNING_MODEL, CONTENTS


class Upload(HandlerBase):
    """
    Allows uploading a local file into the BLOB (raw file) store.
    leanda upload {local-file-path} [{metadata}]
    Command: upload
    """
    # url = 'https://api.dataledger.io/blob/v1/api/blobs/{}'

    info = '''
            name: upload
            help: Allows uploading a local file into the BLOB(raw file) store
            params:
                -
                    names:
                        - container
                    default: .
                    nargs: '?'
                    help: >
                          Remote Leanda user's folder
                          or none for current working folder.
                          Leanda user's folder can be choosed by its
                          full id system wide or by substring for
                          subfolders in current folder.
                          Substring compared to folder name starting
                          from the beggining or to folder id ending.
                -
                    names:
                        - -p
                        - --path
                    dest: file
                    action: append
                    required: True
                    help: Local file path
                -
                    names:
                        - -n
                        - --name
                    action: append
                    help: Name Leanda file
                -
                    names:
                        - -m
                        - --meta
                    help: Model metadata in json or yaml formats
    '''

    def __call__(self):
        # super().__call__()
        ep = EndPoint()
        session = ep.connect()
        mime_type = 'multipart/mixed'

        list_url = CONTENTS.format(session['cwd'])
        if self.container == '.':
            self.container = session['cwd']
        else:
            record = ep.get_container_by_id(self.container)
            if not record:
                records = ep.get_containers(list_url)
                record = ep.get_uniq_container(records, self.container)

            assert record['type'] in ('User', 'Folder'), \
                "Container '{name}' is not a folder".format(**record)
            self.container = session['cwd'] = record['id']

        cwd = session['cwd']
        owner = session['owner']
        files = {}
        meta = {}

        # prepare model data for uploading
        if self.meta:
            meta = MACHINE_LEARNING_MODEL
            meta.update({'UserId': cwd, 'ParentId': cwd, })
            model_meta = self.get_meta(filepath=self.meta)
            meta['ModelInfo'] = json.dumps(model_meta)

        # prepare file data for upload
        if self.meta:
            self.file = self.file[:1]  # only one model allowed
            mime_type = 'application/x-spss-sav'
        total_names = self.name and len(self.name) or 0
        for idx, file in enumerate(self.file):
            if not os.path.isfile(file):
                raise IOError('File %s not found' % file)
            fh = open(file, 'rb')
            if idx < total_names and self.name[idx]:
                filename = self.name[idx]
            else:
                filename = os.path.basename(file)
            if self.meta:
                filename = model_meta.get('ModelName', filename)
            files.update({'file%d' % idx: (filename, fh, mime_type)})

        url = UPLOAD.format(id=owner)
        meta.update({'parentId': cwd, })

        resp = ep.post(url, meta, files=files)
