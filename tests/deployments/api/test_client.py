import unittest

import requests_mock

from abeja.deployments import APIClient
from abeja.exceptions import BadRequest


ORGANIZATION_ID = '1111111111111'
DEPLOYMENT_ID = '2222222222222'
DEPLOYMENT_NAME = 'deployment_name'
DEPLOYMENT_DEFAULT_ENV = {
    'ENV_A': 'abc'
}

DEPLOYMENT_RES = {
    'deployment_id': DEPLOYMENT_ID,
    'name': DEPLOYMENT_NAME,
    'description': 'description',
    'creator': {
        'display_name': None,
        'email': 'platform-support@abeja.asia',
        'id': '1111111111111',
        'is_registered': True,
        'role': 'admin',
        'created_at': '2017-05-29T07:48:55Z',
        'updated_at': '2017-11-29T10:21:24Z'
    },
    'default_environment': {},
    'runs': [],
    'daemons': [],
    'services': [],
    'triggers': [],
    'created_at': '2018-06-05T08:52:02.428441Z',
    'modified_at': '2018-06-05T08:52:02.428587Z'
}
DEPLOYMENT_LIST_RES = [
    DEPLOYMENT_RES
]

TEMPLATE_ID = 1
DEPLOYMENT_VERSION_ID = 'ver-c37e4e41b25243c9'
VERSION = '0.0.1'
HANDLER = 'main:handler'
IMAGE = 'abeja-inc/minimal:0.1.0'
DEPLOYMENT_VERSION_RES = {
    'version': VERSION,
    'version_id': DEPLOYMENT_VERSION_ID,
    'image': IMAGE,
    'handler': HANDLER,
    'created_at': '2017-10-27T08:00:38.334312Z',
    'modified_at': '2017-10-27T08:00:38.334436Z',
    'training_job_id': None,
    'job_definition_id': None,
    'job_definition_version': None
}
DEPLOYMENT_VERSION_LIST_RES = {
    'entries': [
        DEPLOYMENT_VERSION_RES
    ]
}


