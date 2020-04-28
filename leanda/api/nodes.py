import json
import uuid

from leanda.config import config
from leanda.session import session
from leanda.api import http
from leanda import util
from urllib.parse import unquote
from leanda.util import print_red, print_yellow


def get_node_by_id(node_id):
    url = f'{config.web_core_api_url}/nodes/{node_id}'
    res = http.get(url)
    if res.status_code == 200:
        return res.json()
    else:
        util.print_red('Node with ID {%s} not found' % node_id)


def get_node_breadcrumbs(node_id):
    url = f'{config.web_core_api_url}/nodes/{node_id}'
    res = http.get(url)
    if res.status_code == 200:
        return json.loads(res.headers['X-Breadcrumbs'])
    else:
        util.print_red('Node with ID {%s} not found' % node_id)


def get_nodes_by_id_or_name(node_id_or_name, remote_folder_id=None):
    if util.is_valid_uuid4(node_id_or_name):
        return [get_node_by_id(node_id_or_name)]
    else:
        cwd_nodes = get_all_nodes(remote_folder_id)
        found_nodes = filter(lambda x: x['name'] == node_id_or_name, cwd_nodes)
        return list(found_nodes)


def get_nodes(remote_folder_id=None, page=1, size=100):
    url = f'{config.web_core_api_url}/nodes/{remote_folder_id or session.cwd}/nodes?pageSize={size}&pageNumber={page}'
    return http.get(url).json()


def get_all_nodes(remote_folder_id=None):
    url = f'{config.web_core_api_url}/nodes/{remote_folder_id or session.cwd}/nodes?pageSize=100&pageNumber=1'
    res = http.get(url)
    if res.status_code != 200:
        util.print_red("Couldn't get nodes")
        return
    pages = json.loads(res.headers['X-Pagination'])
    items = res.json()
    while pages['nextPageLink']:
        res = get(pages['nextPageLink'].replace(
            'http://api.leanda.io/api', config.web_core_api_url))
        if 'X-Pagination' not in res.headers:
            break
        pages = json.loads(res.headers['X-Pagination'])
        items += res.json()
    return items


def get_all_folders(remote_folder_id=None):
    return list(filter(lambda x: x['type'] == 'Folder', get_all_nodes(remote_folder_id)))


def get_all_files(remote_folder_id=None):
    return list(filter(lambda x: x['type'] == 'File', get_all_nodes(remote_folder_id)))


def get_first_folder_by_name(name, remote_folder_id=None):
    """returns the first found folder with exact name"""
    for item in get_all_folders(remote_folder_id):
        if item['name'] == name:
            return item


def get_first_file_by_name(name, remote_folder_id=None):
    """returns the first found file with exact name"""
    for item in get_all_files(remote_folder_id):
        if item['name'] == name:
            return item


def rename(node_id, new_name):
    if not new_name:
        util.print_red('New name required when rename')
        return

    node = get_node_by_id(node_id)
    if not node:
        return
    if 'version' not in node:
        util.print_red('Node has not version')
        return

    url = f'{config.web_core_api_url}/entities/folders/{node_id}?version={node["version"]}'
    data = [{"op": "replace", "path": "/name", "value": new_name}]
    http.patch(url, json.dumps(data))


def remove(node_name_or_id):
    cwd_nodes = get_nodes_by_id_or_name(node_name_or_id)
    if not len(cwd_nodes):
        print('No nodes to remove')
        return
    for node in cwd_nodes:
        data = '''
                [{"value": [{"id": "%s", "type": "File"}],
                    "path": "/deleted",
                    "op": "add",
                }]
                ''' % node['id']
        url = f'{config.web_core_api_url}/nodecollections'
        res = http.patch(url, data=data)
        if res.status_code == 202:
            util.print_green('Node "%s" {%s} was removed!' % (
                node['name'], node['id']))
        else:
            util.print_red('Couldn\'t remove node {%s}' % node['id'])


def create_folder(name, remote_folder_id=None):
    url = f'{config.web_core_api_url}/entities/folders'
    data = {"Name": name, "ParentId": remote_folder_id or session.cwd}
    res = http.post(url=url, data=data)

    if res.status_code == 202:
        id = res.headers["Location"][-36:]
        util.print_green(f'Folder "{name}" {{{id}}} successfully created')
        return id
    else:
        util.print_red('Cannot create remote folder')


def set_cwd(location):
    """ Location can be ID or remote folder name"""

    folder_node = get_node_by_location(location)

    if folder_node['type'] not in ['Folder', 'User']:
        print('Node type is not a folder')
        return

    print(get_location(folder_node))

    session.cwd = folder_node['id']
    # util.print_green('Current remote directory now is "%s" {%s}' % (
    #     folder_node.get('name', '/'), folder_node['id']))
    return folder_node


def print_cwd_nodes(show_id):
    cwd_nodes = get_all_nodes()
    if show_id:
        for node in cwd_nodes:
            name = util.truncate_string_middle(node['name'], 30).ljust(30, ' ')
            print('%s {%s}' % (name, node['id']))
    else:
        names = list(map(lambda x: x['name'], cwd_nodes))
        num_in_group = 4
        groups = [names[i:i+num_in_group]
                  for i in range(0, len(names), num_in_group)]
        for group in groups:
            for n in range(len(group), num_in_group):
                group.append('')
            group = map(lambda x: util.truncate_string_middle(
                x, 20).ljust(23, ' '), group)
            print('%s %s %s %s' % tuple(group))


def get_location(node=None):
    node = node or get_node_by_id(session.cwd)
    breadcrumbs = get_node_breadcrumbs(node['id'])
    names = list(map(lambda x: x['Name'] or '', breadcrumbs))
    if 'name' in node:
        names.insert(0, node['name'])
    return unquote('/'.join(names[::-1])) or '/'


def get_node_by_location(location: str, prev_node=None):
    """ Location can be ID or remote folder name"""

    if location == '/':
        return get_node_by_id(session.owner)

    if location.startswith('/'):
        prev_node = get_node_by_id(session.owner)
    else:
        prev_node = prev_node or get_node_by_id(
            session.cwd)

    location_parts = list(filter(lambda x: x, location.split('/')))
    if len(location_parts) > 1:
        node = get_node_by_location(location_parts[0], prev_node)
        return get_node_by_location('/'.join(location_parts[1:]), node)
    else:
        location = location_parts[0]

    if location == '..':
        breadcrumbs = get_node_breadcrumbs(prev_node['id'])
        node_id = breadcrumbs and breadcrumbs[0].get('Id') or session.owner
        node = get_node_by_id(node_id)

        if not node:
            util.print_red('Node not found' % location)
            return
        return node

    nodes = get_nodes_by_id_or_name(location, prev_node['id'])
    nodes = list(filter(lambda x: x['name'] == location, nodes))

    if not nodes:
        print_red('Couldn\'t find remote location "%s"' % location)
        return

    if len(nodes) > 1:
        print_yellow('Found more than one node with name "%s"' % location)
    return nodes[0]
