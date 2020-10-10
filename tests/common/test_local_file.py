from abeja.common import local_file
from abeja.common.local_file import use_text_cache, use_binary_cache, use_iter_content_cache
from abeja.common.config import DEFAULT_CHUNK_SIZE
import pytest
import secrets
from functools import partial


class SourceURI:
    def __init__(self, uri: str) -> None:
        self.uri = uri


@pytest.fixture
def mount_dir(monkeypatch, tmpdir):
    monkeypatch.setattr(local_file, 'MOUNT_DIR', str(tmpdir))
    return tmpdir


@pytest.fixture
def fake_file_factory(mount_dir, tmp_path):
    def factory(content):
        filename = 'testfile'
        obj = SourceURI(f'http://example.com/files/{filename}')
        original = tmp_path / filename

        if isinstance(content, str):
            mode = 'r'
            original.write_text(content)
        else:
            mode = 'rb'
            original.write_bytes(content)

        return open(str(original), mode), obj
    return factory


@pytest.fixture
def read_file_factory(fake_file_factory):
    def factory(cache_func, content):
        f, obj = fake_file_factory(content)

        with f:
            decorated = cache_func(f.read)
            return decorated(obj), decorated(obj)
    return factory


@pytest.fixture
def read_iter_factory(fake_file_factory):
    def factory(cache_func, content):
        f, obj = fake_file_factory(content)

        def make_iter(chunk_size):
            return iter(partial(f.read, chunk_size), b'')

        with f:
            decorated = cache_func(make_iter)
            return decorated(obj), decorated(obj)
    return factory


def test_use_text_cache(read_file_factory):
    content = 'Hello, World!'
    saved, cached = read_file_factory(use_text_cache, content)
    assert saved == content
    assert cached == content


def test_use_binary_cache(read_file_factory):
    content = b'test'
    saved, cached = read_file_factory(use_binary_cache, content)
    assert saved == content
    assert cached == content


def test_use_iter_content_cache(read_iter_factory):
    content = secrets.token_bytes(int(DEFAULT_CHUNK_SIZE * 3.7))
    saved, cached = read_iter_factory(use_iter_content_cache, content)
    assert b''.join(list(saved)) == content
    assert b''.join(list(cached)) == content
