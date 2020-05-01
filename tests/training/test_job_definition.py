import pytest
from abeja.training import APIClient, JobDefinition, JobDefinitions
from tests.utils import fake_iso8601


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def job_definition_factory(api_client, organization_id, job_definition_id, job_definition_name):
    def factory(organization_id=organization_id, job_definition_id=job_definition_id, job_definition_name=job_definition_name, **kwargs):
        return JobDefinition(
            api=api_client,
            organization_id=organization_id,
            job_definition_id=job_definition_id,
            name=job_definition_name,
            version_count=0,
            model_count=0,
            notebook_count=0,
            tensorboard_count=0,
            versions=None,
            jobs=None,
            archived=False,
            created_at=fake_iso8601(),
            modified_at=fake_iso8601(),
            **kwargs
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
    assert not definition.jobs
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
    assert definition.jobs == res['jobs']
    assert definition.archived is False
    assert definition.created_at == res['created_at']
    assert definition.modified_at == res['modified_at']

# JobDefinitionVersions


def test_job_definition_versions(job_definition_factory):
    definition = job_definition_factory()
    adapter = definition.job_definition_versions()
    adapter.organization_id == definition.organization_id
    adapter.job_definition_id == definition.job_definition_id


def test_get_job_definition_version(requests_mock, api_base_url,
                                    job_definition_factory, training_job_definition_version_response):
    version_id = 1
    definition = job_definition_factory()
    adapter = definition.job_definition_versions()

    res = training_job_definition_version_response(
        adapter.organization_id,
        adapter.job_definition_id,
        version_id,
        environment=None
    )
    requests_mock.get(
        '{}/organizations/{}/training/definitions/{}/versions/{}'.format(
            api_base_url, adapter.organization_id, adapter.job_definition_name, version_id),
        json=res)

    version = adapter.get(job_definition_version=version_id)
    assert version
    assert version.organization_id == adapter.organization_id
    assert version.job_definition_id == adapter.job_definition_id
    assert version.job_definition_version == version_id
    assert version.handler == res['handler']
    assert version.image == res['image']
    assert version.image == res['image']
    assert version.environment == {}
    assert version.created_at == res['created_at']
    assert version.modified_at == res['modified_at']
