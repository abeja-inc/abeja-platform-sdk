# pytest: sharing fixture functions
import pytest
import datetime
import random
import string
import uuid
from gzip import compress as compress_gzip
import requests_mock as requests_mock_module
from collections import namedtuple
from pathlib import Path
import shutil
from abeja.common.connection import Connection


def random_hex(n):
    return '%030x' % random.randrange((n * 2)**30)


def fake_platform_id():
    """Generates pseudo ABEJA Platform ID (e.g. "1335799549456")"""
    return '1' + ''.join([str(random.randint(0, 9)) for x in range(0, 12)])


def fake_iso8601():
    return '{}-{:02}-{:02}T{:02}:{:02}:{:02}+00:00'.format(
        random.randint(1996, 2020),
        random.randint(1, 12),
        random.randint(1, 30),
        random.randint(0, 23),
        random.randint(0, 59),
        random.randint(0, 59))


def fake_file_id():
    return '{}{:02}{:02}T{:02}{:02}{:02}-{}'.format(
        random.randint(1996, 2020),
        random.randint(1, 12),
        random.randint(1, 30),
        random.randint(0, 23),
        random.randint(0, 59),
        random.randint(0, 59),
        uuid.uuid4()
    )


@pytest.fixture
def requests_mock():
    with requests_mock_module.Mocker() as m:
        yield m


# Faker - ABEJA Platform


@pytest.fixture
def auth_jwt_token():
    # dummy
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9." \
        "eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ." \
        "SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"


@pytest.fixture
def user_id():
    return fake_platform_id()


@pytest.fixture
def personal_access_token():
    return random_hex(20)


@pytest.fixture
def organization_id():
    return fake_platform_id()


@pytest.fixture
def channel_id():
    return fake_platform_id()


@pytest.fixture
def job_definition_id():
    return fake_platform_id()


@pytest.fixture
def job_definition_name():
    return 'job-definition-{}'.format(random.randint(0, 1000))


@pytest.fixture
def job_id_factory():
    def factory():
        return fake_platform_id()
    return factory


@pytest.fixture
def job_id(job_id_factory):
    return job_id_factory()


@pytest.fixture
def job_definition_version_id():
    return 'ver-' + random_hex(8)


# Faker - Plala

@pytest.fixture
def job_parent_name():
    now = datetime.datetime.now()
    return now.strftime("%Y%m%d%H%M%S")


@pytest.fixture
def target_date():
    now = datetime.datetime.now()
    return now.strftime("%Y%m%d")

# Utilities


FakeCompletionProcess = namedtuple('FakeCompletionProcess', ['returncode'])


@pytest.fixture
def subprocess_completion_process_factory():
    """subprocess.CompletionProcess stub"""
    def factory(returncode):
        return FakeCompletionProcess(returncode=returncode)

    return factory


@pytest.fixture
def make_random_file_content():
    def factory(n_bytes=None, gzip=False):
        if n_bytes is None:
            n_bytes = random.randint(1, 1024 * 1024)
        chars = [random.choice(string.ascii_letters + string.digits)
                 for i in range(n_bytes)]
        bytes = ''.join(chars).encode('utf-8')
        return compress_gzip(bytes) if gzip else bytes
    return factory


@pytest.fixture
def make_zip_content(tmpdir_factory):
    """Returns the function which takes a dict parameter with
    filename as key and file content as value."""
    def factory(name_and_content_dict):
        d = tmpdir_factory.mktemp('artifact_work')
        with d.as_cwd():
            artifact_dir = Path('artifact')
            artifact_dir.mkdir(parents=True, exist_ok=True)

            for name in name_and_content_dict:
                path = (artifact_dir / name)
                content = name_and_content_dict[name]

                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(content)

            artifact_path = Path(shutil.make_archive(
                'artifact', 'zip', str(artifact_dir)))
            return artifact_path.read_bytes()

    return factory

# Platform Related Fixtures


@pytest.fixture
def api_base_url(monkeypatch):
    url = 'https://{}.api.example.com'.format(fake_platform_id())
    monkeypatch.setattr(Connection, 'BASE_URL', url)
    return url


# Responses

@pytest.fixture
def channel_response():
    def response(organization_id, channel_id):
        return {
            "updated_at": fake_iso8601(),
            "organization_name": "plala-test",
            "organization_id": organization_id,
            "created_at": fake_iso8601(),
            "account": {
                "updated_at": fake_iso8601(),
                "name": "plala-test",
                "id": "1939118753793",
                "display_name": "plala-test",
                "created_at": fake_iso8601()
            },
            "channel": {
                "updated_at": fake_iso8601(),
                "storage_type": "datalake",
                "security_method": "organization",
                "name": "plala-recommend-files",
                "created_at": fake_iso8601(),
                "channel_id": channel_id,
                "archived": False
            }
        }
    return response


