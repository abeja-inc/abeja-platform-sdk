from unittest import TestCase
from unittest.mock import Mock

from parameterized import parameterized

from abeja.common.file_factory import file_factory
from abeja.common.public_file import PublicFile
from abeja.datalake.file import DatalakeFile
from abeja.exceptions import UnsupportedURI


class TestFileFactory(TestCase):
    @parameterized.expand(
        [
            ('datalake://1234567890123/20171128T113546-9fa120a3-96bc-4b84-b56b-1bc2273178a1',
             'image/jpeg',
             DatalakeFile,
             ),
            ("http://example.com/hoge/foo/bar",
             None,
             PublicFile,
             ),
            ("https://example.com/1/2/3/4",
             None,
             PublicFile,
             )])
    def test_file_factory(self, uri, _type, expected):
        mock_api = Mock()
        file = file_factory(mock_api, uri, _type)
        self.assertIsInstance(file, expected)

    def test_file_factory_not_supported(self):
        mock_api = Mock()
        uri = 's3://1234567890123/20171128T113546-9fa120a3-96bc-4b84-b56b-1bc2273178a1'
        type = 'image/jpeg'
        with self.assertRaises(UnsupportedURI):
            file_factory(mock_api, uri, type)
