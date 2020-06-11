import json
import os
import shutil
import unittest
from unittest.mock import patch, create_autospec

import requests
from mock import MagicMock

from abeja.exceptions import HttpError
from abeja.datalake.file import (
    FileMixin,
    FileIterator,
    DatalakeFile
)
from abeja.exceptions import BadRequest

TEST_MOUNT_DIR = 'tests/datasets/tmp'

ORGANIZATION_ID = '1234567890123'
CHANNEL_ID = '1230000000000'


class TestFileMixin(unittest.TestCase):
    def test_init(self):
        class AFile(FileMixin):
            pass
        uri = 'datalake://1234567890123/20171128T113546-9fa120a3-96bc-4b84-b56b-1bc2273178a1'
        type = 'image/jpeg'
        height = 500,
        width = 200
        a_file = AFile(None, uri, type, height=height, width=width)
        self.assertEqual(a_file.uri, uri)
        self.assertEqual(a_file.type, type)
        self.assertEqual(a_file.height, height)
        self.assertEqual(a_file.width, width)


class TestFileIterator(unittest.TestCase):
    def test_next(self):
        mock_api = MagicMock()
        mock_api.list_channel_files.side_effect = [
            {
                'next_page_token': 'dummy1',
                'files': [
                    {'file_id': 'file_id_1'},
                    {'file_id': 'file_id_2'},
                    {'file_id': 'file_id_3'}
                ]
            },
            {
                'next_page_token': 'dummy2',
                'files': [
                    {'file_id': 'file_id_4'},
                    {'file_id': 'file_id_5'},
                    {'file_id': 'file_id_6'}
                ]
            },
            {
                'next_page_token': None,
                'files': [
                    {'file_id': 'file_id_7'},
                    {'file_id': 'file_id_8'},
                    {'file_id': 'file_id_9'}
                ]
            }
        ]
        iterator = FileIterator(
            mock_api,
            organization_id=ORGANIZATION_ID,
            channel_id=CHANNEL_ID)
        file_1 = next(iterator)
        self.assertEqual(file_1.file_id, 'file_id_1')
        file_2 = next(iterator)
        self.assertEqual(file_2.file_id, 'file_id_2')
        self.assertEqual(len(list(iterator)), 7)

    def test_next_raise_stop_iteration(self):
        mock_api = MagicMock()
        mock_api.list_channel_files.side_effect = [
            {
                'next_page_token': 'dummy',
                'files': [
                    {'file_id': 'file_id_1'},
                    {'file_id': 'file_id_2'},
                    {'file_id': 'file_id_3'}
                ]
            },
            {
                'next_page_token': None,
                'files': [
                    {'file_id': 'file_id_4'},
                    {'file_id': 'file_id_5'}
                ]
            }
        ]
        iterator = FileIterator(
            mock_api,
            organization_id=ORGANIZATION_ID,
            channel_id=CHANNEL_ID)
        for i in range(5):
            next(iterator)
        with self.assertRaises(StopIteration):
            next(iterator)
        self.assertEqual(mock_api.list_channel_files.call_count, 2)

    def test_next_up_to_next_page_and_iter_1(self):
        mock_api = MagicMock()
        mock_api.list_channel_files.side_effect = [
            {
                'next_page_token': 'dummy',
                'files': [
                    {'file_id': 'file_id_1'},
                    {'file_id': 'file_id_2'},
                    {'file_id': 'file_id_3'}
                ]
            },
            {
                'next_page_token': None,
                'files': [
                    {'file_id': 'file_id_4'},
                    {'file_id': 'file_id_5'}
                ]
            }
        ]
        iterator = FileIterator(
            mock_api,
            organization_id=ORGANIZATION_ID,
            channel_id=CHANNEL_ID)
        file_1 = next(iterator)
        self.assertEqual(file_1.file_id, 'file_id_1')
        file_2 = next(iterator)
        self.assertEqual(file_2.file_id, 'file_id_2')
        file_3 = next(iterator)
        self.assertEqual(file_3.file_id, 'file_id_3')

        mock_api.list_channel_files.assert_called_with(CHANNEL_ID)
        file_4 = next(iterator)
        self.assertEqual(file_4.file_id, 'file_id_4')
        self.assertEqual(len(list(iterator)), 1)
        mock_api.list_channel_files.assert_called_with(
            CHANNEL_ID, next_page_token='dummy')
        self.assertEqual(mock_api.list_channel_files.call_count, 2)

    def test_next_up_to_next_page_and_iter_2(self):
        mock_api = MagicMock()
        mock_api.list_channel_files.side_effect = [
            {
                'next_page_token': 'dummy',
                'files': [
                    {'file_id': 'file_id_1'},
                    {'file_id': 'file_id_2'},
                    {'file_id': 'file_id_3'}
                ]
            },
            {
                'next_page_token': None,
                'files': [
                    {'file_id': 'file_id_4'},
                    {'file_id': 'file_id_5'}
                ]
            }
        ]
        iterator = FileIterator(
            mock_api,
            organization_id=ORGANIZATION_ID,
            channel_id=CHANNEL_ID)
        file_1 = next(iterator)
        self.assertEqual(file_1.file_id, 'file_id_1')
        file_2 = next(iterator)
        self.assertEqual(file_2.file_id, 'file_id_2')
        file_3 = next(iterator)
        self.assertEqual(file_3.file_id, 'file_id_3')
        mock_api.list_channel_files.assert_called_with(CHANNEL_ID)

        self.assertEqual(len(list(iterator)), 2)
        self.assertEqual(mock_api.list_channel_files.call_count, 2)
        mock_api.list_channel_files.assert_called_with(
            CHANNEL_ID, next_page_token='dummy')

    def test_next_file_item_contains_channel_id(self):
        mock_api = MagicMock()
        mock_api.list_channel_files.side_effect = [
            {
                'next_page_token': None,
                'files': [
                    {'file_id': 'file_id_1', 'channel_id': '1234567890123'}
                ]
            }
        ]
        iterator = FileIterator(
            mock_api,
            organization_id=ORGANIZATION_ID,
            channel_id=CHANNEL_ID)
        file_1 = next(iterator)
        self.assertEqual(file_1.file_id, 'file_id_1')

    def test_page(self):
        mock_api = MagicMock()
        mock_api.list_channel_files.return_value = {
            'next_page_token': 'dummy',
            'files': [
                {
                    'url_expires_on': '2018-06-04T05:04:46+00:00',
                    'uploaded_at': '2018-06-01T05:22:44+00:00',
                    'metadata': {
                        'x-abeja-meta-filename': 'DcZzLGkV4AA8FQc.jpg'},
                    'file_id': '20180601T052244-250482c0-d361-4c5b-a0f9-e796af1a5f0d',
                    'download_uri': 'https://example.com/dummy_download_uri',
                    'content_type': 'image/jpeg'}]}
        iterator = FileIterator(
            mock_api,
            organization_id=ORGANIZATION_ID,
            channel_id=CHANNEL_ID)
        files = iterator._page()

        mock_api.list_channel_files.assert_called_once_with(CHANNEL_ID)

        self.assertIsInstance(files[0], DatalakeFile)

    def test_page_iter(self):
        mock_api = MagicMock()
        mock_api.list_channel_files.side_effect = [{'next_page_token': 'dummy',
                                                    'files': [{'url_expires_on': '2018-06-04T05:04:46+00:00',
                                                               'uploaded_at': '2018-06-01T05:22:44+00:00',
                                                               'metadata': {'x-abeja-meta-filename': 'DcZzLGkV4AA8FQc.jpg'},
                                                               'file_id': '20180601T052244-250482c0-d361-4c5b-a0f9-e796af1a5f0d',
                                                               'download_uri': 'http://example/dummy/donwload_url',
                                                               'content_type': 'image/jpeg'}]},
                                                   {'next_page_token': None,
                                                    'files': [{'url_expires_on': '2018-06-04T05:04:46+00:00',
                                                               'uploaded_at': '2018-06-01T05:22:44+00:00',
                                                               'metadata': {'x-abeja-meta-filename': 'DcZzLGkV4AA8FQc.jpg'},
                                                               'file_id': '20180601T052244-250482c0-d361-4c5b-a0f9-e796af1a5f0d',
                                                               'download_uri': 'http://example/dummy/donwload_url',
                                                               'content_type': 'image/jpeg'}]},
                                                   {'next_page_token': None,
                                                    'files': []}]
        iterator = FileIterator(
            mock_api,
            organization_id=ORGANIZATION_ID,
            channel_id=CHANNEL_ID)
        file_pages = [file for file in iterator._page_iter()]

        self.assertEqual(mock_api.list_channel_files.call_count, 2)
        for file_page in file_pages:
            for file in file_page:
                self.assertIsInstance(file, DatalakeFile)

    def test_page_return_partial(self):
        mock_api = MagicMock()
        mock_api.list_channel_files.return_value = {
            'next_page_token': 'dummy',
            'files': [
                {'file_id': 'file_id_1'},
                {'file_id': 'file_id_2'}
            ]
        }
        iterator = FileIterator(
            mock_api,
            organization_id=ORGANIZATION_ID,
            channel_id=CHANNEL_ID)
        file = next(iterator)
        self.assertEqual(file.file_id, 'file_id_1')
        page = iterator._page()
        self.assertEqual(len(page), 1)
        self.assertEqual(page[0].file_id, 'file_id_2')

    def test_page_with_start_and_end(self):
        mock_api = MagicMock()
        mock_api.list_channel_files.side_effect = [
            {
                'next_page_token': 'dummy',
                'files': [
                    {'file_id': 'file_id_1'},
                    {'file_id': 'file_id_2'},
                    {'file_id': 'file_id_3'}
                ]
            },
            {
                'next_page_token': None,
                'files': [
                    {'file_id': 'file_id_4'},
                    {'file_id': 'file_id_5'}
                ]
            }
        ]
        iterator = FileIterator(
            mock_api, organization_id=ORGANIZATION_ID, channel_id=CHANNEL_ID,
            start='20190308', end='20190308')
        # call `_page` method
        list(iterator)

        self.assertEqual(mock_api.list_channel_files.call_count, 2)
        # kwargs
        self.assertDictEqual(
            mock_api.list_channel_files.call_args_list[0][1],
            {'start': '20190308', 'end': '20190308'})
        self.assertDictEqual(
            mock_api.list_channel_files.call_args_list[1][1],
            {'next_page_token': 'dummy'})

    def test_page_with_sort(self):
        mock_api = MagicMock()
        mock_api.list_channel_files.side_effect = [
            {
                'next_page_token': 'dummy',
                'files': [
                    {'file_id': 'file_id_1'},
                    {'file_id': 'file_id_2'},
                    {'file_id': 'file_id_3'}
                ]
            },
            {
                'next_page_token': None,
                'files': [
                    {'file_id': 'file_id_4'},
                    {'file_id': 'file_id_5'}
                ]
            }
        ]
        iterator = FileIterator(
            mock_api, organization_id=ORGANIZATION_ID, channel_id=CHANNEL_ID,
            sort='-uploaded_at')
        # call `_page` method
        list(iterator)

        self.assertEqual(mock_api.list_channel_files.call_count, 2)
        # kwargs
        self.assertDictEqual(
            mock_api.list_channel_files.call_args_list[0][1],
            {'sort': '-uploaded_at'})
        self.assertDictEqual(
            mock_api.list_channel_files.call_args_list[1][1],
            {'next_page_token': 'dummy'})


