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


def test_get_job_definition(requests_mock, api_base_url, api_client,
                            organization_id, job_definition_id, job_definition_name,
                            training_job_definition_response, training_job_definition_version_response):
    requests_mock.get(
        '{}/organizations/{}/training/definitions/{}?include_jobs=false'.format(
            api_base_url, organization_id, job_definition_name),
        json=training_job_definition_response(
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
            ]))
    adapter = JobDefinitions(api=api_client, organization_id=organization_id)
    definition = adapter.get(job_definition_name)
    assert definition
    assert definition.job_definition_id == job_definition_id
    assert definition.name == job_definition_name
    assert definition.notebook_count == 1
    assert definition.tensorboard_count == 2
    assert definition.model_count == 3
    assert definition.version_count == 4
    assert definition.versions
    assert not definition.jobs
    assert not definition.archived
    assert definition.created_at
    assert definition.modified_at

    version = definition.versions[0]
    assert version.job_definition_id == job_definition_id


def test_job_definition_versions(job_definition_factory):
    definition = job_definition_factory()
    adapter = definition.job_definition_versions()
    adapter.organization_id == definition.organization_id
    adapter.job_definition_id == definition.job_definition_id
