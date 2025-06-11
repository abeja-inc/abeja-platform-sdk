import os
import unittest
import base64

import requests_mock

from abeja.secret import APIClient
from abeja.exceptions import BadRequest

os.environ['USER_AUTH_ARMS'] = 'False'
ORGANIZATION_ID = '1410000000000'
SECRET_ID = '3053595942757'
SECRET_NAME = 'AWS_ACCESS_KEY'
SECRET_VALUE = 'AKIAIOSFODNN7EXAMPLE'
SECRET_DESCRIPTION = 'AWS access key'
SECRET_VERSION_ID = '1234567890123'
ENCODED_SECRET_VALUE = base64.b64encode(SECRET_VALUE.encode('utf-8')).decode('utf-8')
EXPIRED_AT = '2024-12-15T16:50:33+09:00'
UPDATED_EXPIRED_AT = '2025-12-15T16:50:33+09:00'
USER_ID = '3614618482910'
PROVIDER = 'aws-secret-manager'
INTEGRATION_SERVICE_TYPE = 'abeja-platform-labs'
INTEGRATION_SERVICE_IDS = ['9909389711171', '9916291917033']

SECRET_VERSION = {
    'id': SECRET_VERSION_ID,
    'secret_id': SECRET_ID,
    'version': 1,
    'created_at': '2023-12-15T16:50:33+09:00',
    'organization_id': ORGANIZATION_ID,
    'provider': PROVIDER,
    'status': 'active',
    'updated_at': '2023-12-15T16:50:33+09:00'
}

SECRET_VERSION_WITH_VALUE = {
    'id': SECRET_VERSION_ID,
    'secret_id': SECRET_ID,
    'version': 1,
    'value': ENCODED_SECRET_VALUE,
    'created_at': '2023-12-15T16:50:33+09:00',
    'organization_id': ORGANIZATION_ID,
    'provider': PROVIDER,
    'status': 'active',
    'updated_at': '2023-12-15T16:50:33+09:00'
}

SECRET = {
    'id': SECRET_ID,
    'organization_id': ORGANIZATION_ID,
    'name': SECRET_NAME,
    'description': SECRET_DESCRIPTION,
    'rotation': False,
    'expired_at': EXPIRED_AT,
    'created_at': '2023-12-15T16:50:33+09:00',
    'updated_at': '2023-12-15T16:50:33+09:00',
    'versions': [SECRET_VERSION],
    'properties': None,
    'provider': PROVIDER,
    'user_id': USER_ID,
    'integration_service_type': INTEGRATION_SERVICE_TYPE,
    'integration_service_ids': INTEGRATION_SERVICE_IDS
}

SECRET_WITH_VALUE = {
    'id': SECRET_ID,
    'organization_id': ORGANIZATION_ID,
    'name': SECRET_NAME,
    'description': SECRET_DESCRIPTION,
    'rotation': False,
    'expired_at': EXPIRED_AT,
    'created_at': '2023-12-15T16:50:33+09:00',
    'updated_at': '2023-12-15T16:50:33+09:00',
    'versions': [SECRET_VERSION_WITH_VALUE],
    'properties': None,
    'provider': PROVIDER,
    'user_id': USER_ID,
    'integration_service_type': INTEGRATION_SERVICE_TYPE,
    'integration_service_ids': INTEGRATION_SERVICE_IDS
}

SECRETS_RESPONSE = {
    'organization_id': ORGANIZATION_ID,
    'secrets': [SECRET],
    'offset': 0,
    'limit': 50,
    'has_next': False
}

SECRETS_WITH_VALUE_RESPONSE = {
    'organization_id': ORGANIZATION_ID,
    'secrets': [SECRET_WITH_VALUE],
    'offset': 0,
    'limit': 50,
    'has_next': False
}

