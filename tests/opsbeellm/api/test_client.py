import unittest

import requests_mock

from abeja.opsbeellm import APIClient
from abeja.exceptions import BadRequest

ACCOUNT_ID = '1111111111111'
ORGANIZATION_ID = '2222222222222'
DEPLOYMENT_ID = '3333333333333'
THREAD_ID = '4444444444444'
HISTORY_ID = '5555555555555'
INPUT_TEXT = 'ABEJAについて教えて'
OUTPUT_TEXT = 'ABEJAは、スペイン語で「ミツバチ」の意味であり、植物の受粉を手伝い、世界の食料生産を支える存在として社名になっています。'
INPUT_TOKEN_COUNT = 10
OUTPUT_TOKEN_COUNT = 10

DEPLOYMENT_QA_RES = {
    'id': DEPLOYMENT_ID,
    'account_id': ACCOUNT_ID,
    'organization_id': ORGANIZATION_ID,
    'name': 'deployment name',
    'description': 'deployment description',
    'type': 'qa',
    'history_count': 0,
    'created_at': "2023-12-14T04:42:34.913644Z",
    'updated_at': "2023-12-14T04:42:34.913644Z",
}
DEPLOYMENT_CHAT_RES = {
    'id': DEPLOYMENT_ID,
    'account_id': ACCOUNT_ID,
    'organization_id': ORGANIZATION_ID,
    'name': 'deployment name',
    'description': 'deployment description',
    'type': 'chat',
    'history_count': 0,
    'created_at': "2023-12-14T04:42:34.913644Z",
    'updated_at': "2023-12-14T04:42:34.913644Z",
}
THREADS_RES = {
    'account_id': ACCOUNT_ID,
    'organization_id': ORGANIZATION_ID,
    'deployment_id': DEPLOYMENT_ID,
    'threads': [
        {
            'id': THREAD_ID,
            'account_id': ACCOUNT_ID,
            'organization_id': ORGANIZATION_ID,
            'deployment_id': DEPLOYMENT_ID,
            'name': "thread name",
            'description': "thread description",
            'created_at': "2023-12-14T04:42:34.913644Z",
            'updated_at': "2023-12-14T04:42:34.913644Z",
        }
    ],
    'offset': 0,
    'limit': 1000,
    'has_next': False,
}
HISOTRY_RES = {
    "id": HISTORY_ID,
    "account_id": ACCOUNT_ID,
    "organization_id": ORGANIZATION_ID,
    "deployment_id": DEPLOYMENT_ID,
    "thread_id": THREAD_ID,
    "input_text": INPUT_TEXT,
    "output_text": OUTPUT_TEXT,
    "input_token_count": INPUT_TOKEN_COUNT,
    "output_token_count": OUTPUT_TOKEN_COUNT,
    "tags": [],
    "matadata": [],
    "created_at": "2023-12-14T04:42:34.913644Z",
    "updated_at": "2018-12-15T04:42:34.913726Z"
}


class TestOpsBeeLLMAPIClient(unittest.TestCase):

    @requests_mock.Mocker()
    def test_create_history(self, m):
        # get-deployment-api mock
        path = '/accounts/{}/organizations/{}/deployments/{}'.format(
            ACCOUNT_ID,
            ORGANIZATION_ID,
            DEPLOYMENT_ID,
        )
        m.get(path, json=DEPLOYMENT_QA_RES)

        # get-threads-api mock
        path = '/accounts/{}/organizations/{}/deployments/{}/threads'.format(
            ACCOUNT_ID,
            ORGANIZATION_ID,
            DEPLOYMENT_ID,
        )
        m.get(path, json=THREADS_RES)

        # create-history-api mock
        path = '/accounts/{}/organizations/{}/deployments/{}/threads/{}/history'.format(
            ACCOUNT_ID,
            ORGANIZATION_ID,
            DEPLOYMENT_ID,
            THREAD_ID,
        )
        m.post(path, json=HISOTRY_RES)

        # unit test
        client = APIClient()
        ret = client.create_history(
            ACCOUNT_ID,
            ORGANIZATION_ID,
            DEPLOYMENT_ID,
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

        self.assertDictEqual(m.request_history[2].json(), expected_payload)
        self.assertDictEqual(ret, HISOTRY_RES)

        with self.assertRaises(BadRequest) as e:
            client.create_history(
                ACCOUNT_ID,
                ORGANIZATION_ID,
                DEPLOYMENT_ID,
                input_text=None,
                output_text=None,
            )
        self.assertEqual(e.exception.error_description, '"input_text" is necessary')

        with self.assertRaises(BadRequest) as e:
            client.create_history(
                ACCOUNT_ID,
                ORGANIZATION_ID,
                DEPLOYMENT_ID,
                input_text=INPUT_TEXT,
                output_text=None,
            )
        self.assertEqual(e.exception.error_description, '"output_text" is necessary')

    @requests_mock.Mocker()
    def test_create_chat_history(self, m):
        # get-deployment-api mock
        path = '/accounts/{}/organizations/{}/deployments/{}'.format(
            ACCOUNT_ID,
            ORGANIZATION_ID,
            DEPLOYMENT_ID,
        )
        m.get(path, json=DEPLOYMENT_CHAT_RES)

        # create-history-api mock
        path = '/accounts/{}/organizations/{}/deployments/{}/threads/{}/history'.format(
            ACCOUNT_ID,
            ORGANIZATION_ID,
            DEPLOYMENT_ID,
            THREAD_ID,
        )
        m.post(path, json=HISOTRY_RES)

        # unit test
        client = APIClient()
        ret = client.create_chat_history(
            ACCOUNT_ID,
            ORGANIZATION_ID,
            DEPLOYMENT_ID,
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
        self.assertDictEqual(ret, HISOTRY_RES)

        with self.assertRaises(BadRequest) as e:
            client.create_chat_history(
                ACCOUNT_ID,
                ORGANIZATION_ID,
                DEPLOYMENT_ID,
                THREAD_ID,
                input_text=None,
                output_text=None,
            )
        self.assertEqual(e.exception.error_description, '"input_text" is necessary')

        with self.assertRaises(BadRequest) as e:
            client.create_chat_history(
                ACCOUNT_ID,
                ORGANIZATION_ID,
                DEPLOYMENT_ID,
                THREAD_ID,
                input_text=INPUT_TEXT,
                output_text=None,
            )
        self.assertEqual(e.exception.error_description, '"output_text" is necessary')
