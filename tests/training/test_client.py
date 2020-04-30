from abeja.training import Client


def test_init(organization_id):
    client = Client(organization_id=organization_id)
    assert client.organization_id == organization_id


def test_get_job_definition(requests_mock, api_base_url,
                            organization_id, job_definition_id, job_definition_name,
                            training_job_definition_response):
    requests_mock.get(
        '{}/organizations/{}/training/definitions/{}?include_jobs=false'.format(
            api_base_url, organization_id, job_definition_name),
        json=training_job_definition_response(
            organization_id,
            job_definition_id,
            name=job_definition_name))
    client = Client(organization_id=organization_id)
    definition = client.get_job_definition(job_definition_name)
    assert definition
    assert definition.job_definition_id == job_definition_id
    assert definition.name == job_definition_name
    assert definition.version_count == 0
    assert definition.model_count == 0
    assert definition.notebook_count == 0
    assert definition.tensorboard_count == 0
    assert not definition.versions
    assert not definition.jobs
    assert not definition.archived
    assert definition.created_at
    assert definition.modified_at
