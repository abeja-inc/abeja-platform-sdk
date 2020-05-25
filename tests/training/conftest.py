import pytest
import random
from abeja.training import APIClient, JobDefinition, Job, Statistics, JobDefinitionVersion


@pytest.fixture
def training_api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def job_definition_factory(
        training_api_client,
        organization_id,
        job_definition_id,
        job_definition_response):
    def factory(
            organization_id=organization_id,
            job_definition_id=job_definition_id,
            **kwargs):
        response = job_definition_response(
            organization_id, job_definition_id, **kwargs)
        return JobDefinition.from_response(
            api=training_api_client,
            organization_id=organization_id,
            response=response)
    return factory


@pytest.fixture
def job_definition_version_factory(
        training_api_client,
        organization_id,
        job_definition_id,
        job_definition_version_response):
    def factory(
            organization_id=organization_id,
            job_definition_id=job_definition_id,
            **kwargs):
        response = job_definition_version_response(
            organization_id, job_definition_id, **kwargs)
        return JobDefinitionVersion.from_response(
            api=training_api_client,
            organization_id=organization_id,
            response=response
        )
    return factory


@pytest.fixture
def job_factory(
        training_api_client,
        organization_id,
        job_definition_id,
        job_id,
        job_response):
    def factory(
            organization_id=organization_id,
            job_definition_id=job_definition_id,
            job_id=job_id,
            **kwargs):
        response = job_response(
            organization_id,
            job_definition_id,
            job_id,
            **kwargs)
        return Job.from_response(
            api=training_api_client,
            organization_id=organization_id,
            response=response
        )
    return factory


@pytest.fixture
def statistics_factory():
    def factory():
        statistics = Statistics(num_epochs=random.choice(
            [10, 20, 30]), epoch=random.randint(1, 10))
        statistics.add_stage(
            name=Statistics.STAGE_TRAIN, accuracy=random.uniform(
                0.0, 100.0), loss=random.uniform(
                0.0, 100.0))
        statistics.add_stage(
            name=Statistics.STAGE_VALIDATION, accuracy=random.uniform(
                0.0, 100.0), loss=random.uniform(
                0.0, 100.0))
        return statistics
    return factory
