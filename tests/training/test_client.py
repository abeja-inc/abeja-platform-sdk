from abeja.training import Client, JobDefinitions


def test_init(organization_id):
    client = Client(organization_id=organization_id)
    assert client.organization_id == organization_id


def test_adapters(requests_mock, api_base_url,
                  organization_id, job_definition_id, job_definition_name,
                  job_definition_response) -> None:

    client = Client(organization_id=organization_id)
    adapter = client.job_definitions()
    assert isinstance(adapter, JobDefinitions)
    assert adapter.organization_id == organization_id

    # Make sure returned adapter work
    requests_mock.get(
        '{}/organizations/{}/training/definitions/{}?include_jobs=false'.format(
            api_base_url,
            organization_id,
            job_definition_name),
        json=job_definition_response(
            organization_id,
            job_definition_id))
    definition = adapter.get(job_definition_name)
    assert definition
