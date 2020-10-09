from abeja.common import local_file
from abeja.common.local_file import use_text_cache, use_binary_cache
import pytest


class SourceURI:
    def __init__(self, uri: str) -> None:
        self.uri = uri


@pytest.fixture
def read_cache_factory(monkeypatch, tmp_path, tmpdir):
    def factory(cache_func, content):
        filename = 'testfile'
        monkeypatch.setattr(local_file, 'MOUNT_DIR', str(tmpdir))

        obj = SourceURI(f'http://example.com/files/{filename}')
        original = tmp_path / filename

        if isinstance(content, str):
            mode = 'r'
            original.write_text(content)
        else:
            mode = 'rb'
            original.write_bytes(content)

        with open(str(original), mode) as f:
            decorated = cache_func(f.read)
            return decorated(obj)
    return factory


def test_use_text_cache(read_cache_factory):
    content = 'Hello, World!'
    assert read_cache_factory(use_text_cache, content) == content


def test_use_binary_cache(read_cache_factory):
    content = b'test'
    assert read_cache_factory(use_binary_cache, content) == content
