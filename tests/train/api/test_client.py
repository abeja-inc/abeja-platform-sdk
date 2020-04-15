from mock import patch
import os
import pytest
import tempfile
from abeja import VERSION
from abeja.common.connection import Connection
from abeja.exceptions import BadRequest
from abeja.train.api.client import APIClient

ORGANIZATION_ID = '1234567890123'
JOB_DEFINITION_NAME = 'dummy_job_def_name'
TRAINING_JOB_ID = '1112223334440'
VERSION_ID = 1
ABEJA_API_URL = 'http://localhost:8080'


class TestApiClient:
    def setup_method(self, _method):
        Connection.BASE_URL = ABEJA_API_URL
        self.api_client = APIClient()

    @patch('requests.Session.request')
    def test_create_training_job_definition(self, m):
        self.api_client.create_training_job_definition(
            ORGANIZATION_ID, JOB_DEFINITION_NAME)
        url = '{}/organizations/{}/training/definitions/'.format(
            ABEJA_API_URL, ORGANIZATION_ID)
        expected_data = {
            'name': JOB_DEFINITION_NAME
        }
        m.assert_called_once_with('POST', url, params=None,
                                  headers={
                                      'User-Agent': 'abeja-platform-sdk/{}'.format(VERSION)},
                                  timeout=30, data=None, json=expected_data)

    @patch('requests.Session.request')
    def test_get_training_job_definitions(self, m):
        self.api_client.get_training_job_definitions(ORGANIZATION_ID)
        url = '{}/organizations/{}/training/definitions/'.format(
            ABEJA_API_URL, ORGANIZATION_ID)
        m.assert_called_once_with('GET', url, params=None,
                                  headers={
                                      'User-Agent': 'abeja-platform-sdk/{}'.format(VERSION)},
                                  timeout=30, data=None, json=None)

    @patch('requests.Session.request')
    def test_get_training_job_definitions_filter_archived_true(self, m):
        self.api_client.get_training_job_definitions(
            ORGANIZATION_ID, filter_archived=True)
        url = '{}/organizations/{}/training/definitions/'.format(
            ABEJA_API_URL, ORGANIZATION_ID)
        expected_params = {
            'filter_archived': 'exclude_archived'
        }
        m.assert_called_once_with('GET', url, params=expected_params,
                                  headers={
                                      'User-Agent': 'abeja-platform-sdk/{}'.format(VERSION)},
                                  timeout=30, data=None, json=None)

    @patch('requests.Session.request')
    def test_get_training_job_definitions_filter_archived_false(self, m):
        self.api_client.get_training_job_definitions(
            ORGANIZATION_ID, filter_archived=False)
        url = '{}/organizations/{}/training/definitions/'.format(
            ABEJA_API_URL, ORGANIZATION_ID)
        expected_params = {
            'filter_archived': 'include_archived'
        }
        m.assert_called_once_with('GET', url, params=expected_params,
                                  headers={
                                      'User-Agent': 'abeja-platform-sdk/{}'.format(VERSION)},
                                  timeout=30, data=None, json=None)

    @patch('requests.Session.request')
    def test_get_training_job_definition(self, m):
        self.api_client.get_training_job_definition(
            ORGANIZATION_ID, JOB_DEFINITION_NAME)
        url = '{}/organizations/{}/training/definitions/{}'.format(
            ABEJA_API_URL, ORGANIZATION_ID, JOB_DEFINITION_NAME)
        m.assert_called_once_with('GET', url, params=None,
                                  headers={
                                      'User-Agent': 'abeja-platform-sdk/{}'.format(VERSION)},
                                  timeout=30, data=None, json=None)

    @patch('requests.Session.request')
    @pytest.mark.parametrize(
        'include_jobs,expected',
        [
            (True, 'true'),
            (False, 'false'),
        ]
    )
    def test_get_training_job_definition_with_include_jobs(self, m, include_jobs, expected):
        self.api_client.get_training_job_definition(
            ORGANIZATION_ID, JOB_DEFINITION_NAME, include_jobs=include_jobs)
        url = '{}/organizations/{}/training/definitions/{}'.format(
            ABEJA_API_URL, ORGANIZATION_ID, JOB_DEFINITION_NAME)
        expected_params = {
            'include_jobs': expected
        }
        m.assert_called_once_with('GET', url, params=expected_params,
                                  headers={
                                      'User-Agent': 'abeja-platform-sdk/{}'.format(VERSION)},
                                  timeout=30, data=None, json=None)

    @patch('requests.Session.request')
    def test_delete_training_job_definition(self, m):
        self.api_client.delete_training_job_definition(
            ORGANIZATION_ID, JOB_DEFINITION_NAME)
        url = '{}/organizations/{}/training/definitions/{}'.format(
            ABEJA_API_URL, ORGANIZATION_ID, JOB_DEFINITION_NAME)
        m.assert_called_once_with('DELETE', url, params=None,
                                  headers={
                                      'User-Agent': 'abeja-platform-sdk/{}'.format(VERSION)},
                                  timeout=30, data=None, json=None)

    @patch('requests.Session.request')
    def test_create_training_job_definition_version(self, m):
        handler = "train:handler"
        image = "abeja-inc/minimal:0.1.0"
        environment = {}
        description = ""
        with tempfile.TemporaryDirectory() as dname:
            filepath = os.path.join(dname, 'requirements.txt')
            with open(filepath, 'w') as f:
                f.write("requests==1.0.0")
            filepaths = [filepath]
            self.api_client.create_training_job_definition_version(
                ORGANIZATION_ID, JOB_DEFINITION_NAME, filepaths=filepaths, handler=handler,
                image=image, environment=environment, description=description)
        url = '{}/organizations/{}/training/definitions/{}/versions'.format(
            ABEJA_API_URL, ORGANIZATION_ID, JOB_DEFINITION_NAME)
        m.assert_called_once_with('POST', url, params=None,
                                  headers={
                                      'User-Agent': 'abeja-platform-sdk/{}'.format(VERSION)},
                                  timeout=30, data=None,
                                  json=None, files=m.call_args[1]['files'])

    @patch('requests.Session.request')
    def test_create_training_job_definition_version_file_not_found(self, m):
        filepaths = ['hoge.txt']
        handler = "train:handler"
        image = "abeja-inc/minimal:0.1.0"
        environment = {}
        description = ""
        with pytest.raises(FileNotFoundError):
            self.api_client.create_training_job_definition_version(
                ORGANIZATION_ID, JOB_DEFINITION_NAME, filepaths=filepaths, handler=handler,
                image=image, environment=environment, description=description)

    @patch('requests.Session.request')
    def test_get_training_job_definition_versions(self, m):
        self.api_client.get_training_job_definition_versions(
            ORGANIZATION_ID, JOB_DEFINITION_NAME)
        url = '{}/organizations/{}/training/definitions/{}/versions'.format(
            ABEJA_API_URL, ORGANIZATION_ID, JOB_DEFINITION_NAME)
        m.assert_called_once_with('GET', url, params=None,
                                  headers={
                                      'User-Agent': 'abeja-platform-sdk/{}'.format(VERSION)},
                                  timeout=30, data=None, json=None)

    @patch('requests.Session.request')
    def test_get_training_job_definition_versions_filter_archived_true(self, m):
        self.api_client.get_training_job_definition_versions(
            ORGANIZATION_ID, JOB_DEFINITION_NAME, filter_archived=True)
        url = '{}/organizations/{}/training/definitions/{}/versions'.format(
            ABEJA_API_URL, ORGANIZATION_ID, JOB_DEFINITION_NAME)
        expected_params = {
            'filter_archived': 'exclude_archived'
        }
        m.assert_called_once_with('GET', url, params=expected_params,
                                  headers={
                                      'User-Agent': 'abeja-platform-sdk/{}'.format(VERSION)},
                                  timeout=30, data=None, json=None)

    @patch('requests.Session.request')
    def test_get_training_job_definition_versions_filter_archived_false(self, m):
        self.api_client.get_training_job_definition_versions(
            ORGANIZATION_ID, JOB_DEFINITION_NAME, filter_archived=False)
        url = '{}/organizations/{}/training/definitions/{}/versions'.format(
            ABEJA_API_URL, ORGANIZATION_ID, JOB_DEFINITION_NAME)
        expected_params = {
            'filter_archived': 'include_archived'
        }
        m.assert_called_once_with('GET', url, params=expected_params,
                                  headers={
                                      'User-Agent': 'abeja-platform-sdk/{}'.format(VERSION)},
                                  timeout=30, data=None, json=None)

    @patch('requests.Session.request')
    def test_get_training_job_definition_version(self, m):
        self.api_client.get_training_job_definition_version(
            ORGANIZATION_ID, JOB_DEFINITION_NAME, VERSION_ID)
        url = '{}/organizations/{}/training/definitions/{}/versions/{}'.format(
            ABEJA_API_URL, ORGANIZATION_ID, JOB_DEFINITION_NAME, VERSION_ID)
        m.assert_called_once_with('GET', url, params=None,
                                  headers={
                                      'User-Agent': 'abeja-platform-sdk/{}'.format(VERSION)},
                                  timeout=30, data=None, json=None)

    @patch('requests.Session.request')
    def test_delete_training_job_definition_version(self, m):
        self.api_client.delete_training_job_definition_version(
            ORGANIZATION_ID, JOB_DEFINITION_NAME, VERSION_ID)
        url = '{}/organizations/{}/training/definitions/{}/versions/{}'.format(
            ABEJA_API_URL, ORGANIZATION_ID, JOB_DEFINITION_NAME, VERSION_ID)
        m.assert_called_once_with('DELETE', url, params=None,
                                  headers={
                                      'User-Agent': 'abeja-platform-sdk/{}'.format(VERSION)},
                                  timeout=30, data=None, json=None)

    @patch('requests.Session.request')
    @pytest.mark.parametrize(
        'user_params,environment,datasets,instance_type,description,expected',
        [
            (None, None, None, None, None, {}),
            (
                {'DUMMY_ENV_VAR': 'dummy'},
                None,
                None,
                None,
                None,
                {'environment': {'DUMMY_ENV_VAR': 'dummy'}}
            ),
            (
                None,
                {'DUMMY_ENV_VAR': 'dummy'},
                None,
                None,
                None,
                {'environment': {'DUMMY_ENV_VAR': 'dummy'}}
            ),
            (
                {'DUMMY_ENV_VAR': 'dummy1'},
                {'DUMMY_ENV_VAR': 'dummy2'},
                None,
                None,
                None,
                {'environment': {'DUMMY_ENV_VAR': 'dummy2'}}
            ),
            (
                None,
                None,
                {"mnist": "1111111111111"},
                None,
                None,
                {'datasets': {"mnist": "1111111111111"}}
            ),
            (
                None,
                None,
                None,
                'cpu-1',
                None,
                {'instance_type': 'cpu-1'}
            ),
            (
                {'DUMMY_ENV_VAR': 'dummy'},
                None,
                {"mnist": "1111111111111"},
                'cpu-1',
                'dummy description',
                {
                    'datasets': {"mnist": "1111111111111"},
                    'environment': {'DUMMY_ENV_VAR': 'dummy'},
                    'instance_type': 'cpu-1',
                    'description': 'dummy description'
                }
            ),
        ]
    )
    def test_create_training_job(self, m, user_params, environment, datasets, instance_type, description, expected):
        self.api_client.create_training_job(
            ORGANIZATION_ID, JOB_DEFINITION_NAME, VERSION_ID,
            user_params, datasets, instance_type, environment, description)
        url = '{}/organizations/{}/training/definitions/{}/versions/{}/jobs'.format(
            ABEJA_API_URL, ORGANIZATION_ID, JOB_DEFINITION_NAME, VERSION_ID)
        m.assert_called_once_with('POST', url, params=None,
                                  headers={
                                      'User-Agent': 'abeja-platform-sdk/{}'.format(VERSION)},
                                  timeout=30, data=None, json=expected)

    @patch('requests.Session.request')
    def test_create_training_job_invalid_instance_type(self, m):
        instance_type = "dummy"
        with pytest.raises(BadRequest):
            self.api_client.create_training_job(
                ORGANIZATION_ID, JOB_DEFINITION_NAME, VERSION_ID, instance_type=instance_type)

    @patch('requests.Session.request')
    def test_get_training_jobs(self, m):
        self.api_client.get_training_jobs(ORGANIZATION_ID, JOB_DEFINITION_NAME)
        url = '{}/organizations/{}/training/definitions/{}/jobs'.format(
            ABEJA_API_URL, ORGANIZATION_ID, JOB_DEFINITION_NAME, VERSION_ID)
        m.assert_called_once_with('GET', url, params={},
                                  headers={
                                      'User-Agent': 'abeja-platform-sdk/{}'.format(VERSION)},
                                  timeout=30, data=None, json=None)

    @patch('requests.Session.request')
    def test_get_training_jobs_with_limit(self, m):
        self.api_client.get_training_jobs(
            ORGANIZATION_ID, JOB_DEFINITION_NAME, limit=100)
        url = '{}/organizations/{}/training/definitions/{}/jobs'.format(
            ABEJA_API_URL, ORGANIZATION_ID, JOB_DEFINITION_NAME, VERSION_ID)
        expected_params = {
            'limit': 100
        }
        m.assert_called_once_with('GET', url, params=expected_params,
                                  headers={
                                      'User-Agent': 'abeja-platform-sdk/{}'.format(VERSION)},
                                  timeout=30, data=None, json=None)

    @patch('requests.Session.request')
    def test_get_training_jobs_with_offset(self, m):
        self.api_client.get_training_jobs(
            ORGANIZATION_ID, JOB_DEFINITION_NAME, offset=20)
        url = '{}/organizations/{}/training/definitions/{}/jobs'.format(
            ABEJA_API_URL, ORGANIZATION_ID, JOB_DEFINITION_NAME, VERSION_ID)
        expected_params = {
            'offset': 20
        }
        m.assert_called_once_with('GET', url, params=expected_params,
                                  headers={
                                      'User-Agent': 'abeja-platform-sdk/{}'.format(VERSION)},
                                  timeout=30, data=None, json=None)

    @patch('requests.Session.request')
    def test_get_training_jobs_with_limit_and_offset(self, m):
        self.api_client.get_training_jobs(
            ORGANIZATION_ID, JOB_DEFINITION_NAME, limit=5, offset=20)
        url = '{}/organizations/{}/training/definitions/{}/jobs'.format(
            ABEJA_API_URL, ORGANIZATION_ID, JOB_DEFINITION_NAME, VERSION_ID)
        expected_params = {
            'offset': 20,
            'limit': 5
        }
        m.assert_called_once_with('GET', url, params=expected_params,
                                  headers={
                                      'User-Agent': 'abeja-platform-sdk/{}'.format(VERSION)},
                                  timeout=30, data=None, json=None)

    @patch('requests.Session.request')
    def test_get_training_jobs_filter_archived_true(self, m):
        self.api_client.get_training_jobs(
            ORGANIZATION_ID, JOB_DEFINITION_NAME, filter_archived=True)
        url = '{}/organizations/{}/training/definitions/{}/jobs'.format(
            ABEJA_API_URL, ORGANIZATION_ID, JOB_DEFINITION_NAME, VERSION_ID)
        expected_params = {
            'filter_archived': 'exclude_archived'
        }
        m.assert_called_once_with('GET', url, params=expected_params,
                                  headers={
                                      'User-Agent': 'abeja-platform-sdk/{}'.format(VERSION)},
                                  timeout=30, data=None, json=None)

    @patch('requests.Session.request')
    def test_get_training_jobs_filter_archived_false(self, m):
        self.api_client.get_training_jobs(
            ORGANIZATION_ID, JOB_DEFINITION_NAME, filter_archived=False)
        url = '{}/organizations/{}/training/definitions/{}/jobs'.format(
            ABEJA_API_URL, ORGANIZATION_ID, JOB_DEFINITION_NAME, VERSION_ID)
        expected_params = {
            'filter_archived': 'include_archived'
        }
        m.assert_called_once_with('GET', url, params=expected_params,
                                  headers={
                                      'User-Agent': 'abeja-platform-sdk/{}'.format(VERSION)},
                                  timeout=30, data=None, json=None)

    @patch('requests.Session.request')
    def test_get_training_job(self, m):
        self.api_client.get_training_job(
            ORGANIZATION_ID, JOB_DEFINITION_NAME, TRAINING_JOB_ID)
        url = '{}/organizations/{}/training/definitions/{}/jobs/{}'.format(
            ABEJA_API_URL, ORGANIZATION_ID, JOB_DEFINITION_NAME, TRAINING_JOB_ID)
        m.assert_called_once_with('GET', url, params=None,
                                  headers={
                                      'User-Agent': 'abeja-platform-sdk/{}'.format(VERSION)},
                                  timeout=30, data=None, json=None)

    def test_stop_training_job(self, requests_mock):
        path = '/organizations/{}/training/definitions/{}/jobs/{}/stop'.format(
            ORGANIZATION_ID, JOB_DEFINITION_NAME, TRAINING_JOB_ID)
        requests_mock.post(path, json={
            'message': f'{JOB_DEFINITION_NAME}:{TRAINING_JOB_ID} stopped'
        })
        self.api_client.stop_training_job(
            ORGANIZATION_ID, JOB_DEFINITION_NAME, TRAINING_JOB_ID)

        request = requests_mock.request_history[0]
        assert request.method == 'POST'
        assert 'User-Agent' in request.headers
        assert request.headers['User-Agent'] == 'abeja-platform-sdk/{}'.format(VERSION)
        assert request.timeout == 30
        assert request.query == ''
        assert request.text is None