class TestDatalakeFile(unittest.TestCase):
    def setUp(self):
        self.channel_id = '1234567890123'
        self.file_id = '20171128T113546-9fa120a3-96bc-4b84-b56b-1bc2273178a1'
        self.uri = 'datalake://{}/{}'.format(self.channel_id, self.file_id)
        self.type = 'image/jpeg'
        self.binary_data = b'test binary'
        self.text_data = 'test text'
        self.json_data = {'test': 'json'}
        self.file_info = {
            "url_expires_on": "2017-12-20T17:08:26+00:00",
            "uploaded_at": "2017-12-18T05:39:47+00:00",
            "metadata": {
                "x-abeja-meta-filename": "test.jpg"
            },
            "file_id": "20171218T053947-821bd0a3-3992-4320-bc1c-1ee8d0a0ad6b",
            "download_uri": "...",
            "content_type": "image/jpeg"
        }
        if os.path.exists(TEST_MOUNT_DIR):
            shutil.rmtree(TEST_MOUNT_DIR)

    def tearDown(self):
        if os.path.exists(TEST_MOUNT_DIR):
            shutil.rmtree(TEST_MOUNT_DIR)

    def _build_content_response(self):
        res = requests.models.Response()
        res._content = self.binary_data
        return res

    def _build_text_response(self):
        res = requests.models.Response()
        res._content = self.text_data.encode('utf-8')
        return res

    def _build_json_response(self):
        res = requests.models.Response()
        data = json.dumps(self.json_data)
        res._content = data.encode('utf-8')
        return res

    @patch('abeja.common.local_file.MOUNT_DIR', TEST_MOUNT_DIR)
    def test_init(self):
        datalake_file = DatalakeFile(None, uri=self.uri, type=type)
        self.assertEqual(datalake_file.uri, self.uri)
        self.assertEqual(datalake_file.type, type)
        self.assertEqual(datalake_file.channel_id, self.channel_id)
        self.assertEqual(datalake_file.file_id, self.file_id)

    def test_lifetime(self):
        datalake_file = DatalakeFile(None, uri=self.uri, type=type)
        datalake_file.lifetime = None

    def test_lifetime_1month(self):
        datalake_file = DatalakeFile(None, uri=self.uri, type=type)
        datalake_file.lifetime = '1month'

    def test_lifetime_invalid(self):
        with self.assertRaises(RuntimeError):
            DatalakeFile(None, uri=self.uri, type=type, lifetime='invalid')

    def test_lifetime_cannot_update_with_none(self):
        datalake_file = DatalakeFile(
            None, uri=self.uri, type=type, lifetime='1day')
        with self.assertRaises(RuntimeError):
            datalake_file.lifetime = None

    def test_to_source_data(self):
        datalake_file = DatalakeFile(None, uri=self.uri)
        assert datalake_file.to_source_data() == {
            'data_uri': self.uri
        }
        datalake_file.type = 'image/jpeg'
        assert datalake_file.to_source_data() == {
            'data_uri': self.uri,
            'data_type': 'image/jpeg'
        }

    @patch('abeja.common.local_file.MOUNT_DIR', TEST_MOUNT_DIR)
    def test_get_content(self):
        datalake_file = DatalakeFile(None, uri=self.uri, type=type)
        mock_func = create_autospec(
            datalake_file._get_content_from_remote,
            return_value=self.binary_data)
        datalake_file._get_content_from_remote = mock_func
        content = datalake_file.get_content()
        self.assertEqual(content, self.binary_data)
        mock_func.assert_called_once_with()

    @patch('abeja.common.local_file.MOUNT_DIR', TEST_MOUNT_DIR)
    def test_get_content_using_cache(self):
        cache_dir = '{}/{}'.format(TEST_MOUNT_DIR, self.channel_id)
        os.makedirs(cache_dir, exist_ok=True)
        with open('{}/{}'.format(cache_dir, self.file_id), 'wb') as f:
            f.write(self.binary_data)
        datalake_file = DatalakeFile(None, uri=self.uri, type=type)
        mock_func = MagicMock()
        datalake_file._get_content_from_remote = mock_func
        content = datalake_file.get_content()
        self.assertEqual(content, self.binary_data)
        mock_func.assert_not_called()

    @patch('abeja.common.local_file.MOUNT_DIR', TEST_MOUNT_DIR)
    def test_get_iter_content(self):
        datalake_file = DatalakeFile(None, uri=self.uri, type=type)
        mock_func = create_autospec(
            datalake_file._get_iter_content_from_remote,
            return_value=self._generate_iter_content())
        datalake_file._get_iter_content_from_remote = mock_func
        iter_content = datalake_file.get_iter_content(chunk_size=128)
        content = b''
        for c in iter_content:
            content += c
        self.assertEqual(content, self.binary_data)
        mock_func.assert_called_once_with(128)

    @patch('abeja.common.local_file.MOUNT_DIR', TEST_MOUNT_DIR)
    def test_get_text(self):
        datalake_file = DatalakeFile(None, uri=self.uri, type=type)
        mock_func = create_autospec(
            datalake_file._get_text_from_remote, return_value=self.text_data)
        datalake_file._get_text_from_remote = mock_func
        text = datalake_file.get_text()
        self.assertEqual(text, self.text_data)
        mock_func.assert_called_once_with()

    @patch('abeja.common.local_file.MOUNT_DIR', TEST_MOUNT_DIR)
    def test_get_text_using_cache(self):
        cache_dir = '{}/{}'.format(TEST_MOUNT_DIR, self.channel_id)
        os.makedirs(cache_dir, exist_ok=True)
        with open('{}/{}'.format(cache_dir, self.file_id), 'w') as f:
            f.write(self.text_data)
        datalake_file = DatalakeFile(None, uri=self.uri, type=type)
        mock_func = MagicMock()
        datalake_file._get_text_from_remote = mock_func
        text = datalake_file.get_text()
        self.assertEqual(text, self.text_data)
        mock_func.assert_not_called()

    @patch('abeja.common.local_file.MOUNT_DIR', TEST_MOUNT_DIR)
    def test_get_json(self):
        datalake_file = DatalakeFile(None, uri=self.uri, type=type)
        mock_func = create_autospec(
            datalake_file._get_json_from_remote,
            return_value=self.json_data)
        datalake_file._get_json_from_remote = mock_func
        data = datalake_file.get_json()
        self.assertEqual(data, self.json_data)
        mock_func.assert_called_once_with()

    @patch('abeja.common.local_file.MOUNT_DIR', TEST_MOUNT_DIR)
    def test_get_iter_lines(self):
        datalake_file = DatalakeFile(None, uri=self.uri, type=type)
        mock_func = create_autospec(
            datalake_file._get_iter_lines_from_remote,
            return_value=self._generate_iter_lines())
        datalake_file._get_iter_lines_from_remote = mock_func
        iter_lines = datalake_file.get_iter_lines()
        content = ('').join(list(iter_lines))
        self.assertEqual(content, self.text_data)
        mock_func.assert_called_once_with()

    def test_file_info(self):
        mock_api = MagicMock()
        datalake_file = DatalakeFile(mock_api, uri=self.uri, type=type)
        datalake_file._api._connection.api_request.return_value = self.file_info
        file_info = datalake_file.get_file_info()
        self.assertEqual(file_info, self.file_info)
        datalake_file._api._connection.api_request.assert_called_once()

    def test_get_content_from_remote(self):
        datalake_file = DatalakeFile(None, uri=self.uri, type=type)
        mock_response = self._build_content_response()
        datalake_file._do_download = MagicMock(return_value=mock_response)
        content = datalake_file._get_content_from_remote()
        self.assertEqual(content, self.binary_data)

    def test_get_text_from_remote(self):
        datalake_file = DatalakeFile(None, uri=self.uri, type=type)
        mock_response = self._build_text_response()
        datalake_file._do_download = MagicMock(return_value=mock_response)
        text = datalake_file._get_text_from_remote()
        self.assertEqual(text, self.text_data)

    def test_get_json_from_remote(self):
        datalake_file = DatalakeFile(None, uri=self.uri, type=type)
        mock_response = self._build_json_response()
        datalake_file._do_download = MagicMock(return_value=mock_response)
        data = datalake_file._get_json_from_remote()
        self.assertEqual(data, self.json_data)

    @patch('abeja.common.local_file.MOUNT_DIR', TEST_MOUNT_DIR)
    def test_convert_to_file_id(self):
        path = '/{}'.format(self.file_id)
        datalake_file = DatalakeFile(None, uri=self.uri, type=type)
        file_id = datalake_file._convert_to_file_id(path)
        self.assertEqual(file_id, self.file_id)

    def test_get_download_uri(self):
        mock_api = MagicMock()
        datalake_file = DatalakeFile(mock_api, uri=self.uri, type=type)
        datalake_file._api._connection.api_request.return_value = self.file_info
        download_uri = datalake_file._get_download_uri()
        self.assertEqual(download_uri, self.file_info['download_uri'])
        datalake_file._api._connection.api_request.assert_called_once()

    def test_do_download(self):
        mock_api = MagicMock()
        datalake_file = DatalakeFile(mock_api, uri=self.uri, type=type)
        dummy_url = 'dummy url'
        datalake_file._get_download_uri = MagicMock(return_value=dummy_url)
        data = datalake_file._api._connection.request.return_value = self.text_data
        datalake_file._do_download()

        self.assertEqual(data, self.text_data)
        datalake_file._get_download_uri.assert_called_once()
        datalake_file._api._connection.request.assert_called_with(
            'GET', dummy_url, stream=False)

    def test_do_download_error_handling(self):
        mock_api = MagicMock()
        datalake_file = DatalakeFile(mock_api, uri=self.uri, type=type)
        dummy_url = 'dummy url'
        datalake_file._get_download_uri = MagicMock(return_value=dummy_url)

        http_error = requests.exceptions.HTTPError()
        res = requests.models.Response()
        res.status_code = 400
        res._content = 'test error'.encode('utf-8')
        http_error.response = res
        datalake_file._api._connection.request.side_effect = http_error

        with self.assertRaises(BadRequest):
            datalake_file._do_download()

    def _generate_iter_content(self):
        yield self.binary_data

    def _generate_iter_lines(self):
        yield self.text_data

    def test_commit(self):
        mock_api = MagicMock()
        datalake_file = DatalakeFile(
            mock_api, uri=self.uri, type=type,
            metadata={'x-abeja-meta-filename': 'DcZzLGkV4AA8FQc.jpg'})
        file_info = {
            'url_expires_on': '2018-06-04T05:04:46+00:00',
            'uploaded_at': '2018-06-01T05:22:44+00:00',
            'metadata': {
                'x-abeja-meta-filename': 'DcZzLGkV4AA8FQc.jpg'
            },
            'file_id': self.file_id,
            'download_uri': 'https://example.com/dummy_download_uri',
            'content_type': 'image/jpeg'
        }
        datalake_file.get_file_info = MagicMock(return_value=file_info)

        datalake_file.lifetime = '1day'
        datalake_file.metadata['label'] = 'cat'
        self.assertTrue(datalake_file.commit())

        expected_metadata = {
            'x-abeja-meta-filename': 'DcZzLGkV4AA8FQc.jpg',
            'x-abeja-meta-label': 'cat'
        }
        mock_api.put_channel_file_metadata.assert_called_once_with(
            self.channel_id, self.file_id, metadata=expected_metadata)
        mock_api.put_channel_file_lifetime.assert_called_once_with(
            self.channel_id, self.file_id, lifetime='1day')

    def test_commit_without_change_in_lifetime(self):
        mock_api = MagicMock()
        datalake_file = DatalakeFile(
            mock_api, uri=self.uri, type=type,
            metadata={'x-abeja-meta-filename': 'DcZzLGkV4AA8FQc.jpg'})
        file_info = {
            'url_expires_on': '2018-06-04T05:04:46+00:00',
            'uploaded_at': '2018-06-01T05:22:44+00:00',
            'metadata': {
                'x-abeja-meta-filename': 'DcZzLGkV4AA8FQc.jpg'
            },
            'file_id': self.file_id,
            'download_uri': 'https://example.com/dummy_download_uri',
            'content_type': 'image/jpeg'
        }
        datalake_file.get_file_info = MagicMock(return_value=file_info)

        datalake_file.metadata['label'] = 'cat'
        self.assertTrue(datalake_file.commit())

        expected_metadata = {
            'x-abeja-meta-filename': 'DcZzLGkV4AA8FQc.jpg',
            'x-abeja-meta-label': 'cat'
        }
        mock_api.put_channel_file_metadata.assert_called_once_with(
            self.channel_id, self.file_id, metadata=expected_metadata)
        mock_api.put_channel_file_lifetime.assert_not_called()

    def test_commit_without_change_in_metadata(self):
        mock_api = MagicMock()
        datalake_file = DatalakeFile(
            mock_api, uri=self.uri, type=type,
            metadata={'x-abeja-meta-filename': 'DcZzLGkV4AA8FQc.jpg'})
        file_info = {
            'url_expires_on': '2018-06-04T05:04:46+00:00',
            'uploaded_at': '2018-06-01T05:22:44+00:00',
            'metadata': {
                'x-abeja-meta-filename': 'DcZzLGkV4AA8FQc.jpg'
            },
            'file_id': self.file_id,
            'download_uri': 'https://example.com/dummy_download_uri',
            'content_type': 'image/jpeg'
        }
        datalake_file.get_file_info = MagicMock(return_value=file_info)

        datalake_file.lifetime = '1day'
        self.assertTrue(datalake_file.commit())

        expected_metadata = {
            'x-abeja-meta-filename': 'DcZzLGkV4AA8FQc.jpg',
        }
        mock_api.put_channel_file_metadata.assert_called_once_with(
            self.channel_id, self.file_id, metadata=expected_metadata)
        mock_api.put_channel_file_lifetime.assert_called_once_with(
            self.channel_id, self.file_id, lifetime='1day')

    def test_commit_without_changes(self):
        mock_api = MagicMock()
        datalake_file = DatalakeFile(
            mock_api, uri=self.uri, type=type,
            metadata={'x-abeja-meta-filename': 'DcZzLGkV4AA8FQc.jpg'})
        file_info = {
            'url_expires_on': '2018-06-04T05:04:46+00:00',
            'uploaded_at': '2018-06-01T05:22:44+00:00',
            'metadata': {
                'x-abeja-meta-filename': 'DcZzLGkV4AA8FQc.jpg'
            },
            'file_id': self.file_id,
            'download_uri': 'https://example.com/dummy_download_uri',
            'content_type': 'image/jpeg'
        }
        datalake_file.get_file_info = MagicMock(return_value=file_info)

        self.assertTrue(datalake_file.commit())

        expected_metadata = {
            'x-abeja-meta-filename': 'DcZzLGkV4AA8FQc.jpg',
        }
        mock_api.put_channel_file_metadata.assert_called_once_with(
            self.channel_id, self.file_id, metadata=expected_metadata)
        mock_api.put_channel_file_lifetime.assert_not_called()

    def test_commit_failed_in_updating_lifetime(self):
        mock_api = MagicMock()
        datalake_file = DatalakeFile(
            mock_api, uri=self.uri, type=type,
            metadata={'x-abeja-meta-filename': 'DcZzLGkV4AA8FQc.jpg'})
        file_info = {
            'url_expires_on': '2018-06-04T05:04:46+00:00',
            'uploaded_at': '2018-06-01T05:22:44+00:00',
            'metadata': {
                'x-abeja-meta-filename': 'DcZzLGkV4AA8FQc.jpg'
            },
            'file_id': self.file_id,
            'download_uri': 'https://example.com/dummy_download_uri',
            'content_type': 'image/jpeg'
        }
        datalake_file.get_file_info = MagicMock(return_value=file_info)
        mock_api.put_channel_file_lifetime.side_effect = HttpError(
            error='bad_request', error_description='bad request',
            status_code=400, url='dummy')

        datalake_file.metadata['label'] = 'cat'
        datalake_file.lifetime = '1week'
        with self.assertRaises(HttpError):
            datalake_file.commit()

        mock_api.put_channel_file_lifetime.assert_called_once_with(
            self.channel_id, self.file_id, lifetime='1week')
        self.assertEqual(mock_api.put_channel_file_metadata.call_count, 2)

        call_args = mock_api.put_channel_file_metadata.call_args_list

        expected_metadata = {
            'x-abeja-meta-filename': 'DcZzLGkV4AA8FQc.jpg',
            'x-abeja-meta-label': 'cat'
        }
        self.assertListEqual(
            list(call_args[0]),
            [(self.channel_id, self.file_id), {'metadata': expected_metadata}])

        expected_metadata = {'x-abeja-meta-filename': 'DcZzLGkV4AA8FQc.jpg'}
        self.assertListEqual(
            list(call_args[1]),
            [(self.channel_id, self.file_id), {'metadata': expected_metadata}])
