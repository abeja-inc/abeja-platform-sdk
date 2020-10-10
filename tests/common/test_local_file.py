from abeja.common import local_file
from abeja.common.local_file import use_text_cache, use_binary_cache, use_iter_content_cache, use_iter_lines_cache
from abeja.common.config import DEFAULT_CHUNK_SIZE
import pytest
import secrets
import io
import errno
from functools import partial
import builtins

ORIGINAL_OPEN = builtins.open


class MockIO:
    def __init__(self, file, raise_stale=False):
        self.file = file
        self.raise_stale = raise_stale

    def read(self, size=-1):
        if self.raise_stale:
            raise OSError(errno.ESTALE, 'Stale file handle')
        else:
            return self.file.read(size)

    def __iter__(self):
        return self

    def __next__(self):
        if self.raise_stale:
            raise OSError(errno.ESTALE, 'Stale file handle')
        else:
            line = self.file.readline()
            if line == '':
                raise StopIteration()
            else:
                return line

    def __enter__(self):
        self.file.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return self.file.__exit__(exc_type, exc_value, traceback)


def mock_open_factory():
    global first_invocation
    first_invocation = True

    def mock_open(path, mode):
        global first_invocation

        if mode.startswith('r'):
            raise_stale = first_invocation
            first_invocation = False
            return MockIO(ORIGINAL_OPEN(path, mode), raise_stale=raise_stale)
        else:
            return ORIGINAL_OPEN(path, mode)
    return mock_open


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
def read_file_factory(fake_file_factory, monkeypatch):
    def factory(cache_func, content):
        f, obj = fake_file_factory(content)

        with f:
            decorated = cache_func(f.read)
            with monkeypatch.context() as m:
                m.setattr(builtins, 'open', mock_open_factory())
                return decorated(obj), decorated(obj)
    return factory


@pytest.fixture
def read_iter_factory(fake_file_factory, monkeypatch):
    def factory(cache_func, content):
        f, obj = fake_file_factory(content)

        def make_iter(chunk_size=DEFAULT_CHUNK_SIZE):
            sentinel = '' if isinstance(content, str) else b''
            return iter(partial(f.read, chunk_size), sentinel)

        with f:
            decorated = cache_func(make_iter)
            with monkeypatch.context() as m:
                m.setattr(builtins, 'open', mock_open_factory())
                return list(decorated(obj)), list(decorated(obj))
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


def test_use_iter_lines_cache(read_iter_factory):
    content = '1\n2\n3'
    saved, cached = read_iter_factory(use_iter_lines_cache, content)
    assert list(saved) == ['1\n', '2\n', '3']
    assert list(cached) == ['1\n', '2\n', '3']
