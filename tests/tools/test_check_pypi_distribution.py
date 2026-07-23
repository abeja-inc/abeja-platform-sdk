import hashlib
import json
from unittest import mock
from urllib.error import HTTPError

import pytest

from tools.check_pypi_distribution import get_distribution_state


def pypi_response(filename, digest, yanked=False):
    response = mock.MagicMock()
    response.__enter__.return_value.read.return_value = json.dumps({
        'urls': [{
            'filename': filename,
            'digests': {'sha256': digest},
            'yanked': yanked,
        }],
    }).encode()
    return response


def test_distribution_state_is_missing_for_unknown_release(tmp_path):
    distribution = tmp_path / 'abeja_sdk-2.3.6-py3-none-any.whl'
    distribution.write_bytes(b'wheel')
    error = HTTPError('https://pypi.example', 404, 'Not Found', None, None)

    state = get_distribution_state(
        'abeja-sdk',
        '2.3.6',
        [distribution],
        urlopen=mock.Mock(side_effect=error),
    )

    assert state == 'missing'


def test_distribution_state_fails_closed_for_pypi_error(tmp_path):
    distribution = tmp_path / 'abeja_sdk-2.3.6-py3-none-any.whl'
    distribution.write_bytes(b'wheel')
    error = HTTPError(
        'https://pypi.example',
        500,
        'Internal Server Error',
        None,
        None,
    )

    with pytest.raises(RuntimeError, match='Could not fetch'):
        get_distribution_state(
            'abeja-sdk',
            '2.3.6',
            [distribution],
            urlopen=mock.Mock(side_effect=error),
        )


def test_distribution_state_fails_closed_for_malformed_json(tmp_path):
    distribution = tmp_path / 'abeja_sdk-2.3.6-py3-none-any.whl'
    distribution.write_bytes(b'wheel')
    response = mock.MagicMock()
    response.__enter__.return_value.read.return_value = b'not-json'

    with pytest.raises(RuntimeError, match='Could not fetch'):
        get_distribution_state(
            'abeja-sdk',
            '2.3.6',
            [distribution],
            urlopen=mock.Mock(return_value=response),
        )


def test_distribution_state_fails_closed_for_json_null(tmp_path):
    distribution = tmp_path / 'abeja_sdk-2.3.6-py3-none-any.whl'
    distribution.write_bytes(b'wheel')
    response = mock.MagicMock()
    response.__enter__.return_value.read.return_value = b'null'

    with pytest.raises(RuntimeError, match='invalid JSON object'):
        get_distribution_state(
            'abeja-sdk',
            '2.3.6',
            [distribution],
            urlopen=mock.Mock(return_value=response),
        )


def test_distribution_state_is_identical_for_matching_digest(tmp_path):
    distribution = tmp_path / 'abeja_sdk-2.3.6-py3-none-any.whl'
    content = b'wheel'
    distribution.write_bytes(content)
    digest = hashlib.sha256(content).hexdigest()

    state = get_distribution_state(
        'abeja-sdk',
        '2.3.6',
        [distribution],
        urlopen=mock.Mock(return_value=pypi_response(distribution.name, digest)),
    )

    assert state == 'identical'


def test_distribution_state_rejects_different_digest(tmp_path):
    distribution = tmp_path / 'abeja_sdk-2.3.6-py3-none-any.whl'
    distribution.write_bytes(b'wheel')

    with pytest.raises(RuntimeError, match='different or missing files'):
        get_distribution_state(
            'abeja-sdk',
            '2.3.6',
            [distribution],
            urlopen=mock.Mock(
                return_value=pypi_response(distribution.name, 'different')
            ),
        )


def test_distribution_state_rejects_yanked_wheel(tmp_path):
    distribution = tmp_path / 'abeja_sdk-2.3.6-py3-none-any.whl'
    content = b'wheel'
    distribution.write_bytes(content)
    digest = hashlib.sha256(content).hexdigest()

    with pytest.raises(RuntimeError, match='files are yanked'):
        get_distribution_state(
            'abeja-sdk',
            '2.3.6',
            [distribution],
            urlopen=mock.Mock(
                return_value=pypi_response(
                    distribution.name,
                    digest,
                    yanked=True,
                )
            ),
        )
