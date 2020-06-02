from io import BytesIO
import pytest
from unittest import TestCase
from unittest.mock import patch

import requests_mock

from abeja import VERSION
from abeja.common.connection import Connection
from abeja.datalake.api.client import APIClient
from abeja.exceptions import BadRequest


ORGANIZATION_ID = '1234567890123'
CHANNEL_ID = '1230000000000'
CHANNEL_NAME = 'dummy_channel'
CHANNEL_DESCRIPTION = 'dummy_channel_description'
STORAGE_TYPE = 'datalake'
DATASOURCE_ID = '1230000000001'
CONTENT_TYPE = 'image/jpeg'
METADATA = {
    'x-abeja-meta-filename': '日本語',
    'x-abeja-meta-テスト': 'テスト１'
}
ENCODED_METADATA = {
    'x-abeja-meta-filename': '%E6%97%A5%E6%9C%AC%E8%AA%9E',
    'x-abeja-meta-%E3%83%86%E3%82%B9%E3%83%88': '%E3%83%86%E3%82%B9%E3%83%88%EF%BC%91'
}
LIFETIME = '1day'
CONFLICT_TARGET = 'filename'
FILE_ID = '20180510T110208-193d0d17-f0b1-4549-96df-651c02ccb8c9'
API_BASE_URL = 'http://localhost:8080'
BUCKET_ID = '1240000000000'
BUCKET_NAME = 'dummy_bucket'
BUCKET_DESCRIPTION = 'dummy_bucket_description'
BUCKET_FILE_ID = 'aaa/bbb'


class TestClient:
    def test_archive_channel(self, requests_mock):
        path = '/organizations/{}/channels/{}/archive'.format(
            ORGANIZATION_ID, CHANNEL_ID)
        requests_mock.post(path, json={})

        client = APIClient()
        client.archive_channel(ORGANIZATION_ID, CHANNEL_ID)

    def test_unarchive_channel(self, requests_mock):
        path = '/organizations/{}/channels/{}/unarchive'.format(
            ORGANIZATION_ID, CHANNEL_ID)
        requests_mock.post(path, json={})

        client = APIClient()
        client.unarchive_channel(ORGANIZATION_ID, CHANNEL_ID)

    def test_archive_bucket(self, requests_mock):
        path = '/organizations/{}/buckets/{}/archive'.format(
            ORGANIZATION_ID, BUCKET_ID)
        requests_mock.post(path, json={})

        client = APIClient()
        client.archive_bucket(ORGANIZATION_ID, BUCKET_ID)

    def test_unarchive_bucket(self, requests_mock):
        path = '/organizations/{}/buckets/{}/unarchive'.format(
            ORGANIZATION_ID, BUCKET_ID)
        requests_mock.post(path, json={})

        client = APIClient()
        client.unarchive_bucket(ORGANIZATION_ID, BUCKET_ID)


