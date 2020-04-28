from os import path, walk
import os
from time import ctime
from requests_toolbelt import MultipartEncoder
import requests
import time
from glob import glob
from colorama import Fore
from tqdm import tqdm
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, FileSystemEventHandler, FileSystemEvent

from leanda.config import config
from leanda.session import session
from leanda.api import http, nodes
from leanda import util
from leanda.util import print_green, print_red


def upload_file(file_path, remote_folder_id=None):
    file_path = path.abspath(file_path)
    if not path.isfile(file_path):
        print(f'File {file_path} not found')
        return
    file_stat = Path(file_path).stat()
    data = {'parentId': remote_folder_id or session.cwd,
            'created': str(file_stat.st_ctime_ns),
            'modified': str(file_stat.st_mtime_ns),
            'accessed': str(file_stat.st_atime_ns)}
    url = f'{config.web_blob_api_url}/blobs/{session.owner}'

    file_size = path.getsize(file_path)
    with tqdm(total=file_size, bar_format='{l_bar}{bar}|') as pbar:
        truncate_length = 50
        desc = util.truncate_string_middle(file_path, truncate_length)
        desc = desc.ljust(truncate_length, ' ')
        pbar.set_description(desc)

        if file_size > 1024 * 1024 * config.file_download_limit:
            pbar.bar_format = '%s{desc}Skipped (larger than %sMB)%s' % (
                Fore.YELLOW, config.file_download_limit, Fore.RESET)
            pbar.clear()
            return

        basename = path.basename(file_path)
        nodes_with_the_same_name = nodes.get_all_nodes(remote_folder_id)
        remove_after_upload = filter(
            lambda x: x['name'] == basename, nodes_with_the_same_name)

        if file_size < 1024 * 1024 * 1:  # 1 MB
            res = http.upload_small_file(url, file_path, data)
        else:
            res = http.upload_large_file(url, file_path, data, pbar.update)

        if res.status_code == 200:
            pbar.bar_format = '%s{desc}Uploaded%s' % (
                Fore.GREEN, Fore.RESET)
        else:
            pbar.bar_format = '%s{desc}Failed when upload. Reason:%s%s' % (
                Fore.RED, res.reason, Fore.RESET)
        pbar.clear()
        for node in remove_after_upload:
            nodes.remove(node['id'])
        return res


def upload_files(local_files, remote_folder_id=None):
    local_files = map(lambda x: path.abspath(x), local_files)
    local_files = list(set(local_files))
    for file_path in local_files:
        upload_file(file_path, remote_folder_id)


def upload_directories(local_folders, remote_folder_id=None):
    local_folders = list(set(local_folders))
    for folder_path in local_folders:
        folder_path = path.abspath(folder_path)
        id = nodes.create_folder(path.basename(folder_path), remote_folder_id)
        if not id:
            print_red('Couldn\'t create folder with ID {%s}' % id)
            continue
        for (dirpath, dirnames, filenames) in walk(folder_path):
            local_files = map(lambda x: path.join(
                folder_path, x), filenames)
            local_folders = map(
                lambda x: path.join(folder_path, x), dirnames)
            upload_files(list(local_files), id)
            upload_directories(local_folders, id)
            break


def upload(local_paths, remote_folder_id):
    """Upload directory of files (can be used with glob patterns)"""
    local_paths = local_paths or [os.getcwd()]
    (directories, files) = util.get_normalized_paths(local_paths)
    upload_directories(directories, remote_folder_id)
    upload_files(files, remote_folder_id)


def download_file(file_node, local_folder=None):
    if not file_node:
        return

    if file_node['type'] != 'File':
        print('Node type is not a file')
        return

    if not file_node['blob']:
        'No blob data for node'
        return

    local_folder = path.abspath(local_folder or os.getcwd())
    url = f'{config.web_core_api_url}/entities/files/{file_node["id"]}/blobs/{file_node["blob"]["id"]}'

    blob_length = int(file_node['blob']['length'])
    with tqdm(total=blob_length, bar_format='{l_bar}{bar}|') as pbar:
        truncate_length = 50
        desc = util.truncate_string_middle(file_node['name'], truncate_length)
        desc = desc.ljust(truncate_length, ' ')
        pbar.set_description(desc)

        file_path = path.join(local_folder, file_node['name'])
        if blob_length > 1024 * 1024 * config.file_download_limit:
            pbar.bar_format = '%s{desc}Skipped (larger than %sMB)%s' % (
                Fore.YELLOW, config.file_download_limit, Fore.RESET)
            pbar.clear()
            return

        if blob_length < 1024 * 1024 * 1:  # 1 MB
            res = http.download_small_file(url, file_path)
        else:
            res = http.download_large_file(url, file_path, pbar.update)

        if res.status_code == 200:
            pbar.bar_format = '%s{desc}Downloaded%s' % (
                Fore.GREEN, Fore.RESET)
        else:
            pbar.bar_format = '%s{desc}Failed when download. Reason:%s%s' % (
                Fore.RED, res.reason, Fore.RESET)
        pbar.clear()
        return res


def download_folder(folder_node, local_folder=None):
    if not folder_node:
        return

    if folder_node['type'] not in ['Folder', 'User']:
        print('Node type is not a folder')
        return

    local_folder = path.abspath(local_folder)
    local_folder = path.join(local_folder, folder_node.get('name', ''))
    Path(local_folder).mkdir(parents=True, exist_ok=True)

    remote_nodes = nodes.get_all_nodes(folder_node['id'])
    for remote_node in remote_nodes:
        if remote_node['type'] == 'Folder':
            download_folder(remote_node, local_folder)
        else:
            download_file(remote_node, local_folder)


def sync(local_directory, remote_folder_node):
    print_green('Sync...')
    try:
        observer = watch_local(
            local_directory, remote_folder_node, lambda x, e: print(x, e))
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


class CustomEventHandler(FileSystemEventHandler):
    fn: object

    def __init__(self, local_directory, remote_folder_node, fn):
        self.local_directory = local_directory
        self.remote_folder_node = remote_folder_node
        self.fn = fn

    def on_any_event(self, event: FileSystemEvent):
        pass

    def on_modified(self, event: FileSystemEvent):
        # path = self.normalize_path(event)
        # self.fn('modified', path)
        pass

    def on_deleted(self, event: FileSystemEvent):
        path = self.normalize_path(event)
        self.fn('deleted', path)
        # node = nodes.get_node_by_location(eve)
        # nodes.remove(node['id'])

    def on_moved(self, event: FileSystemEvent):
        path = self.normalize_path(event)
        self.fn('moved', path)

    def on_created(self, event: FileSystemEvent):
        path = self.normalize_path(event)
        self.fn('created', path)
        upload([event.src_path], self.remote_folder_node['id'])

    def normalize_path(self, event: FileSystemEvent):
        return event.src_path.replace(self.local_directory + '/', '').replace(self.local_directory, '')


def watch_local(local_directory, remote_folder_node, fn):
    handler = CustomEventHandler(local_directory, remote_folder_node, fn)
    observer = Observer()
    observer.schedule(handler, local_directory, recursive=True)
    observer.start()
    return observer
