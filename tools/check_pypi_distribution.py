#!/usr/bin/env python3
"""Check whether local distributions are already published unchanged on PyPI."""

import argparse
import hashlib
import json
import sys
import urllib.request
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import quote


def get_pypi_release_files(package_name, version, urlopen=None):
    """Return PyPI filename-to-SHA256 mappings, or None for a missing release."""
    opener = urlopen or urllib.request.urlopen
    package = quote(package_name, safe='')
    release = quote(version, safe='')
    url = f'https://pypi.org/pypi/{package}/{release}/json'

    try:
        with opener(url, timeout=10) as response:
            data = json.loads(response.read())
    except HTTPError as error:
        if error.code == 404:
            return None
        raise RuntimeError(f'Could not fetch {package_name} {version} from PyPI: {error}') from error
    except Exception as error:
        raise RuntimeError(f'Could not fetch {package_name} {version} from PyPI: {error}') from error

    if not isinstance(data, dict):
        raise RuntimeError(f'PyPI returned an invalid JSON object for {package_name} {version}')
    urls = data.get('urls')
    if not isinstance(urls, list):
        raise RuntimeError(f'PyPI returned an invalid file list for {package_name} {version}')

    files = {}
    for item in urls:
        if not isinstance(item, dict) or not item.get('filename'):
            continue
        digests = item.get('digests')
        files[item['filename']] = {
            'sha256': digests.get('sha256') if isinstance(digests, dict) else None,
            'yanked': item.get('yanked') is True,
        }
    return files


def sha256sum(path):
    digest = hashlib.sha256()
    with path.open('rb') as distribution:
        for chunk in iter(lambda: distribution.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def get_distribution_state(package_name, version, distribution_paths, urlopen=None):
    """Return missing or identical; raise if PyPI contains different files."""
    paths = [Path(path) for path in distribution_paths]
    if not paths:
        raise ValueError('At least one distribution path is required')
    for path in paths:
        if not path.is_file():
            raise ValueError(f'Distribution does not exist: {path}')

    remote_files = get_pypi_release_files(package_name, version, urlopen=urlopen)
    if remote_files is None:
        return 'missing'

    mismatches = []
    yanked = []
    for path in paths:
        remote_file = remote_files.get(path.name)
        local_digest = sha256sum(path)
        if remote_file and remote_file['yanked']:
            yanked.append(path.name)
        elif not remote_file or remote_file['sha256'] != local_digest:
            mismatches.append(path.name)

    if yanked:
        raise RuntimeError(
            f'PyPI files are yanked for {package_name} {version}: '
            f'{", ".join(yanked)}'
        )
    if mismatches:
        raise RuntimeError(
            f'PyPI already has different or missing files for {package_name} {version}: '
            f'{", ".join(mismatches)}'
        )
    return 'identical'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--package', required=True)
    parser.add_argument('--version', required=True)
    parser.add_argument('distributions', nargs='+')
    args = parser.parse_args()

    try:
        state = get_distribution_state(
            args.package,
            args.version,
            args.distributions,
        )
    except Exception as error:
        print(f'Error: {error}', file=sys.stderr)
        return 1

    print(state)
    return 0


if __name__ == '__main__':
    sys.exit(main())
