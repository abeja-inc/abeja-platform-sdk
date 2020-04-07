import unittest

import requests_mock

from abeja.triggers import APIClient


ORGANIZATION_ID = '1111111111111'
DEPLOYMENT_ID = '3333333333333'

MODEL_ID = '2222222222222'
MODEL_VERSION = '0.0.3'
VERSION_ID = 'ver-1111111111111111'
TRAINING_MODEL_ID = '4444444444444'

INPUT_SERVICE_NAME = 'datalake'
CHANNEL_ID = '4444444444444'
FILE_ID = '20180101T112233-44444444-5555-6666-7777-888888888888'

RETRY_COUNT = 7
DISTRIBUTION = 0
ENVIRONMENT = {
    'ENV': 'testing'
}

TRIGGER_ID = 'tri-5555555555555555'
RUN_ID = 'run-6666666666666666'

TRIGGER_RES = {
    'created_at': '2018-01-01T00:00:00.000000Z',
    'deployment_id': DEPLOYMENT_ID,
    'input_service_id': CHANNEL_ID,
    "input_service_name": INPUT_SERVICE_NAME,
    'models': {
        'alias': TRAINING_MODEL_ID
    },
    'model_version': MODEL_VERSION,
    'model_version_id': VERSION_ID,
    'modified_at': '2018-01-01T00:00:00.000000Z',
    'retry_count': RETRY_COUNT,
    'distribution': DISTRIBUTION,
    'trigger_id': TRIGGER_ID,
    'user_env_vars': ENVIRONMENT
}
TRIGGER_LIST_RES = {
    'entries': [
        TRIGGER_RES
    ]
}
TRIGGER_RUN_RES = {
    "created_at": "2019-01-01T00:00:00.000000Z",
    "deployment_id": DEPLOYMENT_ID,
    "input_data": {
        "$datalake:1": "{}/{}".format(CHANNEL_ID, FILE_ID)
    },
    'models': {
        'alias': TRAINING_MODEL_ID
    },
    "model_version_id": VERSION_ID,
    "modified_at": "2019-01-01T00:00:00.000000Z",
    "output_template": None,
    "retry_count": RETRY_COUNT,
    "distribution": DISTRIBUTION,
    "run_id": RUN_ID,
    "status": "SUCCEEDED",
    "trigger_id": TRIGGER_ID,
    "user_env_vars": {}
}
TRIGGER_RUN_LIST_RES = {
    'entries': [
        TRIGGER_RUN_RES
    ]
}


