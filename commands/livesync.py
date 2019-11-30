# _*_ encoding: utf-8 _*_

from parser_helper import HandlerBase
from endpoint_helper import EndPoint
from filelist_helper import ListHelper, LocalFiles, RemoteFiles
from config import CONTENTS, FILE
import os


class LiveSync(HandlerBase):
    """
    osdr livesync
    Two-way synchronization of local folder with the user's OSDR folder.
    """
    url = 'https://api.dataledger.io/osdr/v1/api/me'
    info = '''
            name: livesync
            help: >
                Two-way synchronization of local folder
                with the OSDR user's folder. Comparision between
                folders based on file names. For more precise
                comparision see -ul and -ur keys.
            params:
                -
                    names:
                        - -l
                        - --local-folder
                    default: .
                    dest: folder
                    help: >
                         Path to local folder or
                         none for working directory
                -
                    names:
                        - -r
                        - --remote-folder
                    dest: container
                    default: .
                    help: >
                          Remote OSDR user's folder
                          or none for current working folder.
                          OSDR user's folder can be choosed by its
                          full id system wide or by substring for
                          subfolders in current folder.
                          Substring compared to folder name starting
                          from the beggining or to folder id ending.
                -
                    names:
                        - -ul
                        - --update-local
                    action: store_true
                    help: Compare by name and OSDR file's version
                -
                    names:
                        - -ur
                        - --update-remote
                    action: store_true
                    help: Compare by name and last modification time.


    '''

    def _is_local_file(self, name):
        filename = os.path.basename(name)
        return os.path.isfile(name) \
            and not (filename.startswith('.') or filename.startswith('_'))

    def _is_remote_file(self, rec):
        return rec['type'] == FILE

    def __call__(self):

        assert os.path.isdir(self.folder), \
            "'{folder}' is not a folder".format(folder=self.folder)

        ep = EndPoint()
        session = ep.connect()

        # Local files
        lfiles = ListHelper(path=self.folder,
                            update=self.update_remote)

        for file in os.listdir(self.folder):
            path = os.path.join(self.folder, file)
            rec = LocalFiles(name=os.path.basename(path),
                             mtime=os.path.getmtime(path))
            if self._is_local_file(path):
                lfiles.list.append(rec)

        # remote folder id
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

        list_url = CONTENTS.format(self.container)

        # remote files
        records = ep.get_containers(list_url)
        records = list(records)

        rfiles = ListHelper(self.folder, update=self.update_local)
        rfiles.list = [RemoteFiles(name=rec['name'], id=rec['id'],
                                   version=rec['version'],
                                   length=rec['blob']['length'],
                                   bucket=rec['blob']['bucket'],
                                   bid=rec['blob']['id'])
                       for rec in filter(self._is_remote_file, records)]

        # # files to download
        print('\n\nDownloading...')
        for file in rfiles - lfiles:
            rec = {'type': 'File', 'name': file.name, 'length': file.length,
                   'blob': {'id': file.bid, 'bucket': file.bucket, 'file_id': file.id,
                            'length': file.length}}
            path = os.path.join(self.folder, file.name)
            try:
                ep.download(rec, path=path)
                lfiles.log(path=path, file=file)
            except Exception as e:
                print(e)

        # file to upload
        print('Uploading...')
        for file in lfiles - rfiles:
            path = os.path.join(self.folder, file.name)
            try:
                print('Uploading %s' % path)
                ep.upload(session, path)
                lfiles.log(path=path, file=file)
            except Exception as e:
                print(e)
        lfiles.store_log()
