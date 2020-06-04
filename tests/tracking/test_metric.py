import pytest

from abeja.tracking.metric import Metric


class TestMetric:
    @pytest.mark.parametrize(
        'given,expected',
        [
            ('main/loss', True),
            ('main/acc', True),
            ('test/loss', True),
            ('test/acc', True),
            ('xxx', False)
        ]
    )
    def test_is_scalar(self, given, expected):
        metric = Metric(given, 0.01)
        assert metric.is_scalar() is expected

    @pytest.mark.parametrize(
        'given,expected',
        [
            (('main/loss', 0.1), {'main_loss': 0.1}),
            (('test/loss', 9.8e-06), {'test_loss': 9.8e-06}),
            (('xxx', 123), {'xxx': 123}),
            (('main/acc', float('inf')), {'main_acc': 'Infinity'}),
            (('xxx', float('-inf')), {'xxx': '-Infinity'}),
        ]
    )
    def test_to_dict(self, given, expected):
        metric = Metric(*given)
        assert metric.to_dict() == expected
