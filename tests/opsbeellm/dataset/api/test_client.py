import os
import unittest

import requests_mock

from abeja.opsbeellm.dataset import APIClient
from abeja.exceptions import BadRequest

os.environ['USER_AUTH_ARMS'] = 'False'
ORGANIZATION_ID = '2222222222222'
DATASET_ID = '3333333333333'
DATASET_QA_ID = '4444444444444'
DATASET_LLM_ID = '5555555555555'
DATASET_NAME = 'datasetA'
DATASET_DESCRIPTION = 'datasetA description'
DATASET_ITEM_ID = '6666666666666'
DATASET_ITEM_INPUT_TEXT = 'ABEJAについて教えて'
DATASET_ITEM_OUTPUT_TEXT = 'ABEJAは、スペイン語で「ミツバチ」の意味であり、植物の受粉を手伝い、世界の食料生産を支える存在として社名になっています。'

DATASET_RES = {
    'id': DATASET_ID,
    'organization_id': ORGANIZATION_ID,
    'name': DATASET_NAME,
    'description': DATASET_DESCRIPTION,
    'type': 'qa',
    'created_at': "2023-12-14T04:42:34.913644Z",
    'updated_at': "2023-12-14T04:42:34.913644Z",
}
DATASETS_RES = {
    'organization_id': ORGANIZATION_ID,
    'datasets': [
        DATASET_RES,
    ],
    'has_next': False, 'limit': 10, 'offset': 0,
}

DATASET_QA_ITEM_RES = {
    'id': DATASET_ITEM_ID,
    'organization_id': ORGANIZATION_ID,
    'dataset_id': DATASET_QA_ID,
    'inputs': DATASET_ITEM_INPUT_TEXT,
    'outputs': DATASET_ITEM_OUTPUT_TEXT,
    'tags': [
        'TAG1',
        'TAG2',
    ],
    'metadata': [
        {'metadata1': "value1"},
        {'metadata2': "value2"},
    ],
    'created_at': "2023-12-14T04:42:34.913644Z",
    'updated_at': "2023-12-14T04:42:34.913644Z",
}
DATASET_LLM_ITEM_RES = {
    'id': DATASET_ITEM_ID,
    'organization_id': ORGANIZATION_ID,
    'dataset_id': DATASET_LLM_ID,
    'inputs': [
        {'input_text': DATASET_ITEM_INPUT_TEXT},
    ],
    'outputs': [
        {'output_text': DATASET_ITEM_OUTPUT_TEXT},
    ],
    'tags': [
        'TAG1',
        'TAG2',
    ],
    'metadata': [
        {'metadata1': "value1"},
        {'metadata2': "value2"},
    ],
    'created_at': "2023-12-14T04:42:34.913644Z",
    'updated_at': "2023-12-14T04:42:34.913644Z",
}
DATASET_QA_ITEMS_RES = {
    'organization_id': ORGANIZATION_ID,
    'dataset_id': DATASET_QA_ID,
    'items': [
        DATASET_QA_ITEM_RES,
        DATASET_QA_ITEM_RES,
    ],
    'has_next': False, 'limit': 10, 'offset': 0,
}
DATASET_LLM_ITEMS_RES = {
    'organization_id': ORGANIZATION_ID,
    'dataset_id': DATASET_LLM_ID,
    'items': [
        DATASET_LLM_ITEM_RES,
        DATASET_LLM_ITEM_RES,
    ],
    'has_next': False, 'limit': 10, 'offset': 0,
}


