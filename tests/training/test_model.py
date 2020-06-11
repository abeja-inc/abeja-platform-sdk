from abeja.training.model import Model


def test_from_response(training_api_client, organization_id, training_model_response):
    response = training_model_response()
    model = Model.from_response(training_api_client, organization_id, response)
    assert model


def test_get_job(requests_mock, api_base_url, training_api_client,
                 organization_id, job_definition_id, job_definition_name, job_id,
                 training_model_response, job_definition_response, job_response):
    requests_mock.get(
        '{}/organizations/{}/training/definitions/{}'.format(
            api_base_url,
            organization_id,
            job_definition_id),
        json=job_definition_response())
    requests_mock.get(
        '{}/organizations/{}/training/definitions/{}/jobs/{}'.format(
            api_base_url,
            organization_id,
            job_definition_name,
            job_id),
        json=job_response())

    response = training_model_response()
    model = Model.from_response(training_api_client, organization_id, response)
    job = model.job
    assert job
