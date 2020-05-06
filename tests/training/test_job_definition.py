import pytest
from io import BytesIO
import json
import cgi
from pathlib import Path
from abeja.training import APIClient, JobDefinition, Job, Statistics, JobDefinitionVersion, JobDefinitions, job_status
from abeja.common import instance_type, exec_env
from abeja.common.instance_type import InstanceType, CPUType
from abeja.common.docker_image_name import DockerImageName, ALL_GPU_19_04, ALL_CPU_19_10


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def job_definition_factory(api_client, organization_id, job_definition_id, training_job_definition_response):
    def factory(organization_id=organization_id, job_definition_id=job_definition_id, **kwargs):
        response = training_job_definition_response(organization_id, job_definition_id, **kwargs)
        return JobDefinition.from_response(
            api=api_client,
            organization_id=organization_id,
            response=response)
    return factory


@pytest.fixture
def job_definition_version_factory(api_client, organization_id, job_definition_id, training_job_definition_version_response):
    def factory(organization_id=organization_id, job_definition_id=job_definition_id, **kwargs):
        response = training_job_definition_version_response(organization_id, job_definition_id, **kwargs)
        return JobDefinitionVersion.from_response(
            api=api_client,
            organization_id=organization_id,
            response=response
        )
    return factory


@pytest.fixture
def job_factory(api_client, organization_id, job_definition_id, job_id, job_response):
    def factory(organization_id=organization_id, job_definition_id=job_definition_id, job_id=job_id, **kwargs):
        response = job_response(organization_id, job_definition_id, job_id, **kwargs)
        return Job.from_response(
            api=api_client,
            organization_id=organization_id,
            response=response
        )
    return factory

# JobDefinitions


def test_job_definitions(organization_id, job_definition_id):
    adapter = JobDefinitions(api=api_client, organization_id=organization_id)
    assert adapter.organization_id == organization_id


def test_get_job_definition(requests_mock, api_base_url, api_client,
                            organization_id, job_definition_id, job_definition_name,
                            training_job_definition_response, training_job_definition_version_response):
    res = training_job_definition_response(
        organization_id,
        job_definition_id,
        name=job_definition_name,
        notebook_count=1,
        tensorboard_count=2,
        model_count=3,
        version_count=4,
        versions=[
            training_job_definition_version_response(
                organization_id,
                job_definition_id,
                1
            )
        ])
    requests_mock.get(
        '{}/organizations/{}/training/definitions/{}?include_jobs=false'.format(
            api_base_url, organization_id, job_definition_name),
        json=res)
    adapter = JobDefinitions(api=api_client, organization_id=organization_id)
    definition = adapter.get(name=job_definition_name)
    assert definition
    assert definition.job_definition_id == job_definition_id
    assert definition.name == job_definition_name
    assert definition.notebook_count == res['notebook_count']
    assert definition.tensorboard_count == res['tensorboard_count']
    assert definition.model_count == res['model_count']
    assert definition.version_count == res['version_count']
    assert definition.versions
    # TODO
    # assert not definition.jobs
    assert definition.archived is False
    assert definition.created_at == res['created_at']
    assert definition.modified_at == res['modified_at']

    version = definition.versions[0]
    assert version.job_definition_id == job_definition_id


def test_create_job_definition(requests_mock, api_base_url, api_client,
                               organization_id, job_definition_id, job_definition_name,
                               training_job_definition_response, training_job_definition_version_response):
    adapter = JobDefinitions(api=api_client, organization_id=organization_id)

    res = training_job_definition_response(
        organization_id,
        job_definition_id,
        name=job_definition_name,
        # 2020/05/01: Create API response
        archived=None,
        jobs=None,
        versions=[]
    )
    requests_mock.post(
        '{}/organizations/{}/training/definitions/'.format(api_base_url, organization_id),
        json=res)

    definition = adapter.create(name=job_definition_name)

    assert definition
    assert definition.job_definition_id == job_definition_id
    assert definition.name == job_definition_name
    assert definition.notebook_count == res['notebook_count']
    assert definition.tensorboard_count == res['tensorboard_count']
    assert definition.model_count == res['model_count']
    assert definition.version_count == res['version_count']
    assert definition.versions == res['versions']
    # TODO
    # assert definition.jobs == res['jobs']
    assert definition.archived is False
    assert definition.created_at == res['created_at']
    assert definition.modified_at == res['modified_at']


