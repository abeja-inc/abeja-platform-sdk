from unittest import TestCase
from unittest.mock import Mock

from abeja.common.file_factory import file_factory
from abeja.datalake.file import DatalakeFile
from abeja.exceptions import UnsupportedURI


class TestFileFactory(TestCase):
    def test_file_factory(self):
        mock_api = Mock()
        uri = 'datalake://1234567890123/20171128T113546-9fa120a3-96bc-4b84-b56b-1bc2273178a1'
        type = 'image/jpeg'
        file = file_factory(mock_api, uri, type)
        self.assertIsInstance(file, DatalakeFile)

    def test_file_factory_not_supported(self):
        mock_api = Mock()
        uri = 's3://1234567890123/20171128T113546-9fa120a3-96bc-4b84-b56b-1bc2273178a1'
        type = 'image/jpeg'
        with self.assertRaises(UnsupportedURI):
            file_factory(mock_api, uri, type)
