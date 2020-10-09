# The ABEJA Platform SDK for Python

ABEJA Platform SDK is the ABEJA Platform Software Development Kit (SDK) for Python, which allows Python developers to write software that makes use of services like Datalake, Dataset, Training, Deployment, etc. You can find the latest, most up to date, documentation at our doc site, including a list of services that are supported.

[![CircleCI](https://circleci.com/gh/abeja-inc/abeja-platform-sdk.svg?style=svg)](https://circleci.com/gh/abeja-inc/abeja-platform-sdk)

## How to install

### Using pip

```
$ pip install abeja-sdk>=1.0.0
```

If you want to use latest version including **release candidate**, add `--pre` option.

```
$ pip install abeja-sdk>=1.0.0 --pre
```

If you have bigger version than latest pre-release, bigger not-pre-release version in installed.
For example, when there are versions of `1.0.1` and `1.0.0rc1`, `1.0.1` is installed even if you specify `--pre` option.

Release candidate is published when release branch is pushed to Github.

### Using requirements.txt

_`requirements.txt`_

```
abeja-sdk>=1.0.0
```

If you want to use pre-release, add `rc0` suffix.

```
abeja-sdk>=1.0.0rc
```

## Development

```bash
$ poetry install
$ poetry run pre-commit install
```

### Running Tests

You can run tests in all supported Python versions using `pytest`.

```bash
$ make test
```

You can also run individual tests with your default Python version:

```bash
$ poetry run pytest tests/
```

### Generating Documentation

Sphinx is used for documentation. You can generate HTML locally with the following:

```bash
$ poetry install -E docs
$ make docs
```

#### Installling dependencies

```
$ brew install sphinx-doc
$ echo 'export PATH="/usr/local/opt/sphinx-doc/bin:$PATH"' >> ~/.bashrc
$ poetry install
```

## Release

Synchronize master and develop branch.

```bash
$ git checkout master
$ git pull
$ git checkout develop
$ git pull
```

Create release branch and prepare for release.

```bash
$ git flow release start X.X.X
$ vim CHANGELOG.md
# update to new version
$ poetry version X.X.X
$ git add pyproject.toml
$ git add CHANGELOG.md
$ git commit -m "bump version"
$ git flow release publish X.X.X
```

After pushing to relase branch, RC package is published to packagecloud.

Check CircleCI result.
If the build succeeded then execute:

```bash
$ git flow release finish X.X.X
$ git push origin develop
$ git push origin master
$ git push origin X.X.X
```
