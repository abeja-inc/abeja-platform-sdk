import unittest

import requests_mock

from abeja.opsbeellm.deployment import APIClient
from abeja.exceptions import BadRequest

ACCOUNT_ID = '1111111111111'
ORGANIZATION_ID = '2222222222222'
DEPLOYMENT_ID = '3333333333333'
DEPLOYMENT_NAME = 'deployment A'
DEPLOYMENT_DESCRIPTION = 'deployment A'

DEPLOYMENT_QA_RES = {
    'id': DEPLOYMENT_ID,
    'account_id': ACCOUNT_ID,
    'organization_id': ORGANIZATION_ID,
    'name': DEPLOYMENT_NAME,
    'description': DEPLOYMENT_DESCRIPTION,
    'type': 'qa',
    'created_at': "2023-12-14T04:42:34.913644Z",
    'updated_at': "2023-12-14T04:42:34.913644Z",
}
DEPLOYMENT_CHAT_RES = {
    'id': DEPLOYMENT_ID,
    'account_id': ACCOUNT_ID,
    'organization_id': ORGANIZATION_ID,
    'name': DEPLOYMENT_NAME,
    'description': DEPLOYMENT_DESCRIPTION,
    'type': 'chat',
    'created_at': "2023-12-14T04:42:34.913644Z",
    'updated_at': "2023-12-14T04:42:34.913644Z",
}
DEPLOYMENTS_RES = {
    'account_id': ACCOUNT_ID,
    'organization_id': ORGANIZATION_ID,
    'deployments': [
        DEPLOYMENT_QA_RES,
        DEPLOYMENT_CHAT_RES,
    ],
    'has_next': False, 'limit': 10, 'offset': 0,
}


class TestOpsBeeLLMAPIClient(unittest.TestCase):

    @requests_mock.Mocker()
    def test_get_deployments(self, m):
        # get-deployments-api mock
        path = '/accounts/{}/organizations/{}/deployments'.format(
            ACCOUNT_ID,
            ORGANIZATION_ID,
        )
        m.get(path, json=DEPLOYMENTS_RES)

        # unit test
        client = APIClient()
        ret = client.get_deployments(
            ACCOUNT_ID,
            ORGANIZATION_ID,
        )
        self.assertDictEqual(ret, DEPLOYMENTS_RES)

    @requests_mock.Mocker()
    def test_get_deployment(self, m):
        # get-deployment-api mock
        path = '/accounts/{}/organizations/{}/deployments/{}'.format(
            ACCOUNT_ID,
            ORGANIZATION_ID,
            DEPLOYMENT_ID,
        )
        m.get(path, json=DEPLOYMENT_QA_RES)

        # unit test
        client = APIClient()
        ret = client.get_deployment(
            ACCOUNT_ID,
            ORGANIZATION_ID,
            DEPLOYMENT_ID
        )
        self.assertDictEqual(ret, DEPLOYMENT_QA_RES)

    @requests_mock.Mocker()
    def test_create_deployment(self, m):
        # create-deployment-api mock
        path = '/accounts/{}/organizations/{}/deployments'.format(
            ACCOUNT_ID,
            ORGANIZATION_ID,
        )
        m.post(path, json=DEPLOYMENT_QA_RES)

        # unit test
        client = APIClient()
        ret = client.create_deployment(
            ACCOUNT_ID,
            ORGANIZATION_ID,
            name=DEPLOYMENT_NAME,
            description=DEPLOYMENT_DESCRIPTION,
            type='qa'
        )
        expected_payload = {
            'name': DEPLOYMENT_NAME,
            'description': DEPLOYMENT_DESCRIPTION,
            'type': 'qa',
        }

        self.assertDictEqual(m.request_history[0].json(), expected_payload)
        self.assertDictEqual(ret, DEPLOYMENT_QA_RES)

        with self.assertRaises(BadRequest) as e:
            client.create_deployment(
                ACCOUNT_ID,
                ORGANIZATION_ID,
                name=None,
                description=None,
                type=None,
            )
        self.assertEqual(e.exception.error_description, '"name" is necessary')

        with self.assertRaises(BadRequest) as e:
            client.create_deployment(
                ACCOUNT_ID,
                ORGANIZATION_ID,
                name=DEPLOYMENT_NAME,
                description=None,
                type=None,
            )
        self.assertEqual(e.exception.error_description, '"type" is necessary')

        with self.assertRaises(BadRequest) as e:
            client.create_deployment(
                ACCOUNT_ID,
                ORGANIZATION_ID,
                name=DEPLOYMENT_NAME,
                description=None,
                type='llm',
            )
        self.assertEqual(e.exception.error_description, '"type" need to "qa" or "chat"')

    @requests_mock.Mocker()
    def test_update_deployment(self, m):
        # update-deployment-api mock
        path = '/accounts/{}/organizations/{}/deployments/{}'.format(
            ACCOUNT_ID,
            ORGANIZATION_ID,
            DEPLOYMENT_ID,
        )
        m.patch(path, json=DEPLOYMENT_QA_RES)

        # unit test
        client = APIClient()
        ret = client.update_deployment(
            ACCOUNT_ID,
            ORGANIZATION_ID,
            DEPLOYMENT_ID,
            name=DEPLOYMENT_NAME,
            description=DEPLOYMENT_DESCRIPTION,
        )
        expected_payload = {
            'name': DEPLOYMENT_NAME,
            'description': DEPLOYMENT_DESCRIPTION,
        }

        self.assertDictEqual(m.request_history[0].json(), expected_payload)
        self.assertDictEqual(ret, DEPLOYMENT_QA_RES)

        with self.assertRaises(BadRequest) as e:
            client.update_deployment(
                ACCOUNT_ID,
                ORGANIZATION_ID,
                DEPLOYMENT_ID,
                name=None,
                description=None,
            )
        self.assertEqual(e.exception.error_description, '"name" is necessary')

    @requests_mock.Mocker()
    def test_delete_deployment(self, m):
        # delete-deployment-api mock
        path = '/accounts/{}/organizations/{}/deployments/{}'.format(
            ACCOUNT_ID,
            ORGANIZATION_ID,
            DEPLOYMENT_ID
        )
        res = {
            'message': f'deployment {DEPLOYMENT_ID} was deleted.'
        }
        m.delete(path, json=res)

        # unit test
        client = APIClient()
        ret = client.delete_deployment(
            ACCOUNT_ID,
            ORGANIZATION_ID,
            DEPLOYMENT_ID
        )
        self.assertDictEqual(ret, res)
