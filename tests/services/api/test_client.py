import json
import unittest

import requests_mock

from abeja.common.connection import Connection
from abeja.services import APIClient


ABEJA_API_NETLOC = 'localhost:8080'
ABEJA_API_URL = 'http://{}'.format(ABEJA_API_NETLOC)

ORGANIZATION_ID = '1111111111111'
SERVICE_ID = '2222222222222'
DEPLOYMENT_ID = '3333333333333'
TRAINING_MODEL_ID = '4444444444444'
VERSION_ID = 'ver-abc1111111111111'
ENV_VARS = {
    'EXAMPLE_ENV': 'abc'
}
SERVICE_INSTANCE_TYPE = 'cpu-2'
SERVICE_INSTANCE_NUMBER = 3
SERVICE_RES = {
    'service_id': SERVICE_ID,
    'deployment_id': DEPLOYMENT_ID,
    'model_version': '0.0.1',
    'model_version_id': VERSION_ID,
    'models': {
        'alias': TRAINING_MODEL_ID
    },
    'status': 'READY',
    'instance_number': 1,
    'min_instance_number': 1,
    'max_instance_number': 2,
    "enable_autoscale": True,
    'instance_type': 'cpu-0.25',
    'metrics_url': 'https://p.datadoghq.com/sb/aaaaaaaaa-bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb',
    'user_env_vars': ENV_VARS,
    'created_at': '2018-06-05T12:34:33.485329Z',
    'modified_at': '2018-06-05T12:34:34.568985Z'
}
SERVICE_PAYLOAD = {
    "instance_number": 4,
    "min_instance_number": 2,
    "max_instance_number": 6,
    "enable_autoscale": True
}
SERVICE_LIST_RES = [
    SERVICE_RES
]
SERVICE_RECENT_LOG_RES = {
    "events": [
        {
            "message": "...",
            "timestamp": "2018-01-01T00:00:00.000000Z"
        }
    ],
    "next_backward_token": "...",
    "next_forward_token": "..."
}


