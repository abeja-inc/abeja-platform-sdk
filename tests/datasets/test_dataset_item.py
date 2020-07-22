import unittest

from mock import MagicMock, patch
from parameterized import parameterized

from abeja.datalake.file import DatalakeFile
from abeja.datasets.dataset_item import DatasetItem, DatasetItems, DatasetItemIterator


DATASET_ITEM_SOURCE_DATA_DATALAKE = [
    {
        'data_type': 'image/jpeg',
        'data_uri': 'datalake://1200123803688/20170815T044617-f20dde80-1e3b-4496-bc06-1b63b026b872',
        'height': 500,
        'width': 200
    }
]
DATASET_ITEM_SOURCE_DATA_HTTP = [
    {
        "data_uri": "http://example.com/hoge/foo/bar.jpg",
    }
]


class TestDatasetItem(unittest.TestCase):
    def setUp(self):
        self.organization_id = '1234567890000'
        self.dataset_id = '1234567890100'
        self.item_id = '1234567890123'
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
        self.source_data = [
            {
                'data_type': 'image/jpeg',
                'data_uri': 'datalake://1200123803688/20170815T044617-f20dde80-1e3b-4496-bc06-1b63b026b872',
                'height': 500,
                'width': 200}]
        self.created_at = "2017-01-01T00:00:00Z"
        self.updated_at = "2017-01-01T00:00:00Z"
        self.maxDiff = None

    def test_init(self):
        item = DatasetItem(None, self.organization_id,
                           self.dataset_id, self.item_id,
                           attributes=self.attributes,
                           source_data=self.source_data,
                           created_at=self.created_at,
                           updated_at=self.updated_at)
        self.assertEqual(item.dataset_item_id, self.item_id)
        self.assertEqual(item._api, None)
        self.assertDictEqual(item.attributes, self.attributes)
        self.assertIsInstance(item.source_data, list)
        self.assertIsInstance(item.source_data[0], DatalakeFile)
        self.assertEqual(item.created_at, self.created_at)
        self.assertEqual(item.updated_at, self.updated_at)

    def test_init_with_two_source_data(self):
        source_data = [{'data_type': 'image/jpeg',
                        'data_uri': 'datalake://1200123803688/20170815T044617-f20dde80-1e3b-4496-bc06-1b63b026b872',
                        'height': 500,
                        'width': 200},
                       {'data_type': 'image/jpeg',
                        'data_uri': 'datalake://1200123803688/20170815T044617-f20dde80-1e3b-4496-bc06-1b63b026b872',
                        'height': 500,
                        'width': 200}]
        item = DatasetItem(None, self.organization_id,
                           self.dataset_id, self.item_id,
                           attributes=self.attributes,
                           source_data=source_data,
                           created_at=self.created_at,
                           updated_at=self.updated_at)
        self.assertEqual(item.dataset_item_id, self.item_id)
        self.assertEqual(item._api, None)
        self.assertDictEqual(item.attributes, self.attributes)
        self.assertIsInstance(item.source_data, list)
        self.assertIsInstance(item.source_data[0], DatalakeFile)
        self.assertEqual(item.created_at, self.created_at)
        self.assertEqual(item.updated_at, self.updated_at)

    @parameterized.expand([
        (
            DATASET_ITEM_SOURCE_DATA_DATALAKE,
            [
                {
                    "data_type": "image/jpeg",
                    "data_uri": "datalake://1200123803688/20170815T044617-f20dde80-1e3b-4496-bc06-1b63b026b872",
                }
            ]
        ),
        (
            DATASET_ITEM_SOURCE_DATA_HTTP,
            DATASET_ITEM_SOURCE_DATA_HTTP
        )
    ])
    def test_asdict(self, source_data, expected_source_data):
        item = DatasetItem(None, self.organization_id,
                           self.dataset_id, self.item_id,
                           attributes=self.attributes,
                           source_data=source_data,
                           created_at=self.created_at,
                           updated_at=self.updated_at)
        assert item.asdict() == {
            'dataset_id': self.dataset_id,
            'dataset_item_id': self.item_id,
            'source_data': expected_source_data,
            'attributes': self.attributes,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class TestDatasetItemIterator(unittest.TestCase):
    def setUp(self):
        self.organization_id = '1234567890000'
        self.dataset_id = '1234567890100'
        self.item_id = '1234567890123'
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
        self.source_data = [
            {
                'data_type': 'image/jpeg',
                'data_uri': 'datalake://1200123803688/20170815T044617-f20dde80-1e3b-4496-bc06-1b63b026b872',
                'height': 500,
                'width': 200}]
        self.created_at = "2017-01-01T00:00:00Z"
        self.updated_at = "2017-01-01T00:00:00Z"

    def test_next(self):
        mock_api = MagicMock()
        mock_api.list_dataset_items.side_effect = [
            {
                'next_page_token': 'dummy1',
                'items': [
                    {'dataset_id': self.dataset_id, 'dataset_item_id': 'item_id_1'},
                    {'dataset_id': self.dataset_id, 'dataset_item_id': 'item_id_2'},
                    {'dataset_id': self.dataset_id, 'dataset_item_id': 'item_id_3'},
                ]
            },
            {
                'next_page_token': 'dummy2',
                'items': [
                    {'dataset_id': self.dataset_id, 'dataset_item_id': 'item_id_4'},
                    {'dataset_id': self.dataset_id, 'dataset_item_id': 'item_id_5'},
                    {'dataset_id': self.dataset_id, 'dataset_item_id': 'item_id_6'},
                ]
            },
            {
                'next_page_token': 'dummy3',
                'items': [
                    {'dataset_id': self.dataset_id, 'dataset_item_id': 'item_id_7'},
                    {'dataset_id': self.dataset_id, 'dataset_item_id': 'item_id_8'},
                    {'dataset_id': self.dataset_id, 'dataset_item_id': 'item_id_9'},
                ]
            },
            {
                'next_page_token': None,
                'items': []
            }
        ]
        iterator = DatasetItemIterator(
            mock_api,
            organization_id=self.organization_id,
            dataset_id=self.dataset_id)
        item_1 = next(iterator)
        self.assertEqual(item_1.dataset_item_id, 'item_id_1')
        item_2 = next(iterator)
        self.assertEqual(item_2.dataset_item_id, 'item_id_2')
        self.assertEqual(len(list(iterator)), 7)

    def test_next_raise_stop_iteration(self):
        mock_api = MagicMock()
        mock_api.list_dataset_items.side_effect = [
            {
                'next_page_token': 'dummy1',
                'items': [
                    {'dataset_id': self.dataset_id, 'dataset_item_id': 'item_id_1'},
                    {'dataset_id': self.dataset_id, 'dataset_item_id': 'item_id_2'},
                    {'dataset_id': self.dataset_id, 'dataset_item_id': 'item_id_3'},
                ]
            },
            {
                'next_page_token': 'dummy2',
                'items': [
                    {'dataset_id': self.dataset_id, 'dataset_item_id': 'item_id_4'},
                    {'dataset_id': self.dataset_id, 'dataset_item_id': 'item_id_5'}
                ]
            },
            {
                'next_page_token': None,
                'items': []
            }
        ]
        iterator = DatasetItemIterator(
            mock_api,
            organization_id=self.organization_id,
            dataset_id=self.dataset_id)
        for i in range(5):
            next(iterator)
        with self.assertRaises(StopIteration):
            next(iterator)
        self.assertEqual(mock_api.list_dataset_items.call_count, 3)

    def test_next_up_to_next_page_and_iter_1(self):
        mock_api = MagicMock()
        mock_api.list_dataset_items.side_effect = [
            {
                'next_page_token': 'dummy1',
                'items': [
                    {'dataset_id': self.dataset_id, 'dataset_item_id': 'item_id_1'},
                    {'dataset_id': self.dataset_id, 'dataset_item_id': 'item_id_2'},
                    {'dataset_id': self.dataset_id, 'dataset_item_id': 'item_id_3'},
                ]
            },
            {
                'next_page_token': 'dummy2',
                'items': [
                    {'dataset_id': self.dataset_id, 'dataset_item_id': 'item_id_4'},
                    {'dataset_id': self.dataset_id, 'dataset_item_id': 'item_id_5'}
                ]
            },
            {
                'next_page_token': None,
                'items': []
            }
        ]
        iterator = DatasetItemIterator(
            mock_api,
            organization_id=self.organization_id,
            dataset_id=self.dataset_id)
        item_1 = next(iterator)
        self.assertEqual(item_1.dataset_item_id, 'item_id_1')
        item_2 = next(iterator)
        self.assertEqual(item_2.dataset_item_id, 'item_id_2')
        item_3 = next(iterator)
        self.assertEqual(item_3.dataset_item_id, 'item_id_3')

        mock_api.list_dataset_items.assert_called_with(
            self.organization_id, self.dataset_id, params={})

        item_4 = next(iterator)
        self.assertEqual(item_4.dataset_item_id, 'item_id_4')

        # take last one from __iter__
        self.assertEqual(len(list(iterator)), 1)
        self.assertEqual(mock_api.list_dataset_items.call_count, 3)

    def test_next_up_to_next_page_and_iter_2(self):
        mock_api = MagicMock()
        mock_api.list_dataset_items.side_effect = [
            {
                'next_page_token': 'dummy1',
                'items': [
                    {'dataset_id': self.dataset_id, 'dataset_item_id': 'item_id_1'},
                    {'dataset_id': self.dataset_id, 'dataset_item_id': 'item_id_2'},
                    {'dataset_id': self.dataset_id, 'dataset_item_id': 'item_id_3'},
                ]
            },
            {
                'next_page_token': 'dummy2',
                'items': [
                    {'dataset_id': self.dataset_id, 'dataset_item_id': 'item_id_4'},
                    {'dataset_id': self.dataset_id, 'dataset_item_id': 'item_id_5'}
                ]
            },
            {
                'next_page_token': None,
                'items': []
            }
        ]
        iterator = DatasetItemIterator(
            mock_api,
            organization_id=self.organization_id,
            dataset_id=self.dataset_id)
        item_1 = next(iterator)
        self.assertEqual(item_1.dataset_item_id, 'item_id_1')
        item_2 = next(iterator)
        self.assertEqual(item_2.dataset_item_id, 'item_id_2')
        item_3 = next(iterator)
        self.assertEqual(item_3.dataset_item_id, 'item_id_3')

        self.assertEqual(len(list(iterator)), 2)
        self.assertEqual(mock_api.list_dataset_items.call_count, 3)
        mock_api.list_dataset_items.assert_called_with(
            self.organization_id, self.dataset_id, params={
                'next_page_token': 'dummy2'})

    def test__page_iter(self):
        mock_api = MagicMock()
        mock_api.list_dataset_items.side_effect = [
            self._build_dataset_items_response(),
            self._build_empty_dataset_items_response()
        ]
        iterator = DatasetItemIterator(
            mock_api, self.organization_id, self.dataset_id)
        page_iterator = iterator._page_iter()
        for page in page_iterator:
            self.assertIsInstance(page, list)
            for item in page:
                self.assertIsInstance(item, DatasetItem)

    def test__items_iter(self):
        mock_api = MagicMock()
        mock_api.list_dataset_items.side_effect = [
            self._build_dataset_items_response(),
            self._build_empty_dataset_items_response()
        ]
        iterator = DatasetItemIterator(
            mock_api, self.organization_id, self.dataset_id)
        with patch('abeja.datalake.file.DatalakeFile.get_content') as m:
            for item in iterator:
                self.assertIsInstance(item, DatasetItem)
            self.assertEqual(m.call_count, 0)

    def test__items_iter_with_prefetch(self):
        mock_api = MagicMock()
        mock_api.list_dataset_items.side_effect = [
            self._build_dataset_items_response(),
            self._build_empty_dataset_items_response()
        ]
        iterator = DatasetItemIterator(
            mock_api,
            self.organization_id,
            self.dataset_id,
            prefetch=True)
        with patch('abeja.datalake.file.DatalakeFile.get_content') as m:
            for item in iterator:
                self.assertIsInstance(item, DatasetItem)
            self.assertEqual(m.call_count, 1)

    def test__page(self):
        mock_api = MagicMock()
        mock_api.list_dataset_items.return_value = self._build_dataset_items_response()
        iterator = DatasetItemIterator(
            mock_api, self.organization_id, self.dataset_id)
        page = iterator._page()
        self.assertIsInstance(page, list)
        item = page[0]
        self.assertIsInstance(item, DatasetItem)

    def _build_dataset_item_response(self):
        return {
            "dataset_id": self.dataset_id,
            "dataset_item_id": self.item_id,
            "attributes": self.attributes,
            "source_data": self.source_data,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    def _build_dataset_items_response(self):
        return {
            'items': [
                self._build_dataset_item_response()
            ],
            'next_page_token': 'xxxxx'
        }

    def _build_empty_dataset_items_response(self):
        return {
            'items': [],
            'next_page_token': None
        }


class TestDatasetItems(unittest.TestCase):
    def setUp(self):
        self.organization_id = '1234567890000'
        self.dataset_id = '1234567890100'
        self.item_id = '1234567890123'
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
        self.bulk_attributes = [
            {
                "dataset_item_id": 1111111111111,
                "attributes": {
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
            }
        ]
        self.source_data = [
            {
                'data_type': 'image/jpeg',
                'data_uri': 'datalake://1200123803688/20170815T044617-f20dde80-1e3b-4496-bc06-1b63b026b872',
                'height': 500,
                'width': 200}]
        self.created_at = "2017-01-01T00:00:00Z"
        self.updated_at = "2017-01-01T00:00:00Z"

    def _build_dataset_item_response(self):
        return {
            "dataset_id": self.dataset_id,
            "dataset_item_id": self.item_id,
            "attributes": self.attributes,
            "source_data": self.source_data,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    def _build_dataset_items_response(self):
        return {
            'items': [
                self._build_dataset_item_response()
            ]
        }

    def _build_empty_dataset_items_response(self):
        return {
            'items': [],
            'next_page_token': None
        }

    def test_create(self):
        mock_api = MagicMock()
        mock_api.create_dataset_item.return_value = self._build_dataset_item_response()
        dataset_items = DatasetItems(
            mock_api, self.organization_id, self.dataset_id)
        item = dataset_items.create(self.source_data, self.attributes)
        self.assertIsInstance(item, DatasetItem)
        self.assertEqual(item.dataset_item_id, self.item_id)
        self.assertDictEqual(item.attributes, self.attributes)
        self.assertIsInstance(item.source_data, list)
        self.assertIsInstance(item.source_data[0], DatalakeFile)
        self.assertEqual(item.created_at, self.created_at)
        self.assertEqual(item.updated_at, self.updated_at)

    def test_get(self):
        mock_api = MagicMock()
        mock_api.get_dataset_item.return_value = self._build_dataset_item_response()
        dataset_items = DatasetItems(
            mock_api, self.organization_id, self.dataset_id)
        item = dataset_items.get(self.item_id)
        self.assertIsInstance(item, DatasetItem)
        self.assertEqual(item.dataset_item_id, self.item_id)
        self.assertDictEqual(item.attributes, self.attributes)
        self.assertIsInstance(item.source_data, list)
        self.assertIsInstance(item.source_data[0], DatalakeFile)
        self.assertEqual(item.created_at, self.created_at)
        self.assertEqual(item.updated_at, self.updated_at)

    def test_list(self):
        mock_api = MagicMock()
        mock_api.list_dataset_items.side_effect = [
            self._build_dataset_items_response(),
            self._build_empty_dataset_items_response()
        ]
        dataset_items = DatasetItems(
            mock_api, self.organization_id, self.dataset_id)
        for item in dataset_items.list():
            self.assertIsInstance(item, DatasetItem)

    def test_update(self):
        mock_api = MagicMock()
        mock_api.update_dataset_item.return_value = self._build_dataset_item_response()
        dataset_items = DatasetItems(
            mock_api, self.organization_id, self.dataset_id)
        item = dataset_items.update(self.item_id, self.attributes)
        self.assertIsInstance(item, DatasetItem)
        self.assertEqual(item.dataset_item_id, self.item_id)
        self.assertDictEqual(item.attributes, self.attributes)
        self.assertIsInstance(item.source_data, list)
        self.assertIsInstance(item.source_data[0], DatalakeFile)
        self.assertEqual(item.created_at, self.created_at)
        self.assertEqual(item.updated_at, self.updated_at)

    def test_bulk_update(self):
        mock_api = MagicMock()
        mock_api.update_dataset_item.return_value = self._build_dataset_item_response()
        dataset_items = DatasetItems(
            mock_api, self.organization_id, self.dataset_id)
        item = dataset_items.bulk_update(self.bulk_attributes)
        for item in item:
            self.assertIsInstance(item, DatasetItem)
            self.assertIsInstance(item, DatasetItem)
            self.assertEqual(item.dataset_item_id, self.item_id)
            self.assertDictEqual(item.attributes, self.attributes)
            self.assertIsInstance(item.source_data, list)
            self.assertIsInstance(item.source_data[0], DatalakeFile)
            self.assertEqual(item.created_at, self.created_at)
            self.assertEqual(item.updated_at, self.updated_at)

    def test_delete(self):
        mock_api = MagicMock()
        mock_api.delete_dataset_item.return_value = self._build_dataset_item_response()
        dataset_items = DatasetItems(
            mock_api, self.organization_id, self.dataset_id)
        item = dataset_items.delete(self.item_id)
        self.assertIsInstance(item, DatasetItem)
        self.assertEqual(item.dataset_item_id, self.item_id)
        self.assertDictEqual(item.attributes, self.attributes)
        self.assertIsInstance(item.source_data, list)
        self.assertIsInstance(item.source_data[0], DatalakeFile)
        self.assertEqual(item.created_at, self.created_at)
        self.assertEqual(item.updated_at, self.updated_at)
