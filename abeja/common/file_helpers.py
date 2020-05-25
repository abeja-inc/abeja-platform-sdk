import os
import tempfile
import zipfile
from pathlib import Path
from typing import Iterable, IO

from abeja.exceptions import InvalidPathException


def extract_zipfile(content: bytes, path: str=None):
    """extract zipfile

    :param filename:
    :param path: a different directory to extract to.
    :return:
    :raises: PermissionError
             ValueError
             IOError
    """
    with tempfile.NamedTemporaryFile() as tf:
        tf.write(content)
        tf.seek(0)
        with zipfile.ZipFile(tf.name) as zf:
            zf.extractall(path=path)


def generate_path_iter(path: str, **kwargs) -> Iterable[str]:
    if os.path.isfile(path):
        yield path
    elif os.path.isdir(path):
        for root, _, file_paths in os.walk(path):
            for file_path in file_paths:
                yield os.path.join(root, file_path)
    else:
        raise InvalidPathException(path)


def convert_to_zipfile_object(fileobj: IO):
    if zipfile.is_zipfile(fileobj):
        return fileobj
    if hasattr(fileobj, "name"):
        named_fileobj = fileobj
    else:
        named_fileobj = tempfile.NamedTemporaryFile(suffix='.zip')
        named_fileobj.write(fileobj.read())
        fileobj.close()
        named_fileobj.seek(0)
    tmp_file = tempfile.NamedTemporaryFile(suffix='.zip')
    with zipfile.ZipFile(tmp_file.name, 'w', compression=zipfile.ZIP_DEFLATED) as new_zip:
        new_zip.write(
            named_fileobj.name,
            arcname=Path(
                named_fileobj.name).name)
    tmp_file.seek(0)
    named_fileobj.close()
    return tmp_file


def convert_to_valid_path(filepath: str) -> Path:
    """
    Remove a root path prefix "/", and a relative path "." and "..".
    :param filepath:
    :return:
    """
    valid_factors = [factor for factor in filepath.split(
        "/") if factor and factor != ".."]
    return Path(*valid_factors)
