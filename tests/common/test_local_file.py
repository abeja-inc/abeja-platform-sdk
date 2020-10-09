from abeja.common import local_file
from abeja.common.local_file import use_text_cache


class SourceURI:
    def __init__(self, uri: str) -> None:
        self.uri = uri


def test_use_binary_cache(monkeypatch, tmp_path, tmpdir):
    content = 'Hello, World!'
    filename = 'hello.txt'
    monkeypatch.setattr(local_file, 'MOUNT_DIR', str(tmpdir))

    obj = SourceURI(f'http://example.com/files/{filename}')
    original = tmp_path / filename
    original.write_text(content)

    with open(str(original), 'r') as f:
        decorated = use_text_cache(f.read)
        assert decorated(obj) == content