class APIClientTest(unittest.TestCase):
    @requests_mock.Mocker()
    def test_create_trigger(self, m):
        path = '/organizations/{}/deployments/{}/triggers'.format(ORGANIZATION_ID, DEPLOYMENT_ID)
        m.post(path, json=TRIGGER_RES)

        client = APIClient()
        res = client.create_trigger(
            organization_id=ORGANIZATION_ID,
            deployment_id=DEPLOYMENT_ID,
            version_id=VERSION_ID,
            input_service_name=INPUT_SERVICE_NAME,
            input_service_id=CHANNEL_ID,
            model_id=TRAINING_MODEL_ID,
            distribution=DISTRIBUTION,
            retry_count=RETRY_COUNT,
            environment=ENVIRONMENT
        )
        expected_payload = {
            'environment': ENVIRONMENT,
            'input_service_name': INPUT_SERVICE_NAME,
            'input_service_id': CHANNEL_ID,
            'retry_count': RETRY_COUNT,
            'distribution': DISTRIBUTION,
            'version_id': VERSION_ID,
            'models': {
                'alias': TRAINING_MODEL_ID
            }
        }
        self.assertDictEqual(m.request_history[0].json(), expected_payload)
        self.assertDictEqual(res, TRIGGER_RES)

    @requests_mock.Mocker()
    def test_create_trigger_no_retry_count(self, m):
        path = '/organizations/{}/deployments/{}/triggers'.format(ORGANIZATION_ID, DEPLOYMENT_ID)
        m.post(path, json=TRIGGER_RES)

        client = APIClient()
        res = client.create_trigger(
            organization_id=ORGANIZATION_ID,
            deployment_id=DEPLOYMENT_ID,
            version_id=VERSION_ID,
            input_service_name=INPUT_SERVICE_NAME,
            input_service_id=CHANNEL_ID,
            model_id=TRAINING_MODEL_ID,
            distribution=DISTRIBUTION,
            environment=ENVIRONMENT
        )
        expected_payload = {
            'environment': ENVIRONMENT,
            'input_service_name': INPUT_SERVICE_NAME,
            'input_service_id': CHANNEL_ID,
            'distribution': DISTRIBUTION,
            'version_id': VERSION_ID,
            'models': {
                'alias': TRAINING_MODEL_ID
            }
        }
        self.assertDictEqual(m.request_history[0].json(), expected_payload)
        self.assertDictEqual(res, TRIGGER_RES)

    @requests_mock.Mocker()
    def test_create_trigger_no_distribution(self, m):
        path = '/organizations/{}/deployments/{}/triggers'.format(ORGANIZATION_ID, DEPLOYMENT_ID)
        m.post(path, json=TRIGGER_RES)

        client = APIClient()
        res = client.create_trigger(
            organization_id=ORGANIZATION_ID,
            deployment_id=DEPLOYMENT_ID,
            version_id=VERSION_ID,
            input_service_name=INPUT_SERVICE_NAME,
            input_service_id=CHANNEL_ID,
            model_id=TRAINING_MODEL_ID,
            retry_count=RETRY_COUNT,
            environment=ENVIRONMENT
        )
        expected_payload = {
            'environment': ENVIRONMENT,
            'input_service_name': INPUT_SERVICE_NAME,
            'input_service_id': CHANNEL_ID,
            'retry_count': RETRY_COUNT,
            'version_id': VERSION_ID,
            'models': {
                'alias': TRAINING_MODEL_ID
            }
        }
        self.assertDictEqual(m.request_history[0].json(), expected_payload)
        self.assertDictEqual(res, TRIGGER_RES)

    @requests_mock.Mocker()
    def test_get_trigger(self, m):
        path = '/organizations/{}/deployments/{}/triggers/{}'.format(
            ORGANIZATION_ID, DEPLOYMENT_ID, TRIGGER_ID)
        m.get(path, json=TRIGGER_RES)

        client = APIClient()
        res = client.get_trigger(
            organization_id=ORGANIZATION_ID,
            deployment_id=DEPLOYMENT_ID,
            trigger_id=TRIGGER_ID
        )
        self.assertDictEqual(res, TRIGGER_RES)

    @requests_mock.Mocker()
    def test_get_triggers(self, m):
        path = '/organizations/{}/deployments/{}/triggers'.format(
            ORGANIZATION_ID, DEPLOYMENT_ID)
        m.get(path, json=TRIGGER_LIST_RES)

        client = APIClient()
        res = client.get_triggers(
            organization_id=ORGANIZATION_ID,
            deployment_id=DEPLOYMENT_ID
        )
        self.assertDictEqual(res, TRIGGER_LIST_RES)

    @requests_mock.Mocker()
    def test_delete_trigger(self, m):
        path = '/organizations/{}/deployments/{}/triggers/{}'.format(
            ORGANIZATION_ID, DEPLOYMENT_ID, TRIGGER_ID)
        m.delete(path, json={
            "message": "tri-3333333333333333 deleted"
        })

        client = APIClient()
        res = client.delete_trigger(
            organization_id=ORGANIZATION_ID,
            deployment_id=DEPLOYMENT_ID,
            trigger_id=TRIGGER_ID
        )
        self.assertDictEqual(res, {
            "message": "tri-3333333333333333 deleted"
        })

    @requests_mock.Mocker()
    def test_get_trigger_runs(self, m):
        path = '/organizations/{}/deployments/{}/triggers/{}/runs'.format(
            ORGANIZATION_ID, DEPLOYMENT_ID, TRIGGER_ID)
        m.get(path, json=TRIGGER_RUN_LIST_RES)

        client = APIClient()
        res = client.get_trigger_runs(
            organization_id=ORGANIZATION_ID,
            deployment_id=DEPLOYMENT_ID,
            trigger_id=TRIGGER_ID
        )
        self.assertDictEqual(res, TRIGGER_RUN_LIST_RES)
