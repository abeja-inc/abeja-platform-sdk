import os
from io import BytesIO
import json
import tempfile
from unittest import TestCase
from unittest.mock import Mock, patch

from abeja.datalake.file import DatalakeFile
from abeja.datalake.channel import Channel, Channels
from abeja.datalake.storage_type import StorageType

ORGANIZATION_ID = ' 1234567890123'
CHANNEL_ID = '1230000000000'
CHANNEL_NAME = 'test_channel'
CHANNEL_DISPLAY_NAME = 'test_display_channel_name'
CHANNEL_DESCRIPTION = 'description of a test channel'
CHANNEL_STORAGE_TYPE = 'datalake'
CHANNEL_ARCHIVED = False


class TestChannel(TestCase):

    def test_files(self):
        mock_api = Mock()
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
                                                               'content_type': 'image/jpeg'}]}]
        channel = Channel(mock_api, ORGANIZATION_ID, CHANNEL_ID)
        self.assertIsInstance(channel, Channel)
        files = list(channel.list_files())
        for file in files:
            self.assertIsInstance(file, DatalakeFile)

        self.assertEqual(mock_api.list_channel_files.call_count, 2)

        call_args_1 = mock_api.list_channel_files.call_args_list[0]
        self.assertTupleEqual(call_args_1[0], (CHANNEL_ID,))
        self.assertDictEqual(call_args_1[1], {})

        call_args_2 = mock_api.list_channel_files.call_args_list[1]
        self.assertTupleEqual(call_args_2[0], (CHANNEL_ID,))
        self.assertDictEqual(call_args_2[1], {'next_page_token': 'dummy'})

        self.assertEqual(len(files), 2)

    def test_files_below_items_per_page(self):
        mock_api = Mock()
        mock_api.list_channel_files.side_effect = [
            {
                'next_page_token': None,
                'files': [
                    {
                        'url_expires_on': '2018-06-04T05:04:46+00:00',
                        'uploaded_at': '2018-06-01T05:22:44+00:00',
                        'metadata': {
                            'x-abeja-meta-filename': 'DcZzLGkV4AA8FQc.jpg'},
                        'file_id': '20180601T052244-250482c0-d361-4c5b-a0f9-e796af1a5f0d',
                        'download_uri': 'http://example/dummy/donwload_url',
                        'content_type': 'image/jpeg'}]}]
        channel = Channel(mock_api, ORGANIZATION_ID, CHANNEL_ID)
        self.assertIsInstance(channel, Channel)
        files = list(channel.list_files())
        for file in files:
            self.assertIsInstance(file, DatalakeFile)
        self.assertEqual(mock_api.list_channel_files.call_count, 1)
        self.assertEqual(
            mock_api.list_channel_files.call_args[0][0],
            CHANNEL_ID)
        self.assertEqual(len(files), 1)

    def test_files_with_both_items_per_page_and_next_page_token(self):
        mock_api = Mock()
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
                                                               'content_type': 'image/jpeg'}]}]
        channel = Channel(mock_api, ORGANIZATION_ID, CHANNEL_ID)
        self.assertIsInstance(channel, Channel)
        files = list(channel.list_files(limit=1))
        for file in files:
            self.assertIsInstance(file, DatalakeFile)
        self.assertEqual(mock_api.list_channel_files.call_count, 2)

        call_args_1 = mock_api.list_channel_files.call_args_list[0]
        self.assertTupleEqual(call_args_1[0], (CHANNEL_ID,))
        self.assertDictEqual(call_args_1[1], {'items_per_page': 1})

        call_args_2 = mock_api.list_channel_files.call_args_list[1]
        self.assertTupleEqual(call_args_2[0], (CHANNEL_ID,))
        # items_per_page should not be passed as query parameter
        self.assertDictEqual(call_args_2[1], {'next_page_token': 'dummy'})

        self.assertEqual(len(files), 2)

    def test_files_with_empty_items(self):
        mock_api = Mock()
        mock_api.list_channel_files.side_effect = [
            {
                'next_page_token': None,
                'files': []
            }
        ]
        channel = Channel(mock_api, ORGANIZATION_ID, CHANNEL_ID)
        self.assertIsInstance(channel, Channel)
        files = list(channel.list_files())
        self.assertEqual(len(files), 0)

    def test_get_file(self):
        mock_api = Mock()
        dummy_file_id = "20180101T000000-00000000-1111-2222-3333-999999999999"
        dummy_content_type = "image/jpeg"
        dummy_download_uri = "http://example.com/dummy_upload_url"
        dummy_url_expires_on = "2018-01-01T00:00:00+00:00"
        dummy_metadata = {'x-abeja-meta-filename': 'test_filename'}
        mock_api.get_channel_file_download.return_value = {
            "url_expires_on": dummy_url_expires_on,
            "download_uri": dummy_download_uri,
            "uploaded_at": None,
            "metadata": dummy_metadata,
            "content_type": dummy_content_type,
            "file_id": dummy_file_id
        }
        channel = Channel(mock_api, ORGANIZATION_ID, CHANNEL_ID)
        file = channel.get_file(dummy_file_id)
        self.assertIsInstance(file, DatalakeFile)
        self.assertEqual(file.organization_id, ORGANIZATION_ID)
        self.assertEqual(file.channel_id, CHANNEL_ID)
        self.assertEqual(file.file_id, dummy_file_id)
        self.assertEqual(file.content_type, dummy_content_type)
        self.assertEqual(file.url_expires_on, dummy_url_expires_on)
        self.assertEqual(file.metadata['filename'], 'test_filename')

    def test_upload(self):
        mock_api = Mock()
        mock_api.post_channel_file_upload.return_value = {
            "uploaded_at": None,
            "metadata": {},
            "content_type": "image/jpeg",
            "lifetime": None,
            "file_id": "20180515T180605-f4acc798-9afa-40a1-b500-ebce42a4fa3f"
        }
        channel = Channel(mock_api, ORGANIZATION_ID, CHANNEL_ID)
        content_type = 'application/json'
        metadata = {'label': 'dummy label'}
        dummy_file_data = json.dumps({'data': 'dummy'}).encode('utf-8')
        dummy_file = BytesIO(dummy_file_data)
        file = channel.upload(
            dummy_file,
            content_type=content_type,
            metadata=metadata)
        self.assertIsInstance(file, DatalakeFile)

        expected_metadata = {
            'x-abeja-meta-label': 'dummy label'
        }
        mock_api.post_channel_file_upload.assert_called_once_with(
            CHANNEL_ID, dummy_file, content_type,
            metadata=expected_metadata, lifetime=None, conflict_target=None)

    def test_upload_file(self):
        mock_api = Mock()
        mock_api.post_channel_file_upload.return_value = {
            "url_expires_on": "2018-05-15T19:06:05+00:00",
            "uploaded_at": None,
            "metadata": {},
            "content_type": "image/jpeg",
            "lifetime": None,
            "file_id": "20180515T180605-f4acc798-9afa-40a1-b500-ebce42a4fa3f"
        }
        channel = Channel(mock_api, ORGANIZATION_ID, CHANNEL_ID)
        content_type = 'application/json'
        metadata = {'filename': 'dummy', 'label': 'dummy label'}
        dummy_file_data = json.dumps({'data': 'dummy'}).encode('utf-8')
        with tempfile.NamedTemporaryFile() as tmp:
            tmp.write(dummy_file_data)
            tmp.seek(0)
            file = channel.upload_file(
                tmp.name, metadata=metadata, content_type=content_type)
            self.assertIsInstance(file, DatalakeFile)

        expected_metadata = {
            'x-abeja-meta-filename': 'dummy',
            'x-abeja-meta-label': 'dummy label'
        }
        self.assertEqual(mock_api.post_channel_file_upload.call_count, 1)

        call_args = mock_api.post_channel_file_upload.call_args[0]
        call_kwargs = mock_api.post_channel_file_upload.call_args[1]

        self.assertEqual(call_args[0], CHANNEL_ID)
        self.assertDictEqual(call_kwargs, {
            'lifetime': None,
            'conflict_target': None,
            'metadata': expected_metadata
        })

    def test_upload_file_without_filename(self):
        mock_api = Mock()
        mock_api.post_channel_file_upload.return_value = {
            "uploaded_at": None,
            "metadata": {},
            "content_type": "image/jpeg",
            "file_id": "20180515T180605-f4acc798-9afa-40a1-b500-ebce42a4fa3f"
        }
        channel = Channel(mock_api, ORGANIZATION_ID, CHANNEL_ID)
        dummy_file_data = json.dumps({'data': 'dummy'}).encode('utf-8')
        with tempfile.NamedTemporaryFile(suffix='.json') as tmp:
            tmp.write(dummy_file_data)
            tmp.seek(0)
            filename = os.path.basename(tmp.name)
            file = channel.upload_file(tmp.name)
        self.assertIsInstance(file, DatalakeFile)

        content_type = 'application/json'
        metadata = {'x-abeja-meta-filename': filename}

        self.assertEqual(mock_api.post_channel_file_upload.call_count, 1)

        call_args = mock_api.post_channel_file_upload.call_args[0]
        call_kwargs = mock_api.post_channel_file_upload.call_args[1]

        self.assertEqual(call_args[0], CHANNEL_ID)
        self.assertEqual(call_args[2], content_type)
        self.assertDictEqual(call_kwargs, {
            'lifetime': None,
            'conflict_target': None,
            'metadata': metadata
        })

    def test_upload_file_with_lifetime(self):
        mock_api = Mock()
        dummy_lifetime = "1day"
        mock_api.post_channel_file_upload.return_value = {
            "uploaded_at": None,
            "metadata": {},
            "content_type": "image/jpeg",
            "lifetime": dummy_lifetime,
            "file_id": "20180515T180605-f4acc798-9afa-40a1-b500-ebce42a4fa3f"
        }
        channel = Channel(mock_api, ORGANIZATION_ID, CHANNEL_ID)
        dummy_file_data = json.dumps({'data': 'dummy'}).encode('utf-8')
        with tempfile.NamedTemporaryFile(suffix='.json') as tmp:
            tmp.write(dummy_file_data)
            tmp.seek(0)
            filename = os.path.basename(tmp.name)
            file = channel.upload_file(tmp.name, lifetime=dummy_lifetime)
        self.assertIsInstance(file, DatalakeFile)

        content_type = 'application/json'
        metadata = {'x-abeja-meta-filename': filename}

        self.assertEqual(mock_api.post_channel_file_upload.call_count, 1)

        call_args = mock_api.post_channel_file_upload.call_args[0]
        call_kwargs = mock_api.post_channel_file_upload.call_args[1]

        self.assertEqual(call_args[0], CHANNEL_ID)
        self.assertEqual(call_args[2], content_type)
        self.assertDictEqual(call_kwargs, {
            'lifetime': dummy_lifetime,
            'conflict_target': None,
            'metadata': metadata
        })

    def test_upload_file_with_conflict_target(self):
        conflict_target = 'filename'
        mock_api = Mock()
        mock_api.post_channel_file_upload.return_value = {
            "uploaded_at": None,
            "metadata": {},
            "content_type": "image/jpeg",
            "lifetime": None,
            "file_id": "20180515T180605-f4acc798-9afa-40a1-b500-ebce42a4fa3f"
        }
        channel = Channel(mock_api, ORGANIZATION_ID, CHANNEL_ID)
        dummy_file_data = json.dumps({'data': 'dummy'}).encode('utf-8')
        with tempfile.NamedTemporaryFile(suffix='.json') as tmp:
            tmp.write(dummy_file_data)
            tmp.seek(0)
            filename = os.path.basename(tmp.name)
            file = channel.upload_file(tmp.name, conflict_target=conflict_target)
        self.assertIsInstance(file, DatalakeFile)

        content_type = 'application/json'
        metadata = {'x-abeja-meta-filename': filename}

        self.assertEqual(mock_api.post_channel_file_upload.call_count, 1)

        call_args = mock_api.post_channel_file_upload.call_args[0]
        call_kwargs = mock_api.post_channel_file_upload.call_args[1]

        self.assertEqual(call_args[0], CHANNEL_ID)
        self.assertEqual(call_args[2], content_type)
        self.assertDictEqual(call_kwargs, {
            'lifetime': None,
            'conflict_target': conflict_target,
            'metadata': metadata
        })

    def test_upload_with_dir(self):
        mock_api = Mock()
        mock_api.get_channel_file_upload.return_value = {
            "url_expires_on": "2018-05-15T19:06:05+00:00",
            "upload_url": "http://example.com/dummy_upload_url",
            "uploaded_at": None,
            "metadata": {},
            "content_type": "image/jpeg",
            "file_id": "20180515T180605-f4acc798-9afa-40a1-b500-ebce42a4fa3f"
        }
        channel = Channel(mock_api, ORGANIZATION_ID, CHANNEL_ID)
        with tempfile.NamedTemporaryFile() as tmp:
            tmp.write(json.dumps({'data': 'dummy'}).encode('utf-8'))
            tmp.seek(0)
            base_dir = '/'.join(tmp.name.split('/')[:-1])
            with self.assertRaises(IsADirectoryError):
                channel.upload_file(
                    base_dir,
                    metadata={
                        'x-abeja-meta-filename': 'dummy'},
                    content_type='application/json')

    @patch('abeja.datalake.channel.generate_path_iter')
    def test_upload_dir(self, mock_generate_path_iter):
        mock_api = Mock()
        mock_api.post_channel_file_upload.side_effect = [
            {
                "uploaded_at": None,
                "metadata": {},
                "content_type": "image/jpeg",
                "lifetime": None,
                "file_id": "20180515T180605-f4acc798-9afa-40a1-b500-ebce42a4fa3f"
            },
            {
                "uploaded_at": None,
                "metadata": {},
                "content_type": "image/jpeg",
                "lifetime": None,
                "file_id": "20180515T180605-f4acc798-9afa-40a1-b500-ebce42a4fa3f"
            }
        ]
        with tempfile.NamedTemporaryFile() as tmp1:
            tmp1.write(b'dummy1')
            tmp1.seek(0)
            with tempfile.NamedTemporaryFile() as tmp2:
                tmp2.write(b'dummy2')
                tmp2.seek(0)
                mock_generate_path_iter.return_value = [tmp1.name, tmp2.name]

                channel = Channel(mock_api, ORGANIZATION_ID, CHANNEL_ID)
                dummy_metadata = {'dummy': 'data'}
                content_type = 'image/jpeg'
                files = channel.upload_dir(
                    'dummy_path',
                    metadata=dummy_metadata,
                    content_type=content_type)
                files = list(files)

        file = files[0]
        self.assertIsInstance(file, DatalakeFile)
        self.assertEqual(mock_api.post_channel_file_upload.call_count, 2)

    @patch('abeja.datalake.channel.logger')
    @patch('abeja.datalake.channel.generate_path_iter')
    def test_upload_dir_with_exception(
            self, mock_generate_path_iter, mock_logger):
        mock_api = Mock()
        dummy_exception = Exception('dummy exception')
        mock_api.post_channel_file_upload.side_effect = [
            {
                "url_expires_on": "2018-05-15T19:06:05+00:00",
                "upload_url": "http://example.com/dummy_upload_url",
                "uploaded_at": None,
                "metadata": {},
                "content_type": "image/jpeg",
                "file_id": "20180515T180605-f4acc798-9afa-40a1-b500-ebce42a4fa3f"},
            dummy_exception]
        with tempfile.NamedTemporaryFile() as tmp1:
            tmp1.write(b'dummy1')
            tmp1.seek(0)
            with tempfile.NamedTemporaryFile() as tmp2:
                tmp2.write(b'dummy2')
                tmp2.seek(0)
                mock_generate_path_iter.return_value = [tmp1.name, tmp2.name]

                channel = Channel(mock_api, ORGANIZATION_ID, CHANNEL_ID)
                dummy_metadata = {'dummy': 'data'}
                content_type = 'image/jpeg'
                files = channel.upload_dir(
                    'dummy_path',
                    metadata=dummy_metadata,
                    content_type=content_type)
                files = list(files)

        self.assertEqual(len(files), 1)

        file = files[0]
        self.assertIsInstance(file, DatalakeFile)
        self.assertEqual(mock_api.post_channel_file_upload.call_count, 2)

        mock_logger.error.assert_called_once_with(dummy_exception)

    @patch('abeja.datalake.channel.generate_path_iter')
    def test_upload_dir_without_thread(self, mock_generate_path_iter):
        mock_api = Mock()
        mock_api.post_channel_file_upload.side_effect = [
            {
                "url_expires_on": "2018-05-15T19:06:05+00:00",
                "upload_url": "http://example.com/dummy_upload_url",
                "uploaded_at": None,
                "metadata": {},
                "content_type": "image/jpeg",
                "file_id": "20180515T180605-f4acc798-9afa-40a1-b500-ebce42a4fa3f"
            },
            {
                "url_expires_on": "2018-05-15T19:06:05+00:00",
                "upload_url": "http://example.com/dummy_upload_url",
                "uploaded_at": None,
                "metadata": {},
                "content_type": "image/jpeg",
                "file_id": "20180515T180605-f4acc798-9afa-40a1-b500-ebce42a4fa3f"
            }
        ]
        with tempfile.NamedTemporaryFile() as tmp1:
            tmp1.write(b'dummy1')
            tmp1.seek(0)
            with tempfile.NamedTemporaryFile() as tmp2:
                tmp2.write(b'dummy2')
                tmp2.seek(0)
                mock_generate_path_iter.return_value = [tmp1.name, tmp2.name]

                channel = Channel(mock_api, ORGANIZATION_ID, CHANNEL_ID)
                dummy_metadata = {'dummy': 'data'}
                content_type = 'image/jpeg'
                files = channel.upload_dir(
                    'dummy_path', metadata=dummy_metadata,
                    content_type=content_type, use_thread=False)
                files = list(files)

        file = files[0]
        self.assertIsInstance(file, DatalakeFile)
        self.assertEqual(mock_api.post_channel_file_upload.call_count, 2)

    def list_datasources(self):
        pass

    def add_datasource(self):
        pass

    def remove_datasource(self):
        pass


