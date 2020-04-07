import unittest

from mock import MagicMock

from abeja.datasets.dataset import Dataset, Datasets
from abeja.datasets.dataset_item import DatasetItems


class TestDataset(unittest.TestCase):
    def setUp(self):
        self.organization_id = '1234567890120'
        self.dataset_id = '1234567890121'
        self.dataset_item_id = '1234567890122'
        self.name = 'test dataset'
        self.type = 'detection'
        self.props = {
            "categories": [
                {
                    "id": 1,
                    "name": "犬"
                },
                {
                    "id": 2,
                    "name": "猫"
                }
            ],
            "id": 0,
            "name": "test dog or cat"
        }
        self.total_count = 3670
        self.source_data = [
            {
                'data_type': 'image/jpeg',
                'data_uri': 'datalake://1200123803688/20170815T044617-f20dde80-1e3b-4496-bc06-1b63b026b872',
                'height': 500,
                'width': 200
            }
        ]
        self.attributes = {
            'classification': {
                'id': 1,
                'label': '犬'
            },
            'custom': {
                'anything': 'something'
            },
            'detection': [
                {
                    'id': 2,
                    'label': '猫',
                    'rect': [795, 118, 1143, 418]
                }
            ]
        }

    def _build_dataset_response(self):
        return {
            "organization_id": self.organization_id,
            "dataset_id": self.dataset_id,
            "name": self.name,
            "props": self.props,
            "total_count": self.total_count,
            "type": self.type,
            "created_at": "2017-01-01T00:00:00.000000",
            "updated_at": "2017-01-01T00:00:00.000000"
        }

    def test_init(self):
        dataset = Dataset(None, self.organization_id, self.dataset_id,
                          name=self.name, type=self.type, props=self.props, total_count=self.total_count)
        self.assertEqual(dataset.organization_id, self.organization_id)
        self.assertEqual(dataset.dataset_id, self.dataset_id)
        self.assertEqual(dataset.name, self.name)
        self.assertEqual(dataset.type, self.type)
        self.assertEqual(dataset.props, self.props)
        self.assertEqual(dataset.total_count, self.total_count)
        self.assertIsInstance(dataset.dataset_items, DatasetItems)

    def test_skip_unrecognized_arguments(self):
        # make sure constructor can ignore unknown parameters because API response can change any time
        dataset = Dataset(None, self.organization_id, self.dataset_id,
                          name=self.name, type=self.type, props=self.props,
                          total_count=self.total_count,
                          ____undefined='____undefined')
        self.assertEqual(dataset.organization_id, self.organization_id)
        self.assertEqual(dataset.dataset_id, self.dataset_id)
        self.assertEqual(dataset.name, self.name)
        self.assertEqual(dataset.type, self.type)
        self.assertEqual(dataset.props, self.props)
        self.assertEqual(dataset.total_count, self.total_count)
        self.assertIsInstance(dataset.dataset_items, DatasetItems)


class TestDatasets(unittest.TestCase):
    def setUp(self):
        self.organization_id = '1234567890120'
        self.dataset_id = '1234567890121'
        self.dataset_item_id = '1234567890122'
        self.name = 'test dataset'
        self.type = 'detection'
        self.props = {
            "categories": [
                {
                    "id": 1,
                    "name": "犬"
                },
                {
                    "id": 2,
                    "name": "猫"
                }
            ],
            "id": 0,
            "name": "test dog or cat"
        }
        self.total_count = 3670
        self.source_data = {
            'data_type': 'image/jpeg',
            'data_uri': 'datalake://1200123803688/20170815T044617-f20dde80-1e3b-4496-bc06-1b63b026b872',
            'height': 500,
            'width': 200
        }
        self.attributes = {
            'classification': {
                'id': 1,
                'label': '犬'
            },
            'custom': {
                'anything': 'something'
            },
            'detection': [
                {
                    'id': 2,
                    'label': '猫',
                    'rect': [795, 118, 1143, 418]
                }
            ]
        }

    def _build_dataset_response(self):
        return {
            "organization_id": self.organization_id,
            "dataset_id": self.dataset_id,
            "name": self.name,
            "props": self.props,
            "total_count": self.total_count,
            "type": self.type,
            "created_at": "2017-01-01T00:00:00.000000",
            "updated_at": "2017-01-01T00:00:00.000000"
        }

    def _build_dataset_item_response(self):
        return {
            'dataset_id': self.dataset_id,
            'dataset_item_id': self.dataset_item_id,
            'source_data': self.source_data,
            'attributes': self.attributes,
            'created_at': '2017-01-01T00:00:00.000000',
            'updated_at': '2017-01-01T00:00:00.000000'
        }

    def _build_dataset_items_response(self):
        return {
            'items': [
                self._build_dataset_item_response()
            ],
            'next_page_token': 'dummy page token'
        }

    def test_create(self):
        mock_api = MagicMock()
        mock_api.create_dataset.return_value = self._build_dataset_response()
        datasets = Datasets(mock_api, self.organization_id)
        dataset = datasets.create(self.name, self.type, self.props)
        self.assertIsInstance(dataset, Dataset)
        self.assertEqual(dataset.dataset_id, self.dataset_id)
        self.assertEqual(dataset.name, self.name)
        self.assertEqual(dataset.type, self.type)
        self.assertDictEqual(dataset.props, self.props)
        self.assertEqual(dataset.total_count, self.total_count)
        self.assertIsInstance(dataset.dataset_items, DatasetItems)
        mock_api.create_dataset.assert_called_once()

    def test_get(self):
        mock_api = MagicMock()
        mock_api.get_dataset.return_value = self._build_dataset_response()
        datasets = Datasets(mock_api, self.organization_id)
        dataset = datasets.get(self.dataset_id)
        self.assertIsInstance(dataset, Dataset)
        self.assertEqual(dataset.dataset_id, self.dataset_id)
        self.assertEqual(dataset.name, self.name)
        self.assertEqual(dataset.type, self.type)
        self.assertDictEqual(dataset.props, self.props)
        self.assertEqual(dataset.total_count, self.total_count)
        self.assertIsInstance(dataset.dataset_items, DatasetItems)
        mock_api.get_dataset.assert_called_once()

    def test_list(self):
        mock_api = MagicMock()
        mock_api.list_datasets.return_value = [self._build_dataset_response()]
        datasets = Datasets(mock_api, self.organization_id)
        _datasets = datasets.list()
        dataset = _datasets[0]
        self.assertIsInstance(dataset, Dataset)
        self.assertEqual(dataset.dataset_id, self.dataset_id)
        self.assertEqual(dataset.name, self.name)
        self.assertEqual(dataset.type, self.type)
        self.assertDictEqual(dataset.props, self.props)
        self.assertEqual(dataset.total_count, self.total_count)
        self.assertIsInstance(dataset.dataset_items, DatasetItems)
        mock_api.list_datasets.assert_called_once()

    def test_delete(self):
        mock_api = MagicMock()
        mock_api.delete_dataset.return_value = self._build_dataset_response()
        datasets = Datasets(mock_api, self.organization_id)
        dataset = datasets.delete(self.dataset_id)
        self.assertIsInstance(dataset, Dataset)
        self.assertEqual(dataset.dataset_id, self.dataset_id)
        self.assertEqual(dataset.name, self.name)
        self.assertEqual(dataset.type, self.type)
        self.assertDictEqual(dataset.props, self.props)
        self.assertEqual(dataset.total_count, self.total_count)
        self.assertIsInstance(dataset.dataset_items, DatasetItems)
        mock_api.delete_dataset.assert_called_once()
