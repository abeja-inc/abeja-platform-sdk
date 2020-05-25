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
    def test_get_training_models(self, m):
        path = '/organizations/{}/training/definitions/{}/models'.format(
            ORGANIZATION_ID, JOB_DEFINITION_NAME)
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
        client.get_training_models(
            ORGANIZATION_ID,
            JOB_DEFINITION_NAME,
            filter_archived=True)
        m.assert_called_once_with(
            'GET',
            url,
            params=expected_params,
            headers={
                'User-Agent': 'abeja-platform-sdk/{}'.format(SDK_VERSION)},
            timeout=30,
            data=None,
            json=None)

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
        client.get_training_models(
            ORGANIZATION_ID,
            JOB_DEFINITION_NAME,
            filter_archived=False)
        m.assert_called_once_with(
            'GET',
            url,
            params=expected_params,
            headers={
                'User-Agent': 'abeja-platform-sdk/{}'.format(SDK_VERSION)},
            timeout=30,
            data=None,
            json=None)

    @requests_mock.Mocker()
    def test_create_training_model(self, m):
        model_data = BytesIO(b'...')
        parameters = {
            "description": "description",
            "user_parameters": {}
        }
        path = '/organizations/{}/training/definitions/{}/models'.format(
            ORGANIZATION_ID, JOB_DEFINITION_NAME)
        m.post(path, json=TRAINING_MODEL_RES)

        client = APIClient()
        ret = client.create_training_model(
            ORGANIZATION_ID,
            JOB_DEFINITION_NAME,
            model_data=model_data,
            parameters=parameters)
        self.assertDictEqual(ret, TRAINING_MODEL_RES)

        with self.assertRaises(BadRequest) as e:
            client.create_training_model(
                ORGANIZATION_ID, JOB_DEFINITION_NAME, None)
        self.assertEqual(
            e.exception.error_description,
            'model_data is necessary')

    @requests_mock.Mocker()
    def test_get_training_model(self, m):
        path = '/organizations/{}/training/definitions/{}/models/{}'.format(
            ORGANIZATION_ID, JOB_DEFINITION_NAME, TRAINING_MODEL_ID)
        m.get(path, json=TRAINING_MODEL_RES)

        client = APIClient()
        ret = client.get_training_model(
            ORGANIZATION_ID,
            JOB_DEFINITION_NAME,
            TRAINING_MODEL_ID)
        self.assertDictEqual(ret, TRAINING_MODEL_RES)

    @requests_mock.Mocker()
    def test_patch_training_model(self, m):
        description = 'new description'
        path = '/organizations/{}/training/definitions/{}/models/{}'.format(
            ORGANIZATION_ID, JOB_DEFINITION_NAME, TRAINING_MODEL_ID)
        m.patch(path, json=TRAINING_MODEL_RES)

        client = APIClient()
        ret = client.patch_training_model(
            ORGANIZATION_ID,
            JOB_DEFINITION_NAME,
            TRAINING_MODEL_ID,
            description)
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
        ret = client.download_training_model(
            ORGANIZATION_ID, JOB_DEFINITION_NAME, TRAINING_MODEL_ID)
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
        ret = client.archive_training_model(
            ORGANIZATION_ID, JOB_DEFINITION_NAME, TRAINING_MODEL_ID)
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
        ret = client.unarchive_training_model(
            ORGANIZATION_ID, JOB_DEFINITION_NAME, TRAINING_MODEL_ID)
        self.assertDictEqual(ret, res)