def test_archive_job_definition(requests_mock, api_base_url, api_client,
                                organization_id, job_definition_id, job_definition_name) -> None:
    adapter = JobDefinitions(api=api_client, organization_id=organization_id)

    requests_mock.post(
        '{}/organizations/{}/training/definitions/{}/archive'.format(api_base_url, organization_id, job_definition_id),
        json={'message': "test-1 archived"})

    adapter.archive(name=job_definition_id)
    assert requests_mock.called


def test_unarchive_job_definition(requests_mock, api_base_url, api_client,
                                  organization_id, job_definition_id, job_definition_name) -> None:
    adapter = JobDefinitions(api=api_client, organization_id=organization_id)

    requests_mock.post(
        '{}/organizations/{}/training/definitions/{}/unarchive'.format(api_base_url, organization_id, job_definition_id),
        json={'message': "test-1 unarchived"})

    adapter.unarchive(name=job_definition_id)
    assert requests_mock.called


def test_delete_job_definition(requests_mock, api_base_url, api_client,
                               organization_id, job_definition_id, job_definition_name) -> None:
    adapter = JobDefinitions(api=api_client, organization_id=organization_id)

    requests_mock.delete(
        '{}/organizations/{}/training/definitions/{}'.format(api_base_url, organization_id, job_definition_id),
        json={'message': "test-1 deleted"})

    adapter.delete(name=job_definition_id)
    assert requests_mock.called


def test_list_job_definitions(requests_mock, api_base_url, api_client,
                              organization_id, job_definition_id, job_definition_name,
                              training_job_definition_response) -> None:
    adapter = JobDefinitions(api=api_client, organization_id=organization_id)

    definition1 = training_job_definition_response(organization_id, job_definition_id)
    definition2 = training_job_definition_response(organization_id, job_definition_id)
    requests_mock.get(
        '{}/organizations/{}/training/definitions/'.format(
            api_base_url, organization_id),
        json={
            'entries': [definition1, definition2],
            'limit': 50,
            'offset': 0,
            'total': 2
        })

    iterator = adapter.list()
    assert len(iterator) == 2

    definitions = list(iterator)
    assert len(definitions) == 2
    assert definitions[0].job_definition_id == definition1['job_definition_id']
    assert definitions[1].job_definition_id == definition2['job_definition_id']


def test_list_job_definitions_filter_archived(requests_mock, api_base_url, api_client,
                                              organization_id, job_definition_id, job_definition_name,
                                              training_job_definition_response) -> None:
    adapter = JobDefinitions(api=api_client, organization_id=organization_id)

    definition1 = training_job_definition_response(organization_id, job_definition_id)
    requests_mock.get(
        '{}/organizations/{}/training/definitions/?filter_archived=exclude_archived'.format(
            api_base_url, organization_id),
        json={
            'entries': [definition1],
            'limit': 50,
            'offset': 0,
            'total': 1
        })

    iterator = adapter.list(filter_archived=True)
    assert len(iterator) == 1

    definitions = list(iterator)
    assert len(definitions) == 1
    assert definitions[0].job_definition_id == definition1['job_definition_id']


def test_list_job_definitions_paging(requests_mock, api_base_url, api_client,
                                     organization_id, job_definition_id, job_definition_name,
                                     training_job_definition_response) -> None:
    adapter = JobDefinitions(api=api_client, organization_id=organization_id)

    definition1 = training_job_definition_response(organization_id, job_definition_id)
    definition2 = training_job_definition_response(organization_id, job_definition_id)
    definition3 = training_job_definition_response(organization_id, job_definition_id)

    requests_mock.get(
        '{}/organizations/{}/training/definitions/?limit=2&offset=0'.format(
            api_base_url, organization_id),
        json={
            'entries': [definition1, definition2],
            'limit': 2,
            'offset': 0,
            'total': 3
        })
    requests_mock.get(
        '{}/organizations/{}/training/definitions/?limit=2&offset=2'.format(
            api_base_url, organization_id),
        json={
            'entries': [definition3],
            'limit': 2,
            'offset': 2,
            'total': 3
        })

    iterator = adapter.list(limit=2)
    assert len(iterator) == 3

    definitions = list(iterator)
    assert len(definitions) == 3
    assert definitions[0].job_definition_id == definition1['job_definition_id']
    assert definitions[1].job_definition_id == definition2['job_definition_id']
    assert definitions[2].job_definition_id == definition3['job_definition_id']

