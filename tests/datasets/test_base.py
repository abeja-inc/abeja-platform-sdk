import unittest
from abeja.datasets.base import DatasetBase


class TestDatasetBase(unittest.TestCase):
    def test_set_value(self):
        values = {
            'a': 'test',
            'b': 'test'
        }

        class Dataset(DatasetBase):
            pass

        dataset = Dataset()
        dataset._set_values(values)
        self.assertEqual(dataset.a, values['a'])
        self.assertEqual(dataset.b, values['b'])
