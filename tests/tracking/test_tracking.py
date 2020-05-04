import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

from abeja import VERSION as SDK_VERSION
from abeja.common.connection import Connection
from abeja.exceptions import BadRequest, InvalidPathException
from abeja.tracking import Tracking


ABEJA_API_URL = 'http://localhost:8080'
ORGANIZATION_ID = '1111111111111'
JOB_DEFINITION_NAME = 'dummy_job_def_name'
TRAINING_MODEL_ID = "1111111111111"
JOB_DEFINITION_ID = '1111111111111'
TRAINING_JOB_ID = '1111111111111'
DESCRIPTION = "this is description of the model"
USER_PARAMETERS = {
    'key': 'value'
}
METRICS = {
    'metric': 1.00
}
TRAINING_MODEL_RES = {
    "training_model_id": TRAINING_MODEL_ID,
    "job_definition_id": JOB_DEFINITION_ID,
    "training_job_id": TRAINING_JOB_ID,
    "user_parameters": USER_PARAMETERS,
    "metrics": METRICS,
    "description": DESCRIPTION,
    "archived": False,
    "exec_env": "cloud",
    "created_at": "2018-01-01T00:00:00.00000Z",
    "modified_at": "2018-01-01T00:00:00.00000Z"
}

PATCHED_ENVIRON = {
    'ABEJA_ORGANIZATION_ID': ORGANIZATION_ID,
    'TRAINING_JOB_DEFINITION_NAME': JOB_DEFINITION_NAME,
    'TRAINING_JOB_ID': TRAINING_JOB_ID
}


