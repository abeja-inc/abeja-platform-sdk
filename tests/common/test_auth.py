import os
import unittest
from unittest.mock import patch
from abeja.common.auth import (
    get_token_from_environment,
    get_basic_auth_from_environment,
    get_credential
)

TEST_TOKEN = 'test_token'
TEST_USER_ID = 'test_user_id'
TEST_PERSONAL_ACCESS_TOKEN = 'test_personal_access_token'


class TestAuth(unittest.TestCase):
    @patch.dict(os.environ, {'PLATFORM_AUTH_TOKEN': TEST_TOKEN})
    def test_get_token_from_environment(self):
        token = get_token_from_environment()
        self.assertDictEqual(token, {
            'auth_token': TEST_TOKEN
        })

    @patch.dict(os.environ, {
        'ABEJA_PLATFORM_USER_ID': TEST_USER_ID,
        'ABEJA_PLATFORM_PERSONAL_ACCESS_TOKEN': TEST_PERSONAL_ACCESS_TOKEN
    })
    def test_get_basic_auth_from_environment(self):
        token = get_basic_auth_from_environment()
        self.assertDictEqual(token, {
            'user_id': TEST_USER_ID,
            'personal_access_token': TEST_PERSONAL_ACCESS_TOKEN
        })

    @patch.dict(os.environ, {'ABEJA_PLATFORM_USER_ID': TEST_USER_ID})
    def test_get_basic_auth_from_environment_with_only_user_id(self):
        token = get_basic_auth_from_environment()
        self.assertIsNone(token)

    @patch.dict(os.environ, {'PLATFORM_AUTH_TOKEN': TEST_TOKEN})
    def test_get_credential_with_token(self):
        token = get_credential()
        self.assertDictEqual(token, {
            'auth_token': TEST_TOKEN
        })

    @patch.dict(os.environ, {
        'ABEJA_PLATFORM_USER_ID': TEST_USER_ID,
        'ABEJA_PLATFORM_PERSONAL_ACCESS_TOKEN': TEST_PERSONAL_ACCESS_TOKEN
    })
    def test_get_credential_with_user_id_and_personal_access_token(self):
        token = get_credential()
        self.assertDictEqual(token, {
            'user_id': TEST_USER_ID,
            'personal_access_token': TEST_PERSONAL_ACCESS_TOKEN
        })

    @patch.dict(os.environ, {})
    def test_get_credential_without_anything(self):
        token = get_credential()
        self.assertIsNone(token)
