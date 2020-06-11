from abeja.training.model import Model
from abeja.common import exec_env
from abeja.training import JobDefinition  # noqa: F401


def test_model_from_response(training_api_client, organization_id, training_model_response):
    response = training_model_response()
    model = Model.from_response(training_api_client, organization_id, response)
    assert model


def test_model_get_job(requests_mock, api_base_url, training_api_client,
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


def test_get_model(requests_mock, api_base_url,
                   training_model_id,
                   job_definition_factory, training_model_response) -> None:
    definition = job_definition_factory()  # type: JobDefinition
    adapter = definition.models()

    res = training_model_response()
    training_model_id = res['id']
    requests_mock.get(
        '{}/organizations/{}/training/definitions/{}/models/{}'.format(
            api_base_url,
            adapter.organization_id,
            adapter.job_definition_name,
            training_model_id),
        json=res)

    model = adapter.get(model_id=training_model_id)
    assert model
    assert model.model_id == training_model_id
    assert model.organization_id == adapter.organization_id
    assert model.job_definition_id == adapter.job_definition_id
    assert model.exec_env == exec_env.CLOUD
    assert model.creator
    assert model.creator.user_id == res['user']['id']
    assert model.creator.email == res['user']['email']
    assert model.creator.display_name == res['user']['display_name']
    assert model.creator.profile_icon
    assert model.creator.profile_icon.thumbnail_icon_url == res[
        'user']['profile_icon']['thumbnail_icon_url']

    assert model.job_definition
    assert model.job_definition.job_definition_id == adapter.job_definition_id