# JobDefinitionVersions


def test_job_definition_version(requests_mock, api_base_url, job_definition_version_factory, training_job_definition_response) -> None:
    version = job_definition_version_factory()  # type: JobDefinitionVersion

    res = training_job_definition_response(version.organization_id, version.job_definition_id)
    requests_mock.get(
        '{}/organizations/{}/training/definitions/{}?include_jobs=false'.format(
            api_base_url, version.organization_id, version.job_definition_id),
        json=res)

    definition = version.job_definition
    assert definition
    assert definition.organization_id == version.organization_id
    assert definition.job_definition_id == version.job_definition_id


def test_job_definition_versions(job_definition_factory) -> None:
    definition = job_definition_factory()  # type: JobDefinition
    adapter = definition.job_definition_versions()
    assert adapter.organization_id == definition.organization_id
    assert adapter.job_definition_id == definition.job_definition_id


def test_get_job_definition_version(requests_mock, api_base_url,
                                    job_definition_factory, training_job_definition_version_response) -> None:
    definition = job_definition_factory()  # type: JobDefinition
    adapter = definition.job_definition_versions()

    res = training_job_definition_version_response(
        adapter.organization_id,
        adapter.job_definition_id,
        environment=None
    )
    version_id = res['job_definition_version']
    requests_mock.get(
        '{}/organizations/{}/training/definitions/{}/versions/{}'.format(
            api_base_url, adapter.organization_id, adapter.job_definition_name, version_id),
        json=res)

    version = adapter.get(job_definition_version_id=version_id)
    assert version
    assert version.organization_id == adapter.organization_id
    assert version.job_definition_id == adapter.job_definition_id
    assert version.job_definition_version_id == version_id
    assert version.handler == res['handler']
    assert version.image == DockerImageName.parse(res['image'])
    assert version.environment == {}
    assert version.created_at == res['created_at']
    assert version.modified_at == res['modified_at']

    assert version.job_definition
    assert version.job_definition_id == adapter.job_definition_id


def test_get_job_definition_versions(requests_mock, api_base_url,
                                     job_definition_factory, training_job_definition_version_response) -> None:
    definition = job_definition_factory()  # type: JobDefinition
    adapter = definition.job_definition_versions()

    res1 = training_job_definition_version_response(
        adapter.organization_id,
        adapter.job_definition_id,
        environment=None
    )
    res2 = training_job_definition_version_response(
        adapter.organization_id,
        adapter.job_definition_id,
        environment={'foo': '1'}
    )
    requests_mock.get(
        '{}/organizations/{}/training/definitions/{}/versions'.format(
            api_base_url, adapter.organization_id, adapter.job_definition_name),
        json={
            'entries': [res1, res2]
        })

    it = adapter.list()
    assert len(it) == 2

    versions = list(it)
    assert len(versions) == 2
    for version, res in zip(versions, [res1, res2]):
        assert version.organization_id == adapter.organization_id
        assert version.job_definition_id == adapter.job_definition_id
        assert version.job_definition_version_id == res['job_definition_version']
        assert version.handler == res['handler']
        assert version.image == DockerImageName.parse(res['image'])
        assert version.environment == {} if res['environment'] is None else res['environment']
        assert version.created_at == res['created_at']
        assert version.modified_at == res['modified_at']
        assert version.job_definition
        assert version.job_definition_id == adapter.job_definition_id


def test_get_job_definition_versions_filter_archived(requests_mock, api_base_url,
                                                     job_definition_factory, training_job_definition_version_response) -> None:
    definition = job_definition_factory()  # type: JobDefinition
    adapter = definition.job_definition_versions()

    res1 = training_job_definition_version_response(
        adapter.organization_id,
        adapter.job_definition_id,
        environment=None
    )
    requests_mock.get(
        '{}/organizations/{}/training/definitions/{}/versions?filter_archived=exclude_archived'.format(
            api_base_url, adapter.organization_id, adapter.job_definition_name),
        json={
            'entries': [res1]
        })

    versions = list(adapter.list(filter_archived=True))
    assert len(versions) == 1