class TestAPIClient(unittest.TestCase):

    @requests_mock.Mocker()
    def test_create_service(self, m):
        path = '/organizations/{}/deployments/{}/services'.format(
            ORGANIZATION_ID, DEPLOYMENT_ID)
        m.post(path, json=SERVICE_RES)

        client = APIClient()
        ret = client.create_service(
            ORGANIZATION_ID,
            DEPLOYMENT_ID,
            VERSION_ID,
            instance_number=SERVICE_INSTANCE_NUMBER,
            min_instance_number=1,
            max_instance_number=SERVICE_INSTANCE_NUMBER * 2,
            enable_autoscale=True,
            instance_type=SERVICE_INSTANCE_TYPE,
            environment=ENV_VARS,
            model_id=TRAINING_MODEL_ID)
        expected_payload = {
            'version_id': VERSION_ID,
            'instance_type': SERVICE_INSTANCE_TYPE,
            'instance_number': SERVICE_INSTANCE_NUMBER,
            'min_instance_number': 1,
            'max_instance_number': SERVICE_INSTANCE_NUMBER * 2,
            'enable_autoscale': True,
            'models': {
                'alias': TRAINING_MODEL_ID
            },
            'environment': ENV_VARS,
        }
        self.assertDictEqual(m.request_history[0].json(), expected_payload)
        self.assertDictEqual(ret, SERVICE_RES)

    @requests_mock.Mocker()
    def test_get_service(self, m):
        path = '/organizations/{}/deployments/{}/services/{}'.format(
            ORGANIZATION_ID, DEPLOYMENT_ID, SERVICE_ID)
        m.get(path, json=SERVICE_RES)

        client = APIClient()
        ret = client.get_service(ORGANIZATION_ID, DEPLOYMENT_ID, SERVICE_ID)
        self.assertDictEqual(ret, SERVICE_RES)

    @requests_mock.Mocker()
    def test_get_services(self, m):
        path = '/organizations/{}/deployments/{}/services'.format(
            ORGANIZATION_ID, DEPLOYMENT_ID)
        m.get(path, json=SERVICE_LIST_RES)

        client = APIClient()
        ret = client.get_services(ORGANIZATION_ID, DEPLOYMENT_ID)
        self.assertListEqual(ret, SERVICE_LIST_RES)

    @requests_mock.Mocker()
    def test_update_service(self, m):
        path = '/organizations/{}/deployments/{}/services/{}'.format(
            ORGANIZATION_ID, DEPLOYMENT_ID, SERVICE_ID)
        m.patch(path, json=SERVICE_PAYLOAD)

        client = APIClient()
        ret = client.update_service(ORGANIZATION_ID, DEPLOYMENT_ID, SERVICE_ID)
        self.assertDictEqual(ret, SERVICE_PAYLOAD)

    @requests_mock.Mocker()
    def test_delete_service(self, m):
        path = '/organizations/{}/deployments/{}/services/{}'.format(
            ORGANIZATION_ID, DEPLOYMENT_ID, SERVICE_ID)
        message_res = {
            "message": "ser-abc1111111111111 deleted"
        }
        m.delete(path, json=message_res)

        client = APIClient()
        ret = client.delete_service(ORGANIZATION_ID, DEPLOYMENT_ID, SERVICE_ID)
        self.assertDictEqual(ret, message_res)

    @requests_mock.Mocker()
    def test_stop_service(self, m):
        path = '/organizations/{}/deployments/{}/services/{}/stop'.format(
            ORGANIZATION_ID, DEPLOYMENT_ID, SERVICE_ID)
        message_res = {
            "message": "ser-abc1111111111111 stopped"
        }
        m.post(path, json=message_res)

        client = APIClient()
        ret = client.stop_service(ORGANIZATION_ID, DEPLOYMENT_ID, SERVICE_ID)
        self.assertDictEqual(ret, message_res)

    @requests_mock.Mocker()
    def test_start_service(self, m):
        path = '/organizations/{}/deployments/{}/services/{}/start'.format(
            ORGANIZATION_ID, DEPLOYMENT_ID, SERVICE_ID)
        message_res = {
            "message": "ser-abc1111111111111 started"
        }
        m.post(path, json=message_res)

        client = APIClient()
        ret = client.start_service(ORGANIZATION_ID, DEPLOYMENT_ID, SERVICE_ID)
        self.assertDictEqual(ret, message_res)

    @requests_mock.Mocker()
    def test_get_service_recent_logs(self, m):
        path = '/organizations/{}/deployments/{}/services/{}/recentlogs'.format(
            ORGANIZATION_ID, DEPLOYMENT_ID, SERVICE_ID)
        m.get(path, json=SERVICE_RECENT_LOG_RES)

        client = APIClient()
        res = client.get_service_recent_logs(
            organization_id=ORGANIZATION_ID,
            deployment_id=DEPLOYMENT_ID,
            service_id=SERVICE_ID
        )
        self.assertDictEqual(res, SERVICE_RECENT_LOG_RES)

    @requests_mock.Mocker()
    def test_request_service_with_json_data(self, m):
        request_json = {'foo': 'bar'}

        def match_request(request):
            content_type = request._request.headers.get('Content-Type', "")
            if content_type != 'application/json':
                return False
            body = request._request.body.decode()
            if json.dumps(request_json) != body:
                return False
            return True

        url = 'http://{}.{}/deployments/{}/services/{}'.format(
            ORGANIZATION_ID, ABEJA_API_NETLOC, DEPLOYMENT_ID, SERVICE_ID)
        message_res = {
            "message": "ok"
        }
        m.post(url, additional_matcher=match_request, json=message_res)

        Connection.BASE_URL = ABEJA_API_URL
        client = APIClient()
        ret = client.request_service(
            organization_id=ORGANIZATION_ID,
            deployment_id=DEPLOYMENT_ID,
            service_id=SERVICE_ID,
            json=request_json)
        self.assertEqual(ret.json(), message_res)

    @requests_mock.Mocker()
    def test_request_service_with_binary_data(self, m):
        request_binary = b'binary data'

        def match_request(request):
            content_type = request._request.headers.get('Content-Type', "")
            if content_type != 'image/png':
                return False
            body = request._request.body
            if request_binary != body:
                return False
            return True

        url = 'http://{}.{}/deployments/{}/services/{}'.format(
            ORGANIZATION_ID, ABEJA_API_NETLOC, DEPLOYMENT_ID, SERVICE_ID)
        message_res = {
            "message": "ok"
        }
        m.post(url, additional_matcher=match_request, json=message_res)

        Connection.BASE_URL = ABEJA_API_URL
        client = APIClient()
        ret = client.request_service(
            organization_id=ORGANIZATION_ID,
            deployment_id=DEPLOYMENT_ID,
            service_id=SERVICE_ID,
            data=request_binary,
            content_type='image/png')
        self.assertEqual(ret.json(), message_res)
