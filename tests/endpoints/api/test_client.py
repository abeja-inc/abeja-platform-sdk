import unittest

import requests_mock

from abeja.endpoints import APIClient


ORGANIZATION_ID = '1111111111111'
SERVICE_ID = 'ser-abc1111111111111'
UPDATED_SERVICE_ID = 'ser-abc2222222222222'
DEPLOYMENT_ID = '3333333333333'
ENDPOINT_ID = 'pnt-abc1111111111111'
CUSTOM_ALIAS = 'default'
ENDPOINT_RES = {
    'endpoint_id': ENDPOINT_ID,
    'custom_alias': CUSTOM_ALIAS,
    'service_id': SERVICE_ID
}
ENDPOINT_LIST_RES = [
    ENDPOINT_RES
]


class TestAPIClient(unittest.TestCase):

    @requests_mock.Mocker()
    def test_create_endpoint(self, m):
        path = '/organizations/{}/deployments/{}/endpoints'.format(ORGANIZATION_ID, DEPLOYMENT_ID)
        m.post(path, json=ENDPOINT_RES)

        client = APIClient()
        ret = client.create_endpoint(ORGANIZATION_ID, DEPLOYMENT_ID, SERVICE_ID, CUSTOM_ALIAS)

        expected_payload = {
            'service_id': SERVICE_ID,
            'custom_alias': CUSTOM_ALIAS
        }
        self.assertDictEqual(m.request_history[0].json(), expected_payload)
        self.assertDictEqual(ret, ENDPOINT_RES)

    @requests_mock.Mocker()
    def test_get_endpoint(self, m):
        path = '/organizations/{}/deployments/{}/endpoints/{}'.format(ORGANIZATION_ID, DEPLOYMENT_ID, ENDPOINT_ID)
        m.get(path, json=ENDPOINT_RES)

        client = APIClient()
        ret = client.get_endpoint(ORGANIZATION_ID, DEPLOYMENT_ID, ENDPOINT_ID)
        self.assertDictEqual(ret, ENDPOINT_RES)

    @requests_mock.Mocker()
    def test_get_endpoints(self, m):
        path = '/organizations/{}/deployments/{}/endpoints'.format(ORGANIZATION_ID, DEPLOYMENT_ID)
        m.get(path, json=ENDPOINT_LIST_RES)

        client = APIClient()
        ret = client.get_endpoints(ORGANIZATION_ID, DEPLOYMENT_ID)
        self.assertListEqual(ret, ENDPOINT_LIST_RES)

    @requests_mock.Mocker()
    def test_update_endpoint(self, m):
        path = '/organizations/{}/deployments/{}/endpoints/{}'.format(ORGANIZATION_ID, DEPLOYMENT_ID, ENDPOINT_ID)
        expected_res = {
            "message": "{} updated".format(ENDPOINT_ID)
        }
        m.patch(path, json=expected_res)

        client = APIClient()
        ret = client.update_endpoint(ORGANIZATION_ID, DEPLOYMENT_ID, ENDPOINT_ID, UPDATED_SERVICE_ID)
        self.assertDictEqual(ret, expected_res)

    @requests_mock.Mocker()
    def test_delete_endpoint(self, m):
        path = '/organizations/{}/deployments/{}/endpoints/{}'.format(ORGANIZATION_ID, DEPLOYMENT_ID, ENDPOINT_ID)
        message_res = {
            "message": "{} deleted".format(ENDPOINT_ID)
        }
        m.delete(path, json=message_res)

        client = APIClient()
        ret = client.delete_endpoint(ORGANIZATION_ID, DEPLOYMENT_ID, ENDPOINT_ID)
        self.assertDictEqual(ret, message_res)