def test_create_job_definition_version_zip(
        requests_mock, api_base_url,
        make_zip_content,
        job_definition_factory, training_job_definition_version_response) -> None:
    definition = job_definition_factory()  # type: JobDefinition
    adapter = definition.job_definition_versions()

    res = training_job_definition_version_response(adapter.organization_id, adapter.job_definition_id)
    requests_mock.post(
        '{}/organizations/{}/training/definitions/{}/versions'.format(
            api_base_url, adapter.organization_id, adapter.job_definition_name),
        json=res)

    zip_content = make_zip_content({'train.py': b'print(1)'})
    version = adapter.create(BytesIO(zip_content), 'train:main', ALL_GPU_19_04, {'key': 'value'}, description='new version')
    assert version
    assert version.job_definition_version_id == res['job_definition_version']
    assert version.job_definition
    assert version.job_definition_id == adapter.job_definition_id

    history = requests_mock.request_history
    assert len(history) == 1

    fs = cgi.FieldStorage(fp=BytesIO(history[0].body), headers=history[0].headers, environ={'REQUEST_METHOD': 'POST'})

    item = fs['parameters']
    parameters = json.loads(item.value.decode('utf-8'))

    assert item.headers['Content-Type'] == 'application/json'
    assert parameters['handler'] == 'train:main'
    assert parameters['image'] == 'abeja-inc/all-gpu:19.04'
    assert parameters['environment'] == {'key': 'value'}

    item = fs['source_code']
    assert item.headers['Content-Type'] == 'application/zip'
    assert item.value == zip_content


def test_create_job_definition_version_files(
        requests_mock, api_base_url,
        tmpdir, make_zip_content,
        job_definition_factory, training_job_definition_version_response) -> None:
    definition = job_definition_factory()  # type: JobDefinition
    adapter = definition.job_definition_versions()

    # Make some files
    files = []
    with tmpdir.as_cwd():
        d = Path('work')
        d.mkdir(parents=True, exist_ok=True)

        path = d / 'test.txt'
        path.write_bytes(b'test')
        files.append(str(path))
        path = d / 'train.py'
        path.write_bytes(b'def handler(): pass')
        files.append(str(path))

        res = training_job_definition_version_response(adapter.organization_id, adapter.job_definition_id)
        requests_mock.post(
            '{}/organizations/{}/training/definitions/{}/versions'.format(
                api_base_url, adapter.organization_id, adapter.job_definition_name),
            json=res)

        version = adapter.create(files, 'train:handler', ALL_CPU_19_10, {'KEY': 'VALUE'}, description='new version')
        assert version
        assert version.job_definition_version_id == res['job_definition_version']
        assert version.job_definition
        assert version.job_definition_id == adapter.job_definition_id

    history = requests_mock.request_history
    assert len(history) == 1

    fs = cgi.FieldStorage(fp=BytesIO(history[0].body), headers=history[0].headers, environ={'REQUEST_METHOD': 'POST'})

    item = fs['parameters']
    parameters = json.loads(item.value.decode('utf-8'))

    assert item.headers['Content-Type'] == 'application/json'
    assert parameters['handler'] == 'train:handler'
    assert parameters['image'] == 'abeja-inc/all-cpu:19.10'
    assert parameters['environment'] == {'KEY': 'VALUE'}
    item = fs['source_code']
    assert item.headers['Content-Type'] == 'application/zip'
    assert item.value


def test_update_job_definition_version(requests_mock, api_base_url,
                                       job_definition_factory, training_job_definition_version_response) -> None:
    definition = job_definition_factory()  # type: JobDefinition
    adapter = definition.job_definition_versions()

    res = training_job_definition_version_response(adapter.organization_id, adapter.job_definition_id)
    version_id = res['job_definition_version']
    requests_mock.patch(
        '{}/organizations/{}/training/definitions/{}/versions/{}'.format(
            api_base_url, adapter.organization_id, adapter.job_definition_name, version_id),
        json=res)

    description = 'new version'
    version = adapter.update(version_id, description)
    assert version
    assert version.job_definition_version_id == version_id

    assert version.job_definition
    assert version.job_definition_id == adapter.job_definition_id

    history = requests_mock.request_history
    assert len(history) == 1
    assert history[0].json() == {'description': description}


