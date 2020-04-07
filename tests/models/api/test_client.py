import unittest
from io import BytesIO
from mock import patch

import requests_mock
from abeja import VERSION as SDK_VERSION
from abeja.common.connection import Connection

from abeja.exceptions import BadRequest
from abeja.models import APIClient
ABEJA_API_URL = 'http://localhost:8080'


ORGANIZATION_ID = '1111111111111'
MODEL_ID = '1111111111111'
MODEL_NAME = 'model_name'
MODEL_DESCRIPTION = 'this is description of the model '
MODEL_RES = {
    'model_id': MODEL_ID,
    'name': 'model_name',
    'description': 'this is description of the model',
    'created_at': '2018-01-01T00:00:00.000000Z',
    'modified_at': '2018-01-01T00:00:00.000000Z',
    'versions': []
}
MODEL_LIST_RES = [
    MODEL_RES
]

MODEL_VERSION_ID = 'ver-c37e4e41b25243c9'
VERSION = '0.0.1'
HANDLER = 'main:handler'
IMAGE = 'abeja-inc/minimal:0.1.0'

MODEL_VERSION_RES = {
    'version': VERSION,
    'version_id': MODEL_VERSION_ID,
    'image': IMAGE,
    'handler': HANDLER,
    'model_id': MODEL_ID,
    'created_at': '2017-10-27T08:00:38.334312Z',
    'modified_at': '2017-10-27T08:00:38.334436Z',
    'training_job_id': None,
    'job_definition_id': None,
    'job_definition_version': None
}
MODEL_VERSION_LIST_RES = [
    MODEL_VERSION_RES
]

JOB_DEFINITION_NAME = 'dummy_job_def_name'
TRAINING_MODEL_ID = "1111111111111"
JOB_DEFINITION_ID = '1111111111111'
TRAINING_JOB_ID = '1111111111111'
TRAINING_MODEL_RES = {
    "training_model_id": TRAINING_MODEL_ID,
    "job_definition_id": JOB_DEFINITION_ID,
    "training_job_id": TRAINING_JOB_ID,
    "user_parameters": {},
    "description": "this is description of the model",
    "archived": False,
    "exec_env": "cloud",
    "created_at": "2018-01-01T00:00:00.00000Z",
    "modified_at": "2018-01-01T00:00:00.00000Z"
}
TRAINING_MODEL_LIST_RES = {
    "entities": [TRAINING_MODEL_RES]
}


