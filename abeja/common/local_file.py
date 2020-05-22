# -*- coding: utf-8 -*-
"""
set of decorators to utilize local files.
local file is saved in MOUNT_DIR and follows the rules below.

|   scheme   |  base dir   | rest dirs and file name |
|:-----------|:------------|:------------------------|
| datalake   | channel_id  | file_id                 |
| S3n        | bucket      | key                     |
| http       | domain:port | path                    |

"""
import os
from functools import wraps
from urllib.parse import urlparse
from datetime import datetime
import random

from abeja.common.config import MOUNT_DIR, DEFAULT_CHUNK_SIZE


def use_binary_cache(func):
    """NOTE: this function expects to take `method object` as an arg"""
    @wraps(func)
    def inner(obj):
        path = _prepare_file_path(obj.uri)

        if os.path.exists(path):
            return _read_file(path, 'binary')

        content = func()

        _write_file(path, 'binary', content)

        return content
    return inner


def use_text_cache(func):
    """NOTE: this function expects to take `method object` as an arg"""
    @wraps(func)
    def inner(obj):
        path = _prepare_file_path(obj.uri)

        if os.path.exists(path):
            return _read_file(path, 'text')

        content = func()

        _write_file(path, 'text', content)

        return content
    return inner


def use_iter_content_cache(func):
    """NOTE: this function expects to take `method object` as an arg"""
    @wraps(func)
    def inner(obj, chunk_size=DEFAULT_CHUNK_SIZE):
        """
        if file does not exist, save content in a file,
        and return content by reading the file
        """
        path = _prepare_file_path(obj.uri)

        if os.path.exists(path):
            return _read_iter_content_file(path, chunk_size)

        iter_content = func(chunk_size)
        _write_iter_file(path, 'binary', iter_content)

        return _read_iter_content_file(path, chunk_size)
    return inner


def use_iter_lines_cache(func):
    """NOTE: this function expects to take `method object` as an arg"""
    @wraps(func)
    def inner(obj):
        """if file does not exist, save content in a file,
        and return content by reading the file
        """
        path = _prepare_file_path(obj.uri)

        if os.path.exists(path):
            return _read_iter_lines_file(path)

        iter_lines = func()
        _write_iter_file(path, 'text', iter_lines)

        return _read_iter_lines_file(path)
    return inner


def _prepare_file_path(uri):
    """prepare directory for cache file to be saved.

    :param uri: ex. datalake://<channel_id>/<file_id>
    :return: str
    """
    base_dir, file = _parse_in_base_dir_and_file(uri)

    os.makedirs(base_dir, exist_ok=True)

    return os.path.join(base_dir, file)


def _parse_in_base_dir_and_file(uri):
    """base_dir is directory where a file is contained

    :param uri: ex. datalake://<channel_id>/<file_id>
    :return: str, str
    """
    pr = urlparse(uri)
    base_dir = os.path.join(MOUNT_DIR, pr.netloc)
    path = pr.path[1:]  # pr.path should start with '/'. eliminate it.
    entries = path.split('/')
    entries, _file = entries[:-1], entries[-1]
    _dir = ('/').join(entries)
    if _dir:
        base_dir = os.path.join(base_dir, _dir)
    return base_dir, _file


def _read_in_chunks(infile, chunk_size):
    """read file and create iterator that returns the content iteratively.

    :param infile:
    :param chunk_size:
    :return:
    """
    while True:
        chunk = infile.read(chunk_size)
        if chunk:
            yield chunk
        else:
            return


def _read_file(path, file_type):
    mode = 'r'
    if file_type == 'binary':
        mode += 'b'
    with open(path, mode) as f:
        return f.read()


def _read_iter_content_file(path, chunk_size):
    with open(path, 'rb') as f:
        for chunk in _read_in_chunks(f, chunk_size):
            yield chunk


def _read_iter_lines_file(path):
    with open(path, 'r') as f:
        for line in f.readline():
            yield line


def _write_file(path, file_type, content):
    _write_iter_file(path, file_type, [content])


def _write_iter_file(path, file_type, iter_content):
    # To attempt to write a file atomically, write contents into
    # temporary file, then rename it to the original path.
    #
    # 'Path.PID-DateTime-Random'
    # e.g.
    # 20171128T113546-9fa120a3-96bc-4b84-b56b-1bc2273178a1.30304-20191220162525-ee5a
    suffix = '{}-{}-{:04x}'.format(
        os.getpid(),
        datetime.now().strftime('%Y%m%d%H%M%S'),
        random.randint(0, 0xffff))
    tmppath = '{}.{}'.format(path, suffix)

    mode = 'w'
    if file_type == 'binary':
        mode += 'b'
    with open(tmppath, mode) as f:
        for content in iter_content:
            f.write(content)
    os.replace(tmppath, path)
