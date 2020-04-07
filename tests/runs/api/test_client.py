import unittest
from unittest.mock import patch
import json
from datetime import datetime

import requests_mock
from parameterized import parameterized

from abeja.runs import APIClient


ORGANIZATION_ID = '1111111111111'
DEPLOYMENT_ID = '3333333333333'

MODEL_ID = '2222222222222'
MODEL_VERSION = '0.0.3'
VERSION_ID = 'ver-1111111111111111'
TRAINING_MODEL_ID = '4444444444444'

CHANNEL_ID = '4444444444444'
FILE_ID = '20180101T112233-44444444-5555-6666-7777-888888888888'
INPUT_DATA = {
    "$datalake:1": "{}/{}".format(CHANNEL_ID, FILE_ID)
}

RETRY_COUNT = 7
DISTRIBUTION = 0
ENVIRONMENT = {
    'ENV': 'testing'
}

RUN_ID = 'run-5555555555555555'

RUN_RES = {
    'created_at': '2018-01-01T00:00:00.000000Z',
    'deployment_id': DEPLOYMENT_ID,
    'input_data': json.dumps(INPUT_DATA),
    'models': {
        'alias': TRAINING_MODEL_ID
    },
    'model_version': MODEL_VERSION,
    'model_version_id': VERSION_ID,
    'modified_at': '2018-01-01T00:00:00.000000Z',
    'output_template': None,
    'retry_count': RETRY_COUNT,
    'distribution': DISTRIBUTION,
    'run_id': RUN_ID,
    'status': 'SUBMITTED',
    'user_env_vars': ENVIRONMENT
}
RUN_LIST_RES = {
    'entries': [
        RUN_RES
    ]
}
RUN_LOG_RES = {
    "events": [
        {
            "message": "...",
            "timestamp": "2018-01-01T00:00:00.000000Z"
        }
    ],
    "next_token": "..."
}
RUN_RECENT_LOG_RES = {
    "events": [
        {
            "message": "...",
            "timestamp": "2018-01-01T00:00:00.000000Z"
        }
    ],
    "next_backward_token": "...",
    "next_forward_token": "..."
}