class TestAPIClient(unittest.TestCase):

    @requests_mock.Mocker()
    def test_create_model(self, m):
        path = '/organizations/{}/models'.format(ORGANIZATION_ID)
        m.post(path, json=MODEL_RES)

        client = APIClient()
        ret = client.create_model(ORGANIZATION_ID, MODEL_NAME, MODEL_DESCRIPTION)
        expected_payload = {
            'name': MODEL_NAME,
            'description': MODEL_DESCRIPTION,
        }
        self.assertDictEqual(m.request_history[0].json(), expected_payload)
        self.assertDictEqual(ret, MODEL_RES)

    @requests_mock.Mocker()
    def test_get_model(self, m):
        path = '/organizations/{}/models/{}'.format(ORGANIZATION_ID, MODEL_ID)
        m.get(path, json=MODEL_RES)

        client = APIClient()
        ret = client.get_model(ORGANIZATION_ID, MODEL_ID)
        self.assertDictEqual(ret, MODEL_RES)

    @requests_mock.Mocker()
    def test_get_models(self, m):
        path = '/organizations/{}/models'.format(ORGANIZATION_ID)
        m.get(path, json=MODEL_LIST_RES)

        client = APIClient()
        ret = client.get_models(ORGANIZATION_ID)
        self.assertListEqual(ret, MODEL_LIST_RES)

    @requests_mock.Mocker()
    def test_delete_model(self, m):
        path = '/organizations/{}/models/{}'.format(ORGANIZATION_ID, MODEL_ID)
        m.delete(path, json=MODEL_RES)

        client = APIClient()
        ret = client.delete_model(ORGANIZATION_ID, MODEL_ID)
        self.assertDictEqual(ret, MODEL_RES)

    @requests_mock.Mocker()
    def test_create_model_version(self, m):
        path = '/organizations/{}/models/{}/versions'.format(ORGANIZATION_ID, MODEL_ID)
        upload_url = "https://xxxxxxxx.s3.amazonaws.com/9999999999999/ver-abcdefghij123456/" \
                     "source.tgz?XXXXXXXXXXXXXXXXXXXX"
        res = {
            "created_at": "2018-06-14T07:15:43.462664Z",
            "handler": "main:handler",
            "image": "abeja-inc/minimal:0.1.0",
            "job_definition_id": None,
            "job_definition_version": None,
            "model_id": "1462815098134",
            "modified_at": "2018-06-14T07:15:43.462824Z",
            "training_job_id": None,
            "upload_url": upload_url,
            "version": VERSION,
            "version_id": MODEL_VERSION_ID
        }

        m.post(path, json=res)

        params = {
            'version': VERSION,
            'handler': HANDLER,
            'image': IMAGE,
            'content_type': 'test/csv'
        }
        client = APIClient()
        client.create_model_version(ORGANIZATION_ID, MODEL_ID, **params)
        self.assertDictEqual(m.request_history[0].json(), params)

    @requests_mock.Mocker()
    def test_get_model_version(self, m):
        path = '/organizations/{}/models/{}/versions/{}'.format(ORGANIZATION_ID, MODEL_ID, MODEL_VERSION_ID)
        m.get(path, json=MODEL_VERSION_RES)

        client = APIClient()
        ret = client.get_model_version(ORGANIZATION_ID, MODEL_ID, MODEL_VERSION_ID)
        self.assertDictEqual(ret, MODEL_VERSION_RES)

    @requests_mock.Mocker()
    def test_get_model_versions(self, m):
        path = '/organizations/{}/models/{}/versions'.format(ORGANIZATION_ID, MODEL_ID)
        m.get(path, json=MODEL_VERSION_LIST_RES)

        client = APIClient()
        ret = client.get_model_versions(ORGANIZATION_ID, MODEL_ID)
        self.assertListEqual(ret, MODEL_VERSION_LIST_RES)

    @requests_mock.Mocker()
    def test_delete_model_version(self, m):
        path = '/organizations/{}/models/{}/versions/{}'.format(ORGANIZATION_ID, MODEL_ID, MODEL_VERSION_ID)
        m.delete(path, json=MODEL_VERSION_RES)

        client = APIClient()
        ret = client.delete_model_version(ORGANIZATION_ID, MODEL_ID, MODEL_VERSION_ID)
        self.assertDictEqual(ret, MODEL_VERSION_RES)

    @requests_mock.Mocker()
    def test_get_training_models(self, m):
        path = '/organizations/{}/training/definitions/{}/models'.format(ORGANIZATION_ID, JOB_DEFINITION_NAME)
        m.get(path, json=TRAINING_MODEL_LIST_RES)

        client = APIClient()
        ret = client.get_training_models(ORGANIZATION_ID, JOB_DEFINITION_NAME)
        self.assertDictEqual(ret, TRAINING_MODEL_LIST_RES)

    @patch('requests.Session.request')
    def test_get_training_models_filter_archived_true(self, m):
        url = '{}/organizations/{}/training/definitions/{}/models'.format(
            ABEJA_API_URL, ORGANIZATION_ID, JOB_DEFINITION_NAME)
        m.get(url, json=TRAINING_MODEL_LIST_RES)
        expected_params = {
            'filter_archived': 'exclude_archived'
        }
        Connection.BASE_URL = ABEJA_API_URL
        client = APIClient()
        client.get_training_models(ORGANIZATION_ID, JOB_DEFINITION_NAME, filter_archived=True)
        m.assert_called_once_with('GET', url, params=expected_params,
                                  headers={'User-Agent': 'abeja-platform-sdk/{}'.format(SDK_VERSION)},
                                  timeout=30, data=None, json=None)

    @patch('requests.Session.request')
    def test_get_training_models_filter_archived_false(self, m):
        url = '{}/organizations/{}/training/definitions/{}/models'.format(
            ABEJA_API_URL, ORGANIZATION_ID, JOB_DEFINITION_NAME)
        m.get(url, json=TRAINING_MODEL_LIST_RES)
        expected_params = {
            'filter_archived': 'include_archived'
        }
        Connection.BASE_URL = ABEJA_API_URL
        client = APIClient()
        client.get_training_models(ORGANIZATION_ID, JOB_DEFINITION_NAME, filter_archived=False)
        m.assert_called_once_with('GET', url, params=expected_params,
                                  headers={'User-Agent': 'abeja-platform-sdk/{}'.format(SDK_VERSION)},
                                  timeout=30, data=None, json=None)

    @requests_mock.Mocker()
    def test_create_training_model(self, m):
        model_data = BytesIO(b'...')
        parameters = {
            "description": "description",
            "user_parameters": {}
        }
        path = '/organizations/{}/training/definitions/{}/models'.format(ORGANIZATION_ID, JOB_DEFINITION_NAME)
        m.post(path, json=TRAINING_MODEL_RES)

        client = APIClient()
        ret = client.create_training_model(
            ORGANIZATION_ID, JOB_DEFINITION_NAME, model_data=model_data, parameters=parameters)
        self.assertDictEqual(ret, TRAINING_MODEL_RES)

        with self.assertRaises(BadRequest) as e:
            client.create_training_model(ORGANIZATION_ID, JOB_DEFINITION_NAME, None)
        self.assertEqual(e.exception.error_description, 'model_data is necessary')

    @requests_mock.Mocker()
    def test_get_training_model(self, m):
        path = '/organizations/{}/training/definitions/{}/models/{}'.format(
            ORGANIZATION_ID, JOB_DEFINITION_NAME, TRAINING_MODEL_ID)
        m.get(path, json=TRAINING_MODEL_RES)

        client = APIClient()
        ret = client.get_training_model(ORGANIZATION_ID, JOB_DEFINITION_NAME, TRAINING_MODEL_ID)
        self.assertDictEqual(ret, TRAINING_MODEL_RES)

    @requests_mock.Mocker()
    def test_patch_training_model(self, m):
        description = 'new description'
        path = '/organizations/{}/training/definitions/{}/models/{}'.format(
            ORGANIZATION_ID, JOB_DEFINITION_NAME, TRAINING_MODEL_ID)
        m.patch(path, json=TRAINING_MODEL_RES)

        client = APIClient()
        ret = client.patch_training_model(ORGANIZATION_ID, JOB_DEFINITION_NAME, TRAINING_MODEL_ID, description)
        self.assertDictEqual(ret, TRAINING_MODEL_RES)

    @requests_mock.Mocker()
    def test_download_training_model(self, m):
        res = {
            'download_uri': 'https://dummy.com/download_uri'
        }
        path = '/organizations/{}/training/definitions/{}/models/{}/download'.format(
            ORGANIZATION_ID, JOB_DEFINITION_NAME, TRAINING_MODEL_ID)
        m.get(path, json=res)

        client = APIClient()
        ret = client.download_training_model(ORGANIZATION_ID, JOB_DEFINITION_NAME, TRAINING_MODEL_ID)
        self.assertDictEqual(ret, res)

    @requests_mock.Mocker()
    def test_archive_training_model(self, m):
        res = {
            'message': '{JOB_DEFINITION_NAME}:{TRAINING_MODEL_ID} archived'
        }
        path = '/organizations/{}/training/definitions/{}/models/{}/archive'.format(
            ORGANIZATION_ID, JOB_DEFINITION_NAME, TRAINING_MODEL_ID)
        m.post(path, json=res)

        client = APIClient()
        ret = client.archive_training_model(ORGANIZATION_ID, JOB_DEFINITION_NAME, TRAINING_MODEL_ID)
        self.assertDictEqual(ret, res)

    @requests_mock.Mocker()
    def test_unarchive_training_model(self, m):
        res = {
            'message': '{JOB_DEFINITION_NAME}:{TRAINING_MODEL_ID} unarchived'
        }
        path = '/organizations/{}/training/definitions/{}/models/{}/unarchive'.format(
            ORGANIZATION_ID, JOB_DEFINITION_NAME, TRAINING_MODEL_ID)
        m.post(path, json=res)

        client = APIClient()
        ret = client.unarchive_training_model(ORGANIZATION_ID, JOB_DEFINITION_NAME, TRAINING_MODEL_ID)
        self.assertDictEqual(ret, res)
