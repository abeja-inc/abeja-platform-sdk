import base64
import json
import os
import unittest
from unittest.mock import patch

import requests
from mock import MagicMock

from abeja import VERSION
from abeja.common.connection import Connection
from abeja.common.connection import http_error_handler
from abeja.common.connection import (
    DEFAULT_CONNECTION_TIMEOUT,
    DEFAULT_MAX_RETRY_COUNT
)
from abeja.exceptions import (
    HttpError,
    BadRequest,
    InternalServerError
)

TEST_TOKEN = 'test_token'
TEST_USER_ID = 'user-test_user_id'
TEST_NON_PREFIX_USER_ID = 'test_user_id'
TEST_PERSONAL_ACCESS_TOKEN = 'test_personal_access_token'
TEST_DATASOURCE_ID = 'datasource-test_datasource_id'
TEST_NON_PREFIX_DATASOURCE_ID = 'test_datasource_id'
TEST_DATASOURCE_SECRET = 'test_datasource_secret'
TEST_ABEJA_SDK_CONNECTION_TIMEOUT = '120'
TEST_ABEJA_SDK_MAX_RETRY_COUNT = '10'


class TestConnection(unittest.TestCase):
    @patch.dict(os.environ, {})
    def test_init(self):
        dummy_credential = {
            'auth_token': 'dummy'
        }
        connection = Connection(dummy_credential)
        self.assertEqual(connection.credential, dummy_credential)

    @patch.dict(os.environ, {'PLATFORM_AUTH_TOKEN': TEST_TOKEN})
    def test_init_with_auth_token(self):
        connection = Connection()
        self.assertEqual(connection.credential['auth_token'], TEST_TOKEN)

    @patch.dict(os.environ, {
        'ABEJA_PLATFORM_USER_ID': TEST_USER_ID,
        'ABEJA_PLATFORM_PERSONAL_ACCESS_TOKEN': TEST_PERSONAL_ACCESS_TOKEN
    })
    def test_init_with_user_id_and_personal_access_token(self):
        connection = Connection()
        self.assertEqual(connection.credential['user_id'], TEST_USER_ID)
        self.assertEqual(connection.credential['personal_access_token'],
                         TEST_PERSONAL_ACCESS_TOKEN)

    @patch.dict(os.environ, {
        'ABEJA_PLATFORM_USER_ID': TEST_NON_PREFIX_USER_ID,
        'ABEJA_PLATFORM_PERSONAL_ACCESS_TOKEN': TEST_PERSONAL_ACCESS_TOKEN
    })
    def test_init_with_non_prefix_user_id_and_personal_access_token(self):
        connection = Connection()
        self.assertEqual(connection.credential['user_id'], TEST_USER_ID)
        self.assertEqual(connection.credential['personal_access_token'],
                         TEST_PERSONAL_ACCESS_TOKEN)

    @patch.dict(os.environ, {
        'ABEJA_PLATFORM_DATASOURCE_ID': TEST_DATASOURCE_ID,
        'ABEJA_PLATFORM_DATASOURCE_SECRET': TEST_DATASOURCE_SECRET
    })
    def test_init_with_datasource_id_and_secret(self):
        connection = Connection()
        self.assertEqual(
            connection.credential['datasource_id'],
            TEST_DATASOURCE_ID)
        self.assertEqual(
            connection.credential['datasource_secret'],
            TEST_DATASOURCE_SECRET)

    @patch.dict(os.environ, {
        'ABEJA_PLATFORM_DATASOURCE_ID': TEST_NON_PREFIX_DATASOURCE_ID,
        'ABEJA_PLATFORM_DATASOURCE_SECRET': TEST_DATASOURCE_SECRET
    })
    def test_init_with_non_prefix_datasource_id_and_secret(self):
        connection = Connection()
        self.assertEqual(
            connection.credential['datasource_id'],
            TEST_DATASOURCE_ID)
        self.assertEqual(
            connection.credential['datasource_secret'],
            TEST_DATASOURCE_SECRET)

    def test_api_request(self):
        Connection.BASE_URL = 'http://localhost:8080'
        connection = Connection()
        connection.request = MagicMock()

        method = 'GET'
        path = '/dummy'
        connection.api_request(method, path, headers=None)

        connection.request.assert_called_with(
            method,
            'http://localhost:8080{}'.format(path),
            data=None,
            headers={
                'User-Agent': 'abeja-platform-sdk/{}'.format(VERSION)},
            json=None,
            params=None)

    def test_api_request_with_bad_request(self):
        connection = Connection()
        connection.request = MagicMock()

        error = requests.exceptions.HTTPError()
        res = requests.models.Response()
        res.url = 'https://xxxxxxxx.com'
        res.status_code = 400
        api_response = {
            'error': 'test',
            'error_description': 'test error description'}
        res._content = json.dumps(api_response).encode('utf-8')
        error.response = res

        connection.request.side_effect = error

        method = 'GET'
        path = '/dummy'
        with self.assertRaises(BadRequest) as e:
            connection.api_request(method, path, headers=None)
        self.assertEqual(str(e.exception),
                         '<BadRequest "test": test error description'
                         ' (400 from https://xxxxxxxx.com)>')

    def test_api_request_with_bad_request_with_error_detail(self):
        connection = Connection()
        connection.request = MagicMock()

        error = requests.exceptions.HTTPError()
        res = requests.models.Response()
        res.url = 'https://xxxxxxxx.com'
        res.status_code = 400
        api_response = {
            'error': 'test',
            'error_description': 'test error description',
            'error_detail': {'source_data': ['unknown field']}
        }
        res._content = json.dumps(api_response).encode('utf-8')
        error.response = res

        connection.request.side_effect = error

        method = 'GET'
        path = '/dummy'
        with self.assertRaises(BadRequest) as e:
            connection.api_request(method, path, headers=None)
        self.assertEqual(
            str(e.exception),
            '<BadRequest "test": test error description'
            ' (400 from https://xxxxxxxx.com)'
            ', {\'source_data\': [\'unknown field\']}>')

    def test_api_request_error_with_none_json_response(self):
        connection = Connection()
        connection.request = MagicMock()

        error = requests.exceptions.HTTPError()
        res = requests.models.Response()
        res.status_code = 500
        res._content = 'raw text'.encode('utf-8')
        error.response = res

        connection.request.side_effect = error

        method = 'GET'
        path = '/dummy'
        with self.assertRaises(InternalServerError) as e:
            connection.api_request(method, path, headers=None)
        self.assertEqual(str(e.exception),
                         '<InternalServerError "Internal Server Error": raw text>')

    def test_api_request_error_with_undefined_error_code(self):
        connection = Connection()
        connection.request = MagicMock()

        error = requests.exceptions.HTTPError()
        res = requests.models.Response()
        res.status_code = 501
        api_response = {'error_description': 'test error description'}
        res._content = json.dumps(api_response).encode('utf-8')
        error.response = res

        connection.request.side_effect = error

        method = 'GET'
        path = '/dummy'
        with self.assertRaises(HttpError) as e:
            connection.api_request(method, path, headers=None)
        self.assertEqual(str(e.exception),
                         '<HttpError "Not Implemented": test error description>')

    def test_set_user_agent(self):
        connection = Connection()
        header = connection._set_user_agent()
        self.assertDictEqual(
            header, {
                'User-Agent': 'abeja-platform-sdk/{}'.format(VERSION)})

    def test_get_auth_header_with_auth_token(self):
        auth_token = 'test_token'
        credential = {
            'auth_token': auth_token
        }
        connection = Connection(credential=credential)
        header = connection._get_auth_header()
        self.assertDictEqual(
            header, {
                'Authorization': 'Bearer {}'.format(auth_token)})

    def test_get_auth_header_with_user_id_and_personal_access_token(self):
        user_id = TEST_USER_ID
        personal_access_token = TEST_PERSONAL_ACCESS_TOKEN
        credential = {
            'user_id': user_id,
            'personal_access_token': personal_access_token
        }
        connection = Connection(credential=credential)
        header = connection._get_auth_header()
        s = '{}:{}'.format(user_id, personal_access_token)
        s = base64.b64encode(s.encode('utf-8'))
        expected = {
            'Authorization': 'Basic {}'.format(s.decode('utf-8'))
        }
        self.assertDictEqual(header, expected)

    def test_get_auth_header_with_datasource_id_and_secret(self):
        datasource_id = TEST_DATASOURCE_ID
        datasource_secret = TEST_DATASOURCE_SECRET
        credential = {
            'datasource_id': datasource_id,
            'datasource_secret': datasource_secret
        }
        connection = Connection(credential=credential)
        header = connection._get_auth_header()
        s = '{}:{}'.format(datasource_id, datasource_secret)
        s = base64.b64encode(s.encode('utf-8'))
        expected = {
            'Authorization': 'Basic {}'.format(s.decode('utf-8'))
        }
        self.assertDictEqual(header, expected)

    def test_get_auth_header_without_anything(self):
        credential = {}
        connection = Connection(credential=credential)
        header = connection._get_auth_header()
        expected = {}
        self.assertDictEqual(header, expected)

    def test_http_error_handler(self):
        response = requests.models.Response()
        response.status_code = 400
        response._content = json.dumps({
            "error": "bad_request",
            "error_description": "parameters is insufficient or invalid",
            "error_detail": {
                "source_data": [
                    "unknown field"
                ]
            }
        }).encode('utf-8')
        e = requests.exceptions.HTTPError(response=response)
        with self.assertRaises(BadRequest):
            try:
                http_error_handler(e)
            except Exception as e:
                self.assertDictEqual(
                    e.error_detail, {"source_data": ["unknown field"]})
                raise

    @patch.dict(os.environ, {
        'ABEJA_SDK_CONNECTION_TIMEOUT': TEST_ABEJA_SDK_CONNECTION_TIMEOUT,
        'ABEJA_SDK_MAX_RETRY_COUNT': TEST_ABEJA_SDK_MAX_RETRY_COUNT
    })
    def test_http_request_parameters_with_env_vars(self):
        connection = Connection()
        self.assertEqual(connection.timeout, TEST_ABEJA_SDK_CONNECTION_TIMEOUT)
        self.assertEqual(
            connection.max_retry_count,
            TEST_ABEJA_SDK_MAX_RETRY_COUNT)

    def test_http_request_parameters_with_args(self):
        test_timeout = 80
        test_max_retry_count = 11
        connection = Connection(
            timeout=test_timeout,
            max_retry_count=test_max_retry_count)
        self.assertEqual(connection.timeout, test_timeout)
        self.assertEqual(connection.max_retry_count, test_max_retry_count)

    def test_http_request_parameters_without_args(self):
        connection = Connection()
        self.assertEqual(connection.timeout, DEFAULT_CONNECTION_TIMEOUT)
        self.assertEqual(connection.max_retry_count, DEFAULT_MAX_RETRY_COUNT)
