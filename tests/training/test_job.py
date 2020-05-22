import pytest
from abeja.training import job_status
from abeja.common import instance_type, exec_env
from abeja.common.instance_type import InstanceType, CPUType
from abeja.training import JobDefinition, Job  # noqa: F401


def test_job(
        requests_mock,
        api_base_url,
        job_factory,
        training_job_definition_response,
        training_job_definition_version_response) -> None:
    job = job_factory()  # type: Job

    res = training_job_definition_response(
        job.organization_id, job.job_definition_id)
    requests_mock.get(
        '{}/organizations/{}/training/definitions/{}?include_jobs=false'.format(
            api_base_url,
            job.organization_id,
            job.job_definition_id),
        json=res)
    res = training_job_definition_version_response(
        job.organization_id,
        job.job_definition_id,
        job.job_definition_version_id)
    requests_mock.get(
        '{}/organizations/{}/training/definitions/{}/versions/{}'.format(
            api_base_url,
            job.organization_id,
            job.job_definition.name,
            job.job_definition_version_id),
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


def test_job_statistics_none(
        requests_mock,
        api_base_url,
        job_factory,
        training_job_definition_response,
        training_job_definition_version_response) -> None:
    job = job_factory(statistics=None)  # type: Job
    assert job.statistics is None


def test_job_statistics_no_stages(
        requests_mock,
        api_base_url,
        job_factory,
        training_job_definition_response,
        training_job_definition_version_response) -> None:
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
            api_base_url,
            adapter.organization_id,
            adapter.job_definition_name,
            job_id),
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
    assert job.creator.profile_icon.thumbnail_icon_url == res[
        'creator']['profile_icon']['thumbnail_icon_url']

    assert job.job_definition
    assert job.job_definition.job_definition_id == adapter.job_definition_id


def test_get_job_creator_none(
        requests_mock,
        api_base_url,
        job_definition_factory,
        job_response,
        job_id) -> None:
    definition = job_definition_factory()  # type: JobDefinition
    adapter = definition.jobs()

    res = job_response(
        adapter.organization_id,
        adapter.job_definition_id,
        job_id,
        creator=None)
    requests_mock.get(
        '{}/organizations/{}/training/definitions/{}/jobs/{}'.format(
            api_base_url,
            adapter.organization_id,
            adapter.job_definition_name,
            job_id),
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
            api_base_url,
            adapter.organization_id,
            adapter.job_definition_name),
        json={
            'entries': [
                job1,
                job2],
            'limit': 50,
            'offset': 0,
            'total': 2})

    iterator = adapter.list()
    assert len(iterator) == 2

    jobs = list(iterator)
    assert len(jobs) == 2
    assert jobs[0].job_id == job1['training_job_id']
    assert jobs[1].job_id == job2['training_job_id']


def test_list_jobs_filter_archived(
        requests_mock,
        api_base_url,
        job_definition_factory,
        job_response) -> None:
    definition = job_definition_factory()  # type: JobDefinition
    adapter = definition.jobs()

    job1 = job_response(adapter.organization_id, adapter.job_definition_id)
    requests_mock.get(
        '{}/organizations/{}/training/definitions/{}/jobs?filter_archived=exclude_archived'.format(
            api_base_url,
            adapter.organization_id,
            adapter.job_definition_name),
        json={
            'entries': [job1],
            'limit': 50,
            'offset': 0,
            'total': 1})

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
            api_base_url,
            adapter.organization_id,
            adapter.job_definition_name),
        json={
            'entries': [
                job1,
                job2],
            'limit': 2,
            'offset': 0,
            'total': 3})
    requests_mock.get(
        '{}/organizations/{}/training/definitions/{}/jobs?limit=2&offset=2'.format(
            api_base_url,
            adapter.organization_id,
            adapter.job_definition_name),
        json={
            'entries': [job3],
            'limit': 2,
            'offset': 2,
            'total': 3})

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
            api_base_url,
            adapter.organization_id,
            adapter.job_definition_name,
            version_id),
        json=res)

    instance_type = InstanceType.parse(res['instance_type'])
    job = adapter.create(version_id, instance_type)

    assert job.job_definition
    assert job.job_definition.job_definition_id == definition.job_definition_id


def test_stop_job(requests_mock, api_base_url, training_api_client,
                  job_id, job_definition_factory) -> None:
    definition = job_definition_factory()  # type: JobDefinition
    adapter = definition.jobs()

    requests_mock.post(
        '{}/organizations/{}/training/definitions/{}/jobs/{}/stop'.format(
            api_base_url,
            adapter.organization_id,
            adapter.job_definition_name,
            job_id),
        json={
            'message': "test-1 stopped"})

    adapter.stop(job_id)
    assert requests_mock.called


@pytest.mark.parametrize('expected,res',
                         [('http://example.com/artifacts/1',
                           {'download_uri': 'http://example.com/artifacts/1'}),
                             ('http://example.com/artifacts/1',
                              {'artifacts': {'complete': {'uri': 'http://example.com/artifacts/1'}}}),
                          ])
def test_get_training_result(requests_mock, api_base_url, training_api_client,
                             job_id, job_definition_factory,
                             expected, res) -> None:
    definition = job_definition_factory()  # type: JobDefinition
    adapter = definition.jobs()

    requests_mock.get(
        '{}/organizations/{}/training/definitions/{}/jobs/{}/result'.format(
            api_base_url,
            adapter.organization_id,
            adapter.job_definition_name,
            job_id),
        json=res)

    artifacts = adapter.get_artifacts(job_id)
    assert artifacts
    assert artifacts.download_uri == expected


def test_update_statistics(requests_mock, api_base_url,
                           job_id, job_definition_factory, statistics_factory,
                           job_response) -> None:
    definition = job_definition_factory()  # type: JobDefinition
    adapter = definition.jobs()

    statistics = statistics_factory()
    res = job_response(
        adapter.organization_id,
        adapter.job_definition_name,
        job_id,
        statistics=statistics.get_statistics())
    requests_mock.post(
        '{}/organizations/{}/training/definitions/{}/jobs/{}/statistics'.format(
            api_base_url,
            adapter.organization_id,
            adapter.job_definition_name,
            job_id),
        json=res)

    job = adapter.update_statistics(job_id, statistics)
    assert job
    assert job.job_id == job_id
    assert job.statistics
    assert job.statistics.num_epochs == statistics.num_epochs
    assert job.statistics.epoch == statistics.epoch

    assert requests_mock.called

    history = requests_mock.request_history
    req = history[0]
    req_statistics = req.json()['statistics']
    assert req_statistics['num_epochs'] == statistics.num_epochs
    assert req_statistics['epoch'] == statistics.epoch


def test_update_empty_statistics(
        requests_mock,
        job_id,
        job_definition_factory) -> None:
    definition = job_definition_factory()  # type: JobDefinition
    adapter = definition.jobs()
    adapter.update_statistics(job_id, None)


@pytest.mark.parametrize('status_code', [
    400, 401, 403, 404, 405,
    500, 503
])
def test_update_statistics_with_exception(
        requests_mock,
        api_base_url,
        status_code,
        job_id,
        job_definition_factory,
        statistics_factory) -> None:
    definition = job_definition_factory()  # type: JobDefinition
    adapter = definition.jobs()

    statistics = statistics_factory()
    requests_mock.post(
        '{}/organizations/{}/training/definitions/{}/jobs/{}/statistics'.format(
            api_base_url,
            adapter.organization_id,
            adapter.job_definition_name,
            job_id),
        status_code=status_code,
        json={
            'error': 'error'})

    adapter.update_statistics(job_id, statistics)
