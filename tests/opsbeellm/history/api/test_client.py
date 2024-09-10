import os
import unittest

import requests_mock

from abeja.opsbeellm.history import APIClient
from abeja.exceptions import BadRequest

os.environ['USER_AUTH_ARMS'] = 'False'
ORGANIZATION_ID = '2222222222222'
TAG_ID = '3333333333333'
DEPLOYMENT_ID = '4444444444444'
DEPLOYMENT_QA_ID = '5555555555555'
DEPLOYMENT_CHAT_ID = '6666666666666'
THREAD_ID = '7777777777777'
HISTORY_ID = '8888888888888'
METADATA_ID = '9999999999999'
INPUT_TEXT = 'ABEJAについて教えて'
OUTPUT_TEXT = 'ABEJAは、スペイン語で「ミツバチ」の意味であり、植物の受粉を手伝い、世界の食料生産を支える存在として社名になっています。'
INPUT_TOKEN_COUNT = 10
OUTPUT_TOKEN_COUNT = 10

TAG_RES = {
    'id': TAG_ID,
    'organization_id': ORGANIZATION_ID,
    'name': "TAG",
    'description': "tag description",
    'color': "red",
    'created_at': "2023-12-14T04:42:34.913644Z",
    'updated_at': "2023-12-14T04:42:34.913644Z",
}
TAGS_RES = {
    'organization_id': ORGANIZATION_ID,
    'tags': [
        TAG_RES,
    ],
    'offset': 0,
    'limit': 1000,
    'has_next': False,
}

DEPLOYMENT_QA_RES = {
    'id': DEPLOYMENT_QA_ID,
    'organization_id': ORGANIZATION_ID,
    'name': 'deployment name',
    'description': 'deployment description',
    'type': 'qa',
    'history_count': 0,
    'created_at': "2023-12-14T04:42:34.913644Z",
    'updated_at': "2023-12-14T04:42:34.913644Z",
}
DEPLOYMENT_CHAT_RES = {
    'id': DEPLOYMENT_CHAT_ID,
    'organization_id': ORGANIZATION_ID,
    'name': 'deployment name',
    'description': 'deployment description',
    'type': 'chat',
    'history_count': 0,
    'created_at': "2023-12-14T04:42:34.913644Z",
    'updated_at': "2023-12-14T04:42:34.913644Z",
}

THREAD_RES = {
    'id': THREAD_ID,
    'organization_id': ORGANIZATION_ID,
    'deployment_id': DEPLOYMENT_ID,
    'name': "thread name",
    'description': "thread description",
    'created_at': "2023-12-14T04:42:34.913644Z",
    'updated_at': "2023-12-14T04:42:34.913644Z",
}
THREADS_RES = {
    'organization_id': ORGANIZATION_ID,
    'deployment_id': DEPLOYMENT_ID,
    'threads': [
        THREAD_RES,
    ],
    'offset': 0,
    'limit': 1000,
    'has_next': False,
}

HISTORY_RES = {
    "id": HISTORY_ID,
    "organization_id": ORGANIZATION_ID,
    "deployment_id": DEPLOYMENT_ID,
    "thread_id": THREAD_ID,
    "input_text": INPUT_TEXT,
    "output_text": OUTPUT_TEXT,
    "input_token_count": INPUT_TOKEN_COUNT,
    "output_token_count": OUTPUT_TOKEN_COUNT,
    "tags": [
        TAG_RES,
    ],
    "matadata": [],
    "created_at": "2023-12-14T04:42:34.913644Z",
    "updated_at": "2018-12-15T04:42:34.913726Z"
}
HISTORIES_RES = {
    'organization_id': ORGANIZATION_ID,
    'deployment_id': DEPLOYMENT_ID,
    'thread_id': THREAD_ID,
    'histories': [
        HISTORY_RES,
    ],
    'offset': 0,
    'limit': 1000,
    'has_next': False,
}

METADATA_RES = {
    "id": METADATA_ID,
    "organization_id": ORGANIZATION_ID,
    "deployment_id": DEPLOYMENT_ID,
    "history_id": HISTORY_ID,
    "key": "metadata",
    "value": "dummy",
    "created_at": "2023-12-14T04:42:34.913644Z",
    "updated_at": "2018-12-15T04:42:34.913726Z"
}