def test_archive_job_definition_version(requests_mock, api_base_url, api_client,
                                        job_definition_factory) -> None:
    definition = job_definition_factory()  # type: JobDefinition
    adapter = definition.job_definition_versions()

    requests_mock.post(
        '{}/organizations/{}/training/definitions/{}/versions/1/archive'.format(
            api_base_url, adapter.organization_id, adapter.job_definition_name),
        json={'message': "test-1 archived"})

    adapter.archive(job_definition_version_id=1)
    assert requests_mock.called


def test_unarchive_job_definition_version(requests_mock, api_base_url, api_client,
                                          job_definition_factory) -> None:
    definition = job_definition_factory()  # type: JobDefinition
    adapter = definition.job_definition_versions()

    requests_mock.post(
        '{}/organizations/{}/training/definitions/{}/versions/1/unarchive'.format(
            api_base_url, adapter.organization_id, adapter.job_definition_name),
        json={'message': "test-1 unarchived"})

    adapter.unarchive(job_definition_version_id=1)
    assert requests_mock.called


def test_delete_job_definition_version(requests_mock, api_base_url, api_client,
                                       job_definition_factory) -> None:
    definition = job_definition_factory()  # type: JobDefinition
    adapter = definition.job_definition_versions()

    requests_mock.delete(
        '{}/organizations/{}/training/definitions/{}/versions/1'.format(
            api_base_url, adapter.organization_id, adapter.job_definition_name),
        json={'message': "test-1 deleted"})

    adapter.delete(job_definition_version_id=1)
    assert requests_mock.called

# Job


def test_job(requests_mock, api_base_url, job_factory, training_job_definition_response, training_job_definition_version_response) -> None:
    job = job_factory()  # type: Job

    res = training_job_definition_response(job.organization_id, job.job_definition_id)
    requests_mock.get(
        '{}/organizations/{}/training/definitions/{}?include_jobs=false'.format(
            api_base_url, job.organization_id, job.job_definition_id),
        json=res)
    res = training_job_definition_version_response(job.organization_id, job.job_definition_id, job.job_definition_version_id)
    requests_mock.get(
        '{}/organizations/{}/training/definitions/{}/versions/{}'.format(
            api_base_url, job.organization_id, job.job_definition.name, job.job_definition_version_id),
        json=res)

    assert job.exec_env == exec_env.CLOUD

    definition = job.job_definition
    assert definition
    assert definition.organization_id == job.organization_id
    assert definition.job_definition_id == job.job_definition_id
    version = job.job_definition_version
    assert version
    assert version.organization_id == job.organization_id
    assert version.job_definition_id == job.job_definition_id
    assert version.job_definition_version_id == job.job_definition_version_id


def test_job_statistics_none(requests_mock, api_base_url, job_factory, training_job_definition_response, training_job_definition_version_response) -> None:
    job = job_factory(statistics=None)  # type: Job
    assert job.statistics is None


def test_job_statistics_no_stages(requests_mock, api_base_url, job_factory, training_job_definition_response, training_job_definition_version_response) -> None:
    job = job_factory(statistics={
        "progress_percentage": 0.11,
        "num_epochs": 100,
        "epoch": 11
    })  # type: Job
    assert job.statistics
    assert job.statistics.progress_percentage == 0.11
    assert job.statistics.num_epochs == 100
    assert job.statistics.epoch == 11


@pytest.mark.parametrize('exec_env,expected', [
    ('local', exec_env.LOCAL),
    ('new value', exec_env.ExecEnv('new value')),
    ('', exec_env.ExecEnv('')),
    (None, exec_env.ExecEnv('None')),
])
def test_job_exec_env(job_factory, exec_env, expected) -> None:
    job = job_factory(exec_env=exec_env)  # type: Job
    assert job.exec_env == expected


@pytest.mark.parametrize('job_status,expected', [
    ('Pending', job_status.PENDING),
    ('Complete', job_status.COMPLETE),
    ('', job_status.JobStatus('')),
    ('new value', job_status.JobStatus('new value')),
    (None, job_status.JobStatus('None')),
])
def test_job_status(job_factory, job_status, expected) -> None:
    job = job_factory(status=job_status)  # type: Job
    assert job.status == expected


