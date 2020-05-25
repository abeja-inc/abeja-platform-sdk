import unittest

from mock import MagicMock

from abeja.datasets.api.client import APIClient


class TestAPIClient(unittest.TestCase):
    def setUp(self):
        self.organization_id = '1230000000000'
        self.dataset_id = '1234567890123'
        self.name = 'test dataset'
        self.type = 'test type'
        self.props = {'label': 'test'}
        self.dataset_item_id = '1234567890000'
        self.attributes = {}
        self.source_data = [
            {
                'data_type': 'image/jpeg',
                'data_uri': 'datalake://1200123803688/20170815T044617-f20dde80-1e3b-4496-bc06-1b63b026b872',
                'height': 500,
                'width': 200}]

    def test_create_dataset(self):
        mock_conn = MagicMock()
        client = APIClient()
        client._connection = mock_conn
        client.create_dataset(self.organization_id,
                              self.name, self.type, self.props)
        params = {
            'name': self.name,
            'type': self.type,
            'props': self.props
        }
        path = '/organizations/{}/datasets'.format(self.organization_id)
        mock_conn.api_request.assert_called_once_with(method='POST', path=path,
                                                      json=params)

    def test_get_dataset(self):
        mock_conn = MagicMock()
        client = APIClient()
        client._connection = mock_conn
        client.get_dataset(self.organization_id, self.dataset_id)
        path = '/organizations/{}/datasets/{}'.format(
            self.organization_id, self.dataset_id)
        mock_conn.api_request.assert_called_once_with(method='GET', path=path)

    def test_list_datasets(self):
        mock_conn = MagicMock()
        client = APIClient()
        client._connection = mock_conn
        client.list_datasets(self.organization_id)
        path = '/organizations/{}/datasets'.format(self.organization_id)
        mock_conn.api_request.assert_called_once_with(method='GET',
                                                      path=path,
                                                      params={})

    def test_list_datasets_with_params(self):
        mock_conn = MagicMock()
        client = APIClient()
        client._connection = mock_conn
        next_token = 'dummy'
        client.list_datasets(
            self.organization_id,
            max_results=100,
            next_token=next_token)
        path = '/organizations/{}/datasets'.format(self.organization_id)
        mock_conn.api_request.assert_called_once_with(
            method='GET', path=path, params={
                'max_results': 100, 'next_token': next_token})

    def test_delete_dataset(self):
        mock_conn = MagicMock()
        client = APIClient()
        client._connection = mock_conn
        client.delete_dataset(self.organization_id, self.dataset_id)
        path = '/organizations/{}/datasets/{}'.format(
            self.organization_id, self.dataset_id)
        mock_conn.api_request.assert_called_once_with(
            method='DELETE', path=path)

    def test_create_datatest_item(self):
        mock_conn = MagicMock()
        client = APIClient()
        client._connection = mock_conn
        client.create_dataset_item(self.organization_id, self.dataset_id,
                                   self.source_data,
                                   self.attributes)
        path = '/organizations/{}/datasets/{}/items'.format(
            self.organization_id, self.dataset_id)
        params = {
            'attributes': self.attributes,
            'source_data': self.source_data
        }
        mock_conn.api_request.assert_called_once_with(method='POST',
                                                      path=path,
                                                      json=params)

    def test_get_datatest_item(self):
        mock_conn = MagicMock()
        client = APIClient()
        client._connection = mock_conn
        client.get_dataset_item(self.organization_id, self.dataset_id,
                                self.dataset_item_id)
        path = '/organizations/{}/datasets/{}/items/{}'.format(
            self.organization_id, self.dataset_id, self.dataset_item_id)
        mock_conn.api_request.assert_called_once_with(method='GET',
                                                      path=path)

    def test_list_datatest_items(self):
        mock_conn = MagicMock()
        client = APIClient()
        client._connection = mock_conn
        client.list_dataset_items(self.organization_id, self.dataset_id)
        path = '/organizations/{}/datasets/{}/items'.format(
            self.organization_id, self.dataset_id)
        mock_conn.api_request.assert_called_once_with(method='GET',
                                                      path=path,
                                                      params={})

    def test_list_datatest_items_with_params(self):
        mock_conn = MagicMock()
        client = APIClient()
        client._connection = mock_conn
        params = {'preceding_id': 1}
        client.list_dataset_items(
            self.organization_id, self.dataset_id, params)
        path = '/organizations/{}/datasets/{}/items'.format(
            self.organization_id, self.dataset_id)
        mock_conn.api_request.assert_called_once_with(method='GET',
                                                      path=path,
                                                      params=params)

    def test_delete_datatest_item(self):
        mock_conn = MagicMock()
        client = APIClient()
        client._connection = mock_conn
        client.delete_dataset_item(self.organization_id, self.dataset_id,
                                   self.dataset_item_id)
        path = '/organizations/{}/datasets/{}/items/{}'.format(
            self.organization_id, self.dataset_id, self.dataset_item_id)
        mock_conn.api_request.assert_called_once_with(method='DELETE',
                                                      path=path)
