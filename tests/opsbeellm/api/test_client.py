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
        path = '/accounts/{}/organizations/{}/deployments/{}/threads/{}/history'.format(
            ACCOUNT_ID,
            ORGANIZATION_ID,
            DEPLOYMENT_ID,
            THREAD_ID,
        )
        m.post(path, json=HISOTRY_RES)

        client = APIClient()
        ret = client.create_history(
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

        self.assertDictEqual(m.request_history[0].json(), expected_payload)
        self.assertDictEqual(ret, HISOTRY_RES)

        with self.assertRaises(BadRequest) as e:
            client.create_history(
                ACCOUNT_ID,
                ORGANIZATION_ID,
                DEPLOYMENT_ID,
                THREAD_ID,
                input_text=None,
                output_text=None,
            )
        self.assertEqual(e.exception.error_description, '"input_text" is necessary')

        with self.assertRaises(BadRequest) as e:
            client.create_history(
                ACCOUNT_ID,
                ORGANIZATION_ID,
                DEPLOYMENT_ID,
                THREAD_ID,
                input_text=INPUT_TEXT,
                output_text=None,
            )
        self.assertEqual(e.exception.error_description, '"output_text" is necessary')
