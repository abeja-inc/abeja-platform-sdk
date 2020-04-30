from typing import Dict, Optional
from .api.client import APIClient


# Entity objects

class JobDefinition():
    """Training job definition object.
    """

    def __init__(self, api: APIClient, organization_id: str,
                 job_definition_id: str,
                 name: str,
                 version_count: int,
                 model_count: int,
                 notebook_count: int,
                 tensorboard_count: int,
                 versions: Optional[list],
                 jobs: Optional[list],
                 archived: bool,
                 created_at: str,
                 modified_at: str):
        self.__api = api
        self.__organization_id = organization_id
        self.__job_definition_id = job_definition_id
        self.__name = name
        self.__version_count = version_count
        self.__model_count = model_count
        self.__notebook_count = notebook_count
        self.__tensorboard_count = tensorboard_count
        self.__versions = versions
        self.__jobs = jobs
        self.__archived = archived
        self.__created_at = created_at
        self.__modified_at = modified_at

    @property
    def organization_id(self) -> str:
        """Get the organization ID of this job definition."""
        return self.__organization_id

    @property
    def job_definition_id(self) -> str:
        """Get the job definition ID of this job definition."""
        return self.__job_definition_id

    @property
    def name(self) -> str:
        """Get the name of this job definition."""
        return self.__name

    @property
    def version_count(self) -> int:
        """Get the version count of this job definition."""
        return self.__version_count

    @property
    def model_count(self) -> int:
        """Get the model count of this job definition."""
        return self.__model_count

    @property
    def notebook_count(self) -> int:
        """Get the notebook count of this job definition."""
        return self.__notebook_count

    @property
    def tensorboard_count(self) -> int:
        """Get the tensorboard count of this job definition."""
        return self.__tensorboard_count

    @property
    def versions(self) -> Optional[list]:
        """Get the versions of this job definition."""
        return self.__versions

    @property
    def jobs(self) -> Optional[list]:
        """Get the jobs of this job definition."""
        return self.__jobs

    @property
    def archived(self) -> bool:
        """Get whether this job definition is archived or not."""
        return self.__archived

    @property
    def created_at(self) -> str:
        """Get the created date string (ISO 8601) of this job definition."""
        return self.__created_at

    @property
    def modified_at(self) -> str:
        """Get the modified date string (ISO 8601) of this job definition."""
        return self.__modified_at


class JobDefinitionVersion():
    """Training job definition version object.
    """

    def __init__(self, api: APIClient,
                 organization_id: str,
                 job_definition_id: str,
                 job_definition_version: int,
                 handler: str,
                 image: str,
                 environment: Dict[str, str],
                 description: str,
                 archived: bool,
                 created_at: str,
                 modified_at: str):
        self.__api = api
        self.__organization_id = organization_id
        self.__job_definition_id = job_definition_id
        self.__job_definition_version = job_definition_version
        self.__handler = handler
        self.__image = image
        self.__environment = environment
        self.__description = description
        self.__archived = archived
        self.__created_at = created_at
        self.__modified_at = modified_at

    @property
    def organization_id(self) -> str:
        """Get the organization ID of this job definition."""
        return self.__organization_id

    @property
    def job_definition_id(self) -> str:
        """Get the job_definition ID of this job definition."""
        return self.__job_definition_id

    @property
    def job_definition_version(self) -> int:
        """Get the version of this job definition version."""
        return self.__job_definition_version

    @property
    def handler(self) -> str:
        """Get the handler of this job definition version."""
        return self.__handler

    @property
    def image(self) -> str:
        """Get the image of this job definition version."""
        return self.__image

    @property
    def environment(self) -> Dict[str, str]:
        """Get the environment variables of this job definition version."""
        return self.__environment

    @property
    def description(self) -> str:
        """Get the description of this job definition version."""
        return self.__description

    @property
    def archived(self) -> bool:
        """Get whether this job definition is archived or not."""
        return self.__archived

    @property
    def created_at(self) -> str:
        """Get the created date string (ISO 8601) of this job definition version."""
        return self.__created_at

    @property
    def modified_at(self) -> str:
        """Get the modified date string (ISO 8601) of this job definition version."""
        return self.__modified_at

# Proxy objects


class JobDefinitions():
    """The training job definition iterator class.
    """

    def __init__(self, api: APIClient, organization_id: str):
        self.__api = api
        self.__organization_id = organization_id

    @property
    def organization_id(self) -> str:
        """Get the organization ID."""
        return self.__organization_id

    def get(self, job_definition_name: str, include_jobs: Optional[bool] = False) -> JobDefinition:
        """get a training job definition.

        Request Syntax:
            .. code-block:: python

                definition = definitions.get(job_definition_id=job_definition_id)

            Params:
            - **job_definition_name** (str): training job definition name
            - **include_jobs** (bool): If ``True``, also returns training jobs in response. (Default: ``False``)

        Return type:
            :class:`JobDefinition` object

        """
        res = self.__api.get_training_job_definition(
            organization_id=self.organization_id,
            job_definition_name=job_definition_name,
            include_jobs=include_jobs)

        return JobDefinition(
            api=self.__api,
            organization_id=self.organization_id,
            job_definition_id=res.get('job_definition_id', ''),
            name=res.get('name', ''),
            version_count=res.get('version_count', 0),
            model_count=res.get('model_count', 0),
            notebook_count=res.get('notebook_count', 0),
            tensorboard_count=res.get('tensorboard_count', 0),
            versions=res.get('versions'),
            jobs=res.get('jobs'),
            archived=res.get('archived', False),
            created_at=res.get('created_at', ''),
            modified_at=res.get('modified_at', ''))
