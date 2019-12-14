# _*_ encoding: utf-8 _*_

from leanda.parser_helper import HandlerBase
from leanda.api import Api
from leanda.filelist_helper import ListHelper, LocalFiles, RemoteFiles
from leanda.config import BROWSE_CONTENTS, CONTENTS, DOWNLOAD, FILE, UPLOAD
import os
import json
from clint.textui import colored, progress
from time import time, sleep
from os import listdir, mkdir
from os.path import isfile, isdir, exists, join
import hashlib


class LiveSync(HandlerBase):
    """
    leanda livesync
    Two-way synchronization of local folder with the user's Leanda folder.
    """
    url = 'https://api.dataledger.io/osdr/v1/api/me'
    info = '''
            name: livesync
            help: >
                Two-way synchronization of local folder
                with the Leanda user's folder. Comparision between
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
                          Remote Leanda user's folder
                          or none for current working folder.
                          Leanda user's folder can be choosed by its
                          full id system wide or by substring for
                          subfolders in current folder.
                          Substring compared to folder name starting
                          from the beggining or to folder id ending.
                -
                    names:
                        - -ul
                        - --update-local
                    action: store_true
                    help: Compare by name and Leanda file's version
                -
                    names:
                        - -ur
                        - --update-remote
                    action: store_true
                    help: Compare by name and last modification time.


    '''

    api: Api

    def _is_local_file(self, name):
        filename = os.path.basename(name)
        return os.path.isfile(name) \
            and not (filename.startswith('.') or filename.startswith('_'))

    def _is_remote_file(self, rec):
        return rec['type'] == FILE

    def __call__(self):

        assert os.path.isdir(self.folder), \
            "'{folder}' is not a folder".format(folder=self.folder)

        self.api = Api()

        self.upload_local_files(self.api.session['cwd'], self.folder)
        self.download_remote_files(self.api.session['cwd'], self.folder)
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
        list_url = CONTENTS.format(self.api.session['cwd'])
        if self.container == '.':
            self.container = self.api.session['cwd']
        else:
            record = self.api.get_container_by_id(self.container)
            if not record:
                records = self.api.get_containers(list_url)
                record = self.api.get_uniq_container(records, self.container)

            assert record['type'] in ('User', 'Folder'), \
                "Container '{name}' is not a folder".format(**record)
            self.container = self.api.session['cwd'] = record['id']

        list_url = CONTENTS.format(self.container)

        # remote files
        records = self.api.get_containers(list_url)
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
                self.api.download(rec, path=path)
                lfiles.log(path=path, file=file)
            except Exception as e:
                print(e)

        # file to upload
        print('Uploading...')
        for file in lfiles - rfiles:
            path = os.path.join(self.folder, file.name)
            try:
                print('Uploading %s' % path)
                self.api.upload(self.api.session, path)
                lfiles.log(path=path, file=file)
            except Exception as e:
                print(e)
        lfiles.store_log()

    def download_remote_files(self, parent_id, local_folder_path):
        for item in self.get_all_remote_items(parent_id):
            item_path = join(local_folder_path, item['name'])
            if item['type'] == 'File':
                if not exists(item_path):
                    rec = {'id': item['blob']['id'], 'file_id': item['id']}
                    self.download_remote_file(rec, item_path)
                else:
                    print('File "{}" already exists'.format(item_path))
            elif item['type'] == 'Folder':
                if not exists(item_path):
                    mkdir(item_path)
                self.download_remote_files(item['id'], item_path)

    def download_remote_file(self, record, path):
        url = DOWNLOAD.format(**record)
        result = self.api.get(url=url, stream=True)
        assert result.ok, 'Problem loading file {}'.format(path)

        result.raw.decode_content = True
        it = result.iter_content(chunk_size=1024)
        with open(path, 'wb') as f:
            for i, item in enumerate(it):
                if item:
                    f.write(item)
                    f.flush()

    def upload_local_files(self, parent_id, local_folder_path):
        for item in listdir(local_folder_path):
            item_path = join(local_folder_path, item)
            if isfile(item_path):
                self.upload_local_file(parent_id, item_path)
            else:
                folder = self.get_or_create_remote_folder_by_name(
                    parent_id, item)
                if folder:
                    self.upload_local_files(folder['id'], item_path)

    def list_files(self, startpath):
        for root, dirs, files in os.walk(startpath):
            for f in files:
                yield '{}\{}'.format(root.replace(startpath + '\\', ''), f)

    def get_all_remote_items(self, parent_id):
        url_params = dict(cwd=parent_id, page=1, size=100)
        url = BROWSE_CONTENTS.format(**url_params)
        resp = self.api.get(url)
        if resp.status_code == 500:
            return []
        pages = json.loads(resp.headers['X-Pagination'])
        items = resp.json()
        while pages['nextPageLink']:
            resp = self.api.get(resp.headers['X-Pagination'])
            pages = json.loads(resp.headers['X-Pagination'])
            items += resp.json()
        return items
        # if resp.headers.get('X-Pagination', None):

    def get_all_remote_folders(self, parent_id):
        return filter(lambda x: x['type'] == 'Folder', self.get_all_remote_items(parent_id))

    def get_all_remote_files(self, parent_id):
        return filter(lambda x: x['type'] == 'File', self.get_all_remote_items(parent_id))

    # returns the first found folder with exact name
    def get_first_remote_folder_by_name(self, parent_id, name):
        for item in self.get_all_remote_folders(parent_id):
            if item['name'] == name:
                return item

    # returns the first found folder with exact name
    def get_first_remote_file_by_name(self, parent_id, name):
        for item in self.get_all_remote_files(parent_id):
            if item['name'] == name:
                return item

    def get_or_create_remote_folder_by_name(self, parent_id, name):
        folder = self.get_first_remote_folder_by_name(parent_id, name)
        # print('Folder "{}" already exists'.format(name))
        if folder:
            return folder

        self.api.create_folder(name, parent_id)

        starttime = time()
        while True:
            folder = self.get_first_remote_folder_by_name(parent_id, name)
            if folder:
                return folder
            sleep(1+(time() - starttime) * 2)
            if time() - starttime > 10:
                raise TimeoutError()

    def upload_local_file(self, parent_id, local_file_path):
        if not os.path.isfile(local_file_path):
            raise IOError('File %s not found' % local_file_path)
        filename = os.path.basename(local_file_path)

        if self.get_first_remote_file_by_name(parent_id, filename):
            print('File "{}" already exists'.format(filename))
            return

        with open(local_file_path, 'rb') as fh:
            file = {'file': (filename, fh, 'multipart/mixed')}
            url = UPLOAD.format(id=self.api.session['owner'])
            data = {'parentId': parent_id}
            resp = self.api.post(url, data, files=file)

    def get_local_file_md5(self, local_file_path):
        hash_md5 = hashlib.md5()
        with open(local_file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
