import pytest

from abeja.registry import APIClient


ORGANIZATION_ID = '1111111111111'
REPOSITORY_ID = '2222222222222'
REPOSITORY_NAME = 'sample_repository'
REPOSITORY_DESCRIPTION = 'this is sample repository'
REGISTRY_RES = {
    "id": REPOSITORY_ID,
    "organization_id": ORGANIZATION_ID,
    "name": REPOSITORY_NAME,
    "description": REPOSITORY_DESCRIPTION,
    "tags": [],
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
    "updated_at": "2018-06-07T04:42:34.913726Z"
}


class TestRegistryAPIClient:

    @pytest.mark.parametrize(
        'name,description,expected',
        [
            (REPOSITORY_NAME, REPOSITORY_DESCRIPTION, {
                'name': REPOSITORY_NAME, 'description': REPOSITORY_DESCRIPTION}),
            (REPOSITORY_NAME, None, {'name': REPOSITORY_NAME})
        ]
    )
    def test_create_repository(self, requests_mock, name, description, expected):
        path = '/organizations/{}/registry/repositories'.format(ORGANIZATION_ID)
        requests_mock.post(path, json=REGISTRY_RES)

        client = APIClient()
        client.create_repository(ORGANIZATION_ID, name, description)

        actual_request = requests_mock.request_history[0]

        actual_payload = actual_request.json()
        assert actual_payload == expected

    @pytest.mark.parametrize(
        'limit,offset,expected',
        [
            (100, 1, {'limit=100', 'offset=1'}),
            (100, None, {'limit=100'}),
            (None, 1, {'offset=1'}),
            (None, None, {''}),
        ]
    )
    def test_get_repositories(self, requests_mock, limit, offset, expected):
        path = '/organizations/{}/registry/repositories'.format(ORGANIZATION_ID)
        requests_mock.get(path, json=REGISTRY_RES)

        client = APIClient()
        client.get_repositories(
            ORGANIZATION_ID, limit, offset)

        actual_request = requests_mock.request_history[0]

        assert set(actual_request.query.split('&')) == expected

    def test_get_repository(self, requests_mock):
        path = '/organizations/{}/registry/repositories/{}'.format(
            ORGANIZATION_ID, REPOSITORY_ID)
        requests_mock.get(path, json=REGISTRY_RES)

        client = APIClient()
        client.get_repository(ORGANIZATION_ID, REPOSITORY_ID)

    def test_delete_repository(self, requests_mock):
        path = '/organizations/{}/registry/repositories/{}'.format(
            ORGANIZATION_ID, REPOSITORY_ID)
        requests_mock.delete(path, json=REGISTRY_RES)

        client = APIClient()
        client.delete_repository(ORGANIZATION_ID, REPOSITORY_ID)

    @pytest.mark.parametrize(
        'limit,offset,expected',
        [
            (100, 1, {'limit=100', 'offset=1'}),
            (100, None, {'limit=100'}),
            (None, 1, {'offset=1'}),
            (None, None, {''}),
        ]
    )
    def test_get_repository_tags(self, requests_mock, limit, offset, expected):
        path = '/organizations/{}/registry/repositories/{}/tags'.format(
            ORGANIZATION_ID, REPOSITORY_ID)
        requests_mock.get(path, json=REGISTRY_RES)

        client = APIClient()
        client.get_repository_tags(
            ORGANIZATION_ID, REPOSITORY_ID, limit, offset)

        actual_request = requests_mock.request_history[0]

        assert set(actual_request.query.split('&')) == expected
