from io import BytesIO
import json
import cgi
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


def test_list_models(requests_mock, api_base_url,
                     job_definition_factory, training_model_response) -> None:
    definition = job_definition_factory()  # type: JobDefinition
    adapter = definition.models()

    model1 = training_model_response(id='1020304050123')
    model2 = training_model_response(id='1020304050124')
    requests_mock.get(
        '{}/organizations/{}/training/definitions/{}/models'.format(
            api_base_url,
            adapter.organization_id,
            adapter.job_definition_name),
        json={
            'entries': [
                model1,
                model2],
            'limit': 50,
            'offset': 0,
            'total': 2})

    iterator = adapter.list()
    assert len(iterator) == 2

    models = list(iterator)
    assert len(models) == 2
    assert models[0].model_id == model1['id']
    assert models[1].model_id == model2['id']


def test_list_models_filter_archived(
        requests_mock,
        api_base_url,
        job_definition_factory,
        training_model_response) -> None:
    definition = job_definition_factory()  # type: JobDefinition
    adapter = definition.models()

    model1 = training_model_response(id='1020304050123')
    requests_mock.get(
        '{}/organizations/{}/training/definitions/{}/models?filter_archived=exclude_archived'.format(
            api_base_url,
            adapter.organization_id,
            adapter.job_definition_name),
        json={
            'entries': [model1],
            'limit': 50,
            'offset': 0,
            'total': 1})

    iterator = adapter.list(filter_archived=True)
    assert len(iterator) == 1

    models = list(iterator)
    assert len(models) == 1
    assert models[0].model_id == model1['id']


def test_create_model(
        requests_mock, api_base_url,
        make_random_file_content,
        job_definition_factory, training_model_response) -> None:
    definition = job_definition_factory()  # type: JobDefinition
    adapter = definition.models()

    res = training_model_response()

    requests_mock.post(
        '{}/organizations/{}/training/definitions/{}/models'.format(
            api_base_url,
            adapter.organization_id,
            adapter.job_definition_name),
        json=res)

    file_content = make_random_file_content()
    model_data = BytesIO(file_content)
    environment = {'BATCH_SIZE': 32, 'EPOCHS': 50}
    metrics = {'acc': 0.76, 'loss': 1.99}

    model = adapter.create(
        model_data,
        environment=environment,
        metrics=metrics)

    assert model.job_definition
    assert model.job_definition.job_definition_id == definition.job_definition_id

    history = requests_mock.request_history
    assert len(history) == 1

    fs = cgi.FieldStorage(
        fp=BytesIO(
            history[0].body),
        headers=history[0].headers,
        environ={
            'REQUEST_METHOD': 'POST'})

    item = fs['parameters']
    parameters = json.loads(item.value.decode('utf-8'))

    assert item.headers['Content-Type'] == 'application/json'
    assert parameters['user_parameters'] == environment
    assert parameters['metrics'] == metrics

    item = fs['model_data']
    assert item.headers['Content-Type'] == 'application/zip'
    assert len(history) == 1
