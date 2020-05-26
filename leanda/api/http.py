import click
import json
import logging
import magic
import mimetypes
import requests
import sys

from colorama import Fore
from os import path, stat
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
from requests.exceptions import ChunkedEncodingError
from tqdm import tqdm

from leanda.config import config
from leanda.session import session
from leanda.util import truncate_string_middle
from pprint import pprint

logger = logging.getLogger('blobs')


def exit_by_unauthorized_reason(res):
    if res.status_code == 401:
        logger.error('Please login and retry!')


def fetch(method, url, data=None, headers=None):
    base_headers = {
        'Accept': '*/*',
        'Content-Type': 'application/json',
        'Authorization': session.token
    }
    if headers:
        base_headers.update(headers)

    if isinstance(data, dict):
        data = json.dumps(data)
    try:
        res = getattr(requests, method)(
            url=url, headers=base_headers, data=data)
        if res.status_code == 401:
            login_and_retry()
        return res
    except ChunkedEncodingError as error:
        login_and_retry()


def get(url): return fetch('get', url)


def post(url, data): return fetch(
    'post', url, data=data)


def patch(url, data): return fetch(
    'patch', url, data=data)


def get_mime_type(file_path):
    return mimetypes.guess_type(file_path)[0] or magic.from_file(file_path, mime=True)


def upload_large_file(url, file_path, data, chunk_callback=None):
    if not path.isfile(file_path):
        print(f'File {file_path} not found')
        return
    file = open(file_path, 'rb')
    base_name = path.basename(file_path)
    data.update({'file': (base_name, file, get_mime_type(file_path))})
    encoder = MultipartEncoder(data)

    prev_bytes_read = 0

    def progress_callback(x):
        nonlocal prev_bytes_read
        if chunk_callback:
            chunk_callback(x.bytes_read-prev_bytes_read)
        prev_bytes_read = x.bytes_read
    monitor = MultipartEncoderMonitor(encoder, progress_callback)
    headers = {
        'Content-Type': monitor.content_type,
        'Authorization': session.token
    }
    with requests.post(url, data=monitor, headers=headers, stream=True) as res:
        if res.status_code == 401:
            login_and_retry()
        return res


def upload_small_file(url, file_path, data):
    if not path.isfile(file_path):
        print(f'File {file_path} not found')
        return

    encoded_data = MultipartEncoder(
        fields={
            **data,
            'file': (path.basename(file_path),
                     open(file_path, 'rb'), get_mime_type(file_path)),
        }
    )
    headers = {
        'Accept': '*/*',
        'Content-Type': encoded_data.content_type,
        'Authorization': session.token
    }
    res = requests.post(url, headers=headers, data=encoded_data)
    if res.status_code == 401:
        login_and_retry()
    return res


def download_large_file(url, file_path, chunk_callback=None):
    headers = {
        'Authorization': session.token,
        'Content-Disposition': 'attachment'
    }
    with requests.get(url, headers=headers, stream=True) as res:
        with open(file_path, 'wb') as f:
            for chunk in res.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    if chunk_callback:
                        chunk_callback(len(chunk))
        if res.status_code == 401:
            login_and_retry()
        return res


def download_small_file(url, file_path):
    headers = {
        'Authorization': session.token,
        'Content-Disposition': 'attachment'
    }
    res = requests.get(url, headers=headers)
    if res.status_code == 401:
        login_and_retry()

    with open(file_path, 'wb') as f:
        f.write(res.content)

    return res


def login_and_retry():
    logger.error('Please login and retry!')
    sys.exit()
