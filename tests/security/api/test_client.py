import unittest

import requests_mock

from abeja.security import APIClient


ORGANIZATION_ID = '1111111111111'
CIDR_ID = '305'
SECURITY_RES = {
    "id": "305",
    "description": "Example CIDR",
    "cidr": "192.168.0.0/24",
    "created_at": "2017-04-27T07:49:30Z",
    "updated_at": "2018-02-14T03:14:05Z"
}
SECURITY_LIST_RES = {
    "organization_id": "1111111111111",
    "organization_name": "organization-1178",
    "created_at": "2019-02-19T03:01:49Z",
    "updated_at": "2019-02-19T03:01:49Z",
    "offset": 0,
    "limit": 50,
    "has_next": 'false',
    "cidrs": [
        "192.168.0.0/24"
    ],
}
SECURITY_PAYLOAD = {
    "description": "Example CIDR",
    "cidr": "192.168.0.0/24"
}
CHECK_PAYLOAD = {
    "accessible": 'true',
    "ip_address": "33.222.111.44"
}


class TestAPIClient(unittest.TestCase):

    @requests_mock.Mocker()
    def test_create_ip_address(self, m):
        path = '/organizations/{}/security/cidrs'.format(ORGANIZATION_ID)
        m.post(path, json=SECURITY_RES)

        client = APIClient()
        ret = client.create_ip_address(ORGANIZATION_ID, SECURITY_PAYLOAD)
        self.assertDictEqual(m.request_history[0].json(), SECURITY_PAYLOAD)
        self.assertDictEqual(ret, SECURITY_RES)

    @requests_mock.Mocker()
    def test_get_ip_address(self, m):
        path = '/organizations/{}/security/cidrs/{}'.format(
            ORGANIZATION_ID, CIDR_ID)
        m.get(path, json=SECURITY_RES)

        client = APIClient()
        ret = client.get_ip_address(ORGANIZATION_ID, CIDR_ID)
        self.assertDictEqual(ret, SECURITY_RES)

    @requests_mock.Mocker()
    def test_get_ip_addresses(self, m):
        path = '/organizations/{}/security/cidrs'.format(ORGANIZATION_ID)
        m.get(path, json=SECURITY_LIST_RES)

        client = APIClient()
        ret = client.get_ip_addresses(ORGANIZATION_ID)
        self.assertDictEqual(ret, SECURITY_LIST_RES)

    @requests_mock.Mocker()
    def test_update_ip_address(self, m):
        path = '/organizations/{}/security/cidrs/{}'.format(
            ORGANIZATION_ID, CIDR_ID)
        m.patch(path, json=SECURITY_RES)

        client = APIClient()
        ret = client.update_ip_address(
            ORGANIZATION_ID, CIDR_ID, SECURITY_PAYLOAD)
        self.assertDictEqual(m.request_history[0].json(), SECURITY_PAYLOAD)
        self.assertDictEqual(ret, SECURITY_RES)

    @requests_mock.Mocker()
    def test_delete_ip_address(self, m):
        path = '/organizations/{}/security/cidrs/{}'.format(
            ORGANIZATION_ID, CIDR_ID)
        message_res = {
            "message": "ser-abc1111111111111 deleted"
        }
        m.delete(path, json=message_res)

        client = APIClient()
        ret = client.delete_ip_address(ORGANIZATION_ID, CIDR_ID)
        self.assertDictEqual(ret, message_res)

    @requests_mock.Mocker()
    def test_check_ip_address(self, m):
        path = '/organizations/{}/security/cidrs/check'.format(ORGANIZATION_ID)
        m.post(path, json=CHECK_PAYLOAD)

        client = APIClient()
        ret = client.check_ip_address(ORGANIZATION_ID, CHECK_PAYLOAD)
        self.assertDictEqual(m.request_history[0].json(), CHECK_PAYLOAD)
        self.assertDictEqual(ret, CHECK_PAYLOAD)
