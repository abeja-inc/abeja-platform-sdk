import os
import unittest
import base64

import requests_mock

from abeja.secret_manager.secret_version.api.client import APIClient
from abeja.exceptions import BadRequest

os.environ['USER_AUTH_ARMS'] = 'False'
ORGANIZATION_ID = '1410000000000'
SECRET_ID = '3053595942757'
VERSION_ID = '1234567890123'
SECRET_VALUE = 'AKIAIOSFODNN7EXAMPLE'
ENCODED_SECRET_VALUE = base64.b64encode(SECRET_VALUE.encode('utf-8')).decode('utf-8')
EXPIRED_AT = '2024-12-15T16:50:33+09:00'
CREATED_AT = '2023-12-15T16:50:33+09:00'

# バージョン情報
SECRET_VERSION = {
    'id': VERSION_ID,
    'secret_id': SECRET_ID,
    'version': 1,
    'status': 'active',
    'expired_at': EXPIRED_AT,
    'created_at': CREATED_AT
}

# 値を含むバージョン情報
SECRET_VERSION_WITH_VALUE = {
    'id': VERSION_ID,
    'secret_id': SECRET_ID,
    'version': 1,
    'status': 'active',
    'value': ENCODED_SECRET_VALUE,
    'expired_at': EXPIRED_AT,
    'created_at': CREATED_AT
}

# バージョン一覧のレスポンス
SECRET_VERSIONS_RESPONSE = {
    'secret_id': SECRET_ID,
    'versions': [
        SECRET_VERSION,
        {
            'id': '9876543210987',
            'secret_id': SECRET_ID,
            'version': 2,
            'status': 'inactive',
            'expired_at': EXPIRED_AT,
            'created_at': CREATED_AT
        }
    ],
    'offset': 0,
    'limit': 50,
    'has_next': False
}

# 値を含むバージョン一覧のレスポンス
SECRET_VERSIONS_WITH_VALUE_RESPONSE = {
    'secret_id': SECRET_ID,
    'versions': [
        SECRET_VERSION_WITH_VALUE,
        {
            'id': '9876543210987',
            'secret_id': SECRET_ID,
            'version': 2,
            'status': 'inactive',
            'value': ENCODED_SECRET_VALUE,
            'expired_at': EXPIRED_AT,
            'created_at': CREATED_AT
        }
    ],
    'offset': 0,
    'limit': 50,
    'has_next': False
}

# 更新後のバージョン情報
UPDATED_SECRET_VERSION = {
    'id': VERSION_ID,
    'secret_id': SECRET_ID,
    'version': 1,
    'status': 'inactive',
    'expired_at': EXPIRED_AT,
    'created_at': CREATED_AT
}


