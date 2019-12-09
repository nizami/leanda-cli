# _*_ encodin`: utf-8 _*_

import requests
import os
import re
import sys
import pickle
import json
from oauthlib.oauth2 import LegacyApplicationClient
from requests_oauthlib import OAuth2Session
from requests_toolbelt import MultipartEncoder
from config import (ME_URL, TOKEN_URL, DOWNLOAD, FILE, REMOVE,
                    UPLOAD, ID_PATTERN, NODE, REMOVE_DATA, NODE, WEB_API_URL)
from clint.textui import progress


# from clint.textui import puts, indent


class EndPoint(object):
    API_AUTH = {
        'grant_type': 'password',
        'client_id': 'leanda_cli'
    }

    headers = {
        'Accept': 'application/json',
        'Authorization': None
    }

    def __init__(self):
        from os.path import expanduser
        folder = "{}/osdr".format(expanduser("~"))
        try:
            os.stat(folder)
        except Exception:
            os.mkdir(folder)

        self.storage = "{}/osdr.data".format(folder)
        client_id = self.API_AUTH['client_id']
        client = LegacyApplicationClient(client_id=client_id)

        self.oauth = OAuth2Session(client=client)
        self.oauth.verify = False
        requests.packages.urllib3.disable_warnings()

    def persistent_storage(self, mode='r'):
        return open(self.storage, "%sb" % mode)

    def storage_is_exists(self):
        return os.path.isfile(self.storage)

    def remove_storage(self):
        assert self.storage_is_exists(), "Not logged in"
        os.unlink(self.storage)

    def set_workdir(self, id):
        with self.persistent_storage() as fh:
            self.API_AUTH = pickle.load(fh)
        self.API_AUTH.update({'cwd': id, })
        with self.persistent_storage('w') as fh:
            pickle.dump(self.API_AUTH, fh)

    def connect(self):
        # authorization based on on persistent storage
        with self.persistent_storage() as fh:
            self.API_AUTH = pickle.load(fh)
        auth = {'Authorization': '{token}'.format(**self.API_AUTH), }
        self.headers.update(auth)
        resp = self.get(url=ME_URL)
        if not resp.ok:
            # token expired
            self.authorize_remote()
        return self.API_AUTH

    def authorize_remote(self, credentials=None):
        # credentials dict with login and password
        if self.storage_is_exists():
            with self.persistent_storage() as fh:
                self.API_AUTH = pickle.load(fh)
        if credentials:
            self.API_AUTH.update(credentials)
            # try:
        resp = self.oauth.post(TOKEN_URL, data=self.API_AUTH)
        assert resp.ok, 'Authorization Error'

        token = "{token_type} {access_token}".format(**resp.json())
        self.headers.update({'Authorization': token}, )
        resp = self.get(url=ME_URL)
        # set up owner and start folder id data
        owner = "{id}".format(**resp.json())
        self.API_AUTH.update({'token': token,
                              'cwd': owner, 'owner': owner})
        with self.persistent_storage('w') as fh:
            pickle.dump(self.API_AUTH, fh)
        return self.API_AUTH

    def get(self, url, **params):
        resp = self.oauth.get(url, headers=self.headers)
        return resp

    def delete(self, url, **params):
        resp = self.oauth.delete(url, headers=self.headers)
        return resp

    def post(self, url, data, files=None):
        if files:
            fields = list(data.items())
            files = list(files.items())
            fields.extend(files)
            data = MultipartEncoder(fields=fields)
            self.headers.update({'Content-Type': data.content_type})
        else:
            data = json.dumps(data)
            self.headers.update({'Content-Type': 'application/json', })

        resp = self.oauth.post(url, headers=self.headers, data=data)
        return resp

    def get_containers(self, url):
        containers = "Folder File Records".split()

        def is_contaner(rec):
            return rec['type'] in containers

        resp = self.get(url=url)
        result = filter(is_contaner, resp.json())
        return result

    def get_container_by_id(self, id):
        patt = re.compile(ID_PATTERN)
        if patt.match(id):
            url = NODE.format(id)
            resp = self.get(url=url)
            assert resp.ok, 'No such node'
            return resp.json()
        return False

    def get_uniq_container(self, records, patt):
        patt = patt.lower()

        def valid_rec(rec):
            like_id = rec['id'].endswith(patt)
            like_name = rec['name'].lower().startswith(patt)
            return like_id or like_name

        results = filter(valid_rec, records)
        results = list(results)
        if not results:
            assert False, 'Can not find appropriate container'
        if len(results) > 1:
            assert False, 'Multiply selection. Can not choose single container'
        return results[0]

    def download(self, record, path):
        assert record['type'] == FILE, 'Not a file'

        file_name = path
        assert record['blob'], 'No blob data for {}'.format(file_name)

        length = record['blob']['length']
        url = DOWNLOAD.format(**record['blob'])
        result = self.get(url=url, stream=True)
        assert result.ok, 'Problem loading file {}'.format(file_name)

        total_length = length
        result.raw.decode_content = True
        it = result.iter_content(chunk_size=1024)
        label = "{:20.20}".format(file_name)
        count = total_length // 1024 + 1
        bar = progress.Bar(label=label, width=32,
                           empty_char='.', filled_char='>',
                           expected_size=count, every=3)
        with open(file_name, 'wb') as f:
            with bar:
                for i, item in enumerate(it):
                    bar.show(i + 1)
                    if item:
                        f.write(item)
                        f.flush()

    def upload(self, session, filename):
        if not os.path.isfile(filename):
            raise IOError('File %s not found' % filename)
        fh = open(filename, 'rb')
        filename = os.path.basename(filename)
        file = {'file': (filename, fh, 'multipart/mixed')}

        url = UPLOAD.format(id=session['owner'])
        data = {'parentId': session['cwd'], }
        resp = self.post(url, data, files=file)
        print(resp)

    def upload_file(self, session, parent_id, file_path):
        if not os.path.isfile(file_path):
            raise IOError('File %s not found' % file_path)
        fh = open(file_path, 'rb')
        file_path = os.path.basename(file_path)
        file = {'file': (file_path, fh, 'multipart/mixed')}

        url = UPLOAD.format(id=session['owner'])
        data = {'parentId': parent_id }
        resp = self.post(url, data, files=file)
        print('upload_file', resp)

    def remove(self, record):
        url = REMOVE
        data = REMOVE_DATA % record['id']

        self.headers.update({'Content-Type': 'application/json', })
        resp = self.oauth.patch(url, data, headers=self.headers)
        print(resp)

    def get_full_path(self, id):
        path = []
        id_path = []

        url = NODE.format(id)
        resp = self.get(url=url)
        if not resp.ok: return None, None
        context = resp.json()

        breadcrumbs = []
        if resp.headers['X-Breadcrumbs']:
            breadcrumbs = json.loads(resp.headers['X-Breadcrumbs'])
            if breadcrumbs:
                del breadcrumbs[-1]
            breadcrumbs.reverse()
            for crumb in breadcrumbs:
                path.append(crumb['Name'])
                id_path.append(crumb['Id'])

            if context.get('name'):
                path.append(context['name'])
                id_path.append(context['id'])

        path = '/'.join(path)
        id_path = '/'.join(id_path)
        return path, id_path

    def create_folder(self, name, parent_id):
        url = '{}/entities/folders'.format(WEB_API_URL)
        data = { "Name": name, "parentId": parent_id }
        self.headers.update({'Content-Type': 'application/json'})
        resp = self.post(url=url, data=data)
        return resp