UPDATED_SECRET = {
    'id': SECRET_ID,
    'organization_id': ORGANIZATION_ID,
    'name': SECRET_NAME,
    'description': 'Updated AWS access key',
    'rotation': False,
    'integration_service_type': INTEGRATION_SERVICE_TYPE,
    'integration_service_ids': INTEGRATION_SERVICE_IDS,
    'expired_at': UPDATED_EXPIRED_AT,
    'created_at': '2023-12-15T16:50:33+09:00',
    'updated_at': '2024-04-30T10:30:00+09:00',
    'versions': [{
        'id': SECRET_VERSION_ID,
        'secret_id': SECRET_ID,
        'version': 1,
        'created_at': '2023-12-15T16:50:33+09:00',
        'organization_id': ORGANIZATION_ID,
        'provider': PROVIDER,
        'status': 'active',
        'updated_at': '2023-12-15T16:50:33+09:00'
    }],
    'properties': None,
    'provider': PROVIDER,
    'user_id': USER_ID
}

DELETE_SECRET_RESPONSE = {
    "message": "secret_id {} successfully deleted".format(SECRET_ID)
}


class TestSecretManagerAPIClient(unittest.TestCase):

    @requests_mock.Mocker()
    def test_get_secrets(self, m):
        # get-secrets-api mock
        path = '/secret-manager/organizations/{}/secrets'.format(ORGANIZATION_ID)
        m.get(path, json=SECRETS_RESPONSE)

        # unit test
        client = APIClient()
        ret = client.get_secrets(ORGANIZATION_ID)
        self.assertDictEqual(ret, SECRETS_RESPONSE)

        # with parameters
        path_with_params = '/secret-manager/organizations/{}/secrets?offset=10&limit=20&return_secret_value=true'.format(ORGANIZATION_ID)
        m.get(path_with_params, json=SECRETS_RESPONSE)
        ret = client.get_secrets(ORGANIZATION_ID, offset=10, limit=20)
        self.assertDictEqual(ret, SECRETS_RESPONSE)

        # with return_secret_value
        path_with_secret_value = '/secret-manager/organizations/{}/secrets?offset=0&limit=50&return_secret_value=true'.format(ORGANIZATION_ID)
        m.get(path_with_secret_value, json=SECRETS_WITH_VALUE_RESPONSE)
        ret = client.get_secrets(ORGANIZATION_ID)
        # 値がデコードされていることを確認
        self.assertEqual(ret['secrets'][0]['versions'][0]['value'], SECRET_VALUE)

        # バリデーションエラーテスト
        with self.assertRaises(BadRequest) as e:
            client.get_secrets(None)
        self.assertEqual(e.exception.error_description, '"organization_id" is necessary')

        with self.assertRaises(BadRequest) as e:
            client.get_secrets(ORGANIZATION_ID, offset=-1)
        self.assertEqual(e.exception.error_description, '"offset" must be greater than or equal to 0')

        with self.assertRaises(BadRequest) as e:
            client.get_secrets(ORGANIZATION_ID, limit=0)
        self.assertEqual(e.exception.error_description, '"limit" must be between 1 and 100')

        with self.assertRaises(BadRequest) as e:
            client.get_secrets(ORGANIZATION_ID, limit=101)
        self.assertEqual(e.exception.error_description, '"limit" must be between 1 and 100')

    @requests_mock.Mocker()
    def test_get_secret(self, m):
        # get-secret-api mock
        path = '/secret-manager/organizations/{}/secrets/{}'.format(ORGANIZATION_ID, SECRET_ID)
        m.get(path, json=SECRET)

        # unit test
        client = APIClient()
        ret = client.get_secret(ORGANIZATION_ID, SECRET_ID)
        self.assertDictEqual(ret, SECRET)

        # with return_secret_value
        path_with_secret_value = '/secret-manager/organizations/{}/secrets/{}?return_secret_value=true'.format(ORGANIZATION_ID, SECRET_ID)
        m.get(path_with_secret_value, json=SECRET_WITH_VALUE)
        ret = client.get_secret(ORGANIZATION_ID, SECRET_ID)
        # 値がデコードされていることを確認
        self.assertEqual(ret['versions'][0]['value'], SECRET_VALUE)

        # バリデーションエラーテスト
        with self.assertRaises(BadRequest) as e:
            client.get_secret(None, SECRET_ID)
        self.assertEqual(e.exception.error_description, '"organization_id" is necessary')

        with self.assertRaises(BadRequest) as e:
            client.get_secret(ORGANIZATION_ID, None)
        self.assertEqual(e.exception.error_description, '"secret_id" is necessary')

    @requests_mock.Mocker()
    def test_create_secret(self, m):
        # create-secret-api mock
        path = '/secret-manager/organizations/{}/secrets'.format(ORGANIZATION_ID)
        m.post(path, json=SECRET_WITH_VALUE)

        # unit test
        client = APIClient()
        ret = client.create_secret(
            ORGANIZATION_ID,
            name=SECRET_NAME,
            value=SECRET_VALUE,
            description=SECRET_DESCRIPTION,
            expired_at=EXPIRED_AT,
            integration_service_type=INTEGRATION_SERVICE_TYPE,
            integration_service_ids=INTEGRATION_SERVICE_IDS
        )
        expected_payload = {
            'name': SECRET_NAME,
            'value': ENCODED_SECRET_VALUE,
            'description': SECRET_DESCRIPTION,
            'expired_at': EXPIRED_AT,
            'integration_service_type': INTEGRATION_SERVICE_TYPE,
            'integration_service_ids': INTEGRATION_SERVICE_IDS
        }

        self.assertDictEqual(m.request_history[0].json(), expected_payload)
        self.assertDictEqual(ret, SECRET_WITH_VALUE)

        # バリデーションエラーテスト
        with self.assertRaises(BadRequest) as e:
            client.create_secret(None, SECRET_NAME, SECRET_VALUE)
        self.assertEqual(e.exception.error_description, '"organization_id" is necessary')

        with self.assertRaises(BadRequest) as e:
            client.create_secret(ORGANIZATION_ID, None, SECRET_VALUE)
        self.assertEqual(e.exception.error_description, '"name" is necessary')

        with self.assertRaises(BadRequest) as e:
            client.create_secret(ORGANIZATION_ID, SECRET_NAME, None)
        self.assertEqual(e.exception.error_description, '"value" is necessary')

        with self.assertRaises(BadRequest) as e:
            client.create_secret(ORGANIZATION_ID, SECRET_NAME, '')
        self.assertEqual(e.exception.error_description, '"value" is necessary')

    @requests_mock.Mocker()
    def test_update_secret(self, m):
        # update-secret-api mock
        path = '/secret-manager/organizations/{}/secrets/{}'.format(ORGANIZATION_ID, SECRET_ID)
        m.patch(path, json=UPDATED_SECRET)

        # unit test
        client = APIClient()
        ret = client.update_secret(
            ORGANIZATION_ID,
            SECRET_ID,
            description='Updated AWS access key',
            expired_at=UPDATED_EXPIRED_AT,
            integration_service_type=INTEGRATION_SERVICE_TYPE,
            integration_service_ids=INTEGRATION_SERVICE_IDS
        )
        expected_payload = {
            'description': 'Updated AWS access key',
            'expired_at': UPDATED_EXPIRED_AT,
            'integration_service_type': INTEGRATION_SERVICE_TYPE,
            'integration_service_ids': INTEGRATION_SERVICE_IDS
        }

        self.assertDictEqual(m.request_history[0].json(), expected_payload)
        self.assertDictEqual(ret, UPDATED_SECRET)

        # 一部のパラメータだけを指定
        m.reset()
        m.patch(path, json=UPDATED_SECRET)
        ret = client.update_secret(
            ORGANIZATION_ID,
            SECRET_ID,
            description='Updated AWS access key'
        )
        expected_payload = {
            'description': 'Updated AWS access key'
        }
        self.assertDictEqual(m.request_history[0].json(), expected_payload)

    @requests_mock.Mocker()
    def test_delete_secret(self, m):
        # delete-secret-api mock
        path = '/secret-manager/organizations/{}/secrets/{}'.format(ORGANIZATION_ID, SECRET_ID)
        m.delete(path, json=DELETE_SECRET_RESPONSE)

        # unit test
        client = APIClient()
        ret = client.delete_secret(ORGANIZATION_ID, SECRET_ID)
        self.assertDictEqual(ret, DELETE_SECRET_RESPONSE)

        # バリデーションエラーテスト
        with self.assertRaises(BadRequest) as e:
            client.delete_secret(None, SECRET_ID)
        self.assertEqual(e.exception.error_description, '"organization_id" is necessary')

        with self.assertRaises(BadRequest) as e:
            client.delete_secret(ORGANIZATION_ID, None)
        self.assertEqual(e.exception.error_description, '"secret_id" is necessary')
