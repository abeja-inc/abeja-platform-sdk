import logging
import unittest
from unittest import mock

import requests
from abeja import VERSION
from abeja.common.connection import Connection
from abeja.exceptions import BadRequest, InternalServerError
from abeja.train.api.client import APIClient
from abeja.train.client import Client
from abeja.train.statistics import Statistics

ORGANIZATION_ID = '1111111111111'
TRAINING_JON_DEFINITION_NAME = 'tjd'
TRAINING_JOB_ID = 'job-0123456789abcdef'
ABEJA_API_URL = 'http://localhost:8080'
PATCHED_ENVIRON = {'ABEJA_ORGANIZATION_ID': ORGANIZATION_ID,
                   'TRAINING_JOB_DEFINITION_NAME': TRAINING_JON_DEFINITION_NAME,
                   'TRAINING_JOB_ID': TRAINING_JOB_ID}


@mock.patch.dict('os.environ', PATCHED_ENVIRON)
class TestClient(unittest.TestCase):

    @mock.patch.dict('os.environ', PATCHED_ENVIRON)
    def setUp(self):
        Connection.BASE_URL = ABEJA_API_URL
        self.client = Client()
        self.client.logger.setLevel(logging.FATAL)

    def test_init(self):
        self.assertIsInstance(self.client.api, APIClient)

    @mock.patch('abeja.train.client.extract_zipfile')
    @mock.patch('abeja.train.client.Client._get_content')
    @mock.patch('requests.Session.request')
    def test_download_training_result(self, m, m_get_content, m_extract_zipfile):
        dummy_binary = b'dummy'
        m_get_content.return_value = dummy_binary
        self.client.download_training_result(TRAINING_JOB_ID)
        url = '{}/organizations/{}/training/definitions/{}/jobs/{}/result'.format(
            ABEJA_API_URL, ORGANIZATION_ID, TRAINING_JON_DEFINITION_NAME, TRAINING_JOB_ID)
        m.assert_called_with('GET', url, data=None, headers={'User-Agent': 'abeja-platform-sdk/{}'.format(VERSION)},
                             json=None, params=None, timeout=30)
        m_extract_zipfile.assert_called_once_with(dummy_binary, path=None)

    @mock.patch('requests.Session.request')
    def test_update_statistics(self, m):
        statistics = Statistics(progress_percentage=0.5, epoch=1,
                                num_epochs=5, key1='value1')
        statistics.add_stage(name=Statistics.STAGE_TRAIN, accuracy=0.9, loss=0.05)
        statistics.add_stage(name=Statistics.STAGE_VALIDATION,
                             accuracy=0.8, loss=0.1, key2=2)
        self.client.update_statistics(statistics)
        self.assertEqual(m.call_count, 1)
        url = '{}/organizations/{}/training/definitions/{}/jobs/{}/statistics'.format(
            ABEJA_API_URL, ORGANIZATION_ID, TRAINING_JON_DEFINITION_NAME, TRAINING_JOB_ID)
        expected_data = {
            'statistics': {
                'num_epochs': 5,
                'epoch': 1,
                'progress_percentage': 0.5,
                'stages': {
                    'train': {
                        'accuracy': 0.9,
                        'loss': 0.05
                    },
                    'validation': {
                        'accuracy': 0.8,
                        'loss': 0.1,
                        'key2': 2
                    }
                },
                'key1': 'value1'
            }
        }
        m.assert_called_with('POST', url, params=None, headers={'User-Agent': 'abeja-platform-sdk/{}'.format(VERSION)},
                             timeout=30, data=None, json=expected_data)

    @mock.patch('requests.Session.request')
    def test_update_statistics_without_statistics(self, m):
        statistics = Statistics(progress_percentage=0.5)
        self.client.update_statistics(statistics)
        self.assertEqual(m.call_count, 1)
        url = '{}/organizations/{}/training/definitions/{}/jobs/{}/statistics'.format(
            ABEJA_API_URL, ORGANIZATION_ID, TRAINING_JON_DEFINITION_NAME, TRAINING_JOB_ID)
        m.assert_called_with('POST', url, params=None,
                             headers={'User-Agent': 'abeja-platform-sdk/{}'.format(VERSION)}, timeout=30, data=None,
                             json={'statistics': {'progress_percentage': 0.5}})

    @mock.patch('requests.Session.request')
    def test_update_statistics_progress_within_statistics(self, m):
        statistics = Statistics(progress_percentage=0.5)
        statistics.add_stage(name='other_stage', key1='value1')
        self.client.update_statistics(statistics)
        self.assertEqual(m.call_count, 1)
        url = '{}/organizations/{}/training/definitions/{}/jobs/{}/statistics'.format(
            ABEJA_API_URL, ORGANIZATION_ID, TRAINING_JON_DEFINITION_NAME, TRAINING_JOB_ID)
        expected_data = {
            'statistics': {
                'progress_percentage': 0.5,
                'stages': {
                    'other_stage': {
                        'key1': 'value1'
                    }
                }
            }
        }
        m.assert_called_with('POST', url, params=None, headers={'User-Agent': 'abeja-platform-sdk/{}'.format(VERSION)},
                             timeout=30, data=None, json=expected_data)

    @mock.patch('requests.Session.request')
    def test_update_statistics_override_organization_id(self, m):
        organization_id = '2222222222222'
        client = Client(organization_id=organization_id)
        statistics = Statistics(progress_percentage=0.5, key1='value1')
        client.update_statistics(statistics)
        self.assertEqual(m.call_count, 1)
        url = '{}/organizations/{}/training/definitions/{}/jobs/{}/statistics'.format(
            ABEJA_API_URL, organization_id, TRAINING_JON_DEFINITION_NAME, TRAINING_JOB_ID)
        m.assert_called_with('POST', url, params=None,
                             headers={'User-Agent': 'abeja-platform-sdk/{}'.format(VERSION)}, timeout=30, data=None,
                             json={'statistics': {'progress_percentage': 0.5, 'key1': 'value1'}})

    @mock.patch('abeja.common.connection.Connection.request',
                side_effect=BadRequest('foo', 'bar', 400, 'https://api.abeja.io/'))
    def test_update_statistics_raise_BadRequest(self, m):
        # check: don't raise Exception when model-api returns 400 Bad-Request
        logger_mock = mock.MagicMock()
        self.client.logger = logger_mock
        try:
            statistics = Statistics(progress_percentage=0.5, key1='value1')
            self.client.update_statistics(statistics)
            self.assertEqual(m.call_count, 1)
            url = '{}/organizations/{}/training/definitions/{}/jobs/{}/statistics'.format(
                ABEJA_API_URL, ORGANIZATION_ID, TRAINING_JON_DEFINITION_NAME, TRAINING_JOB_ID)
            m.assert_called_with('POST', url, params=None,
                                 headers={'User-Agent': 'abeja-platform-sdk/{}'.format(VERSION)}, data=None,
                                 json={'statistics': {'progress_percentage': 0.5, 'key1': 'value1'}})
            self.assertEqual(logger_mock.warning.call_count, 1)
            self.assertEqual(logger_mock.exception.call_count, 0)
        except Exception:
            self.fail()

    @mock.patch('abeja.common.connection.Connection.request',
                side_effect=InternalServerError('foo', 'bar', 500, 'https://api.abeja.io/'))
    def test_update_statistics_raise_InternalServerError(self, m):
        # check: don't raise Exception when model-api returns 500 Internal-Server-Error
        logger_mock = mock.MagicMock()
        self.client.logger = logger_mock
        try:
            statistics = Statistics(progress_percentage=0.5, key1='value1')
            self.client.update_statistics(statistics)
            self.assertEqual(m.call_count, 1)
            url = '{}/organizations/{}/training/definitions/{}/jobs/{}/statistics'.format(
                ABEJA_API_URL, ORGANIZATION_ID, TRAINING_JON_DEFINITION_NAME, TRAINING_JOB_ID)
            m.assert_called_with('POST', url, params=None,
                                 headers={'User-Agent': 'abeja-platform-sdk/{}'.format(VERSION)}, data=None,
                                 json={'statistics': {'progress_percentage': 0.5, 'key1': 'value1'}})
            self.assertEqual(logger_mock.warning.call_count, 0)
            self.assertEqual(logger_mock.exception.call_count, 1)
        except Exception:
            self.fail()

    @mock.patch('abeja.common.connection.Connection.request', side_effect=requests.exceptions.ConnectionError())
    def test_update_statistics_raise_ConnectionError(self, m):
        # check: don't raise Exception when model-api returns 500 Internal-Server-Error
        logger_mock = mock.MagicMock()
        self.client.logger = logger_mock
        try:
            statistics = Statistics(progress_percentage=0.5, key1='value1')
            self.client.update_statistics(statistics)
            self.assertEqual(m.call_count, 1)
            url = '{}/organizations/{}/training/definitions/{}/jobs/{}/statistics'.format(
                ABEJA_API_URL, ORGANIZATION_ID, TRAINING_JON_DEFINITION_NAME, TRAINING_JOB_ID)
            m.assert_called_with('POST', url, params=None,
                                 headers={'User-Agent': 'abeja-platform-sdk/{}'.format(VERSION)}, data=None,
                                 json={'statistics': {'progress_percentage': 0.5, 'key1': 'value1'}})
            self.assertEqual(logger_mock.warning.call_count, 0)
            self.assertEqual(logger_mock.exception.call_count, 1)
        except Exception:
            self.fail()

    @mock.patch('abeja.common.connection.Connection.request')
    def test_update_statistics_statistics_none(self, m):
        # check: don't raise Exception
        logger_mock = mock.MagicMock()
        self.client.logger = logger_mock
        try:
            self.client.update_statistics(None)
            m.assert_not_called()
            self.assertEqual(logger_mock.warning.call_count, 1)
            self.assertEqual(logger_mock.exception.call_count, 0)
        except Exception:
            self.fail()

    @mock.patch('abeja.common.connection.Connection.request')
    def test_update_statistics_with_empty_statistics(self, m):
        # check: don't raise Exception
        logger_mock = mock.MagicMock()
        self.client.logger = logger_mock
        try:
            self.client.update_statistics(Statistics())
            m.assert_not_called()
            self.assertEqual(logger_mock.warning.call_count, 1)
            self.assertEqual(logger_mock.exception.call_count, 0)
        except Exception:
            self.fail()
