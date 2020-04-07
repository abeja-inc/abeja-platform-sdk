import unittest

from mock import MagicMock

from abeja.datasets.client import Client
from abeja.datasets.dataset import Datasets, Dataset
from abeja.datasets.api.client import APIClient


class TestClient(unittest.TestCase):
    def setUp(self):
        self.organization_id = '1230000000000'
        self.dataset_id = '1234567890123'
        self.name = 'test_dataset'
        self.type = 'test_type'
        self.props = {'test': 'props'}
        self.client = Client()
        self.dataset_item_id = '1234567890000'
        self.annotation = None

    def _build_dataset_response(self):
        return {
            "organization_id": self.organization_id,
            "dataset_id": self.dataset_id,
            "name": self.name,
            "type": self.type,
            "props": self.props,
            "created_at": "2017-01-01T00:00:00.000000",
            "updated_at": "2017-01-01T00:00:00.000000"
        }

    def _build_datasets_response(self):
        return [
            self._build_dataset_response()
        ]

    def test_init(self):
        client = Client()
        self.assertIsInstance(client.api, APIClient)
        self.assertIsInstance(client.datasets, Datasets)

    def test_datasets(self):
        client = Client(self.organization_id)
        self.assertIsInstance(client.datasets, Datasets)
        self.assertIsInstance(client.datasets._api, APIClient)
        self.assertEqual(client.datasets.organization_id, self.organization_id)

    def test_get_dataset(self):
        client = Client(self.organization_id)
        mock_api = MagicMock()
        mock_api.get_dataset.return_value = self._build_dataset_response()
        client.api = mock_api
        dataset = client.get_dataset(self.dataset_id)
        self.assertIsInstance(dataset, Dataset)
        self.assertEqual(dataset.organization_id, self.organization_id)
        self.assertEqual(dataset.dataset_id, self.dataset_id)
        self.assertEqual(dataset.name, self.name)
        self.assertEqual(dataset.type, self.type)
        self.assertDictEqual(dataset.props, self.props)
