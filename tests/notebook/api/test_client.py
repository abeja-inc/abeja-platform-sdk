import unittest

import requests_mock

from abeja.notebook import APIClient


ORGANIZATION_ID = '1111111111111'
SERVICE_ID = '2222222222222'
JOB_DEFINITION_NAME = 'test-job'
NOTEBOOK_ID = '4444444444444'

NOTEBOOK_RES = {
    "job_definition_id": JOB_DEFINITION_NAME,
    "training_notebook_id": NOTEBOOK_ID,
    "name": "notebook-3",
    "description": None,
    "status": "Pending",
    "status_message": None,
    "instance_type": "cpu-1",
    "image": "abeja-inc/all-cpu:18.10",
    "creator": {
        "updated_at": "2018-01-04T03:02:12Z",
        "role": "admin",
        "is_registered": True,
        "id": "1122334455660",
        "email": "test@abeja.asia",
        "display_name": None,
        "created_at": "2017-05-26T01:38:46Z"
    },
    "created_at": "2018-06-07T04:42:34.913644Z",
    "modified_at": "2018-06-07T04:42:34.913726Z"
}

NOTEBOOK_LIST_RES = [
    NOTEBOOK_RES
]


class TestAPIClient(unittest.TestCase):

    @requests_mock.Mocker()
    def test_create_notebook(self, m):
        path = '/organizations/{}/training/definitions/{}/notebooks'.format(ORGANIZATION_ID, JOB_DEFINITION_NAME)
        m.post(path, json=NOTEBOOK_RES)

        client = APIClient()
        ret = client.create_notebook(ORGANIZATION_ID, JOB_DEFINITION_NAME)
        self.assertDictEqual(m.request_history[0].json(), {})
        self.assertDictEqual(ret, NOTEBOOK_RES)

    @requests_mock.Mocker()
    def test_create_notebook_with_params(self, m):
        path = '/organizations/{}/training/definitions/{}/notebooks'.format(ORGANIZATION_ID, JOB_DEFINITION_NAME)
        m.post(path, json=NOTEBOOK_RES)

        client = APIClient()

        ret = client.create_notebook(
            ORGANIZATION_ID, JOB_DEFINITION_NAME,
            instance_type="gpu-1", image="abeja-inc/all-gpu:18.10"
        )
        expected_payload = {
            "instance_type": "gpu-1",
            "image": 'abeja-inc/all-gpu:18.10'
        }
        self.assertDictEqual(m.request_history[0].json(), expected_payload)
        self.assertDictEqual(ret, NOTEBOOK_RES)

    @requests_mock.Mocker()
    def test_get_notebook(self, m):
        path = '/organizations/{}/training/definitions/{}/notebooks/{}'.format(
            ORGANIZATION_ID, JOB_DEFINITION_NAME, NOTEBOOK_ID)
        m.get(path, json=NOTEBOOK_RES)

        client = APIClient()
        ret = client.get_notebook(ORGANIZATION_ID, JOB_DEFINITION_NAME, NOTEBOOK_ID)
        self.assertDictEqual(ret, NOTEBOOK_RES)

    @requests_mock.Mocker()
    def test_get_notebooks(self, m):
        path = '/organizations/{}/training/definitions/{}/notebooks'.format(ORGANIZATION_ID, JOB_DEFINITION_NAME)
        m.get(path, json=NOTEBOOK_LIST_RES)

        client = APIClient()
        ret = client.get_notebooks(ORGANIZATION_ID, JOB_DEFINITION_NAME)
        self.assertListEqual(ret, NOTEBOOK_LIST_RES)

    @requests_mock.Mocker()
    def test_update_notebook(self, m):
        path = '/organizations/{}/training/definitions/{}/notebooks/{}'.format(
            ORGANIZATION_ID, JOB_DEFINITION_NAME, NOTEBOOK_ID)
        m.put(path, json=NOTEBOOK_RES)

        client = APIClient()
        ret = client.update_notebook(ORGANIZATION_ID, JOB_DEFINITION_NAME, NOTEBOOK_ID)
        self.assertDictEqual(m.request_history[0].json(), {})
        self.assertDictEqual(ret, NOTEBOOK_RES)

    @requests_mock.Mocker()
    def test_update_notebook_with_params(self, m):
        path = '/organizations/{}/training/definitions/{}/notebooks/{}'.format(
            ORGANIZATION_ID, JOB_DEFINITION_NAME, NOTEBOOK_ID)
        m.put(path, json=NOTEBOOK_RES)

        client = APIClient()
        ret = client.update_notebook(
            ORGANIZATION_ID, JOB_DEFINITION_NAME, NOTEBOOK_ID,
            instance_type="gpu-1", image="abeja-inc/all-gpu:18.10"
        )
        expected_payload = {
            "instance_type": "gpu-1",
            "image": 'abeja-inc/all-gpu:18.10'
        }
        self.assertDictEqual(m.request_history[0].json(), expected_payload)
        self.assertDictEqual(ret, NOTEBOOK_RES)

    @requests_mock.Mocker()
    def test_delete_notebook(self, m):
        path = '/organizations/{}/training/definitions/{}/notebooks/{}'.format(
            ORGANIZATION_ID, JOB_DEFINITION_NAME, NOTEBOOK_ID)
        message_res = {
            "message": "abc1111111111111 deleted"
        }
        m.delete(path, json=message_res)

        client = APIClient()
        ret = client.delete_notebook(ORGANIZATION_ID, JOB_DEFINITION_NAME, NOTEBOOK_ID)
        self.assertDictEqual(ret, message_res)

    @requests_mock.Mocker()
    def test_stop_notebook(self, m):
        path = '/organizations/{}/training/definitions/{}/notebooks/{}/stop'.format(
            ORGANIZATION_ID, JOB_DEFINITION_NAME, NOTEBOOK_ID)
        message_res = {
            "message": "abc1111111111111 stopped"
        }
        m.post(path, json=message_res)

        client = APIClient()
        ret = client.stop_notebook(ORGANIZATION_ID, JOB_DEFINITION_NAME, NOTEBOOK_ID)
        self.assertDictEqual(ret, message_res)

    @requests_mock.Mocker()
    def test_start_notebook(self, m):
        path = '/organizations/{}/training/definitions/{}/notebooks/{}/start'.format(
            ORGANIZATION_ID, JOB_DEFINITION_NAME, NOTEBOOK_ID)
        message_res = {
            "message": "abc1111111111111 started"
        }
        m.post(path, json=message_res)

        client = APIClient()
        ret = client.start_notebook(ORGANIZATION_ID, JOB_DEFINITION_NAME, NOTEBOOK_ID)
        self.assertDictEqual(ret, message_res)

    @requests_mock.Mocker()
    def test_get_notebook_recent_logs(self, m):
        path = '/organizations/{}/training/definitions/{}/notebooks/{}/recentlogs'.format(
            ORGANIZATION_ID, JOB_DEFINITION_NAME, NOTEBOOK_ID)
        message_res = {
            "events": [
                {
                    "message": "start executing model with abeja-runtime-python36 (version: 0.X.X)",
                    "timestamp": "2019-10-16T00:00:00.000Z"
                }
            ],
            "next_backward_token": "AAA",
            "next_forward_token": "BBB"
        }
        m.get(path, json=message_res)

        client = APIClient()
        ret = client.get_notebook_recent_logs(ORGANIZATION_ID, JOB_DEFINITION_NAME, NOTEBOOK_ID)
        self.assertDictEqual(ret, message_res)

    @requests_mock.Mocker()
    def test_get_notebook_recent_logs_next_forward_token(self, m):
        path = '/organizations/{}/training/definitions/{}/notebooks/{}/recentlogs?next_forward_token=AAA'.format(
            ORGANIZATION_ID, JOB_DEFINITION_NAME, NOTEBOOK_ID)
        message_res = {
            "events": [
                {
                    "message": "start executing model with abeja-runtime-python36 (version: 0.X.X)",
                    "timestamp": "2019-10-16T00:00:00.000Z"
                }
            ],
            "next_backward_token": "AAA",
            "next_forward_token": "BBB"
        }
        m.get(path, json=message_res)

        client = APIClient()
        ret = client.get_notebook_recent_logs(
            ORGANIZATION_ID, JOB_DEFINITION_NAME, NOTEBOOK_ID,
            next_forward_token="AAA"
        )
        self.assertDictEqual(ret, message_res)

    @requests_mock.Mocker()
    def test_get_notebook_recent_logs_next_backward_token(self, m):
        path = '/organizations/{}/training/definitions/{}/notebooks/{}/recentlogs?next_backward_token=BBB'.format(
            ORGANIZATION_ID, JOB_DEFINITION_NAME, NOTEBOOK_ID)
        message_res = {
            "events": [
                {
                    "message": "start executing model with abeja-runtime-python36 (version: 0.X.X)",
                    "timestamp": "2019-10-16T00:00:00.000Z"
                }
            ],
            "next_backward_token": "AAA",
            "next_forward_token": "BBB"
        }
        m.get(path, json=message_res)

        client = APIClient()
        ret = client.get_notebook_recent_logs(
            ORGANIZATION_ID, JOB_DEFINITION_NAME, NOTEBOOK_ID,
            next_backward_token="BBB"
        )
        self.assertDictEqual(ret, message_res)
