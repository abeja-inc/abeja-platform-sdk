from unittest import mock

import pytest

from tools.get_next_rc_version import get_next_rc_version, get_pypi_versions


def test_get_next_rc_version_starts_at_one():
    assert get_next_rc_version('2.3.6', []) == '2.3.6rc1'


def test_get_next_rc_version_increments_highest_matching_rc():
    versions = ['2.3.5', '2.3.5rc9', '2.3.6rc1', '2.3.6rc3', '2.3.7rc8']

    assert get_next_rc_version('2.3.6', versions) == '2.3.6rc4'


def test_get_next_rc_version_rejects_rc_after_final_release():
    with pytest.raises(ValueError, match='final version 2.3.6 already exists'):
        get_next_rc_version('2.3.6', ['2.3.6rc1', '2.3.6'])


@mock.patch('tools.get_next_rc_version.urllib.request.urlopen',
            side_effect=OSError('network unavailable'))
def test_get_pypi_versions_fails_closed(_urlopen):
    with pytest.raises(RuntimeError, match='Could not fetch versions from PyPI'):
        get_pypi_versions()