class TestOpsBeeLLMAPIClient(unittest.TestCase):
    @requests_mock.Mocker()
    def test_get_threads(self, m):
        # get-threads-api mock
        path = '/opsbee-llm/organizations/{}/deployments/{}/threads'.format(
            ORGANIZATION_ID,
            DEPLOYMENT_ID,
        )
        m.get(path, json=THREADS_RES)

        # unit test
        client = APIClient()
        ret = client.get_threads(
            ORGANIZATION_ID,
            DEPLOYMENT_ID,
        )
        self.assertDictEqual(ret, THREADS_RES)

    @requests_mock.Mocker()
    def test_get_thread(self, m):
        # get-thread-api mock
        path = '/opsbee-llm/organizations/{}/deployments/{}/threads/{}'.format(
            ORGANIZATION_ID,
            DEPLOYMENT_ID,
            THREAD_ID
        )
        m.get(path, json=THREAD_RES)

        # unit test
        client = APIClient()
        ret = client.get_thread(
            ORGANIZATION_ID,
            DEPLOYMENT_ID,
            THREAD_ID
        )
        self.assertDictEqual(ret, THREAD_RES)

    @requests_mock.Mocker()
    def test_create_thread(self, m):
        # create-thread-api mock
        path = '/opsbee-llm/organizations/{}/deployments/{}/threads'.format(
            ORGANIZATION_ID,
            DEPLOYMENT_ID
        )
        m.post(path, json=THREAD_RES)

        # unit test
        client = APIClient()
        ret = client.create_thread(
            ORGANIZATION_ID,
            DEPLOYMENT_ID,
            name=THREAD_RES['name'],
            description=THREAD_RES['description'],
        )
        expected_payload = {
            'name': THREAD_RES['name'],
            'description': THREAD_RES['description'],
        }

        self.assertDictEqual(m.request_history[0].json(), expected_payload)
        self.assertDictEqual(ret, THREAD_RES)

        with self.assertRaises(BadRequest) as e:
            client.create_thread(
                ORGANIZATION_ID,
                DEPLOYMENT_ID,
                name=None,
                description=None,
            )
        self.assertEqual(e.exception.error_description, '"name" is necessary')

    @requests_mock.Mocker()
    def test_update_thread(self, m):
        # update-thread-api mock
        path = '/opsbee-llm/organizations/{}/deployments/{}/threads/{}'.format(
            ORGANIZATION_ID,
            DEPLOYMENT_ID,
            THREAD_ID
        )
        m.patch(path, json=THREAD_RES)

        # unit test
        client = APIClient()
        ret = client.update_thread(
            ORGANIZATION_ID,
            DEPLOYMENT_ID,
            THREAD_ID,
            name=THREAD_RES['name'],
            description=THREAD_RES['description'],
        )
        expected_payload = {
            'name': THREAD_RES['name'],
            'description': THREAD_RES['description'],
        }

        self.assertDictEqual(m.request_history[0].json(), expected_payload)
        self.assertDictEqual(ret, THREAD_RES)

        with self.assertRaises(BadRequest) as e:
            client.update_thread(
                ORGANIZATION_ID,
                DEPLOYMENT_ID,
                THREAD_ID,
                name=None,
                description=None,
            )
        self.assertEqual(e.exception.error_description, '"name" is necessary')

    @requests_mock.Mocker()
    def test_delete_thread(self, m):
        # delete-thread-api mock
        path = '/opsbee-llm/organizations/{}/deployments/{}/threads/{}'.format(
            ORGANIZATION_ID,
            DEPLOYMENT_ID,
            THREAD_ID
        )
        res = {
            'message': f'thread {THREAD_ID} was deleted.'
        }
        m.delete(path, json=res)

        # unit test
        client = APIClient()
        ret = client.delete_thread(
            ORGANIZATION_ID,
            DEPLOYMENT_ID,
            THREAD_ID
        )
        self.assertDictEqual(ret, res)

    @requests_mock.Mocker()
    def test_get_qa_histories(self, m):
        # get-deployment-api mock
        path = '/opsbee-llm/organizations/{}/deployments/{}'.format(
            ORGANIZATION_ID,
            DEPLOYMENT_QA_ID,
        )
        m.get(path, json=DEPLOYMENT_QA_RES)

        # get-historyies-api mock
        path = '/opsbee-llm/organizations/{}/deployments/{}/qa_histories'.format(
            ORGANIZATION_ID,
            DEPLOYMENT_QA_ID,
        )
        m.get(path, json=HISTORIES_RES)

        # unit test
        client = APIClient()
        ret = client.get_qa_histories(
            ORGANIZATION_ID,
            DEPLOYMENT_QA_ID,
        )
        self.assertDictEqual(ret, HISTORIES_RES)

    @requests_mock.Mocker()
    def test_get_qa_history(self, m):
        # get-deployment-api mock
        path = '/opsbee-llm/organizations/{}/deployments/{}'.format(
            ORGANIZATION_ID,
            DEPLOYMENT_QA_ID,
        )
        m.get(path, json=DEPLOYMENT_QA_RES)

        # get-history-api mock
        path = '/opsbee-llm/organizations/{}/deployments/{}/qa_histories/{}'.format(
            ORGANIZATION_ID,
            DEPLOYMENT_QA_ID,
            HISTORY_ID,
        )
        m.get(path, json=HISTORY_RES)

        # unit test
        client = APIClient()
        ret = client.get_qa_history(
            ORGANIZATION_ID,
            DEPLOYMENT_QA_ID,
            HISTORY_ID,
        )
        self.assertDictEqual(ret, HISTORY_RES)

    @requests_mock.Mocker()
    def test_create_qa_history(self, m):
        # get-deployment-api mock
        path = '/opsbee-llm/organizations/{}/deployments/{}'.format(
            ORGANIZATION_ID,
            DEPLOYMENT_QA_ID,
        )
        m.get(path, json=DEPLOYMENT_QA_RES)

        # create-history-api mock
        path = '/opsbee-llm/organizations/{}/deployments/{}/qa_histories'.format(
            ORGANIZATION_ID,
            DEPLOYMENT_QA_ID,
        )
        m.post(path, json=HISTORY_RES)

        # unit test
        client = APIClient()
        ret = client.create_qa_history(
            ORGANIZATION_ID,
            DEPLOYMENT_QA_ID,
            INPUT_TEXT,
            OUTPUT_TEXT,
            INPUT_TOKEN_COUNT,
            OUTPUT_TOKEN_COUNT,
        )
        expected_payload = {
            'input_text': INPUT_TEXT,
            'output_text': OUTPUT_TEXT,
            'input_token_count': INPUT_TOKEN_COUNT,
            'output_token_count': OUTPUT_TOKEN_COUNT,
            'tag_ids': [],
            'metadata': [],
        }

        self.assertDictEqual(m.request_history[1].json(), expected_payload)
        self.assertDictEqual(ret, HISTORY_RES)

        with self.assertRaises(BadRequest) as e:
            client.create_qa_history(
                ORGANIZATION_ID,
                DEPLOYMENT_QA_ID,
                input_text=None,
                output_text=None,
            )
        self.assertEqual(e.exception.error_description, '"input_text" is necessary')

        with self.assertRaises(BadRequest) as e:
            client.create_qa_history(
                ORGANIZATION_ID,
                DEPLOYMENT_QA_ID,
                input_text=INPUT_TEXT,
                output_text=None,
            )
        self.assertEqual(e.exception.error_description, '"output_text" is necessary')

        path = '/opsbee-llm/organizations/{}/deployments/{}'.format(
            ORGANIZATION_ID,
            DEPLOYMENT_CHAT_ID,
        )
        m.get(path, json=DEPLOYMENT_CHAT_RES)
        with self.assertRaises(BadRequest) as e:
            client.create_qa_history(
                ORGANIZATION_ID,
                DEPLOYMENT_CHAT_ID,
                input_text=INPUT_TEXT,
                output_text=OUTPUT_TEXT,
            )
        self.assertEqual(e.exception.error, 'deployment type is not supported')

    @requests_mock.Mocker()
    def test_update_qa_history(self, m):
        # get-deployment-api mock
        path = '/opsbee-llm/organizations/{}/deployments/{}'.format(
            ORGANIZATION_ID,
            DEPLOYMENT_QA_ID,
        )
        m.get(path, json=DEPLOYMENT_QA_RES)

        # get-history-api mock
        path = '/opsbee-llm/organizations/{}/deployments/{}/qa_histories/{}'.format(
            ORGANIZATION_ID,
            DEPLOYMENT_QA_ID,
            HISTORY_ID,
        )
        m.get(path, json=HISTORY_RES)

        # update-history-api mock
        path = '/opsbee-llm/organizations/{}/deployments/{}/qa_histories/{}'.format(
            ORGANIZATION_ID,
            DEPLOYMENT_QA_ID,
            HISTORY_ID,
        )
        m.patch(path, json=HISTORY_RES)

        # unit test
        client = APIClient()
        ret = client.update_qa_history(
            ORGANIZATION_ID,
            DEPLOYMENT_QA_ID,
            HISTORY_ID,
            INPUT_TEXT,
            OUTPUT_TEXT,
            INPUT_TOKEN_COUNT,
            OUTPUT_TOKEN_COUNT,
        )
        expected_payload = {
            'input_text': INPUT_TEXT,
            'output_text': OUTPUT_TEXT,
            'input_token_count': INPUT_TOKEN_COUNT,
            'output_token_count': OUTPUT_TOKEN_COUNT,
            'tag_ids': [TAG_ID],
        }

        self.assertDictEqual(m.request_history[2].json(), expected_payload)
        self.assertDictEqual(ret, HISTORY_RES)

        path = '/opsbee-llm/organizations/{}/deployments/{}'.format(
            ORGANIZATION_ID,
            DEPLOYMENT_CHAT_ID,
        )
        m.get(path, json=DEPLOYMENT_CHAT_RES)
        with self.assertRaises(BadRequest) as e:
            client.update_qa_history(
                ORGANIZATION_ID,
                DEPLOYMENT_CHAT_ID,
                HISTORY_ID,
                input_text=INPUT_TEXT,
                output_text=OUTPUT_TEXT,
            )
        self.assertEqual(e.exception.error, 'deployment type is not supported')

    @requests_mock.Mocker()
    def test_delete_qa_history(self, m):
        # get-deployment-api mock
        path = '/opsbee-llm/organizations/{}/deployments/{}'.format(
            ORGANIZATION_ID,
            DEPLOYMENT_QA_ID,
        )
        m.get(path, json=DEPLOYMENT_QA_RES)

        # delete-history-api mock
        path = '/opsbee-llm/organizations/{}/deployments/{}/qa_histories/{}'.format(
            ORGANIZATION_ID,
            DEPLOYMENT_QA_ID,
            HISTORY_ID,
        )
        m.delete(path, json=HISTORY_RES)

        # unit test
        client = APIClient()
        ret = client.delete_qa_history(
            ORGANIZATION_ID,
            DEPLOYMENT_QA_ID,
            HISTORY_ID,
        )
        self.assertDictEqual(ret, HISTORY_RES)

    @requests_mock.Mocker()
    def test_get_chat_histories(self, m):
        # get-deployment-api mock
        path = '/opsbee-llm/organizations/{}/deployments/{}'.format(
            ORGANIZATION_ID,
            DEPLOYMENT_CHAT_ID,
        )
        m.get(path, json=DEPLOYMENT_CHAT_RES)

        # get-histories-api mock
        path = '/opsbee-llm/organizations/{}/deployments/{}/histories'.format(
            ORGANIZATION_ID,
            DEPLOYMENT_CHAT_ID,
        )
        m.get(path, json=HISTORIES_RES)

        # unit test
        client = APIClient()
        ret = client.get_chat_histories(
            ORGANIZATION_ID,
            DEPLOYMENT_CHAT_ID,
        )
        self.assertDictEqual(ret, HISTORIES_RES)

    @requests_mock.Mocker()
    def test_get_chat_history(self, m):
        # get-deployment-api mock
        path = '/opsbee-llm/organizations/{}/deployments/{}'.format(
            ORGANIZATION_ID,
            DEPLOYMENT_CHAT_ID,
        )
        m.get(path, json=DEPLOYMENT_CHAT_RES)

        # get-history-api mock
        path = '/opsbee-llm/organizations/{}/deployments/{}/threads/{}/histories/{}'.format(
            ORGANIZATION_ID,
            DEPLOYMENT_CHAT_ID,
            THREAD_ID,
            HISTORY_ID,
        )
        m.get(path, json=HISTORY_RES)

        # unit test
        client = APIClient()
        ret = client.get_chat_history(
            ORGANIZATION_ID,
            DEPLOYMENT_CHAT_ID,
            THREAD_ID,
            HISTORY_ID,
        )
        self.assertDictEqual(ret, HISTORY_RES)

    @requests_mock.Mocker()
    def test_create_chat_history(self, m):
        # get-deployment-api mock
        path = '/opsbee-llm/organizations/{}/deployments/{}'.format(
            ORGANIZATION_ID,
            DEPLOYMENT_CHAT_ID,
        )
        m.get(path, json=DEPLOYMENT_CHAT_RES)

        # create-history-api mock
        path = '/opsbee-llm/organizations/{}/deployments/{}/threads/{}/histories'.format(
            ORGANIZATION_ID,
            DEPLOYMENT_CHAT_ID,
            THREAD_ID,
        )
        m.post(path, json=HISTORY_RES)

        # unit test
        client = APIClient()
        ret = client.create_chat_history(
            ORGANIZATION_ID,
            DEPLOYMENT_CHAT_ID,
            THREAD_ID,
            INPUT_TEXT,
            OUTPUT_TEXT,
            INPUT_TOKEN_COUNT,
            OUTPUT_TOKEN_COUNT,
        )
        expected_payload = {
            'input_text': INPUT_TEXT,
            'output_text': OUTPUT_TEXT,
            'input_token_count': INPUT_TOKEN_COUNT,
            'output_token_count': OUTPUT_TOKEN_COUNT,
            'tag_ids': [],
            'metadata': [],
        }

        self.assertDictEqual(m.request_history[1].json(), expected_payload)
        self.assertDictEqual(ret, HISTORY_RES)

        with self.assertRaises(BadRequest) as e:
            client.create_chat_history(
                ORGANIZATION_ID,
                DEPLOYMENT_CHAT_ID,
                THREAD_ID,
                input_text=None,
                output_text=None,
            )
        self.assertEqual(e.exception.error_description, '"input_text" is necessary')

        with self.assertRaises(BadRequest) as e:
            client.create_chat_history(
                ORGANIZATION_ID,
                DEPLOYMENT_CHAT_ID,
                THREAD_ID,
                input_text=INPUT_TEXT,
                output_text=None,
            )
        self.assertEqual(e.exception.error_description, '"output_text" is necessary')

        path = '/opsbee-llm/organizations/{}/deployments/{}'.format(
            ORGANIZATION_ID,
            DEPLOYMENT_QA_ID,
        )
        m.get(path, json=DEPLOYMENT_QA_RES)
        with self.assertRaises(BadRequest) as e:
            client.create_qa_history(
                ORGANIZATION_ID,
                DEPLOYMENT_CHAT_ID,
                input_text=INPUT_TEXT,
                output_text=OUTPUT_TEXT,
            )
        self.assertEqual(e.exception.error, 'deployment type is not supported')

    @requests_mock.Mocker()
    def test_update_chat_history(self, m):
        # get-deployment-api mock
        path = '/opsbee-llm/organizations/{}/deployments/{}'.format(
            ORGANIZATION_ID,
            DEPLOYMENT_CHAT_ID,
        )
        m.get(path, json=DEPLOYMENT_CHAT_RES)

        # get-history-api mock
        path = '/opsbee-llm/organizations/{}/deployments/{}/threads/{}/histories/{}'.format(
            ORGANIZATION_ID,
            DEPLOYMENT_CHAT_ID,
            THREAD_ID,
            HISTORY_ID,
        )
        m.get(path, json=HISTORY_RES)

        # update-history-api mock
        path = '/opsbee-llm/organizations/{}/deployments/{}/threads/{}/histories/{}'.format(
            ORGANIZATION_ID,
            DEPLOYMENT_CHAT_ID,
            THREAD_ID,
            HISTORY_ID,
        )
        m.patch(path, json=HISTORY_RES)

        # unit test
        client = APIClient()
        ret = client.update_chat_history(
            ORGANIZATION_ID,
            DEPLOYMENT_CHAT_ID,
            THREAD_ID,
            HISTORY_ID,
            INPUT_TEXT,
            OUTPUT_TEXT,
            INPUT_TOKEN_COUNT,
            OUTPUT_TOKEN_COUNT,
        )
        expected_payload = {
            'input_text': INPUT_TEXT,
            'output_text': OUTPUT_TEXT,
            'input_token_count': INPUT_TOKEN_COUNT,
            'output_token_count': OUTPUT_TOKEN_COUNT,
            'tag_ids': [TAG_ID],
        }

        self.assertDictEqual(m.request_history[2].json(), expected_payload)
        self.assertDictEqual(ret, HISTORY_RES)

        path = '/opsbee-llm/organizations/{}/deployments/{}'.format(
            ORGANIZATION_ID,
            DEPLOYMENT_QA_ID,
        )
        m.get(path, json=DEPLOYMENT_QA_RES)
        with self.assertRaises(BadRequest) as e:
            client.update_chat_history(
                ORGANIZATION_ID,
                DEPLOYMENT_QA_ID,
                THREAD_ID,
                HISTORY_ID,
                input_text=INPUT_TEXT,
                output_text=OUTPUT_TEXT,
            )
        self.assertEqual(e.exception.error, 'deployment type is not supported')

    @requests_mock.Mocker()
    def test_delete_chat_history(self, m):
        # get-deployment-api mock
        path = '/opsbee-llm/organizations/{}/deployments/{}'.format(
            ORGANIZATION_ID,
            DEPLOYMENT_CHAT_ID,
        )
        m.get(path, json=DEPLOYMENT_CHAT_RES)

        # delete-history-api mock
        path = '/opsbee-llm/organizations/{}/deployments/{}/threads/{}/histories/{}'.format(
            ORGANIZATION_ID,
            DEPLOYMENT_CHAT_ID,
            THREAD_ID,
            HISTORY_ID,
        )
        m.delete(path, json=HISTORY_RES)

        # unit test
        client = APIClient()
        ret = client.delete_chat_history(
            ORGANIZATION_ID,
            DEPLOYMENT_CHAT_ID,
            THREAD_ID,
            HISTORY_ID,
        )
        self.assertDictEqual(ret, HISTORY_RES)

    @requests_mock.Mocker()
    def test_get_tags(self, m):
        # get-tags-api mock
        path = '/opsbee-llm/organizations/{}/tags'.format(
            ORGANIZATION_ID,
        )
        m.get(path, json=TAGS_RES)

        # unit test
        client = APIClient()
        ret = client.get_tags(
            ORGANIZATION_ID,
        )
        self.assertDictEqual(ret, TAGS_RES)

    @requests_mock.Mocker()
    def test_get_tag(self, m):
        # get-tag-api mock
        path = '/opsbee-llm/organizations/{}/tags/{}'.format(
            ORGANIZATION_ID,
            TAG_ID,
        )
        m.get(path, json=TAG_RES)

        # unit test
        client = APIClient()
        ret = client.get_tag(
            ORGANIZATION_ID,
            TAG_ID,
        )
        self.assertDictEqual(ret, TAG_RES)

    @requests_mock.Mocker()
    def test_create_tag(self, m):
        # create-tag-api mock
        path = '/opsbee-llm/organizations/{}/tags'.format(
            ORGANIZATION_ID,
        )
        m.post(path, json=TAG_RES)

        # unit test
        client = APIClient()
        ret = client.create_tag(
            ORGANIZATION_ID,
            name=TAG_RES['name'],
            description=TAG_RES['description'],
            color=TAG_RES['color'],
        )
        expected_payload = {
            'name': TAG_RES['name'],
            'description': TAG_RES['description'],
            'color': TAG_RES['color'],
        }

        self.assertDictEqual(m.request_history[0].json(), expected_payload)
        self.assertDictEqual(ret, TAG_RES)

        with self.assertRaises(BadRequest) as e:
            client.create_tag(
                ORGANIZATION_ID,
                name=None,
                description=None,
                color=None,
            )
        self.assertEqual(e.exception.error_description, '"name" is necessary')

        with self.assertRaises(BadRequest) as e:
            client.create_tag(
                ORGANIZATION_ID,
                name=TAG_RES['name'],
                description=None,
                color="sky blue",
            )
        self.assertEqual(e.exception.error, 'color is not supported')

    @requests_mock.Mocker()
    def test_update_tag(self, m):
        # update-tag-api mock
        path = '/opsbee-llm/organizations/{}/tags/{}'.format(
            ORGANIZATION_ID,
            TAG_ID,
        )
        m.patch(path, json=TAG_RES)

        # unit test
        client = APIClient()
        ret = client.update_tag(
            ORGANIZATION_ID,
            TAG_ID,
            name=TAG_RES['name'],
            description=TAG_RES['description'],
            color=TAG_RES['color'],
        )
        expected_payload = {
            'name': TAG_RES['name'],
            'description': TAG_RES['description'],
            'color': TAG_RES['color'],
        }

        self.assertDictEqual(m.request_history[0].json(), expected_payload)
        self.assertDictEqual(ret, TAG_RES)

        with self.assertRaises(BadRequest) as e:
            client.update_tag(
                ORGANIZATION_ID,
                TAG_ID,
                name=None,
                description=None,
                color=None,
            )
        self.assertEqual(e.exception.error_description, '"name" is necessary')

        with self.assertRaises(BadRequest) as e:
            client.update_tag(
                ORGANIZATION_ID,
                TAG_ID,
                name=TAG_RES['name'],
                description=None,
                color="sky blue",
            )
        self.assertEqual(e.exception.error, 'color is not supported')

    @requests_mock.Mocker()
    def test_delete_tag(self, m):
        # delete-tag-api mock
        path = '/opsbee-llm/organizations/{}/tags/{}'.format(
            ORGANIZATION_ID,
            TAG_ID,
        )
        res = {
            'message': f'tag {TAG_ID} was deleted.'
        }
        m.delete(path, json=res)

        # unit test
        client = APIClient()
        ret = client.delete_tag(
            ORGANIZATION_ID,
            TAG_ID,
        )
        self.assertDictEqual(ret, res)

    @requests_mock.Mocker()
    def test_create_qa_history_metadata(self, m):
        # get-deployment-api mock
        path = '/opsbee-llm/organizations/{}/deployments/{}'.format(
            ORGANIZATION_ID,
            DEPLOYMENT_QA_ID,
        )
        m.get(path, json=DEPLOYMENT_QA_RES)

        # create-history-metadata-api mock
        path = '/opsbee-llm/organizations/{}/deployments/{}/qa_histories/{}/metadata'.format(
            ORGANIZATION_ID,
            DEPLOYMENT_QA_ID,
            HISTORY_ID,
        )
        m.post(path, json=METADATA_RES)

        # unit test
        client = APIClient()
        ret = client.create_qa_history_metadata(
            ORGANIZATION_ID,
            DEPLOYMENT_QA_ID,
            HISTORY_ID,
            key=METADATA_RES['key'],
            value=METADATA_RES['value'],
        )
        expected_payload = {
            'key': METADATA_RES['key'],
            'value': METADATA_RES['value'],
        }

        self.assertDictEqual(m.request_history[1].json(), expected_payload)
        self.assertDictEqual(ret, METADATA_RES)

        with self.assertRaises(BadRequest) as e:
            client.create_qa_history_metadata(
                ORGANIZATION_ID,
                DEPLOYMENT_QA_ID,
                HISTORY_ID,
                key=None,
                value=None,
            )
        self.assertEqual(e.exception.error_description, '"key" is necessary')

        with self.assertRaises(BadRequest) as e:
            client.create_qa_history_metadata(
                ORGANIZATION_ID,
                DEPLOYMENT_QA_ID,
                HISTORY_ID,
                key=METADATA_RES['key'],
                value=None,
            )
        self.assertEqual(e.exception.error_description, '"value" is necessary')

        path = '/opsbee-llm/organizations/{}/deployments/{}'.format(
            ORGANIZATION_ID,
            DEPLOYMENT_CHAT_ID,
        )
        m.get(path, json=DEPLOYMENT_CHAT_RES)
        with self.assertRaises(BadRequest) as e:
            client.create_qa_history_metadata(
                ORGANIZATION_ID,
                DEPLOYMENT_CHAT_ID,
                HISTORY_ID,
                key=METADATA_RES['key'],
                value=METADATA_RES['value'],
            )
        self.assertEqual(e.exception.error, 'deployment type is not supported')

    @requests_mock.Mocker()
    def test_update_qa_history_metadata(self, m):
        # get-deployment-api mock
        path = '/opsbee-llm/organizations/{}/deployments/{}'.format(
            ORGANIZATION_ID,
            DEPLOYMENT_QA_ID,
        )
        m.get(path, json=DEPLOYMENT_QA_RES)

        # update-history-metadata-api mock
        path = '/opsbee-llm/organizations/{}/deployments/{}/qa_histories/{}/metadata/{}'.format(
            ORGANIZATION_ID,
            DEPLOYMENT_QA_ID,
            HISTORY_ID,
            METADATA_ID,
        )
        m.patch(path, json=METADATA_RES)

        # unit test
        client = APIClient()
        ret = client.update_qa_history_metadata(
            ORGANIZATION_ID,
            DEPLOYMENT_QA_ID,
            HISTORY_ID,
            METADATA_ID,
            key=METADATA_RES['key'],
            value=METADATA_RES['value'],
        )
        expected_payload = {
            'key': METADATA_RES['key'],
            'value': METADATA_RES['value'],
        }

        self.assertDictEqual(m.request_history[1].json(), expected_payload)
        self.assertDictEqual(ret, METADATA_RES)

        with self.assertRaises(BadRequest) as e:
            client.update_qa_history_metadata(
                ORGANIZATION_ID,
                DEPLOYMENT_QA_ID,
                HISTORY_ID,
                METADATA_ID,
                key=None,
                value=None,
            )
        self.assertEqual(e.exception.error_description, '"key" is necessary')

        with self.assertRaises(BadRequest) as e:
            client.update_qa_history_metadata(
                ORGANIZATION_ID,
                DEPLOYMENT_QA_ID,
                HISTORY_ID,
                METADATA_ID,
                key=METADATA_RES['key'],
                value=None,
            )
        self.assertEqual(e.exception.error_description, '"value" is necessary')

        path = '/opsbee-llm/organizations/{}/deployments/{}'.format(
            ORGANIZATION_ID,
            DEPLOYMENT_CHAT_ID,
        )
        m.get(path, json=DEPLOYMENT_CHAT_RES)
        with self.assertRaises(BadRequest) as e:
            client.update_qa_history_metadata(
                ORGANIZATION_ID,
                DEPLOYMENT_CHAT_ID,
                HISTORY_ID,
                METADATA_ID,
                key=METADATA_RES['key'],
                value=METADATA_RES['value'],
            )
        self.assertEqual(e.exception.error, 'deployment type is not supported')

    @requests_mock.Mocker()
    def test_delete_qa_history_metadata(self, m):
        # get-deployment-api mock
        path = '/opsbee-llm/organizations/{}/deployments/{}'.format(
            ORGANIZATION_ID,
            DEPLOYMENT_QA_ID,
        )
        m.get(path, json=DEPLOYMENT_QA_RES)

        # delete-history-metadata-api mock
        path = '/opsbee-llm/organizations/{}/deployments/{}/qa_histories/{}/metadata/{}'.format(
            ORGANIZATION_ID,
            DEPLOYMENT_QA_ID,
            HISTORY_ID,
            METADATA_ID,
        )
        res = {
            'message': f'metadata {METADATA_ID} was deleted.'
        }
        m.delete(path, json=res)

        # unit test
        client = APIClient()
        ret = client.delete_qa_history_metadata(
            ORGANIZATION_ID,
            DEPLOYMENT_QA_ID,
            HISTORY_ID,
            METADATA_ID,
        )
        self.assertDictEqual(ret, res)

        path = '/opsbee-llm/organizations/{}/deployments/{}'.format(
            ORGANIZATION_ID,
            DEPLOYMENT_CHAT_ID,
        )
        m.get(path, json=DEPLOYMENT_CHAT_RES)
        with self.assertRaises(BadRequest) as e:
            client.delete_qa_history_metadata(
                ORGANIZATION_ID,
                DEPLOYMENT_CHAT_ID,
                HISTORY_ID,
                METADATA_ID,
            )
        self.assertEqual(e.exception.error, 'deployment type is not supported')

    @requests_mock.Mocker()
    def test_create_chat_history_metadata(self, m):
        # get-deployment-api mock
        path = '/opsbee-llm/organizations/{}/deployments/{}'.format(
            ORGANIZATION_ID,
            DEPLOYMENT_CHAT_ID,
        )
        m.get(path, json=DEPLOYMENT_CHAT_RES)

        # create-history-metadata-api mock
        path = '/opsbee-llm/organizations/{}/deployments/{}/threads/{}/histories/{}/metadata'.format(
            ORGANIZATION_ID,
            DEPLOYMENT_CHAT_ID,
            THREAD_ID,
            HISTORY_ID,
        )
        m.post(path, json=METADATA_RES)

        # unit test
        client = APIClient()
        ret = client.create_chat_history_metadata(
            ORGANIZATION_ID,
            DEPLOYMENT_CHAT_ID,
            THREAD_ID,
            HISTORY_ID,
            key=METADATA_RES['key'],
            value=METADATA_RES['value'],
        )
        expected_payload = {
            'key': METADATA_RES['key'],
            'value': METADATA_RES['value'],
        }

        self.assertDictEqual(m.request_history[1].json(), expected_payload)
        self.assertDictEqual(ret, METADATA_RES)

        with self.assertRaises(BadRequest) as e:
            client.create_chat_history_metadata(
                ORGANIZATION_ID,
                DEPLOYMENT_CHAT_ID,
                THREAD_ID,
                HISTORY_ID,
                key=None,
                value=None,
            )
        self.assertEqual(e.exception.error_description, '"key" is necessary')

        with self.assertRaises(BadRequest) as e:
            client.create_chat_history_metadata(
                ORGANIZATION_ID,
                DEPLOYMENT_CHAT_ID,
                THREAD_ID,
                HISTORY_ID,
                key=METADATA_RES['key'],
                value=None,
            )
        self.assertEqual(e.exception.error_description, '"value" is necessary')

        path = '/opsbee-llm/organizations/{}/deployments/{}'.format(
            ORGANIZATION_ID,
            DEPLOYMENT_QA_ID,
        )
        m.get(path, json=DEPLOYMENT_QA_RES)
        with self.assertRaises(BadRequest) as e:
            client.create_chat_history_metadata(
                ORGANIZATION_ID,
                DEPLOYMENT_QA_ID,
                THREAD_ID,
                HISTORY_ID,
                key=METADATA_RES['key'],
                value=METADATA_RES['value'],
            )
        self.assertEqual(e.exception.error, 'deployment type is not supported')

    @requests_mock.Mocker()
    def test_update_chat_history_metadata(self, m):
        # get-deployment-api mock
        path = '/opsbee-llm/organizations/{}/deployments/{}'.format(
            ORGANIZATION_ID,
            DEPLOYMENT_CHAT_ID,
        )
        m.get(path, json=DEPLOYMENT_CHAT_RES)

        # update-history-metadata-api mock
        path = '/opsbee-llm/organizations/{}/deployments/{}/threads/{}/histories/{}/metadata/{}'.format(
            ORGANIZATION_ID,
            DEPLOYMENT_CHAT_ID,
            THREAD_ID,
            HISTORY_ID,
            METADATA_ID,
        )
        m.patch(path, json=METADATA_RES)

        # unit test
        client = APIClient()
        ret = client.update_chat_history_metadata(
            ORGANIZATION_ID,
            DEPLOYMENT_CHAT_ID,
            THREAD_ID,
            HISTORY_ID,
            METADATA_ID,
            key=METADATA_RES['key'],
            value=METADATA_RES['value'],
        )
        expected_payload = {
            'key': METADATA_RES['key'],
            'value': METADATA_RES['value'],
        }

        self.assertDictEqual(m.request_history[1].json(), expected_payload)
        self.assertDictEqual(ret, METADATA_RES)

        with self.assertRaises(BadRequest) as e:
            client.update_chat_history_metadata(
                ORGANIZATION_ID,
                DEPLOYMENT_CHAT_ID,
                THREAD_ID,
                HISTORY_ID,
                METADATA_ID,
                key=None,
                value=None,
            )
        self.assertEqual(e.exception.error_description, '"key" is necessary')

        with self.assertRaises(BadRequest) as e:
            client.update_chat_history_metadata(
                ORGANIZATION_ID,
                DEPLOYMENT_CHAT_ID,
                THREAD_ID,
                HISTORY_ID,
                METADATA_ID,
                key=METADATA_RES['key'],
                value=None,
            )
        self.assertEqual(e.exception.error_description, '"value" is necessary')

        path = '/opsbee-llm/organizations/{}/deployments/{}'.format(
            ORGANIZATION_ID,
            DEPLOYMENT_QA_ID,
        )
        m.get(path, json=DEPLOYMENT_QA_RES)
        with self.assertRaises(BadRequest) as e:
            client.update_chat_history_metadata(
                ORGANIZATION_ID,
                DEPLOYMENT_QA_ID,
                THREAD_ID,
                HISTORY_ID,
                METADATA_ID,
                key=METADATA_RES['key'],
                value=METADATA_RES['value'],
            )
        self.assertEqual(e.exception.error, 'deployment type is not supported')

    @requests_mock.Mocker()
    def test_delete_chat_history_metadata(self, m):
        # get-deployment-api mock
        path = '/opsbee-llm/organizations/{}/deployments/{}'.format(
            ORGANIZATION_ID,
            DEPLOYMENT_CHAT_ID,
        )
        m.get(path, json=DEPLOYMENT_CHAT_RES)

        # delete-history-metadata-api mock
        path = '/opsbee-llm/organizations/{}/deployments/{}/threads/{}/histories/{}/metadata/{}'.format(
            ORGANIZATION_ID,
            DEPLOYMENT_CHAT_ID,
            THREAD_ID,
            HISTORY_ID,
            METADATA_ID,
        )
        res = {
            'message': f'metadata {METADATA_ID} was deleted.'
        }
        m.delete(path, json=res)

        # unit test
        client = APIClient()
        ret = client.delete_chat_history_metadata(
            ORGANIZATION_ID,
            DEPLOYMENT_CHAT_ID,
            THREAD_ID,
            HISTORY_ID,
            METADATA_ID,
        )
        self.assertDictEqual(ret, res)

        path = '/opsbee-llm/organizations/{}/deployments/{}'.format(
            ORGANIZATION_ID,
            DEPLOYMENT_QA_ID,
        )
        m.get(path, json=DEPLOYMENT_QA_RES)
        with self.assertRaises(BadRequest) as e:
            client.delete_chat_history_metadata(
                ORGANIZATION_ID,
                DEPLOYMENT_QA_ID,
                THREAD_ID,
                HISTORY_ID,
                METADATA_ID,
            )
        self.assertEqual(e.exception.error, 'deployment type is not supported')
