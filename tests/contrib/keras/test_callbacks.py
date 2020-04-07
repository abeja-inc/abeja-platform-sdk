from unittest.mock import patch

from abeja import VERSION
from abeja.contrib.keras.callbacks import Statistics

ABEJA_API_URL = 'http://localhost:8080'


class TestStatistics(object):
    def test_init(self):
        cb = Statistics()
        assert cb.client

    @patch('requests.Session.request')
    def test_on_epoch_end(self, m):
        cb = Statistics()
        cb.params = {'epochs': 20}
        cb.on_epoch_end(1, logs={'acc': 0.756, 'loss': 0.078,
                                 'val_acc': 0.914, 'val_loss': 0.393})
        url = '{}/organizations/None/training/definitions/None/jobs/None/statistics'.format(
            ABEJA_API_URL)
        expected_data = {'statistics': {'num_epochs': 20, 'epoch': 2, 'stages': {'train': {
            'accuracy': 0.756, 'loss': 0.078}, 'validation': {'accuracy': 0.914, 'loss': 0.393}}}}
        m.assert_called_once_with('POST', url, params=None,
                                  headers={'User-Agent': 'abeja-platform-sdk/{}'.format(VERSION)},
                                  timeout=30, data=None, json=expected_data)
