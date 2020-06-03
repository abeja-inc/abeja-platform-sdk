from typing import Any, Dict, List, Optional
from .api.client import APIClient
from .common import SizedIterable, AbstractSizedIterator
from . import job_definition_version, job

# Entity class


class JobDefinition():
    """Training job definition object.
    """

    def __init__(self,
                 api: APIClient,
                 organization_id: str,
                 job_definition_id: str,
                 name: str,
                 version_count: int,
                 model_count: int,
                 notebook_count: int,
                 tensorboard_count: int,
                 versions: Optional[List['job_definition_version.JobDefinitionVersion']],
                 jobs: Optional[list],
                 archived: bool,
                 created_at: str,
                 modified_at: str) -> None:
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

    @classmethod
    def from_response(klass,
                      api: APIClient,
                      organization_id: str,
                      response: Dict[str,
                                     Any]) -> 'JobDefinition':
        """Construct an object from API response.

        NOTE: For convenient, this method DOES NOT validate the input response and
        always returns an object filled with default values.
        """
        versions = None
        vs = response.get('versions')
        if vs is not None:
            versions = [job_definition_version.JobDefinitionVersion.from_response(
                api=api, organization_id=organization_id, response=v) for v in vs]

        return klass(
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
    def versions(
            self) -> Optional[List['job_definition_version.JobDefinitionVersion']]:
        """Get the versions of this job definition."""
        return self.__versions

    # TODO: Uncomment if we finish to implememt Job class
    # @property
    # def jobs(self) -> Optional[List['Job']]:
    #     """Get the jobs of this job definition."""
    #     return self.__jobs

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

    def job_definition_versions(
            self) -> 'job_definition_version.JobDefinitionVersions':
        """Return a adapter object for handling training job definition versions under
        this job definition.

        Request syntax:
            .. code-block:: python

                adapter = definition.job_definition_versions()
                version = adapter.get(job_definition_version_id=1)

        Return type:
            :class:`JobDefinitionVersions <abeja.training.JobDefinitionVersions>` object
        """
        return job_definition_version.JobDefinitionVersions(
            api=self.__api, job_definition=self)

    def jobs(self) -> 'job.Jobs':
        """Return a adapter object for handling training jobs under
        this job definition.

        Request syntax:
            .. code-block:: python

                adapter = definition.jobs()
                version = adapter.get(job_id='1234567890123')

        Return type:
            :class:`Jobs <abeja.training.Jobs>` object
        """
        return job.Jobs(api=self.__api, job_definition=self)

# Adapter classes


class JobDefinitions():
    """The training job definition adapter class.
    """

    def __init__(self, api: APIClient, organization_id: str) -> None:
        self.__api = api
        self.__organization_id = organization_id

    @property
    def organization_id(self) -> str:
        """Get the organization ID."""
        return self.__organization_id

    def get(
            self,
            name: str,
            include_jobs: Optional[bool] = False) -> JobDefinition:
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

    def list(self,
             filter_archived: Optional[bool] = None,
             offset: Optional[int] = None,
             limit: Optional[int] = None) -> SizedIterable[JobDefinition]:
        """Returns an iterator object that iterates training job definitions
        under this object.

        This method returns an instance of :class:`SizedIterable`, so you can
        get the total number of training job definitions.

        Params:
            - **filter_archived** (bool): **[optional]** If ``true``, include archived jobs, otherwise exclude archived jobs. (default: ``false``)
            - **offset** (int): **[optional]** paging offset.
            - **limit** (int): **[optional]** paging limit.

        Return type:
            SizedIterable[JobDefinition]
        """
        return JobDefinitionIterator(
            api=self.__api,
            organization_id=self.organization_id,
            filter_archived=filter_archived,
            offset=offset,
            limit=limit)

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
        """Archive a training job definition.

        Request Syntax:
            .. code-block:: python

                definitions.archive(name=job_definition_name)

        Params:
            - **name** (str): The identifier of a training job definition. It can be either **name or job_definition_id**.
        """
        self.__api.archive_training_job_definition(
            organization_id=self.organization_id,
            job_definition_name=name)

    def unarchive(self, name: str):
        """Unarchive a training job definition.

        Request Syntax:
            .. code-block:: python

                definitions.unarchive(name=job_definition_name)

        Params:
            - **name** (str): The identifier of a training job definition. It can be either **name or job_definition_id**.
        """
        self.__api.unarchive_training_job_definition(
            organization_id=self.organization_id,
            job_definition_name=name)

    def delete(self, name: str):
        """Delete a training job definition.

        Request Syntax:
            .. code-block:: python

                definitions.delete(name=job_definition_name)

        Params:
            - **name** (str): The identifier of a training job definition. It can be either **name or job_definition_id**.
        """
        self.__api.delete_training_job_definition(
            organization_id=self.organization_id,
            job_definition_name=name)


# Iterator class


class JobDefinitionIterator(AbstractSizedIterator[JobDefinition]):

    def invoke_api(self, api: APIClient) -> Dict[str, Any]:
        return api.get_training_job_definitions(
            organization_id=self.organization_id,
            filter_archived=self.filter_archived,
            offset=self.offset,
            limit=self.limit)

    def build_entry(self, api: APIClient,
                    entry: Dict[str, Any]) -> JobDefinition:
        return JobDefinition.from_response(api, self.organization_id, entry)
