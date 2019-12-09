# _*_ encoding: utf-8 _*_

from parser_helper import HandlerBase
from endpoint_helper import EndPoint
from filelist_helper import ListHelper, LocalFiles, RemoteFiles
from config import BROWSE_CONTENTS, CONTENTS, FILE
import os
import json
from clint.textui import colored
from time import time, sleep
from os import listdir
from os.path import isfile, join
import hashlib



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
        print('start')
        # ep.create_folder('so', session['cwd'])
        # aaa = self.get_or_create_folder_by_name('a16f22fe-c36a-4d57-ad78-19746007c82d', 'as212322dw')
        # print(((aaa)))
        # self.upload_local_folder(
        #     session['cwd'], 'C:\w\projects\ArqiSoft\leanda\leanda-sync')
        
        r = self.md5("C:\w\projects\ArqiSoft\leanda\leanda-core\README.md")
        print(r)
        # list(self.get_all_items('2ffbd2b0-8cee-43ab-bb76-7179faf164e0'))
        return
        # Local files
        lfiles = ListHelper(path=self.folder,
                            update=self.update_remote)

        # print('LIST', self.list_files(self.folder))
        # for file in os.listdir(self.folder):
        for file in self.list_files(self.folder):
            # print('file', file)
            path = os.path.join(self.folder, file)
            rec = LocalFiles(name=file,
                             mtime=os.path.getmtime(path))
            if self._is_local_file(path):
                print(rec)
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
        print('RECORDS', records)
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
            print('---', self.folder)
            path = os.path.join(self.folder, file.name)
            try:
                print('Uploading %s' % path)
                ep.upload(session, path)
                lfiles.log(path=path, file=file)
            except Exception as e:
                print(e)
        lfiles.store_log()

    def upload_local_folder(self, parent_id, local_folder_path):
        print(local_folder_path)
        ep = EndPoint()
        session = ep.connect()
        for item in listdir(local_folder_path):
            item_path = join(local_folder_path, item)
            if isfile(item_path):
                ep.upload_file(session, parent_id, item_path)
            else:
                print(item_path)
                folder = self.get_or_create_folder_by_name(parent_id, item)
                print(folder)
                self.upload_local_folder(folder['id'], item_path)
                return

    def list_files(self, startpath):
        for root, dirs, files in os.walk(startpath):
            for f in files:
                yield '{}\{}'.format(root.replace(startpath + '\\', ''), f)

    def get_all_items(self, parent_id, page=1, size=100):
        ep = EndPoint()
        sess = ep.connect()
        url_params = dict(cwd=parent_id, page=page, size=size)
        url = BROWSE_CONTENTS.format(**url_params)
        resp = ep.get(url)
        print('get_all_items parent_id', parent_id)
        print('get_all_items url', url)
        print('get_all_items resp', resp.content)
        yield from resp.json()
        if resp.headers.get('X-Pagination', None):
            pages = json.loads(resp.headers['X-Pagination'])
            if pages['currentPage'] <= pages['totalPages']:
                yield from self.get_all_items(parent_id, pages['currentPage'] + 1, size)

    def get_all_folders(self, parent_id):
        for item in self.get_all_items(parent_id):
            if item['type'] == 'Folder':
                yield item

    # returns the first found folder with exact name
    def get_first_folder_by_name(self, parent_id, name):
        for item in self.get_all_folders(parent_id):
            if item['name'] == name:
                return item

    def get_or_create_folder_by_name(self, parent_id, name):
        folder = self.get_first_folder_by_name(parent_id, name)
        if folder:
            return folder

        ep = EndPoint()
        ep.create_folder(name, parent_id)

        starttime = time()
        while True:
            print(parent_id, name)
            folder = self.get_first_folder_by_name(parent_id, name)
            if folder:
                return folder
            sleep(1+(time() - starttime) * 2)

    def md5(self, file_path):
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()