@pytest.mark.parametrize('instance_type,expected', [
    ('cpu-0.25', instance_type.CPU_0_25),
    ('cpu-2', instance_type.CPU_2),
    ('gpu-1', InstanceType(CPUType.GPU, None, 1)),
    ('gpu:a-1', instance_type.GPU_A1),
    ('gpu:b-4', instance_type.GPU_B4),
])
def test_job_instance_type(job_factory, instance_type, expected) -> None:
    job = job_factory(instance_type=instance_type)  # type: Job
    assert job.instance_type == expected


def test_jobs(job_definition_factory) -> None:
    definition = job_definition_factory()  # type: JobDefinition
    adapter = definition.jobs()
    assert adapter.organization_id == definition.organization_id
    assert adapter.job_definition_id == definition.job_definition_id


def test_get_job(requests_mock, api_base_url,
                 job_definition_factory, job_response, job_id) -> None:
    definition = job_definition_factory()  # type: JobDefinition
    adapter = definition.jobs()

    res = job_response(
        adapter.organization_id,
        adapter.job_definition_id,
        job_id,
        exec_env='cloud')
    requests_mock.get(
        '{}/organizations/{}/training/definitions/{}/jobs/{}'.format(
            api_base_url, adapter.organization_id, adapter.job_definition_name, job_id),
        json=res)

    job = adapter.get(job_id=job_id)
    assert job
    assert job.organization_id == adapter.organization_id
    assert job.job_definition_id == adapter.job_definition_id
    assert job.job_definition_version_id == res['job_definition_version']
    assert job.exec_env == exec_env.CLOUD
    assert job.creator
    assert job.creator.user_id == res['creator']['id']
    assert job.creator.email == res['creator']['email']
    assert job.creator.display_name == res['creator']['display_name']
    assert job.creator.profile_icon
    assert job.creator.profile_icon.thumbnail_icon_url == res['creator']['profile_icon']['thumbnail_icon_url']

    assert job.job_definition
    assert job.job_definition.job_definition_id == adapter.job_definition_id


def test_get_job_creator_none(requests_mock, api_base_url,
                              job_definition_factory, job_response, job_id) -> None:
    definition = job_definition_factory()  # type: JobDefinition
    adapter = definition.jobs()

    res = job_response(
        adapter.organization_id,
        adapter.job_definition_id,
        job_id,
        creator=None)
    requests_mock.get(
        '{}/organizations/{}/training/definitions/{}/jobs/{}'.format(
            api_base_url, adapter.organization_id, adapter.job_definition_name, job_id),
        json=res)

    job = adapter.get(job_id=job_id)
    assert job.creator is None


def test_list_jobs(requests_mock, api_base_url,
                   job_definition_factory, job_response) -> None:
    definition = job_definition_factory()  # type: JobDefinition
    adapter = definition.jobs()

    job1 = job_response(adapter.organization_id, adapter.job_definition_id)
    job2 = job_response(adapter.organization_id, adapter.job_definition_id)
    requests_mock.get(
        '{}/organizations/{}/training/definitions/{}/jobs'.format(
            api_base_url, adapter.organization_id, adapter.job_definition_name),
        json={
            'entries': [job1, job2],
            'limit': 50,
            'offset': 0,
            'total': 2
        })

    iterator = adapter.list()
    assert len(iterator) == 2

    jobs = list(iterator)
    assert len(jobs) == 2
    assert jobs[0].job_id == job1['training_job_id']
    assert jobs[1].job_id == job2['training_job_id']


def test_list_jobs_filter_archived(requests_mock, api_base_url,
                                   job_definition_factory, job_response) -> None:
    definition = job_definition_factory()  # type: JobDefinition
    adapter = definition.jobs()

    job1 = job_response(adapter.organization_id, adapter.job_definition_id)
    requests_mock.get(
        '{}/organizations/{}/training/definitions/{}/jobs?filter_archived=exclude_archived'.format(
            api_base_url, adapter.organization_id, adapter.job_definition_name),
        json={
            'entries': [job1],
            'limit': 50,
            'offset': 0,
            'total': 1
        })

    iterator = adapter.list(filter_archived=True)
    assert len(iterator) == 1

    jobs = list(iterator)
    assert len(jobs) == 1
    assert jobs[0].job_id == job1['training_job_id']