class TestChannels(TestCase):

    def test_create(self):
        mock_api = Mock()
        mock_api.create_channel.return_value = {
            "updated_at": "2017-09-12T10:11:46Z",
            "organization_name": "test-organization",
            "organization_id": ORGANIZATION_ID,
            "created_at": "2017-09-12T10:11:46Z",
            "channel": {
                "updated_at": "2018-06-03T02:57:19Z",
                "storage_type": "datalake",
                "name": CHANNEL_NAME,
                "display_name": CHANNEL_DISPLAY_NAME,
                "description": CHANNEL_DESCRIPTION,
                "created_at": "2018-06-03T02:57:19Z",
                "channel_id": CHANNEL_ID,
                "archived": False
            }
        }
        channels = Channels(api=mock_api, organization_id=ORGANIZATION_ID)
        channel = channels.create(
            name=CHANNEL_NAME, description=CHANNEL_DESCRIPTION,
            storage_type=StorageType.DATALAKE.value)

        mock_api.create_channel.assert_called_once_with(
            ORGANIZATION_ID, CHANNEL_NAME, CHANNEL_DESCRIPTION,
            StorageType.DATALAKE.value)

        self.assertIsInstance(channel, Channel)
        self.assertEqual(channel.organization_id, ORGANIZATION_ID)
        self.assertEqual(channel.channel_id, CHANNEL_ID)
        self.assertEqual(channel.name, CHANNEL_NAME)
        self.assertEqual(channel.description, CHANNEL_DESCRIPTION)
        self.assertEqual(channel.display_name, CHANNEL_DISPLAY_NAME)
        self.assertEqual(channel.storage_type, CHANNEL_STORAGE_TYPE)
        self.assertEqual(channel.archived, CHANNEL_ARCHIVED)

    def test_list(self):
        mock_api = Mock()
        mock_api.list_channels.return_value = {
            "updated_at": "2017-09-12T10:11:46Z",
            "organization_name": "abeja-internal",
            "organization_id": "1225098818583",
            "offset": 0,
            "limit": 50,
            "has_next": True,
            "created_at": "2017-09-12T10:11:46Z",
            "channels": [
                {
                    "updated_at": "2018-06-03T02:57:19Z",
                    "storage_type": "datalake",
                    "name": CHANNEL_NAME,
                    "display_name": CHANNEL_DISPLAY_NAME,
                    "description": CHANNEL_DESCRIPTION,
                    "created_at": "2018-06-03T02:57:19Z",
                    "channel_id": CHANNEL_ID,
                    "archived": False
                }
            ]
        }
        channel_collection = Channels(
            api=mock_api, organization_id=ORGANIZATION_ID)
        channels = channel_collection.list()
        channel = list(channels)[0]

        mock_api.list_channels.assert_called_once_with(
            ORGANIZATION_ID, limit=None, offset=None)

        self.assertIsInstance(channel, Channel)
        self.assertEqual(channel.organization_id, ORGANIZATION_ID)
        self.assertEqual(channel.channel_id, CHANNEL_ID)
        self.assertEqual(channel.name, CHANNEL_NAME)
        self.assertEqual(channel.description, CHANNEL_DESCRIPTION)
        self.assertEqual(channel.display_name, CHANNEL_DISPLAY_NAME)
        self.assertEqual(channel.storage_type, CHANNEL_STORAGE_TYPE)
        self.assertEqual(channel.archived, CHANNEL_ARCHIVED)

    def test_get(self):
        mock_api = Mock()
        mock_api.get_channel.return_value = {
            "updated_at": "2017-09-12T10:11:46Z",
            "organization_name": "test-organization",
            "organization_id": ORGANIZATION_ID,
            "created_at": "2017-09-12T10:11:46Z",
            "channel": {
                "updated_at": "2018-06-03T02:57:19Z",
                "storage_type": "datalake",
                "name": CHANNEL_NAME,
                "display_name": CHANNEL_DISPLAY_NAME,
                "description": CHANNEL_DESCRIPTION,
                "created_at": "2018-06-03T02:57:19Z",
                "channel_id": CHANNEL_ID,
                "archived": False
            }
        }
        channels = Channels(api=mock_api, organization_id=ORGANIZATION_ID)
        channel = channels.get(channel_id=CHANNEL_ID)

        mock_api.get_channel.assert_called_once_with(
            ORGANIZATION_ID, CHANNEL_ID)

        self.assertIsInstance(channel, Channel)
        self.assertEqual(channel.organization_id, ORGANIZATION_ID)
        self.assertEqual(channel.channel_id, CHANNEL_ID)
        self.assertEqual(channel.name, CHANNEL_NAME)
        self.assertEqual(channel.description, CHANNEL_DESCRIPTION)
        self.assertEqual(channel.display_name, CHANNEL_DISPLAY_NAME)
        self.assertEqual(channel.storage_type, CHANNEL_STORAGE_TYPE)
        self.assertEqual(channel.archived, CHANNEL_ARCHIVED)

    def test_patch(self):
        updated_name = 'updated_name'
        updated_description = 'updated description'
        mock_api = Mock()
        mock_api.patch_channel.return_value = {
            "updated_at": "2017-09-12T10:11:46Z",
            "organization_name": "test-organization",
            "organization_id": ORGANIZATION_ID,
            "created_at": "2017-09-12T10:11:46Z",
            "channel": {
                "updated_at": "2018-06-03T02:57:19Z",
                "storage_type": "datalake",
                "name": updated_name,
                "display_name": CHANNEL_DISPLAY_NAME,
                "description": updated_description,
                "created_at": "2018-06-03T02:57:19Z",
                "channel_id": CHANNEL_ID,
                "archived": False
            }
        }
        channels = Channels(api=mock_api, organization_id=ORGANIZATION_ID)
        channel = channels.patch(
            channel_id=CHANNEL_ID,
            name=updated_name,
            description=updated_description)

        mock_api.patch_channel.assert_called_once_with(
            ORGANIZATION_ID, CHANNEL_ID, updated_name, updated_description)

        self.assertIsInstance(channel, Channel)
        self.assertEqual(channel.organization_id, ORGANIZATION_ID)
        self.assertEqual(channel.channel_id, CHANNEL_ID)
        self.assertEqual(channel.name, updated_name)
        self.assertEqual(channel.description, updated_description)
        self.assertEqual(channel.display_name, CHANNEL_DISPLAY_NAME)
        self.assertEqual(channel.storage_type, CHANNEL_STORAGE_TYPE)
        self.assertEqual(channel.archived, CHANNEL_ARCHIVED)
