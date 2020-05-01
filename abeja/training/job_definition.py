from typing import Any, Dict, List, Optional
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
                 versions: Optional[List['JobDefinitionVersion']],
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

    @staticmethod
    def from_response(api: APIClient, organization_id: str, response: Dict[str, Any]) -> 'JobDefinition':
        """Construct an object from API response.

        NOTE: For convenient, this method DOES NOT validate the input response and
        always returns an object filled with default values.
        """
        versions = None
        vs = response.get('versions')
        if vs is not None:
            versions = [
                JobDefinitionVersion.from_response(api=api, organization_id=organization_id, response=v)
                for v in vs]

        return JobDefinition(
            api=api,
            organization_id=organization_id,
            job_definition_id=response.get('job_definition_id', ''),
            name=response.get('name', ''),
            version_count=response.get('version_count', 0),
            model_count=response.get('model_count', 0),
            notebook_count=response.get('notebook_count', 0),
            tensorboard_count=response.get('tensorboard_count', 0),
            versions=versions,
            jobs=response.get('jobs'),
            archived=bool(response.get('archived')),
            created_at=response.get('created_at', ''),
            modified_at=response.get('modified_at', ''))

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

    def job_definition_versions(self) -> 'JobDefinitionVersions':
        """Get a adapter object for handling training job definition versions under
        this job definition.

        Request syntax:
            .. code-block:: python

                adapter = definition.job_definition_versions()
                version = adapter.get(version=1)

        Return type:
            :class:`JobDefinitions <abeja.training.JobDefinitions>` object
        """
        return JobDefinitionVersions(api=self.__api, job_definition=self)


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

    @staticmethod
    def from_response(api: APIClient, organization_id: str, response: Dict[str, Any]) -> 'JobDefinitionVersion':
        """Construct an object from API response.

        NOTE: For convenient, this method DOES NOT validate the input response and
        always returns an object filled with default values.
        """
        return JobDefinitionVersion(
            api=api,
            organization_id=organization_id,
            job_definition_id=response.get('job_definition_id', ''),
            job_definition_version=response.get('job_definition_version', 0),
            handler=response.get('handler', ''),
            image=response.get('image', ''),
            environment=(response.get('environment') or {}),
            description=response.get('description', ''),
            archived=bool(response.get('archived')),
            created_at=response.get('created_at', ''),
            modified_at=response.get('modified_at', ''))

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

# adapter objects


class JobDefinitions():
    """The training job definition adapter/iterator class.
    """

    def __init__(self, api: APIClient, organization_id: str):
        self.__api = api
        self.__organization_id = organization_id

    @property
    def organization_id(self) -> str:
        """Get the organization ID."""
        return self.__organization_id

    def get(self, name: str, include_jobs: Optional[bool] = False) -> JobDefinition:
        """Get a training job definition.

        Request Syntax:
            .. code-block:: python

                definition = definitions.get(name=job_definition_name)

            Params:
            - **name** (str): The identifier of a training job definition. It can be either **name or job_definition_id**.
            - **include_jobs** (bool): If ``True``, also returns training jobs in response. (Default: ``False``)

        Return type:
            :class:`JobDefinition` object

        """
        res = self.__api.get_training_job_definition(
            organization_id=self.organization_id,
            job_definition_name=name,
            include_jobs=include_jobs)

        return JobDefinition.from_response(
            api=self.__api,
            organization_id=self.organization_id,
            response=res)

    def create(self, name: str) -> JobDefinition:
        """Create a new training job definition.

        Request Syntax:
            .. code-block:: python

                definition = definitions.create(name)

            Params:
            - **name** (str): training job definition name

        Return type:
            :class:`JobDefinition` object
        """
        res = self.__api.create_training_job_definition(
            organization_id=self.organization_id,
            job_definition_name=name)

        return JobDefinition.from_response(
            api=self.__api,
            organization_id=self.organization_id,
            response=res)

    def archive(self, name: str):
        """Get a training job definition.

        Request Syntax:
            .. code-block:: python

                definition = definitions.get(name=job_definition_name)

            Params:
            - **name** (str): The identifier of a training job definition. It can be either **name or job_definition_id**.
            - **include_jobs** (bool): If ``True``, also returns training jobs in response. (Default: ``False``)

        Return type:
            :class:`JobDefinition` object

        """
        self.__api.archive_training_job_definition(
            organization_id=self.organization_id,
            job_definition_name=name)


class JobDefinitionVersions():
    """The training job definition version adapter/iterator class.
    """

    def __init__(self, api: APIClient, job_definition: JobDefinition):
        self.__api = api
        self.__job_definition = job_definition

    @property
    def organization_id(self) -> str:
        """Get the organization ID."""
        return self.__job_definition.organization_id

    @property
    def job_definition_id(self) -> str:
        """Get the job definition ID."""
        return self.__job_definition.job_definition_id

    @property
    def job_definition_name(self) -> str:
        """Get the job definition name."""
        return self.__job_definition.name

    def get(self, job_definition_version: int) -> JobDefinitionVersion:
        """Get a training job definition version.

        Request Syntax:
            .. code-block:: python

                version = versions.get(job_definition_version=5)

            Params:
            - **job_definition_version** (int): the version number

        Return type:
            :class:`JobDefinitionVersion` object

        """
        res = self.__api.get_training_job_definition_version(
            organization_id=self.organization_id,
            job_definition_name=self.job_definition_name,
            version_id=job_definition_version)

        return JobDefinitionVersion.from_response(
            api=self.__api,
            organization_id=self.organization_id,
            response=res)
