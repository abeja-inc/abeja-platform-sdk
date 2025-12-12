# The ABEJA Platform SDK for Python

ABEJA Platform SDK is the ABEJA Platform Software Development Kit (SDK) for Python, which allows Python developers to write software that makes use of services like Datalake, Dataset, Training, Deployment, etc. You can find the latest, most up to date, documentation at our doc site, including a list of services that are supported.

ABEJA Platform SDKは、Python 用のABEJA Platform Software Development Kit（SDK）で、Python 開発者はDatalake, Dataset, Training, Deployment などのサービスを利用したソフトウェアを書くことができる。
サポートされているサービスのリストなど、最新のドキュメントはdoc サイトでご覧いただけます。

[![CircleCI](https://circleci.com/gh/abeja-inc/abeja-platform-sdk.svg?style=svg)](https://circleci.com/gh/abeja-inc/abeja-platform-sdk)

## How to install

### Using pip

```
$ pip install abeja-sdk>=1.0.0
```

If you want to use latest version including **release candidate**, add `--pre` option.

**リリース候補を含む最新版**を使用したい場合は、`--pre`オプションを追加してください。

```
$ pip install abeja-sdk>=1.0.0 --pre
```

If you have bigger version than latest pre-release, bigger not-pre-release version in installed.
For example, when there are versions of `1.0.1` and `1.0.0rc1`, `1.0.1` is installed even if you specify `--pre` option.

Release candidate is published when staging branch is pushed to Github.

もし、最新のプレリリース版よりも新しいバージョンがある場合はそのバージョンがインストールされます。
例えば、 `1.0.1` と `1.0.0rc1` というバージョンがある場合、 `--pre` オプションを指定しても、 `1.0.1` がインストールされます。

staging ブランチがGithubにプッシュされると、リリース候補版が公開されます。

### Using requirements.txt

_`requirements.txt`_

```
abeja-sdk>=1.0.0
```

If you want to use pre-release, add `rc0` suffix.

プレリリースを使いたい場合は、最後に`rc0` をつけてください。

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

サポートされているすべてのバージョンのPython で `pytest` を使ってテストを実行することができます。

```bash
$ make test
```

You can also run individual tests with your default Python version:

また、デフォルトのPython バージョンで個々のテストを実行することも可能です。

```bash
$ poetry run pytest tests/
```

### Generating Documentation

Sphinx is used for documentation. You can generate HTML locally with the following:

Sphinx はドキュメント作成に使用します。以下のようにして、ローカルにHTML を生成することができます。

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

### Deploy to Development Environment

When creating a PR from `feature/xxx` to `develop` branch, include version updates in the PR:
- Update `CHANGELOG.md`: Add your changes to the latest version section (do not create a new version section if the current version hasn't been released to staging yet)
- Update `pyproject.toml` version (e.g., `2.3.5` → `2.3.6`)

> **Note**: If the current version in `pyproject.toml` has never been released to staging, you don't need to create a new version section in `CHANGELOG.md` or update `pyproject.toml`. Instead, add your changes to the existing latest version section in `CHANGELOG.md`. Only create a new version section and update `pyproject.toml` when the previous version has been released to staging. Alternatively, update the version only when creating a PR to `staging` to avoid version gaps in PyPI releases.

Then create a PR and merge from `feature/xxx` to `develop` branch.

### Deploy to Staging Environment

Create a PR and merge from `develop` to `staging` branch.

After pushing to staging branch, RC package is automatically published to PyPI with the next available RC version (e.g., `2.3.6rc1`, `2.3.6rc2`, ...). The RC version number is automatically determined by querying PyPI for existing RC versions.

### Deploy to Production Environment

Create a PR and merge from `staging` to `master` branch.

After pushing to master branch, the final package (e.g., `2.3.6`) is published to PyPI.

## 実装中のSDK をローカルで利用する方法
以下のコマンドでwheel ファイルを作成する。dist ディレクトリに`abeja_sdk-x.x.x-py3-none-any.whl` というファイルが爆誕。

```bash
make release
```

SDK を利用する側を想定した環境で、上記のwhl ファイルを指定してpip install する

```bash
> pip install ./abeja_sdk-2.1.4rc3-py3-none-any.whl

Processing ./abeja_sdk-2.1.4rc3-py3-none-any.whl
Collecting protobuf<4
  Downloading protobuf-3.20.3-cp39-cp39-manylinux_2_5_x86_64.manylinux1_x86_64.whl (1.0 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.0/1.0 MB 37.2 MB/s eta 0:00:00

  （省略）

Successfully installed abeja-sdk-2.1.4rc3 protobuf-3.20.1 retrying-1.3.4 tensorboardx-2.5.1 tomlkit-0.7.0 typing-extensions-3.7.4.3
```

以下のようにローカルファイルを指定してabeja-sdk のパッケージがインストールされるので、普通にpython コード内でimport（`import abeja.datalake.Client` とか）すればローカルに閉じて検証可能になる。

```bash
> pip freeze
abeja-sdk @ file:///app/abeja_sdk-2.1.4rc3-py3-none-any.whl
aiofiles==22.1.0
```