class TestOpsBeeLLMAPIClient(unittest.TestCase):

    @requests_mock.Mocker()
    def test_get_datasets(self, m):
        # get-datasets-api mock
        path = '/opsbee-llm/organizations/{}/datasets'.format(
            ORGANIZATION_ID,
        )
        m.get(path, json=DATASETS_RES)

        # unit test
        client = APIClient()
        ret = client.get_datasets(
            ORGANIZATION_ID,
        )
        self.assertDictEqual(ret, DATASETS_RES)

    @requests_mock.Mocker()
    def test_get_dataset(self, m):
        # get-dataset-api mock
        path = '/opsbee-llm/organizations/{}/datasets/{}'.format(
            ORGANIZATION_ID,
            DATASET_ID,
        )
        m.get(path, json=DATASET_RES)

        # unit test
        client = APIClient()
        ret = client.get_dataset(
            ORGANIZATION_ID,
            DATASET_ID,
        )
        self.assertDictEqual(ret, DATASET_RES)

    @requests_mock.Mocker()
    def test_create_dataset(self, m):
        # create-dataset-api mock
        path = '/opsbee-llm/organizations/{}/datasets'.format(
            ORGANIZATION_ID,
        )
        m.post(path, json=DATASET_RES)

        # unit test
        client = APIClient()
        ret = client.create_dataset(
            ORGANIZATION_ID,
            name=DATASET_RES['name'],
            description=DATASET_RES['description'],
            type=DATASET_RES['type'],
        )
        expected_payload = {
            'name': DATASET_RES['name'],
            'description': DATASET_RES['description'],
            'type': DATASET_RES['type'],
        }

        self.assertDictEqual(m.request_history[0].json(), expected_payload)
        self.assertDictEqual(ret, DATASET_RES)

        with self.assertRaises(BadRequest) as e:
            client.create_dataset(
                ORGANIZATION_ID,
                name=None,
                description=None,
                type=None,
            )
        self.assertEqual(e.exception.error_description, '"name" is necessary')

        with self.assertRaises(BadRequest) as e:
            client.create_dataset(
                ORGANIZATION_ID,
                name=DATASET_RES['name'],
                description=None,
                type=None,
            )
        self.assertEqual(e.exception.error_description, '"type" is necessary')

        with self.assertRaises(BadRequest) as e:
            client.create_dataset(
                ORGANIZATION_ID,
                name=DATASET_RES['name'],
                description=None,
                type='chat',
            )
        self.assertEqual(e.exception.error_description, '"type" need to "qa" or "llm"')

    @requests_mock.Mocker()
    def test_update_dataset(self, m):
        # update-dataset-api mock
        path = '/opsbee-llm/organizations/{}/datasets/{}'.format(
            ORGANIZATION_ID,
            DATASET_ID,
        )
        m.patch(path, json=DATASET_RES)

        # unit test
        client = APIClient()
        ret = client.update_dataset(
            ORGANIZATION_ID,
            DATASET_ID,
            name=DATASET_RES['name'],
            description=DATASET_RES['description'],
        )
        expected_payload = {
            'name': DATASET_RES['name'],
            'description': DATASET_RES['description'],
        }

        self.assertDictEqual(m.request_history[0].json(), expected_payload)
        self.assertDictEqual(ret, DATASET_RES)

        with self.assertRaises(BadRequest) as e:
            client.update_dataset(
                ORGANIZATION_ID,
                DATASET_ID,
                name=None,
                description=None,
            )
        self.assertEqual(e.exception.error_description, '"name" is necessary')

    @requests_mock.Mocker()
    def test_delete_dataset(self, m):
        # delete-dataset-api mock
        path = '/opsbee-llm/organizations/{}/datasets/{}'.format(
            ORGANIZATION_ID,
            DATASET_ID,
        )
        m.delete(path, json=DATASET_RES)

        # unit test
        client = APIClient()
        ret = client.delete_dataset(
            ORGANIZATION_ID,
            DATASET_ID,
        )
        self.assertDictEqual(ret, DATASET_RES)

    @requests_mock.Mocker()
    def test_get_dataset_items(self, m):
        # get-dataset-items-api mock
        path = '/opsbee-llm/organizations/{}/datasets/{}/items'.format(
            ORGANIZATION_ID,
            DATASET_QA_ID,
        )
        m.get(path, json=DATASET_QA_ITEMS_RES)

        client = APIClient()
        ret = client.get_dataset_items(
            ORGANIZATION_ID,
            DATASET_QA_ID,
        )
        self.assertDictEqual(ret, DATASET_QA_ITEMS_RES)

        path = '/opsbee-llm/organizations/{}/datasets/{}/items'.format(
            ORGANIZATION_ID,
            DATASET_LLM_ID,
        )
        m.get(path, json=DATASET_LLM_ITEMS_RES)
        ret = client.get_dataset_items(
            ORGANIZATION_ID,
            DATASET_LLM_ID,
        )
        self.assertDictEqual(ret, DATASET_LLM_ITEMS_RES)

    @requests_mock.Mocker()
    def test_get_dataset_item(self, m):
        # get-dataset-item-api mock
        path = '/opsbee-llm/organizations/{}/datasets/{}/items/{}'.format(
            ORGANIZATION_ID,
            DATASET_QA_ID,
            DATASET_ITEM_ID,
        )
        m.get(path, json=DATASET_QA_ITEM_RES)

        client = APIClient()
        ret = client.get_dataset_item(
            ORGANIZATION_ID,
            DATASET_QA_ID,
            DATASET_ITEM_ID,
        )
        self.assertDictEqual(ret, DATASET_QA_ITEM_RES)

        path = '/opsbee-llm/organizations/{}/datasets/{}/items/{}'.format(
            ORGANIZATION_ID,
            DATASET_LLM_ID,
            DATASET_ITEM_ID,
        )
        m.get(path, json=DATASET_LLM_ITEM_RES)
        ret = client.get_dataset_item(
            ORGANIZATION_ID,
            DATASET_LLM_ID,
            DATASET_ITEM_ID,
        )
        self.assertDictEqual(ret, DATASET_LLM_ITEM_RES)

    @requests_mock.Mocker()
    def test_create_dataset_item(self, m):
        # create-dataset-item-api mock
        path = '/opsbee-llm/organizations/{}/datasets/{}/items'.format(
            ORGANIZATION_ID,
            DATASET_ID,
        )
        m.post(path, json=DATASET_LLM_ITEM_RES)

        # unit test
        client = APIClient()
        ret = client.create_dataset_item(
            ORGANIZATION_ID,
            DATASET_ID,
            inputs=DATASET_LLM_ITEM_RES['inputs'],
            outputs=DATASET_LLM_ITEM_RES['outputs'],
            tags=DATASET_LLM_ITEM_RES['tags'],
            metadata=DATASET_LLM_ITEM_RES['metadata']
        )
        expected_payload = {
            'inputs': DATASET_LLM_ITEM_RES['inputs'],
            'outputs': DATASET_LLM_ITEM_RES['outputs'],
            'tags': DATASET_LLM_ITEM_RES['tags'],
            'metadata': DATASET_LLM_ITEM_RES['metadata'],
        }

        self.assertDictEqual(m.request_history[0].json(), expected_payload)
        self.assertDictEqual(ret, DATASET_LLM_ITEM_RES)

        with self.assertRaises(BadRequest) as e:
            client.create_dataset_item(
                ORGANIZATION_ID,
                DATASET_ID,
                inputs=None,
                outputs=None,
                tags=None,
                metadata=DATASET_LLM_ITEM_RES['metadata'],
            )
        self.assertEqual(e.exception.error_description, '"inputs" is necessary')

        with self.assertRaises(BadRequest) as e:
            client.create_dataset_item(
                ORGANIZATION_ID,
                DATASET_ID,
                inputs=[],
                outputs=None,
                tags=None,
                metadata=DATASET_LLM_ITEM_RES['metadata'],
            )
        self.assertEqual(e.exception.error_description, '"inputs" is necessary')

        with self.assertRaises(BadRequest) as e:
            client.create_dataset_item(
                ORGANIZATION_ID,
                DATASET_ID,
                inputs=DATASET_LLM_ITEM_RES['inputs'],
                outputs=None,
                tags=None,
                metadata=DATASET_LLM_ITEM_RES['metadata'],
            )
        self.assertEqual(e.exception.error_description, '"outputs" is necessary')

        with self.assertRaises(BadRequest) as e:
            client.create_dataset_item(
                ORGANIZATION_ID,
                DATASET_ID,
                inputs=DATASET_LLM_ITEM_RES['inputs'],
                outputs=[],
                tags=None,
                metadata=DATASET_LLM_ITEM_RES['metadata'],
            )
        self.assertEqual(e.exception.error_description, '"outputs" is necessary')

    @requests_mock.Mocker()
    def test_delete_dataset_item(self, m):
        # delete-dataset-item-api mock
        path = '/opsbee-llm/organizations/{}/datasets/{}/items/{}'.format(
            ORGANIZATION_ID,
            DATASET_QA_ID,
            DATASET_ITEM_ID,
        )
        m.delete(path, json=DATASET_QA_ITEM_RES)

        client = APIClient()
        ret = client.delete_dataset_item(
            ORGANIZATION_ID,
            DATASET_QA_ID,
            DATASET_ITEM_ID,
        )
        self.assertDictEqual(ret, DATASET_QA_ITEM_RES)

        path = '/opsbee-llm/organizations/{}/datasets/{}/items/{}'.format(
            ORGANIZATION_ID,
            DATASET_LLM_ID,
            DATASET_ITEM_ID,
        )
        m.delete(path, json=DATASET_LLM_ITEM_RES)
        ret = client.delete_dataset_item(
            ORGANIZATION_ID,
            DATASET_LLM_ID,
            DATASET_ITEM_ID,
        )
        self.assertDictEqual(ret, DATASET_LLM_ITEM_RES)