class TestTracking(unittest.TestCase):
    @mock.patch.dict('os.environ', PATCHED_ENVIRON)
    def setUp(self):
        Connection.BASE_URL = ABEJA_API_URL

    @mock.patch('tensorboardX.SummaryWriter.flush')
    @mock.patch('abeja.training.api.client.APIClient.get_training_job')
    @mock.patch('requests.Session.request')
    @mock.patch.dict('os.environ', PATCHED_ENVIRON)
    def test_tracking(self, m, m_get_training_job, m_flush):
        m_get_training_job.return_value = {}
        m_flush.return_value = None

        with tempfile.NamedTemporaryFile(suffix='.zip') as zipfile:
            url = '{}/organizations/{}/training/definitions/{}/models'.format(
                ABEJA_API_URL, ORGANIZATION_ID, JOB_DEFINITION_NAME)
            parameters = {
                'training_job_id': TRAINING_JOB_ID,
                'description': 'STEP 1. {}'.format(DESCRIPTION),
                'user_parameters': USER_PARAMETERS,
                'metrics': METRICS,
            }
            params = json.dumps(parameters).encode()

            tracking = Tracking()
            tracking.log_params(USER_PARAMETERS)
            tracking.log_metrics(METRICS)
            tracking.log_description(description=DESCRIPTION)
            tracking.log_step(step=1)
            tracking.log_artifact(filepath=zipfile.name)
            tracking.flush()

            m_method, m_url = m.call_args[0]
            self.assertEqual('POST', m_method)
            self.assertEqual(url, m_url)

            body = m.call_args[1]
            self.assertIsNone(body['data'])
            self.assertIsNone(body['json'])
            self.assertIsNone(body['params'])
            self.assertDictEqual({'User-Agent': 'abeja-platform-sdk/{}'.format(SDK_VERSION)}, body['headers'])
            self.assertEqual(30, body['timeout'])
            self.assertIn('model_data', body['files'])
            self.assertIn('parameters', body['files'])
            self.assertEqual(params, body['files']['parameters'][1].read())

            self.assertEqual(1, m_flush.call_count)

    @mock.patch('tensorboardX.SummaryWriter.flush')
    @mock.patch('abeja.training.api.client.APIClient.get_training_job')
    @mock.patch('requests.Session.request')
    @mock.patch.dict('os.environ', PATCHED_ENVIRON)
    def test_tracking_2(self, m, m_get_training_job, m_flush):
        m_get_training_job.return_value = {}
        m_flush.return_value = None

        with tempfile.NamedTemporaryFile(suffix='.zip') as zipfile:
            url = '{}/organizations/{}/training/definitions/{}/models'.format(
                ABEJA_API_URL, ORGANIZATION_ID, JOB_DEFINITION_NAME)
            parameters = {
                'training_job_id': TRAINING_JOB_ID,
                'description': 'STEP 1. {}'.format(DESCRIPTION),
                'user_parameters': USER_PARAMETERS,
                'metrics': METRICS,
            }
            params = json.dumps(parameters).encode()

            with Tracking() as tracking:
                for k, v in USER_PARAMETERS.items():
                    tracking.log_param(k, v)
                for k, v in METRICS.items():
                    tracking.log_metric(k, v)
                tracking.log_description(description=DESCRIPTION)
                tracking.log_step(step=1)
                tracking.log_artifact(filepath=zipfile.name)

            m_method, m_url = m.call_args[0]
            self.assertEqual('POST', m_method)
            self.assertEqual(url, m_url)

            body = m.call_args[1]
            self.assertIsNone(body['data'])
            self.assertIsNone(body['json'])
            self.assertIsNone(body['params'])
            self.assertDictEqual({'User-Agent': 'abeja-platform-sdk/{}'.format(SDK_VERSION)}, body['headers'])
            self.assertEqual(30, body['timeout'])
            self.assertIn('model_data', body['files'])
            self.assertIn('parameters', body['files'])
            self.assertEqual(params, body['files']['parameters'][1].read())

            self.assertEqual(1, m_flush.call_count)

    def test_tracking_invalid(self):
        tracking = Tracking()
        with self.assertRaises(TypeError):
            tracking.log_step('val')
        with self.assertRaises(TypeError):
            tracking.log_step(None)

        with self.assertRaises(TypeError):
            tracking.log_description(None)

        with self.assertRaises(TypeError):
            tracking.log_param('key', None)

        with self.assertRaises(TypeError):
            tracking.log_params({'key': None})

        with self.assertRaises(TypeError):
            tracking.log_metric('key', 'val')
        with self.assertRaises(TypeError):
            tracking.log_metric('key', None)

        with self.assertRaises(TypeError):
            tracking.log_metrics({'key': 'val'})
        with self.assertRaises(TypeError):
            tracking.log_metrics({'key': None})

        with self.assertRaises(InvalidPathException):
            tracking.log_artifact('dummy')

    @mock.patch('builtins.print')
    def test_tracking_without_artifact(self, mock_print):
        tracking = Tracking()
        for k, v in USER_PARAMETERS.items():
            tracking.log_param(k, v)
        for k, v in METRICS.items():
            tracking.log_metric(k, v)
        tracking.log_description(description=DESCRIPTION)
        tracking.log_step(step=1)
        tracking.flush()
        mock_print.assert_any_call('No output. Need to add "artifact" by "log_artifact()".')

    @mock.patch('builtins.print')
    def test_tracking_without_org_jobdef_job(self, mock_print):
        Tracking()
        mock_print.assert_any_call(
            'WARNING: No params/metrics/artifact will be uploaded to ABEJA Platform. '
            'Please specify "ABEJA_ORGANIZATION_ID", "TRAINING_JOB_DEFINITION_NAME" '
            'and "TRAINING_JOB_ID" for uploading.')

    @mock.patch('abeja.training.api.client.APIClient.get_training_job',
                side_effect=BadRequest('foo', 'bar', 400, 'https://api.abeja.io/'))
    @mock.patch.dict('os.environ', PATCHED_ENVIRON)
    def test_tracking_error_on_get_training_job(self, m_get_training_job):
        with self.assertRaises(BadRequest):
            Tracking()

    @mock.patch('abeja.training.api.client.APIClient.get_training_job')
    @mock.patch('abeja.models.api.client.APIClient.create_training_model',
                side_effect=BadRequest('foo', 'bar', 400, 'https://api.abeja.io/'))
    @mock.patch.dict('os.environ', PATCHED_ENVIRON)
    def test_tracking_error_on_create_training_model(self, m_create_training_model, m_get_training_job):
        m_get_training_job.return_value = {}

        with self.assertRaises(BadRequest):
            with tempfile.NamedTemporaryFile(suffix='.zip') as zipfile:
                tracking = Tracking()
                tracking.log_artifact(filepath=zipfile.name)
                tracking.flush()

    @mock.patch('abeja.training.api.client.APIClient.get_training_job')
    @mock.patch('abeja.models.api.client.APIClient.create_training_model')
    @mock.patch('abeja.training.api.client.APIClient.update_statistics',
                side_effect=BadRequest('foo', 'bar', 400, 'https://api.abeja.io/'))
    @mock.patch.dict('os.environ', PATCHED_ENVIRON)
    def test_tracking_error_on_update_statistics(
            self, m_update_statistics, m_create_training_model, m_get_training_job):
        m_get_training_job.return_value = {}
        tracking = Tracking(total_steps=10)
        tracking.log_step(1)
        tracking.flush()
        self.assertEqual(1, m_update_statistics.call_count)

    @mock.patch('tensorboardX.SummaryWriter.add_scalar')
    def test_tracking_summary_writer(self, m_add_scalar):
        m_add_scalar.return_value = None
        with Tracking() as tk:
            tk.log_step(1)
            tk.log_metric(key='main/acc', value=0.5)
            tk.log_metric(key='main/loss', value=0.5)
            tk.log_metric(key='test/acc', value=0.5)
            tk.log_metric(key='test/loss', value=0.5)
            tk.log_metric(key='hoge/fuga', value=0.5)
        self.assertEqual(4, m_add_scalar.call_count)

    @mock.patch('abeja.training.api.client.APIClient.get_training_job')
    @mock.patch('abeja.models.api.client.APIClient.create_training_model')
    @mock.patch('abeja.training.api.client.APIClient.update_statistics')
    @mock.patch.dict('os.environ', PATCHED_ENVIRON)
    def test_tracking_statistics(self, m_update_statistics, m_create_training_model, m_get_training_job):
        for i in range(2):
            with Tracking(total_steps=10) as tk:
                tk.log_step(i + 1)
                tk.log_metric(key='main/acc', value=0.5)
                tk.log_metric(key='main/loss', value=0.5)
                tk.log_metric(key='test/acc', value=0.5)
                tk.log_metric(key='test/loss', value=0.5)
                tk.log_param(key='dummy', value='dummy')
        self.assertEqual(2, m_update_statistics.call_count)
        expect = {
            'dummy': 'dummy',
            'accuracy': 0.5,
            'loss': 0.5
        }
        self.assertDictEqual(expect, m_update_statistics.call_args[1]['statistics']['stages']['train'])
        self.assertDictEqual(expect, m_update_statistics.call_args[1]['statistics']['stages']['validation'])

    @mock.patch('abeja.training.api.client.APIClient.update_statistics')
    def test_tracking_statistics_not_work(self, m_update_statistics):
        for i in range(2):
            with Tracking(total_steps=10) as tk:
                tk.log_step(i + 1)
                tk.log_metric(key='main/acc', value=0.5)
                tk.log_metric(key='main/loss', value=0.5)
                tk.log_metric(key='test/acc', value=0.5)
                tk.log_metric(key='test/loss', value=0.5)
        self.assertEqual(0, m_update_statistics.call_count)

    @mock.patch('abeja.training.api.client.APIClient.get_training_job')
    @mock.patch('requests.Session.request')
    @mock.patch.dict('os.environ', PATCHED_ENVIRON)
    def test_tracking_delete_after_flush(self, m, m_get_training_job):
        m_get_training_job.return_value = {}

        zipfile = tempfile.NamedTemporaryFile(suffix='.zip')
        tracking = Tracking()
        tracking.log_artifact(filepath=zipfile.name, delete_flag=True)
        tracking.flush()

        self.assertEqual(1, m.call_count)
        self.assertFalse(Path(zipfile.name).exists())
