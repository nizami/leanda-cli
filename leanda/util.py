import click
import uuid

from os import path
from glob import glob
import json


def truncate_string_middle(s, n):
    if len(s) <= n:
        return s
    n_2 = int(n / 2 - 3)
    n_1 = int(n - n_2 - 3)
    return '{0}...{1}'.format(s[:n_1], s[-n_2:])


def flatten_2d_list(l): return [item for sublist in l for item in sublist]


def progress_bar(total):
    # pbar = tqdm(total=encoder.len, bar_format='{l_bar}{bar}|')
    # progress_index_justify = len(str(len(files_paths)))
    # progress_description = f'{str(index+1).rjust(progress_index_justify, "0")}/{len(files_paths)} - {file_path}'
    # truncate_length = 50
    # progress_description = truncate_string_middle(
    #     progress_description, truncate_length)
    # progress_description = progress_description.ljust(truncate_length, ' ')
    # pbar.set_description(progress_description)
    pass


def is_valid_uuid4(uuid_str):
    try:
        uuid.UUID(uuid_str, version=4)
        return True
    except ValueError:
        return False


def get_normalized_paths(local_paths):
    local_paths = list(set(local_paths))
    directories = []
    files = []
    for local_path in local_paths:
        if path.isdir(local_path):
            directories.append(local_path)
            continue
        local_files = glob(local_path, recursive=True)
        local_files = filter(lambda x: path.isfile(x), local_files)
        files.extend(local_files)
    return (directories, list(set(files)))


def pretty_json(obj):
    if isinstance(obj, str):
        obj = json.loads(obj)
    return json.dumps(obj, indent=4, sort_keys=True)