@pytest.fixture
def file_response(organization_id):
    def response(
            channel_id,
            file_id=None,
            metadata={},
            **extra):
        uploaded_at = fake_iso8601()
        if not file_id:
            file_id = fake_file_id()
        download_uri = "https://abeja-datalake-test.s3.example.com/{}".format(
            file_id)
        return {
            "url_expires_on": fake_iso8601(),
            "uploaded_at": uploaded_at,
            "metadata": {
                "x-abeja-sys-meta-organizationid": organization_id,
                "x-abeja-meta-timestamp": uploaded_at,
                **metadata
            },
            "file_id": file_id,
            "download_url": download_uri,
            "download_uri": download_uri,
            "content_type": "application/octet-stream",
            "channel_id": channel_id,
            **extra
        }
    return response


@pytest.fixture
def delete_file_response():
    def _datalake_delete_file_response(channel_id, file_id, **extra):
        return {
            'message': 'deleted file ({})'.format(file_id),
            **extra
        }

    return _datalake_delete_file_response


@pytest.fixture
def job_definition_response(organization_id, job_definition_id):
    def _training_job_definition_response(
            organization_id=organization_id,
            training_job_definition_id=job_definition_id,
            name=None,
            **extra):
        if name is None:
            name = "test-{}".format(random.randint(1, 1000))
        return {
            "organization_id": organization_id,
            "job_definition_id": training_job_definition_id,
            "name": name,
            "archived": False,
            "versions": [],
            "jobs": None,
            "version_count": 0,
            "model_count": 0,
            "notebook_count": 0,
            "tensorboard_count": 0,
            "created_at": fake_iso8601(),
            "modified_at": fake_iso8601(),
            **extra
        }

    return _training_job_definition_response


@pytest.fixture
def job_definition_version_response():
    def _training_job_definition_version_response(
            _organization_id,
            job_definition_id,
            job_definition_version=None,
            **extra):
        if job_definition_version is None:
            job_definition_version = random.randint(0, 100)

        return {
            "job_definition_id": job_definition_id,
            "job_definition_version": job_definition_version,
            "environment": {},
            "user_parameters": {},
            "datasets": {
                "mnist": "1111111111111"
            },
            "handler": "train:handler",
            "created_at": fake_iso8601(),
            "modified_at": fake_iso8601(),
            "image": "abeja-inc/all-gpu:19.04",
            "archived": False,
            **extra
        }

    return _training_job_definition_version_response


@pytest.fixture
def job_response(organization_id, job_definition_id, job_id):
    def _job_response(
            _organization_id=organization_id,
            training_job_definition_id=job_definition_id,
            training_job_id=job_id,
            **extra):
        user_id = fake_platform_id()

        return {
            "job_definition_id": training_job_definition_id,
            "id": training_job_id,
            "training_job_id": training_job_id,
            "user_parameters": {},
            "start_time": None,
            "created_at": fake_iso8601(),
            "job_definition_version": random.randint(1, 30),
            "completion_time": None,
            "exec_env": "cloud",
            "status": "Pending",
            "instance_type": "cpu-1",
            "modified_at": fake_iso8601(),
            "creator": {
                "email": "test@abeja.asia",
                "is_registered": True,
                "preferred_language": "ja",
                "created_at": fake_iso8601(),
                "id": user_id,
                "display_name": None,
                "updated_at": fake_iso8601(),
                "role": "admin",
                "profile_icon": {
                    "thumbnail_icon_url": "https://icon.example.com/users/{}".format(user_id),
                    "original_icon_url": "https://icon.example.com/users/{}".format(user_id),
                    "mini_icon_url": "https://icon.example.com/users/{}".format(user_id),
                }
            },
            "description": None,
            "statistics": {
                "stages": {
                    "validation": {
                        "loss": random.uniform(0, 1),
                        "accuracy": random.uniform(0, 1)
                    },
                    "train": {
                        "loss": random.uniform(0, 1),
                        "accuracy": random.uniform(0, 1),
                        "debug": "debug"
                    }
                },
                "progress_percentage": random.uniform(0, 1),
                "num_epochs": random.randint(1, 300),
                "epoch": random.randint(1, 300)
            },
            **extra
        }

    return _job_response


@pytest.fixture
def list_jobs_response():
    def _response(jobs, offset=0, limit=50, total=None):
        return {
            'entries': jobs,
            'offset': offset,
            'limit': limit,
            'total': len(jobs) if total is None else total
        }
    return _response


@pytest.fixture
def job_result_response():
    def _job_result_response(
            organization_id,
            training_job_definition_id,
            training_job_id,
            **extra):
        return {
            "artifacts": {
                "complete": {
                    "uri": 'https://download.example.com/organizations/{}/training/definitions/'
                           '{}/jobs/{}'.format(organization_id, training_job_definition_id, training_job_id),
                    **extra
                }
            }
        }

    return _job_result_response