class TestApiClient(TestCase):
    def setUp(self):
        Connection.BASE_URL = API_BASE_URL
        self.api_client = APIClient()

    @patch('requests.Session.request')
    def test_create_channel(self, m):
        self.api_client.create_channel(
            ORGANIZATION_ID, CHANNEL_NAME, CHANNEL_DESCRIPTION, STORAGE_TYPE)
        url = '{}/organizations/{}/channels'.format(
            API_BASE_URL, ORGANIZATION_ID)
        params = {
            'name': CHANNEL_NAME,
            'description': CHANNEL_DESCRIPTION,
            'storage_type': STORAGE_TYPE
        }
        m.assert_called_once_with(
            'POST',
            url,
            params=None,
            headers={
                'User-Agent': 'abeja-platform-sdk/{}'.format(VERSION)},
            timeout=30,
            data=None,
            json=params)

    @patch('requests.Session.request')
    def test_list_channels(self, m):
        self.api_client.list_channels(ORGANIZATION_ID)
        url = '{}/organizations/{}/channels'.format(
            API_BASE_URL, ORGANIZATION_ID)
        m.assert_called_once_with(
            'GET',
            url,
            params={},
            headers={
                'User-Agent': 'abeja-platform-sdk/{}'.format(VERSION)},
            timeout=30,
            data=None,
            json=None)

    @patch('requests.Session.request')
    def test_list_channels_filter_archived_true(self, m):
        self.api_client.list_channels(ORGANIZATION_ID, filter_archived=True)
        url = '{}/organizations/{}/channels'.format(
            API_BASE_URL, ORGANIZATION_ID)
        expected_params = {
            'filter_archived': 'exclude_archived'
        }
        m.assert_called_once_with(
            'GET',
            url,
            params=expected_params,
            headers={
                'User-Agent': 'abeja-platform-sdk/{}'.format(VERSION)},
            timeout=30,
            data=None,
            json=None)

    @patch('requests.Session.request')
    def test_list_channels_filter_archived_false(self, m):
        self.api_client.list_channels(ORGANIZATION_ID, filter_archived=False)
        url = '{}/organizations/{}/channels'.format(
            API_BASE_URL, ORGANIZATION_ID)
        expected_params = {
            'filter_archived': 'include_archived'
        }
        m.assert_called_once_with(
            'GET',
            url,
            params=expected_params,
            headers={
                'User-Agent': 'abeja-platform-sdk/{}'.format(VERSION)},
            timeout=30,
            data=None,
            json=None)

    @patch('requests.Session.request')
    def test_get_channel(self, m):
        self.api_client.get_channel(ORGANIZATION_ID, CHANNEL_ID)
        url = '{}/organizations/{}/channels/{}'.format(
            API_BASE_URL, ORGANIZATION_ID, CHANNEL_ID)
        m.assert_called_once_with(
            'GET',
            url,
            params=None,
            headers={
                'User-Agent': 'abeja-platform-sdk/{}'.format(VERSION)},
            timeout=30,
            data=None,
            json=None)

    @patch('requests.Session.request')
    def test_patch_channel(self, m):
        self.api_client.patch_channel(
            ORGANIZATION_ID, CHANNEL_ID, CHANNEL_NAME, CHANNEL_DESCRIPTION)
        url = '{}/organizations/{}/channels/{}'.format(
            API_BASE_URL, ORGANIZATION_ID, CHANNEL_ID)
        params = {
            'name': CHANNEL_NAME,
            'description': CHANNEL_DESCRIPTION
        }
        m.assert_called_once_with(
            'PATCH',
            url,
            params=None,
            headers={
                'User-Agent': 'abeja-platform-sdk/{}'.format(VERSION)},
            timeout=30,
            data=None,
            json=params)

    @patch('requests.Session.request')
    def test_put_channel_datasource(self, m):
        self.api_client.put_channel_datasource(
            ORGANIZATION_ID, CHANNEL_ID, DATASOURCE_ID)
        url = '{}/organizations/{}/channels/{}/datasources/{}'.format(
            API_BASE_URL, ORGANIZATION_ID, CHANNEL_ID, DATASOURCE_ID)
        m.assert_called_once_with(
            'PUT',
            url,
            params=None,
            headers={
                'User-Agent': 'abeja-platform-sdk/{}'.format(VERSION)},
            timeout=30,
            data=None,
            json=None)

    @patch('requests.Session.request')
    def test_list_channel_datasources(self, m):
        self.api_client.list_channel_datasources(ORGANIZATION_ID, CHANNEL_ID)
        url = '{}/organizations/{}/channels/{}/datasources'.format(
            API_BASE_URL, ORGANIZATION_ID, CHANNEL_ID)
        m.assert_called_once_with(
            'GET',
            url,
            params=None,
            headers={
                'User-Agent': 'abeja-platform-sdk/{}'.format(VERSION)},
            timeout=30,
            data=None,
            json=None)

    @patch('requests.Session.request')
    def test_delete_channel_datasource(self, m):
        self.api_client.delete_channel_datasource(
            ORGANIZATION_ID, CHANNEL_ID, DATASOURCE_ID)
        url = '{}/organizations/{}/channels/{}/datasources/{}'.format(
            API_BASE_URL, ORGANIZATION_ID, CHANNEL_ID, DATASOURCE_ID)
        m.assert_called_once_with(
            'DELETE',
            url,
            params=None,
            headers={
                'User-Agent': 'abeja-platform-sdk/{}'.format(VERSION)},
            timeout=30,
            data=None,
            json=None)

    @requests_mock.Mocker()
    def test_get_channel_file_upload(self, m):
        path = '/channels/{}'.format(CHANNEL_ID)
        m.post(path, json={
            "uploaded_at": "2019-09-17T07:43:51Z",
            "metadata": {
                "x-abeja-sys-meta-organizationid": ORGANIZATION_ID,
                **ENCODED_METADATA
            },
            "file_id": FILE_ID,
            "content_type": CONTENT_TYPE
        })

        api_client = APIClient()
        res = api_client.get_channel_file_upload(
            CHANNEL_ID, CONTENT_TYPE, METADATA)

        req = m.request_history[0]
        assert req.method == 'POST'
        assert ENCODED_METADATA.items() < req.headers.items()
        assert req.headers['Content-Type'] == CONTENT_TYPE

        assert METADATA.items() < res['metadata'].items()

    @patch('requests.Session.request')
    def test_get_channel_file_upload_with_japanese_metadata(self, m):
        metadata = {
            'x-abeja-meta-filename': '日本語',
            'x-abeja-meta-テスト': 'テスト１'
        }
        self.api_client.get_channel_file_upload(
            CHANNEL_ID, CONTENT_TYPE, metadata)
        url = '{}/channels/{}'.format(
            API_BASE_URL, CHANNEL_ID)
        expected_headers = {
            'Content-Type': CONTENT_TYPE,
            'User-Agent': 'abeja-platform-sdk/{}'.format(VERSION),
            'x-abeja-meta-filename': '%E6%97%A5%E6%9C%AC%E8%AA%9E',
            'x-abeja-meta-%E3%83%86%E3%82%B9%E3%83%88': '%E3%83%86%E3%82%B9%E3%83%88%EF%BC%91'}
        m.assert_called_once_with('POST', url, params=None,
                                  headers=expected_headers,
                                  timeout=30, data=None, json=None)

    @requests_mock.Mocker()
    def test_post_channel_file_upload(self, m):
        path = '/channels/{}/upload'.format(CHANNEL_ID)
        m.post(path, json={
            "uploaded_at": "2019-09-17T07:43:51Z",
            "metadata": {
                "x-abeja-sys-meta-organizationid": ORGANIZATION_ID,
                **ENCODED_METADATA
            },
            "lifetime": LIFETIME,
            "file_id": FILE_ID,
            "content_type": CONTENT_TYPE
        })

        api_client = APIClient()
        res = api_client.post_channel_file_upload(
            CHANNEL_ID, BytesIO('test data'.encode('utf-8')), CONTENT_TYPE,
            metadata=METADATA, lifetime=LIFETIME, conflict_target=CONFLICT_TARGET)

        req = m.request_history[0]
        assert req.method == 'POST'
        assert ENCODED_METADATA.items() < req.headers.items()
        assert req.headers['Content-Type'] == CONTENT_TYPE
        assert req.query == 'lifetime={}&conflict_target={}'.format(LIFETIME, CONFLICT_TARGET)

        assert METADATA.items() < res['metadata'].items()

    @requests_mock.Mocker()
    def test_list_channel_files(self, m):
        path = '/channels/{}'.format(CHANNEL_ID)
        m.get(path, json={
            'files': [
                {
                    "uploaded_at": "2019-09-17T07:43:51Z",
                    "metadata": {
                        "x-abeja-sys-meta-organizationid": ORGANIZATION_ID,
                        **ENCODED_METADATA
                    },
                    "lifetime": LIFETIME,
                    "file_id": FILE_ID,
                    "content_type": CONTENT_TYPE
                }
            ]
        })

        api_client = APIClient()
        res = api_client.list_channel_files(CHANNEL_ID)

        req = m.request_history[0]
        assert req.method == 'GET'

        file = res['files'][0]
        assert METADATA.items() < file['metadata'].items()

    @patch('requests.Session.request')
    def test_list_channel_files_with_sort(self, m):
        self.api_client.list_channel_files(CHANNEL_ID, sort='-uploaded_at')
        url = '{}/channels/{}'.format(API_BASE_URL, CHANNEL_ID)
        m.assert_called_once_with(
            'GET',
            url,
            headers={
                'User-Agent': 'abeja-platform-sdk/{}'.format(VERSION)},
            timeout=30,
            data=None,
            json=None,
            params={
                'sort': '-uploaded_at'})

    @requests_mock.Mocker()
    def test_get_channel_file_download(self, m):
        path = '/channels/{}/{}'.format(CHANNEL_ID, FILE_ID)
        m.get(path, json={
            "url_expires_on": "2019-09-17T09:49:14+00:00",
            "uploaded_at": "2019-09-17T07:43:51+00:00",
            "metadata": {
                "x-abeja-sys-meta-organizationid": ORGANIZATION_ID,
                **ENCODED_METADATA
            },
            "file_id": FILE_ID,
            "download_uri": "xxxxx",
            "content_type": CONTENT_TYPE
        })

        api_client = APIClient()
        res = api_client.get_channel_file_download(CHANNEL_ID, FILE_ID)

        req = m.request_history[0]
        assert req.method == 'GET'

        assert METADATA.items() < res['metadata'].items()

    @patch('requests.Session.request')
    def test_delete_channel_file(self, m):
        self.api_client.delete_channel_file(CHANNEL_ID, FILE_ID)
        url = '{}/channels/{}/{}'.format(API_BASE_URL, CHANNEL_ID, FILE_ID)
        m.assert_called_once_with(
            'DELETE',
            url,
            params=None,
            headers={
                'User-Agent': 'abeja-platform-sdk/{}'.format(VERSION)},
            timeout=30,
            data=None,
            json=None)

    @requests_mock.Mocker()
    def test_put_channel_file_metadata(self, m):
        path = '/channels/{}/{}/metadata'.format(CHANNEL_ID, FILE_ID)
        m.put(path, json={
            "uploaded_at": "2019-09-17T07:43:51+00:00",
            "metadata": {
                "x-abeja-sys-meta-organizationid": ORGANIZATION_ID,
                **ENCODED_METADATA
            },
            "file_id": FILE_ID,
            "content_type": CONTENT_TYPE
        })

        api_client = APIClient()
        res = api_client.put_channel_file_metadata(
            CHANNEL_ID, FILE_ID, METADATA)

        req = m.request_history[0]
        assert req.method == 'PUT'
        assert ENCODED_METADATA == req.json()

        assert METADATA.items() < res['metadata'].items()

    @patch('requests.Session.request')
    def test_put_channel_file_lifetime(self, m):
        self.api_client.put_channel_file_lifetime(
            CHANNEL_ID, FILE_ID, LIFETIME)
        url = '{}/channels/{}/{}/lifetime'.format(
            API_BASE_URL, CHANNEL_ID, FILE_ID)
        expected_json = {'lifetime': LIFETIME}
        m.assert_called_once_with(
            'PUT',
            url,
            params=None,
            headers={
                'User-Agent': 'abeja-platform-sdk/{}'.format(VERSION)},
            timeout=30,
            data=None,
            json=expected_json)

    @patch('requests.Session.request')
    def test_create_bucket(self, m):
        self.api_client.create_bucket(
            ORGANIZATION_ID, BUCKET_NAME, BUCKET_DESCRIPTION)
        url = '{}/organizations/{}/buckets'.format(
            API_BASE_URL, ORGANIZATION_ID)
        params = {
            'name': BUCKET_NAME,
            'description': BUCKET_DESCRIPTION
        }
        m.assert_called_once_with(
            'POST',
            url,
            params=None,
            headers={
                'User-Agent': 'abeja-platform-sdk/{}'.format(VERSION)},
            timeout=30,
            data=None,
            json=params)

    @patch('requests.Session.request')
    def test_list_buckets(self, m):
        self.api_client.list_buckets(ORGANIZATION_ID)
        url = '{}/organizations/{}/buckets'.format(
            API_BASE_URL, ORGANIZATION_ID)
        m.assert_called_once_with(
            'GET',
            url,
            params={},
            headers={
                'User-Agent': 'abeja-platform-sdk/{}'.format(VERSION)},
            timeout=30,
            data=None,
            json=None)

    @patch('requests.Session.request')
    def test_get_bucket(self, m):
        self.api_client.get_bucket(ORGANIZATION_ID, BUCKET_ID)
        url = '{}/organizations/{}/buckets/{}'.format(
            API_BASE_URL, ORGANIZATION_ID, BUCKET_ID)
        m.assert_called_once_with(
            'GET',
            url,
            params=None,
            headers={
                'User-Agent': 'abeja-platform-sdk/{}'.format(VERSION)},
            timeout=30,
            data=None,
            json=None)

    @patch('requests.Session.request')
    def test_patch_bucket(self, m):
        self.api_client.patch_bucket(
            ORGANIZATION_ID, BUCKET_ID, BUCKET_NAME, BUCKET_DESCRIPTION)
        url = '{}/organizations/{}/buckets/{}'.format(
            API_BASE_URL, ORGANIZATION_ID, BUCKET_ID)
        params = {
            'name': BUCKET_NAME,
            'description': BUCKET_DESCRIPTION
        }
        m.assert_called_once_with(
            'PATCH',
            url,
            params=None,
            headers={
                'User-Agent': 'abeja-platform-sdk/{}'.format(VERSION)},
            timeout=30,
            data=None,
            json=params)

    @requests_mock.Mocker()
    def test_upload_bucket_file(self, m):
        path = '{}/organizations/{}/buckets/{}/files'.format(
            API_BASE_URL, ORGANIZATION_ID, BUCKET_ID)
        m.post(path, json={
            "uploaded_at": "2019-09-17T07:43:51Z",
            "metadata": {
                "x-abeja-sys-meta-organizationid": ORGANIZATION_ID,
                **ENCODED_METADATA
            },
            "lifetime": LIFETIME,
            "file_id": FILE_ID,
            "content_type": CONTENT_TYPE
        })

        api_client = APIClient()
        filepath = 'tests/dummydata/dummy1.txt'
        res = api_client.upload_bucket_file(
            ORGANIZATION_ID, BUCKET_ID, open(filepath), filepath, CONTENT_TYPE,
            metadata=METADATA, lifetime=LIFETIME)

        req = m.request_history[0]
        assert req.method == 'POST'
        assert ENCODED_METADATA.items() < req.headers.items()
        # assert req.headers['Content-Type'] == CONTENT_TYPE
        # assert req.query == 'lifetime={}'.format(LIFETIME)

        assert METADATA.items() < res['metadata'].items()

        with pytest.raises(BadRequest):
            api_client.upload_bucket_file(
                ORGANIZATION_ID,
                BUCKET_ID,
                open(filepath),
                '/dummy',
                CONTENT_TYPE,
                metadata=METADATA,
                lifetime=LIFETIME)

        with pytest.raises(BadRequest):
            api_client.upload_bucket_file(
                ORGANIZATION_ID,
                BUCKET_ID,
                open(filepath),
                'dummy/../hoge.data',
                CONTENT_TYPE,
                metadata=METADATA,
                lifetime=LIFETIME)

    @requests_mock.Mocker()
    def test_upload_bucket_files(self, m):
        path = '{}/organizations/{}/buckets/{}/files'.format(
            API_BASE_URL, ORGANIZATION_ID, BUCKET_ID)
        m.post(path, json={
            "uploaded_at": "2019-09-17T07:43:51Z",
            "metadata": {
                "x-abeja-sys-meta-organizationid": ORGANIZATION_ID,
                **ENCODED_METADATA
            },
            "lifetime": LIFETIME,
            "file_id": FILE_ID,
            "content_type": CONTENT_TYPE
        })

        api_client = APIClient()
        res = api_client.upload_bucket_files(
            ORGANIZATION_ID, BUCKET_ID, 'tests/dummydata', lifetime=LIFETIME)
        assert res["status"]

        req = m.request_history[0]
        assert req.method == 'POST'
        # assert req.query == 'lifetime={}'.format(LIFETIME)

    @requests_mock.Mocker()
    def test_list_bucket_files(self, m):
        path = '{}/organizations/{}/buckets/{}/files'.format(
            API_BASE_URL, ORGANIZATION_ID, BUCKET_ID)
        m.get(path, json={
            'files': [
                {
                    "size": 4,
                    "etag": "xxx",
                    "is_file": True,
                    "last_modified": "2019-09-17T07:43:51Z",
                    "uploaded_at": "2019-09-17T07:43:51Z",
                    "url_expires_on": "2019-09-17T07:43:51Z",
                    "download_uri": "...",
                    "metadata": {
                        "x-abeja-sys-meta-organizationid": ORGANIZATION_ID,
                        **ENCODED_METADATA
                    },
                    "file_id": FILE_ID,
                }
            ]
        })

        api_client = APIClient()
        res = api_client.list_bucket_files(ORGANIZATION_ID, BUCKET_ID)

        req = m.request_history[0]
        assert req.method == 'GET'

        file = res['files'][0]
        assert METADATA.items() < file['metadata'].items()

    @requests_mock.Mocker()
    def test_get_bucket_file(self, m):
        path = '{}/organizations/{}/buckets/{}/files/{}'.format(
            API_BASE_URL, ORGANIZATION_ID, BUCKET_ID, BUCKET_FILE_ID)
        m.get(path, json={
            "size": 4,
            "etag": "xxx",
            "is_file": True,
            "last_modified": "2019-09-17T07:43:51Z",
            "uploaded_at": "2019-09-17T07:43:51Z",
            "url_expires_on": "2019-09-17T07:43:51Z",
            "download_uri": "...",
            "metadata": {
                "x-abeja-sys-meta-organizationid": ORGANIZATION_ID,
                **ENCODED_METADATA
            },
            "file_id": BUCKET_FILE_ID,
        })

        api_client = APIClient()
        res = api_client.get_bucket_file(
            ORGANIZATION_ID, BUCKET_ID, BUCKET_FILE_ID)

        req = m.request_history[0]
        assert req.method == 'GET'
        assert BUCKET_FILE_ID == res['file_id']
