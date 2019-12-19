# _*_ encoding: utf-8 _*_

from ..parser_helper import HandlerBase
from ..endpoint_helper import EndPoint
from ..config import CONTENTS
import os


class Download(HandlerBase):
    """
    Allows download a  file from Leanda BLOB store.
    leanda download {remote-id} [{metadata}]
    Command: download
    """
    info = '''
            name: download
            help: Allows to download an Leanda file.
            params:
                -
                    names:
                        - container
                    help: >
                          Remote Leanda file id.
                          Leanda file can be choosed by its
                          full id system wide or by substring in 
                          current Leanda folder.
                          Substring compared to filename starting
                          from the beggining or to file id ending.
                -
                    names:
                        - -o
                        - --output
                    help: Path to file or directory to save.
                -
                    names:
                        - -f
                        - --force
                    action: store_true
                    dest: overwrite
                    help: Force overwrite if file exists.


    '''

    def __call__(self):
        # super().__call__()
        ep = EndPoint()
        session = ep.connect()

        list_url = CONTENTS.format(session['cwd'])

        record = ep.get_container_by_id(self.container)
        if not record:
            records = ep.get_containers(list_url)
            record = ep.get_uniq_container(records, self.container)

        folder = '.'
        file_name = record['name']
        if self.output:
            if os.path.isdir(self.output):
                folder = self.output
            elif not os.path.dirname(self.output):
                file_name = self.output
            else:
                file_name = os.path.basename(self.output)
                folder = os.path.dirname(self.output)
                assert os.path.isdir(folder), 'No such folder: {}'.format(folder)

        path = os.path.join(folder, file_name)
        if not self.overwrite:
            assert not os.path.isfile(path), "File {path} exists. To overwrite use -f key.".format(path=path)
        print(record)
        ep.download(record, path)
