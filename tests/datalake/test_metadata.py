from unittest import TestCase
from unittest.mock import Mock

from abeja.datalake.metadata import DatalakeMetadata

CHANNEL_ID = '1230000000000'
FILE_ID = '20180601T052244-250482c0-d361-4c5b-a0f9-e796af1a5f0d'


class TestMetadata(TestCase):
    def test_main(self):
        mock_api = Mock()
        current_metadta = {
            'x-abeja-meta-filename': 'test.jpg'
        }
        metadata = DatalakeMetadata(
            mock_api, CHANNEL_ID, FILE_ID, current_metadta)
        metadata['label'] = 'cat'

        self.assertEqual(len(metadata), 2)
        self.assertIn('filename', metadata)
        self.assertIn('label', metadata)
        self.assertEqual(metadata['filename'], 'test.jpg')
        self.assertEqual(metadata['label'], 'cat')

        expected_keys = ['filename', 'label']
        expected_values = ['test.jpg', 'cat']

        # keys() methods
        self.assertEqual(set(expected_keys), set(metadata.keys()))

        # values() methods
        self.assertEqual(set(expected_values), set(metadata.values()))

        # items() methods
        self.assertDictEqual({
            'filename': 'test.jpg',
            'label': 'cat'
        }, dict(metadata.items()))

        for k, v in metadata.items():
            self.assertIn(k, expected_keys)
            self.assertIn(v, expected_values)

        # get methods
        self.assertIsNone(metadata.get('not_exist_key'))

    def test_initialize_with_none(self):
        mock_api = Mock()
        DatalakeMetadata(mock_api, CHANNEL_ID, FILE_ID, None)

    def test_update(self):
        mock_api = Mock()
        current_metadta = {
            'x-abeja-meta-filename': 'test.jpg'
        }
        metadata = DatalakeMetadata(
            mock_api, CHANNEL_ID, FILE_ID, current_metadta)
        new_metadata = {
            'label': 'cat'
        }
        metadata.update(new_metadata)
        self.assertEqual(len(metadata), 2)
        self.assertIn('filename', metadata)
        self.assertIn('label', metadata)
        self.assertEqual(metadata['filename'], 'test.jpg')
        self.assertEqual(metadata['label'], 'cat')

    def test_update_overwrite(self):
        mock_api = Mock()
        current_metadta = {
            'x-abeja-meta-filename': 'test.jpg'
        }
        metadata = DatalakeMetadata(
            mock_api, CHANNEL_ID, FILE_ID, current_metadta)
        new_metadata = {
            'filename': 'sample.jpg'
        }
        metadata.update(new_metadata)
        self.assertEqual(len(metadata), 1)
        self.assertIn('filename', metadata)
        self.assertEqual(metadata['filename'], 'sample.jpg')
