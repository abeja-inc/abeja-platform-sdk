from io import BytesIO
import json
import cgi
from pathlib import Path
from abeja.common.docker_image_name import DockerImageName, ALL_GPU_19_04, ALL_CPU_19_10
from abeja.training import JobDefinition, JobDefinitionVersion  # noqa: F401


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


def test_archive_job_definition_version(requests_mock, api_base_url, training_api_client,
                                        job_definition_factory) -> None:
    definition = job_definition_factory()  # type: JobDefinition
    adapter = definition.job_definition_versions()

    requests_mock.post(
        '{}/organizations/{}/training/definitions/{}/versions/1/archive'.format(
            api_base_url, adapter.organization_id, adapter.job_definition_name),
        json={'message': "test-1 archived"})

    adapter.archive(job_definition_version_id=1)
    assert requests_mock.called


def test_unarchive_job_definition_version(requests_mock, api_base_url, training_api_client,
                                          job_definition_factory) -> None:
    definition = job_definition_factory()  # type: JobDefinition
    adapter = definition.job_definition_versions()

    requests_mock.post(
        '{}/organizations/{}/training/definitions/{}/versions/1/unarchive'.format(
            api_base_url, adapter.organization_id, adapter.job_definition_name),
        json={'message': "test-1 unarchived"})

    adapter.unarchive(job_definition_version_id=1)
    assert requests_mock.called


def test_delete_job_definition_version(requests_mock, api_base_url, training_api_client,
                                       job_definition_factory) -> None:
    definition = job_definition_factory()  # type: JobDefinition
    adapter = definition.job_definition_versions()

    requests_mock.delete(
        '{}/organizations/{}/training/definitions/{}/versions/1'.format(
            api_base_url, adapter.organization_id, adapter.job_definition_name),
        json={'message': "test-1 deleted"})

    adapter.delete(job_definition_version_id=1)
    assert requests_mock.called