class APIClientTest(unittest.TestCase):
    @requests_mock.Mocker()
    def test_create_run(self, m):
        path = '/organizations/{}/deployments/{}/runs'.format(ORGANIZATION_ID, DEPLOYMENT_ID)
        m.post(path, json=RUN_RES)

        client = APIClient()
        res = client.create_run(
            organization_id=ORGANIZATION_ID,
            deployment_id=DEPLOYMENT_ID,
            version_id=VERSION_ID,
            model_id=TRAINING_MODEL_ID,
            input_data=INPUT_DATA,
            distribution=DISTRIBUTION,
            retry_count=RETRY_COUNT,
            environment=ENVIRONMENT
        )
        expected_payload = {
            'environment': ENVIRONMENT,
            'input_data': INPUT_DATA,
            'retry_count': RETRY_COUNT,
            'distribution': DISTRIBUTION,
            'version_id': VERSION_ID,
            'models': {
                'alias': TRAINING_MODEL_ID
            }
        }
        self.assertDictEqual(m.request_history[0].json(), expected_payload)
        self.assertDictEqual(res, RUN_RES)

    @requests_mock.Mocker()
    def test_create_run_without_inputdata(self, m):
        path = '/organizations/{}/deployments/{}/runs'.format(ORGANIZATION_ID, DEPLOYMENT_ID)
        m.post(path, json=RUN_RES)

        client = APIClient()
        client.create_run(
            organization_id=ORGANIZATION_ID,
            deployment_id=DEPLOYMENT_ID,
            version_id=VERSION_ID,
            model_id=TRAINING_MODEL_ID,
            distribution=DISTRIBUTION,
            retry_count=RETRY_COUNT,
            environment=ENVIRONMENT
        )
        expected_payload = {
            'environment': ENVIRONMENT,
            'retry_count': RETRY_COUNT,
            'distribution': DISTRIBUTION,
            'version_id': VERSION_ID,
            'models': {
                'alias': TRAINING_MODEL_ID
            }
        }
        self.assertDictEqual(m.request_history[0].json(), expected_payload)

    @requests_mock.Mocker()
    def test_create_run_no_retry_count(self, m):
        path = '/organizations/{}/deployments/{}/runs'.format(ORGANIZATION_ID, DEPLOYMENT_ID)
        m.post(path, json=RUN_RES)

        client = APIClient()
        res = client.create_run(
            organization_id=ORGANIZATION_ID,
            deployment_id=DEPLOYMENT_ID,
            version_id=VERSION_ID,
            model_id=TRAINING_MODEL_ID,
            input_data=INPUT_DATA,
            distribution=DISTRIBUTION,
            environment=ENVIRONMENT
        )
        expected_payload = {
            'environment': ENVIRONMENT,
            'input_data': INPUT_DATA,
            'distribution': DISTRIBUTION,
            'version_id': VERSION_ID,
            'models': {
                'alias': TRAINING_MODEL_ID
            }
        }
        self.assertDictEqual(m.request_history[0].json(), expected_payload)
        self.assertDictEqual(res, RUN_RES)

    @requests_mock.Mocker()
    def test_create_run_no_distribution(self, m):
        path = '/organizations/{}/deployments/{}/runs'.format(ORGANIZATION_ID, DEPLOYMENT_ID)
        m.post(path, json=RUN_RES)

        client = APIClient()
        res = client.create_run(
            organization_id=ORGANIZATION_ID,
            deployment_id=DEPLOYMENT_ID,
            version_id=VERSION_ID,
            model_id=TRAINING_MODEL_ID,
            input_data=INPUT_DATA,
            retry_count=RETRY_COUNT,
            environment=ENVIRONMENT
        )
        expected_payload = {
            'environment': ENVIRONMENT,
            'input_data': INPUT_DATA,
            'retry_count': RETRY_COUNT,
            'version_id': VERSION_ID,
            'models': {
                'alias': TRAINING_MODEL_ID
            }
        }
        self.assertDictEqual(m.request_history[0].json(), expected_payload)
        self.assertDictEqual(res, RUN_RES)

    @requests_mock.Mocker()
    def test_get_run(self, m):
        path = '/organizations/{}/deployments/{}/runs/{}'.format(
            ORGANIZATION_ID, DEPLOYMENT_ID, RUN_ID)
        m.get(path, json=RUN_RES)

        client = APIClient()
        res = client.get_run(
            organization_id=ORGANIZATION_ID,
            deployment_id=DEPLOYMENT_ID,
            run_id=RUN_ID
        )
        self.assertDictEqual(res, RUN_RES)

    @requests_mock.Mocker()
    def test_get_runs(self, m):
        path = '/organizations/{}/deployments/{}/runs'.format(
            ORGANIZATION_ID, DEPLOYMENT_ID)
        m.get(path, json=RUN_LIST_RES)

        client = APIClient()
        res = client.get_runs(
            organization_id=ORGANIZATION_ID,
            deployment_id=DEPLOYMENT_ID
        )
        self.assertDictEqual(res, RUN_LIST_RES)

    @requests_mock.Mocker()
    def test_get_run_logs(self, m):
        path = '/organizations/{}/deployments/{}/runs/{}/logs'.format(
            ORGANIZATION_ID, DEPLOYMENT_ID, RUN_ID)
        m.get(path, json=RUN_LOG_RES)

        client = APIClient()
        res = client.get_run_logs(
            organization_id=ORGANIZATION_ID,
            deployment_id=DEPLOYMENT_ID,
            run_id=RUN_ID
        )
        self.assertDictEqual(res, RUN_LOG_RES)

    @parameterized.expand([
        ({"start_time": datetime(2017, 1, 1)}, {"start_time": "2017-01-01T00:00:00"}),
        ({"end_time": datetime(2017, 1, 1)}, {"end_time": "2017-01-01T00:00:00"}),
        ({"next_token": "..."}, {"next_token": "..."})
    ])
    @patch('requests.Session.request')
    def test_get_run_logs_with_options(self, option, expected_params, m):
        client = APIClient()
        params = {
            "organization_id": ORGANIZATION_ID,
            "deployment_id": DEPLOYMENT_ID,
            "run_id": RUN_ID
        }
        params.update(option)
        client.get_run_logs(**params)

        expected_path = '{}/organizations/{}/deployments/{}/runs/{}/logs'.format(
            client._connection.BASE_URL, ORGANIZATION_ID, DEPLOYMENT_ID, RUN_ID)
        self.assertEqual(m.call_args[0][1], expected_path)
        self.assertEqual(m.call_args[1]['params'], expected_params)

    @requests_mock.Mocker()
    def test_get_run_recent_logs(self, m):
        path = '/organizations/{}/deployments/{}/runs/{}/recentlogs'.format(
            ORGANIZATION_ID, DEPLOYMENT_ID, RUN_ID)
        m.get(path, json=RUN_RECENT_LOG_RES)

        client = APIClient()
        res = client.get_run_recent_logs(
            organization_id=ORGANIZATION_ID,
            deployment_id=DEPLOYMENT_ID,
            run_id=RUN_ID
        )
        self.assertDictEqual(res, RUN_RECENT_LOG_RES)

    @parameterized.expand([
        ({"start_time": datetime(2017, 1, 1)}, {"start_time": "2017-01-01T00:00:00"}),
        ({"end_time": datetime(2017, 1, 1)}, {"end_time": "2017-01-01T00:00:00"}),
        ({"next_forward_token": "..."}, {"next_forward_token": "..."}),
        ({"next_backward_token": "..."}, {"next_backward_token": "..."})
    ])
    @patch('requests.Session.request')
    def test_get_run_recent_logs_with_options(self, option, expected_params, m):
        client = APIClient()
        params = {
            "organization_id": ORGANIZATION_ID,
            "deployment_id": DEPLOYMENT_ID,
            "run_id": RUN_ID
        }
        params.update(option)
        client.get_run_recent_logs(**params)

        expected_path = '{}/organizations/{}/deployments/{}/runs/{}/recentlogs'.format(
            client._connection.BASE_URL, ORGANIZATION_ID, DEPLOYMENT_ID, RUN_ID)
        self.assertEqual(m.call_args[0][1], expected_path)
        self.assertEqual(m.call_args[1]['params'], expected_params)
