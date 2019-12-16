# _*_ encoding: utf-8 _*_
import json
from parser_helper import HandlerBase
from endpoint_helper import EndPoint
from config import (NODE, CONTENTS,
                    BROWSE_CONTENTS)
from clint.textui import colored


class PWD(HandlerBase):
    """
    Allows to get info about current working directory
    Command: pwd
    leanda login {username} {password}
    """
    info = '''
            name: pwd
            help: Identify current Leanda working directory.
            params:
                -
                    names:
                        - -v
                        - --verbosity
                    default: 0
                    action: count
                    help: Set verbosity level

    '''

    def __call__(self):
        # super().__call__()
        ep = EndPoint()
        sess = ep.connect()

        path, id_path = ep.get_full_path(sess['cwd'])
        path = '/leanda/home/{username}/'.format(**sess) + path
        id_path = '/{owner}/'.format(**sess) + id_path

        print("Working directory path: {path}".format(path=path))

        if self.verbosity > 0:
            print("Working directory ID path: {path}".format(path=id_path))


class CD(HandlerBase):
    """
    Allows to get info about current working directory
    Command: pwd
    leanda login {username} {password}
    """
    info = '''
            name: cd
            help: Change Leanda's current working directory.
            params:
                -
                    names:
                        - container
                    nargs: '?'
                    default: .
                    help: >
                          Remote Leanda user's folder
                          or none for home folder.
                          Leanda user's folder can be choosed by its
                          full id system wide or by substring for
                          subfolders in current folder.
                          Substring compared to folder name starting
                          from the beggining or to folder id ending.


    '''

    def __call__(self):
        # super().__call__()
        ep = EndPoint()
        session = ep.connect()

        if self.container == '.':
            ep.set_workdir(session['owner'])
            return

        if self.container == '..':
            resp = ep.get(url=NODE.format(session['cwd']))
            context = resp.json()
            if context.get('parentId'):
                ep.set_workdir(context.get('parentId'))
            else:
                print('You are at /leanda/home/{}'.format(session['username']))
            return

        list_url = CONTENTS.format(session['cwd'])

        record = ep.get_container_by_id(self.container)
        if not record:
            records = ep.get_containers(list_url)
            record = ep.get_uniq_container(records, self.container)

        ep.set_workdir(record['id'])


class RM(HandlerBase):
    """
    Allows to get info about current working directory
    Command: pwd
    leanda login {username} {password}
    """
    info = '''
            name: rm 
            help: Allows to remove file or folder
            params:
                -
                    names:
                        - container
                    nargs: 1
                    help: >
                          Remote Leanda user's folder
                          or none for current working folder.
                          Leanda user's folder can be choosed by its
                          full id system wide or by substring for
                          subfolders in current folder.
                          Substring compared to folder name starting
                          from the beggining or to folder id ending.

    '''

    def __call__(self):
        # super().__call__()
        ep = EndPoint()
        session = ep.connect()
        self.container = self.container[0]

        list_url = CONTENTS.format(session['cwd'])
        record = ep.get_container_by_id(self.container)
        if not record:
            records = ep.get_containers(list_url)
            record = ep.get_uniq_container(records, self.container)

        ep.remove(record)


class LS(HandlerBase):
    """
    Allows to get info about current working directory
    Command: pwd
    leanda login {username} {password}
    """
    dataset = {'Folder': {'data': [], 'format': '\t{name:20.20} {id} ', },
               'File': {'data': [],
                        'format': '\t{name:20.20} {subType:12.12} {status:10.10} {id}',
                        'format_recs': '\t{name:20.20} {subType:7.7}({totalRecords:3}) {status:10.10} {id}', },
               'Records': {'data': [], 'format': '\t{name:20.20} {id}', },
               'Record': {'data': [], 'format': '\t{name:10.10}  {subType:12.12} {status:10.10} {id}', }
               }
    pager_format = "Total records:{totalCount:<10} {title:>60} {currentPage}/{totalPages}"
    info = '''
            name: ls
            help: Browse remote Leanda folder
            params:
                -
                    names:
                        - container
                    default: ''
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
                        - -s
                        - --size
                    default: 10
                    help: Report page size (default value 10)
                -
                    names:
                        - -p
                        - --page
                    default: 1
                    help: Report page number (default value 1)

    '''

    def __call__(self):
        # super().__call__()
        ep = EndPoint()
        sess = ep.connect()
        url = BROWSE_CONTENTS.format(cwd=sess['cwd'], page=1, size=100)

        # Get container ID
        url_params = dict(cwd=sess['cwd'], page=self.page, size=self.size)
        if self.container:
            record = ep.get_container_by_id(self.container)
            if not record:
                records = ep.get_containers(url)
                record = ep.get_uniq_container(records, self.container)
            if record:
                url_params.update({'cwd': record['id'], })

        url = BROWSE_CONTENTS.format(**url_params)
        resp = ep.get(url)
        records = resp.json()

        if resp.headers.get('X-Pagination', None):
            pages = json.loads(resp.headers['X-Pagination'])
            page = self.pager_format.format(title='Page:', **pages)
            print(page)

        for key, ds in self.dataset.items():
            self.dataset[key]['data'] = \
                filter(lambda x: x['type'] == key, records)

        for key in ('Folder File Records Record'.split()):
            dataset = list(self.dataset[key]['data'])
            if len(dataset):
                print(colored.yellow(key))
                for rec in sorted(dataset, key=lambda r: r.get('subType', '')):
                    fmt = self.dataset[key]['format']
                    if rec.get('totalRecords'):
                        fmt = self.dataset[key]['format_recs']
                    rep_rec = fmt.format(**rec)
                    if rec.get('status'):
                        status = rec['status']
                        status = status == 'Processed' \
                            and colored.green or colored.red
                        rep_rec = status(rep_rec)
                    print(rep_rec)
                    # print(colored.clean(rep_rec))