class TestSecretVersionAPIClient(unittest.TestCase):

    @requests_mock.Mocker()
    def test_get_secret_versions(self, m):
        # get-secret-versions-api mock
        path = '/secret-manager/organizations/{}/secrets/{}/versions'.format(ORGANIZATION_ID, SECRET_ID)
        m.get(path, json=SECRET_VERSIONS_RESPONSE)

        # unit test
        client = APIClient()
        ret = client.get_secret_versions(ORGANIZATION_ID, SECRET_ID)
        self.assertDictEqual(ret, SECRET_VERSIONS_RESPONSE)

        # with parameters
        path_with_params = '/secret-manager/organizations/{}/secrets/{}/versions?offset=10&limit=20&return_secret_value=false'.format(
            ORGANIZATION_ID, SECRET_ID)
        m.get(path_with_params, json=SECRET_VERSIONS_RESPONSE)
        ret = client.get_secret_versions(ORGANIZATION_ID, SECRET_ID, offset=10, limit=20, return_secret_value=False)
        self.assertDictEqual(ret, SECRET_VERSIONS_RESPONSE)

        # with return_secret_value
        path_with_secret_value = '/secret-manager/organizations/{}/secrets/{}/versions?offset=0&limit=50&return_secret_value=true'.format(
            ORGANIZATION_ID, SECRET_ID)
        m.get(path_with_secret_value, json=SECRET_VERSIONS_WITH_VALUE_RESPONSE)
        ret = client.get_secret_versions(ORGANIZATION_ID, SECRET_ID, return_secret_value=True)
        # 値がデコードされていることを確認
        self.assertEqual(ret['versions'][0]['value'], SECRET_VALUE)

        # バリデーションエラーテスト
        with self.assertRaises(BadRequest) as e:
            client.get_secret_versions(None, SECRET_ID)
        self.assertEqual(e.exception.error_description, '"organization_id" is necessary')

        with self.assertRaises(BadRequest) as e:
            client.get_secret_versions(ORGANIZATION_ID, None)
        self.assertEqual(e.exception.error_description, '"secret_id" is necessary')

        with self.assertRaises(BadRequest) as e:
            client.get_secret_versions(ORGANIZATION_ID, SECRET_ID, offset=-1)
        self.assertEqual(e.exception.error_description, '"offset" must be greater than or equal to 0')

        with self.assertRaises(BadRequest) as e:
            client.get_secret_versions(ORGANIZATION_ID, SECRET_ID, limit=0)
        self.assertEqual(e.exception.error_description, '"limit" must be between 1 and 100')

        with self.assertRaises(BadRequest) as e:
            client.get_secret_versions(ORGANIZATION_ID, SECRET_ID, limit=101)
        self.assertEqual(e.exception.error_description, '"limit" must be between 1 and 100')

    @requests_mock.Mocker()
    def test_get_secret_version(self, m):
        # get-secret-version-api mock
        path = '/secret-manager/organizations/{}/secrets/{}/versions/{}'.format(ORGANIZATION_ID, SECRET_ID, VERSION_ID)
        m.get(path, json=SECRET_VERSION)

        # unit test
        client = APIClient()
        ret = client.get_secret_version(ORGANIZATION_ID, SECRET_ID, VERSION_ID)
        self.assertDictEqual(ret, SECRET_VERSION)

        # with return_secret_value
        path_with_secret_value = '/secret-manager/organizations/{}/secrets/{}/versions/{}?return_secret_value=true'.format(
            ORGANIZATION_ID, SECRET_ID, VERSION_ID)
        m.get(path_with_secret_value, json=SECRET_VERSION_WITH_VALUE)
        ret = client.get_secret_version(ORGANIZATION_ID, SECRET_ID, VERSION_ID, return_secret_value=True)
        # 値がデコードされていることを確認
        self.assertEqual(ret['value'], SECRET_VALUE)

        # バリデーションエラーテスト
        with self.assertRaises(BadRequest) as e:
            client.get_secret_version(None, SECRET_ID, VERSION_ID)
        self.assertEqual(e.exception.error_description, '"organization_id" is necessary')

        with self.assertRaises(BadRequest) as e:
            client.get_secret_version(ORGANIZATION_ID, None, VERSION_ID)
        self.assertEqual(e.exception.error_description, '"secret_id" is necessary')

        with self.assertRaises(BadRequest) as e:
            client.get_secret_version(ORGANIZATION_ID, SECRET_ID, None)
        self.assertEqual(e.exception.error_description, '"version_id" is necessary')

    @requests_mock.Mocker()
    def test_create_secret_version(self, m):
        # create-secret-version-api mock
        path = '/secret-manager/organizations/{}/secrets/{}/versions'.format(ORGANIZATION_ID, SECRET_ID)
        m.post(path, json=SECRET_VERSION_WITH_VALUE)

        # unit test
        client = APIClient()
        ret = client.create_secret_version(
            ORGANIZATION_ID,
            SECRET_ID,
            SECRET_VALUE
        )
        expected_payload = {
            'value': SECRET_VALUE
        }

        self.assertDictEqual(m.request_history[0].json(), expected_payload)
        self.assertDictEqual(ret, SECRET_VERSION_WITH_VALUE)

        # return_secret_valueがTrueの場合のテスト
        path_with_params = '/secret-manager/organizations/{}/secrets/{}/versions?return_secret_value=true'.format(ORGANIZATION_ID, SECRET_ID)
        m.post(path_with_params, json=SECRET_VERSION_WITH_VALUE)
        ret = client.create_secret_version(
            ORGANIZATION_ID,
            SECRET_ID,
            SECRET_VALUE,
            return_secret_value=True
        )
        # 値がデコードされていることを確認
        self.assertEqual(ret['value'], SECRET_VALUE)

        # バリデーションエラーテスト
        with self.assertRaises(BadRequest) as e:
            client.create_secret_version(None, SECRET_ID, SECRET_VALUE)
        self.assertEqual(e.exception.error_description, '"organization_id" is necessary')

        with self.assertRaises(BadRequest) as e:
            client.create_secret_version(ORGANIZATION_ID, None, SECRET_VALUE)
        self.assertEqual(e.exception.error_description, '"secret_id" is necessary')

        with self.assertRaises(BadRequest) as e:
            client.create_secret_version(ORGANIZATION_ID, SECRET_ID, None)
        self.assertEqual(e.exception.error_description, '"value" is necessary')

        with self.assertRaises(BadRequest) as e:
            client.create_secret_version(ORGANIZATION_ID, SECRET_ID, '')
        self.assertEqual(e.exception.error_description, '"value" is necessary')

    @requests_mock.Mocker()
    def test_update_secret_version(self, m):
        # update-secret-version-api mock
        path = '/secret-manager/organizations/{}/secrets/{}/versions/{}'.format(ORGANIZATION_ID, SECRET_ID, VERSION_ID)
        m.patch(path, json=UPDATED_SECRET_VERSION)

        # unit test
        client = APIClient()
        ret = client.update_secret_version(
            ORGANIZATION_ID,
            SECRET_ID,
            VERSION_ID,
            status='inactive'
        )
        expected_payload = {
            'status': 'inactive'
        }

        self.assertDictEqual(m.request_history[0].json(), expected_payload)
        self.assertDictEqual(ret, UPDATED_SECRET_VERSION)

        # valueを指定した場合のテスト
        m.reset()
        m.patch(path, json=UPDATED_SECRET_VERSION)
        ret = client.update_secret_version(
            ORGANIZATION_ID,
            SECRET_ID,
            VERSION_ID,
            status='inactive',
            value='NEW_SECRET_VALUE'
        )
        expected_payload = {
            'status': 'inactive',
            'value': 'NEW_SECRET_VALUE'
        }
        self.assertDictEqual(m.request_history[0].json(), expected_payload)

        # バリデーションエラーテスト
        with self.assertRaises(BadRequest) as e:
            client.update_secret_version(None, SECRET_ID, VERSION_ID, 'inactive')
        self.assertEqual(e.exception.error_description, '"organization_id" is necessary')

        with self.assertRaises(BadRequest) as e:
            client.update_secret_version(ORGANIZATION_ID, None, VERSION_ID, 'inactive')
        self.assertEqual(e.exception.error_description, '"secret_id" is necessary')

        with self.assertRaises(BadRequest) as e:
            client.update_secret_version(ORGANIZATION_ID, SECRET_ID, None, 'inactive')
        self.assertEqual(e.exception.error_description, '"version_id" is necessary')

        with self.assertRaises(BadRequest) as e:
            client.update_secret_version(ORGANIZATION_ID, SECRET_ID, VERSION_ID, None)
        self.assertEqual(e.exception.error_description, '"status" is necessary')

        with self.assertRaises(BadRequest) as e:
            client.update_secret_version(ORGANIZATION_ID, SECRET_ID, VERSION_ID, 'invalid_status')
        self.assertEqual(e.exception.error_description, '"status" need to be "active" or "inactive"')

        with self.assertRaises(BadRequest) as e:
            client.update_secret_version(ORGANIZATION_ID, SECRET_ID, VERSION_ID, 'inactive', value='')
        self.assertEqual(e.exception.error_description, '"value" is necessary')

    @requests_mock.Mocker()
    def test_delete_secret_version(self, m):
        # delete-secret-version-api mock
        path = '/secret-manager/organizations/{}/secrets/{}/versions/{}'.format(ORGANIZATION_ID, SECRET_ID, VERSION_ID)
        m.delete(path, json=SECRET_VERSION)

        # unit test
        client = APIClient()
        ret = client.delete_secret_version(ORGANIZATION_ID, SECRET_ID, VERSION_ID)
        self.assertDictEqual(ret, SECRET_VERSION)

        # バリデーションエラーテスト
        with self.assertRaises(BadRequest) as e:
            client.delete_secret_version(None, SECRET_ID, VERSION_ID)
        self.assertEqual(e.exception.error_description, '"organization_id" is necessary')

        with self.assertRaises(BadRequest) as e:
            client.delete_secret_version(ORGANIZATION_ID, None, VERSION_ID)
        self.assertEqual(e.exception.error_description, '"secret_id" is necessary')

        with self.assertRaises(BadRequest) as e:
            client.delete_secret_version(ORGANIZATION_ID, SECRET_ID, None)
        self.assertEqual(e.exception.error_description, '"version_id" is necessary')