class TestAPIClient(unittest.TestCase):

    @requests_mock.Mocker()
    def test_create_deployment(self, m):
        path = '/organizations/{}/deployments'.format(ORGANIZATION_ID)
        m.post(path, json=DEPLOYMENT_RES)

        client = APIClient()
        ret = client.create_deployment(ORGANIZATION_ID, name=DEPLOYMENT_NAME, description='description')
        expected_payload = {
            'name': DEPLOYMENT_NAME,
            'description': 'description',
        }
        self.assertDictEqual(m.request_history[0].json(), expected_payload)
        self.assertDictEqual(ret, DEPLOYMENT_RES)

        with self.assertRaises(BadRequest) as e:
            client.create_deployment(ORGANIZATION_ID)
        self.assertEqual(e.exception.error_description, '"name" is necessary')

    @requests_mock.Mocker()
    def test_get_deployment(self, m):
        path = '/organizations/{}/deployments/{}'.format(ORGANIZATION_ID, DEPLOYMENT_ID)
        m.get(path, json=DEPLOYMENT_RES)

        client = APIClient()
        ret = client.get_deployment(ORGANIZATION_ID, DEPLOYMENT_ID)
        self.assertDictEqual(ret, DEPLOYMENT_RES)

    @requests_mock.Mocker()
    def test_get_deployments(self, m):
        path = '/organizations/{}/deployments'.format(ORGANIZATION_ID)
        m.get(path, json=DEPLOYMENT_LIST_RES)

        client = APIClient()
        ret = client.get_deployments(ORGANIZATION_ID)
        self.assertListEqual(ret, DEPLOYMENT_LIST_RES)

    @requests_mock.Mocker()
    def test_delete_deployment(self, m):
        path = '/organizations/{}/deployments/{}'.format(ORGANIZATION_ID, DEPLOYMENT_ID)
        res = {
            'message': '{} deleted'.format(DEPLOYMENT_ID)
        }
        m.delete(path, json=res)

        client = APIClient()
        ret = client.delete_deployment(ORGANIZATION_ID, DEPLOYMENT_ID)
        self.assertDictEqual(ret, res)

    @requests_mock.Mocker()
    def test_patch_deployment(self, m):
        path = '/organizations/{}/deployments/{}'.format(ORGANIZATION_ID, DEPLOYMENT_ID)
        m.patch(path, json=DEPLOYMENT_RES)

        client = APIClient()
        ret = client.patch_deployment(ORGANIZATION_ID, DEPLOYMENT_ID, DEPLOYMENT_NAME,
                                      default_environment=DEPLOYMENT_DEFAULT_ENV)
        expected_payload = {
            'name': DEPLOYMENT_NAME,
            'default_environment': DEPLOYMENT_DEFAULT_ENV
        }
        self.assertDictEqual(m.request_history[0].json(), expected_payload)
        self.assertDictEqual(ret, DEPLOYMENT_RES)

    @requests_mock.Mocker()
    def test_get_deployment_versions(self, m):
        path = '/organizations/{}/deployments/{}/versions'.format(ORGANIZATION_ID, DEPLOYMENT_ID)
        m.get(path, json=DEPLOYMENT_VERSION_LIST_RES)

        client = APIClient()
        ret = client.get_deployment_versions(ORGANIZATION_ID, DEPLOYMENT_ID)
        self.assertDictEqual(ret, DEPLOYMENT_VERSION_LIST_RES)

    @requests_mock.Mocker()
    def test_create_deployment_version(self, m):
        path = '/organizations/{}/deployments/{}/versions'.format(ORGANIZATION_ID, DEPLOYMENT_ID)
        upload_url = "https://xxxxxxxx.s3.amazonaws.com/9999999999999/ver-abcdefghij123456/" \
                     "source.tgz?XXXXXXXXXXXXXXXXXXXX"
        res = {
            "created_at": "2018-06-14T07:15:43.462664Z",
            "handler": "main:handler",
            "image": "abeja-inc/minimal:0.1.0",
            "deployment_id": "1462815098134",
            "modified_at": "2018-06-14T07:15:43.462824Z",
            "upload_url": upload_url,
            "version": VERSION,
            "version_id": DEPLOYMENT_VERSION_ID
        }

        m.post(path, json=res)

        params = {
            'version': VERSION,
            'handler': HANDLER,
            'image': IMAGE
        }
        client = APIClient()
        client.create_deployment_version(ORGANIZATION_ID, DEPLOYMENT_ID, **params)
        self.assertDictEqual(m.request_history[0].json(), params)

    @requests_mock.Mocker()
    def test_create_deployment_from_template(self, m):
        path = '/organizations/{}/deployments/{}/code_templates'.format(ORGANIZATION_ID, DEPLOYMENT_ID)
        res = {
            "created_at": "2018-06-14T07:15:43.462664Z",
            "handler": "main:handler",
            "image": "abeja-inc/minimal:0.1.0",
            "deployment_id": "1462815098134",
            "modified_at": "2018-06-14T07:15:43.462824Z",
            "version": VERSION,
            "version_id": DEPLOYMENT_VERSION_ID
        }

        m.post(path, json=res)

        params = {
            'template_id': TEMPLATE_ID,
            'version': VERSION,
            'handler': HANDLER,
            'image': IMAGE
        }
        client = APIClient()
        client.create_deployment_from_template(ORGANIZATION_ID, DEPLOYMENT_ID, **params)
        self.assertDictEqual(m.request_history[0].json(), params)

    @requests_mock.Mocker()
    def test_get_deployment_version(self, m):
        path = '/organizations/{}/deployments/{}/versions/{}'.format(ORGANIZATION_ID, DEPLOYMENT_ID, DEPLOYMENT_VERSION_ID)
        m.get(path, json=DEPLOYMENT_VERSION_RES)

        client = APIClient()
        ret = client.get_deployment_version(ORGANIZATION_ID, DEPLOYMENT_ID, DEPLOYMENT_VERSION_ID)
        self.assertDictEqual(ret, DEPLOYMENT_VERSION_RES)

    @requests_mock.Mocker()
    def test_delete_deployment_version(self, m):
        res = {
            'message': 'ver-123456789012 deleted'
        }
        path = '/organizations/{}/deployments/{}/versions/{}'.format(ORGANIZATION_ID, DEPLOYMENT_ID, DEPLOYMENT_VERSION_ID)
        m.delete(path, json=res)

        client = APIClient()
        ret = client.delete_deployment_version(ORGANIZATION_ID, DEPLOYMENT_ID, DEPLOYMENT_VERSION_ID)
        self.assertDictEqual(ret, res)

    @requests_mock.Mocker()
    def test_download_deployment_version(self, m):
        res = {
            'download_uri': 'https://dummy.com/download_uri'
        }
        path = '/organizations/{}/deployments/{}/versions/{}/download'.format(
            ORGANIZATION_ID, DEPLOYMENT_ID, DEPLOYMENT_VERSION_ID)
        m.get(path, json=res)

        client = APIClient()
        ret = client.download_deployment_version(ORGANIZATION_ID, DEPLOYMENT_ID, DEPLOYMENT_VERSION_ID)
        self.assertDictEqual(ret, res)
