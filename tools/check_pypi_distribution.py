import hashlib
import json
import os
import urllib.request
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import quote


def get_pypi_release_files(package_name, version, urlopen=None):
    opener = urlopen or urllib.request.urlopen
    package = quote(package_name, safe="")
    release = quote(version, safe="")
    url = f"https://pypi.org/pypi/{package}/{release}/json"

    try:
        with opener(url, timeout=10) as response:
            data = json.loads(response.read())
    except HTTPError as error:
        if error.code == 404:
            return None
        raise RuntimeError(
            f"Could not fetch {package_name} {version} from PyPI: {error}"
        ) from error
    except Exception as error:
        raise RuntimeError(
            f"Could not fetch {package_name} {version} from PyPI: {error}"
        ) from error

    if not isinstance(data, dict):
        raise RuntimeError("PyPI returned an invalid JSON object")
    urls = data.get("urls")
    if not isinstance(urls, list):
        raise RuntimeError("PyPI returned an invalid file list")
    return urls


def sha256sum(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def get_distribution_state(
    package_name,
    version,
    distribution_path,
    urlopen=None,
):
    wheel = Path(distribution_path)
    if not wheel.is_file():
        raise ValueError(f"Distribution does not exist: {wheel}")

    remote_files = get_pypi_release_files(
        package_name,
        version,
        urlopen=urlopen,
    )
    if remote_files is None:
        return "missing"
    remote = remote_files[0] if len(remote_files) == 1 else None
    has_expected_file = isinstance(remote, dict)
    if has_expected_file:
        has_expected_file = remote.get("filename") == wheel.name
    if not has_expected_file:
        filenames = [
            item.get("filename") if isinstance(item, dict) else None
            for item in remote_files
        ]
        raise RuntimeError(f"PyPI has an unexpected file set: {filenames}")

    if remote.get("yanked") is True:
        raise RuntimeError(f"PyPI wheel is yanked: {wheel.name}")
    digests = remote.get("digests")
    remote_digest = (
        digests.get("sha256") if isinstance(digests, dict) else None
    )
    if remote_digest != sha256sum(wheel):
        raise RuntimeError(f"PyPI wheel digest differs: {wheel.name}")
    return "identical"


def main():
    wheels = list(Path("dist").glob("*.whl"))
    if len(wheels) != 1:
        raise RuntimeError(f"Expected one wheel, found {len(wheels)}")
    state = get_distribution_state(
        "abeja-sdk",
        os.environ["PACKAGE_VERSION"],
        wheels[0],
    )

    with open(os.environ["GITHUB_OUTPUT"], "a") as output:
        output.write(f"state={state}\n")
    if state == "identical":
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as summary:
            summary.write(
                "The identical wheel is already available on PyPI; "
                "upload is not repeated.\n"
            )


if __name__ == "__main__":
    main()
