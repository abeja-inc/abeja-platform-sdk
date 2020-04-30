from abeja.training import Client, JobDefinitions


def test_init(organization_id):
    client = Client(organization_id=organization_id)
    assert client.organization_id == organization_id


def test_job_definitions(requests_mock, api_base_url,
                         organization_id, job_definition_id, job_definition_name,
                         training_job_definition_response):

    client = Client(organization_id=organization_id)
    proxy = client.job_definitions()
    assert isinstance(proxy, JobDefinitions)
    assert proxy.organization_id == organization_id

    # Make sure returned proxy work
    requests_mock.get(
        '{}/organizations/{}/training/definitions/{}?include_jobs=false'.format(
            api_base_url, organization_id, job_definition_name),
        json=training_job_definition_response(
            organization_id,
            job_definition_id))
    assert proxy.get(job_definition_name)
