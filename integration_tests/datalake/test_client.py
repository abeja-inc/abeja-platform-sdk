import os
import glob
import shutil
from unittest import TestCase

from abeja.datalake import Client
from abeja.datalake.file import DatalakeFile

CHANNEL_ID = os.environ.get('CHANNEL_ID')

ORGANIZATION_ID = os.environ.get('ORGANIZATION_ID')
USER_ID = os.environ.get('USER_ID')
PERSONAL_ACCESS_TOKEN = os.environ.get('PERSONAL_ACCESS_TOKEN')

FIXTURE_IMAGE_PATH = 'integration_tests/fixtures/images'

credential = {
    'user_id': USER_ID,
    'personal_access_token': PERSONAL_ACCESS_TOKEN
}
client = Client(credential=credential, organization_id=ORGANIZATION_ID)
channel = client.get_channel(CHANNEL_ID)


def delete_all_files_in_channel(channel_id):
    res = client.api.list_channel_files(channel_id)
    for file in res['files']:
        file_id = file['file_id']
        client.api.delete_channel_file(channel_id, file_id)


class DatalakeIntegrationTest(TestCase):
    def setUp(self):
        delete_all_files_in_channel(CHANNEL_ID)

    @classmethod
    def tearDownClass(cls):
        delete_all_files_in_channel(CHANNEL_ID)

    def _upload_fixture_images(self):
        for file_path in glob.glob('{}/*'.format(FIXTURE_IMAGE_PATH)):
            with open(file_path, 'rb') as f:
                client.api.post_channel_file_upload(CHANNEL_ID, f, 'image/jpeg')

    def _delete_prefetched_files_if_exist(self):
        if os.path.exists(CHANNEL_ID):
            shutil.rmtree(CHANNEL_ID)

    def test_list_files_with_prefetch(self):
        self._upload_fixture_images()

        files = list(channel.list_files(prefetch=True))

        expected_num_of_files = len(glob.glob('{}/*'.format(FIXTURE_IMAGE_PATH)))
        self.assertEqual(len(files), expected_num_of_files)

        self._delete_prefetched_files_if_exist()

    def test_list_files_without_prefetch(self):
        self._upload_fixture_images()

        files = list(channel.list_files(prefetch=False))

        expected_num_of_files = len(glob.glob('{}/*'.format(FIXTURE_IMAGE_PATH)))
        self.assertEqual(len(files), expected_num_of_files)

    def test_upload_dir_with_thread_with_params(self):
        content_type = 'image/jpeg'
        metadata = {'label': 'cats_and_dogs'}
        lifetime = '1day'
        files = channel.upload_dir(
            FIXTURE_IMAGE_PATH, metadata=metadata, content_type=content_type, lifetime=lifetime)
        expected_num_of_files = len(glob.glob('{}/*'.format(FIXTURE_IMAGE_PATH)))
        self.assertEqual(len(files), expected_num_of_files)

        for file in files:
            self.assertIsInstance(file, DatalakeFile)
            self.assertEqual(file.content_type, content_type)
            # TODO:
            # self.assertEqual(file.lifetime, lifetime)
            self.assertIn('label', file.metadata)

    def test_upload_dir_with_thread_without_params(self):
        files = channel.upload_dir(FIXTURE_IMAGE_PATH)
        expected_num_of_files = len(glob.glob('{}/*'.format(FIXTURE_IMAGE_PATH)))
        self.assertEqual(len(files), expected_num_of_files)

        for file in files:
            self.assertIsInstance(file, DatalakeFile)
            # content_type should be inferred from extension
            self.assertEqual(file.content_type, 'image/jpeg')

    def test_upload_dir_without_thread_with_params(self):
        content_type = 'image/jpeg'
        metadata = {'label': 'cats_and_dogs'}
        lifetime = '1day'
        files = channel.upload_dir(
            FIXTURE_IMAGE_PATH, metadata=metadata, content_type=content_type,
            lifetime=lifetime, use_thread=False)
        expected_num_of_files = len(glob.glob('{}/*'.format(FIXTURE_IMAGE_PATH)))
        self.assertEqual(len(files), expected_num_of_files)

        for file in files:
            self.assertIsInstance(file, DatalakeFile)
            self.assertEqual(file.content_type, content_type)
            # TODO:
            # self.assertEqual(file.lifetime, lifetime)
            self.assertIn('label', file.metadata)

    def test_upload_dir_without_thread_without_params(self):
        files = channel.upload_dir(FIXTURE_IMAGE_PATH, use_thread=False)
        expected_num_of_files = len(glob.glob('{}/*'.format(FIXTURE_IMAGE_PATH)))
        self.assertEqual(len(files), expected_num_of_files)

        for file in files:
            self.assertIsInstance(file, DatalakeFile)
            # content_type should be inferred from extension
            self.assertEqual(file.content_type, 'image/jpeg')