def test_list_jobs_paging(requests_mock, api_base_url,
                          job_definition_factory, job_response) -> None:
    definition = job_definition_factory()  # type: JobDefinition
    adapter = definition.jobs()

    job1 = job_response(adapter.organization_id, adapter.job_definition_id)
    job2 = job_response(adapter.organization_id, adapter.job_definition_id)
    job3 = job_response(adapter.organization_id, adapter.job_definition_id)

    requests_mock.get(
        '{}/organizations/{}/training/definitions/{}/jobs?limit=2&offset=0'.format(
            api_base_url, adapter.organization_id, adapter.job_definition_name),
        json={
            'entries': [job1, job2],
            'limit': 2,
            'offset': 0,
            'total': 3
        })
    requests_mock.get(
        '{}/organizations/{}/training/definitions/{}/jobs?limit=2&offset=2'.format(
            api_base_url, adapter.organization_id, adapter.job_definition_name),
        json={
            'entries': [job3],
            'limit': 2,
            'offset': 2,
            'total': 3
        })

    iterator = adapter.list(limit=2)
    assert len(iterator) == 3

    jobs = list(iterator)
    assert len(jobs) == 3
    assert jobs[0].job_id == job1['training_job_id']
    assert jobs[1].job_id == job2['training_job_id']
    assert jobs[2].job_id == job3['training_job_id']


def test_create_job(
        requests_mock, api_base_url,
        job_definition_factory, job_response) -> None:
    version_id = 4

    definition = job_definition_factory()  # type: JobDefinition
    adapter = definition.jobs()

    res = job_response(adapter.organization_id, adapter.job_definition_id,
                       job_definition_version=version_id,
                       instance_type='gpu:b-4')

    requests_mock.post(
        '{}/organizations/{}/training/definitions/{}/versions/{}/jobs'.format(
            api_base_url, adapter.organization_id, adapter.job_definition_name, version_id),
        json=res)

    instance_type = InstanceType.parse(res['instance_type'])
    job = adapter.create(version_id, instance_type)

    assert job.job_definition
    assert job.job_definition.job_definition_id == definition.job_definition_id


def test_stop_job(requests_mock, api_base_url, api_client,
                  job_id, job_definition_factory) -> None:
    definition = job_definition_factory()  # type: JobDefinition
    adapter = definition.jobs()

    requests_mock.post(
        '{}/organizations/{}/training/definitions/{}/jobs/{}/stop'.format(
            api_base_url, adapter.organization_id, adapter.job_definition_name, job_id),
        json={'message': "test-1 stopped"})

    adapter.stop(job_id)
    assert requests_mock.called


@pytest.mark.parametrize('expected,res', [
    ('http://example.com/artifacts/1', {'download_uri': 'http://example.com/artifacts/1'}),
    ('http://example.com/artifacts/1', {'artifacts': {'complete': {'uri': 'http://example.com/artifacts/1'}}}),
])
def test_get_training_result(requests_mock, api_base_url, api_client,
                             job_id, job_definition_factory,
                             expected, res) -> None:
    definition = job_definition_factory()  # type: JobDefinition
    adapter = definition.jobs()

    requests_mock.get(
        '{}/organizations/{}/training/definitions/{}/jobs/{}/result'.format(
            api_base_url, adapter.organization_id, adapter.job_definition_name, job_id),
        json=res)

    artifacts = adapter.get_artifacts(job_id)
    assert artifacts
    assert artifacts.download_uri == expected


def test_update_statistics(requests_mock, api_base_url, api_client,
                           job_id, job_definition_factory) -> None:
    definition = job_definition_factory()  # type: JobDefinition
    adapter = definition.jobs()

    requests_mock.post(
        '{}/organizations/{}/training/definitions/{}/jobs/{}/statistics'.format(
            api_base_url, adapter.organization_id, adapter.job_definition_name, job_id),
        json={'message': "test-1 updated"})

    statistics = Statistics(num_epochs=10, epoch=1)
    statistics.add_stage(name=Statistics.STAGE_TRAIN, accuracy=90.0, loss=0.10)
    statistics.add_stage(name=Statistics.STAGE_VALIDATION, accuracy=75.0, loss=0.07)

    adapter.update_statistics(job_id, statistics)
    assert requests_mock.called

    history = requests_mock.request_history
    req = history[0]
    req_statistics = req.json()['statistics']
    assert req_statistics['num_epochs'] == statistics.num_epochs
    assert req_statistics['epoch'] == statistics.epoch
