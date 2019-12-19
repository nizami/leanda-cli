from .config import LAST_UPDATED
import os
import pickle
from collections import defaultdict
from .endpoint_helper import EndPoint
from collections import namedtuple

LocalFiles = namedtuple('LocalFiles', 'name,   mtime')
RemoteFiles = namedtuple('RemoteFiles',
                         'name, id, version, bucket, bid, length')


class ListHelper(object):
   
    def __init__(self, path='.', update=False):
        self.update = update
        self.filename = os.path.join(path, LAST_UPDATED)
        self.list = []
        try:
            with open(self.filename, 'rb') as fh:
                self.updated = pickle.load(fh)
        except Exception:
            self.updated = defaultdict(dict)

    def __sub__(self, file_list):
        subs_names = [item.name for item in file_list.list]
        ep = EndPoint()

        if self.update:
            for item in self.list:
                # upload file
                try:
                    if item.mtime > self.updated[item.name]['mtime']:
                        print('>>>', item)
                        for file in file_list.list:
                            if file.name == item.name:
                                ep.remove({'id': file.id, })
                                print('delete', file.id)
                        subs_names.remove(item.name)
                except AttributeError:
                    pass

                # download file
                try:
                    if item.version > self.updated[item.name]['version']:
                        subs_names.remove(item.name)
                except AttributeError:
                    pass

        return [item for item in self.list if item.name not in subs_names]

    def log(self, path, file):
        """
        Log process file
        """
        log = {'mtime': os.path.getmtime(path), }
        if 'version' in file._fields:
            version = {'version': file.version, }
            log.update(version)
        self.updated[file.name].update(log)

    def store_log(self):
        """
        Save processed log
        """
        print(self.updated)
        with open(self.filename, 'wb') as fh:
            pickle.dump(self.updated, fh)