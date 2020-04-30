import pytest
from abeja.training import APIClient, JobDefinitions


@pytest.fixture
def api_client():
    return APIClient()


def test_get_job_definition(requests_mock, api_base_url, api_client,
                            organization_id, job_definition_id, job_definition_name,
                            training_job_definition_response):
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
            version_count=4))
    proxy = JobDefinitions(api=api_client, organization_id=organization_id)
    definition = proxy.get(job_definition_name)
    assert definition
    assert definition.job_definition_id == job_definition_id
    assert definition.name == job_definition_name
    assert definition.notebook_count == 1
    assert definition.tensorboard_count == 2
    assert definition.model_count == 3
    assert definition.version_count == 4
    assert not definition.versions
    assert not definition.jobs
    assert not definition.archived
    assert definition.created_at
    assert definition.modified_at
