from typing import cast, Any, Dict, List, Iterator, Optional, Union, IO, AnyStr
import io
from .api.client import APIClient
from .common import SizedIterable
from .statistics import Statistics
from abeja.common.exec_env import ExecEnv

# Entity classes


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
    def versions(self) -> Optional[List['JobDefinitionVersion']]:
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

    def job_definition_versions(self) -> 'JobDefinitionVersions':
        """Return a adapter object for handling training job definition versions under
        this job definition.

        Request syntax:
            .. code-block:: python

                adapter = definition.job_definition_versions()
                version = adapter.get(job_definition_version_id=1)

        Return type:
            :class:`JobDefinitions <abeja.training.JobDefinitions>` object
        """
        return JobDefinitionVersions(api=self.__api, job_definition=self)

    def jobs(self) -> 'Jobs':
        """Return a adapter object for handling training jobs under
        this job definition.

        Request syntax:
            .. code-block:: python

                adapter = definition.jobs()
                version = adapter.get(job_id='1234567890123')

        Return type:
            :class:`JobDefinitions <abeja.training.Jobs>` object
        """
        return Jobs(api=self.__api, job_definition=self)


class JobDefinitionVersion():
    """Training job definition version object.
    """

    def __init__(self, api: APIClient,
                 organization_id: str,
                 job_definition_id: str,
                 job_definition_version_id: int,
                 handler: str,
                 image: str,
                 environment: Dict[str, str],
                 description: str,
                 archived: bool,
                 created_at: str,
                 modified_at: str,
                 job_definition: Optional[JobDefinition] = None) -> None:
        self.__api = api
        self.__organization_id = organization_id
        self.__job_definition_id = job_definition_id
        self.__job_definition_version_id = job_definition_version_id
        self.__handler = handler
        self.__image = image
        self.__environment = environment
        self.__description = description
        self.__archived = archived
        self.__created_at = created_at
        self.__modified_at = modified_at
        self.__job_definition = job_definition

    @staticmethod
    def from_response(api: APIClient,
                      organization_id: str,
                      response: Dict[str, Any],
                      job_definition: Optional[JobDefinition] = None) -> 'JobDefinitionVersion':
        """Construct an object from API response.

        NOTE: For convenient, this method DOES NOT validate the input response and
        always returns an object filled with default values.
        """
        return JobDefinitionVersion(
            api=api,
            organization_id=organization_id,
            job_definition_id=response.get('job_definition_id', ''),
            job_definition_version_id=response.get('job_definition_version', 0),
            handler=response.get('handler', ''),
            image=response.get('image', ''),
            environment=(response.get('environment') or {}),
            description=response.get('description', ''),
            archived=bool(response.get('archived')),
            created_at=response.get('created_at', ''),
            modified_at=response.get('modified_at', ''),
            job_definition=job_definition)

    @property
    def job_definition(self) -> JobDefinition:
        if self.__job_definition is None:
            self.__job_definition = JobDefinitions(api=self.__api, organization_id=self.organization_id).get(name=self.job_definition_id)
        return self.__job_definition

    @property
    def organization_id(self) -> str:
        """Get the organization ID of this job definition version."""
        return self.__organization_id

    @property
    def job_definition_id(self) -> str:
        """Get the job_definition ID of this job definition version."""
        return self.__job_definition_id

    @property
    def job_definition_version_id(self) -> int:
        """Get the version of this job definition version."""
        return self.__job_definition_version_id

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


class Job():
    """Training job object.
    """

    def __init__(self, api: APIClient,
                 organization_id: str,
                 job_definition_id: str,
                 job_definition_version_id: int,
                 job_id: str,
                 instance_type: str,
                 exec_env: ExecEnv,
                 environment: Dict[str, str],
                 statistics: Optional[Statistics],
                 status_message: Optional[str],
                 status: str,
                 description: str,
                 datasets: Dict[str, str],
                 creator: Optional[Dict[str, Any]],
                 archived: bool,
                 start_time: str,
                 completion_time: str,
                 created_at: str,
                 modified_at: str,
                 job_definition: Optional[JobDefinition] = None,
                 job_definition_version: Optional[JobDefinitionVersion] = None) -> None:
        self.__api = api
        self.__organization_id = organization_id
        self.__job_definition_id = job_definition_id
        self.__job_definition_version_id = job_definition_version_id
        self.__job_id = job_id
        self.__instance_type = instance_type
        self.__exec_env = exec_env
        self.__environment = environment
        self.__statistics = statistics
        self.__status_message = status_message
        self.__status = status
        self.__description = description
        self.__datasets = datasets
        self.__creator = creator
        self.__archived = archived
        self.__start_time = start_time
        self.__completion_time = completion_time
        self.__created_at = created_at
        self.__modified_at = modified_at
        self.__job_definition = job_definition
        self.__job_definition_version = job_definition_version

    @staticmethod
    def build_statistics(response: Optional[Dict[str, Any]]) -> Optional[Statistics]:
        if response is None:
            return None

        stages = {}
        if 'stages' in response:
            stages = response.pop('stages')

        statistics = Statistics(**response)
        for name, values in stages.items():
            statistics.add_stage(name=name, **values)
        return statistics

    @staticmethod
    def from_response(api: APIClient,
                      organization_id: str,
                      response: Dict[str, Any],
                      job_definition: Optional[JobDefinition] = None,
                      job_definition_version: Optional[JobDefinitionVersion] = None) -> 'Job':
        """Construct an object from API response.

        NOTE: For convenient, this method DOES NOT validate the input response and
        always returns an object filled with default values.
        """
        statistics = Job.build_statistics(response.get('statistics'))

        return Job(
            api=api,
            organization_id=organization_id,
            job_definition_id=response.get('job_definition_id', ''),
            job_definition_version_id=response.get('job_definition_version', 0),
            job_id=response.get('id', response.get('training_job_id', '')),
            instance_type=response.get('instance_type', ''),
            exec_env=ExecEnv.from_value(cast(str, response.get('exec_env'))),
            environment=(response.get('environment') or {}),
            statistics=statistics,
            status_message=response.get('status_message', ''),
            status=response.get('status', ''),
            description=response.get('description', ''),
            datasets=(response.get('datasets') or {}),
            creator=response.get('creator'),
            archived=bool(response.get('archived')),
            start_time=response.get('start_time', ''),
            completion_time=response.get('completion_time', ''),
            created_at=response.get('created_at', ''),
            modified_at=response.get('modified_at', ''),
            job_definition=job_definition,
            job_definition_version=job_definition_version)

    @property
    def organization_id(self) -> str:
        """Get the organization id of this job."""
        return self.__organization_id

    @property
    def job_definition_id(self) -> str:
        """Get the job definition id of this job."""
        return self.__job_definition_id

    @property
    def job_definition_version_id(self) -> int:
        """Get the job definition version id of this job."""
        return self.__job_definition_version_id

    @property
    def job_id(self) -> str:
        """Get the id of this job."""
        return self.__job_id

    @property
    def instance_type(self) -> str:
        """Get the instance type of this job."""
        return self.__instance_type

    @property
    def exec_env(self) -> ExecEnv:
        """Get the execution environment which this job runs."""
        return self.__exec_env

    @property
    def environment(self) -> Dict[str, str]:
        """Get environment variables of this job."""
        return self.__environment

    @property
    def statistics(self) -> Optional[Statistics]:
        """Get the statistics of this job."""
        return self.__statistics

    @property
    def status_message(self) -> Optional[str]:
        """Get the status_message of this job."""
        return self.__status_message

    @property
    def status(self) -> str:
        """Get the status of this job."""
        return self.__status

    @property
    def description(self) -> str:
        """Get the description of this job."""
        return self.__description

    @property
    def datasets(self) -> Dict[str, str]:
        """Get the datasets of this job."""
        return self.__datasets

    @property
    def creator(self) -> Optional[Dict[str, Any]]:
        """Get the creator of this job."""
        return self.__creator

    @property
    def archived(self) -> bool:
        """Get the archived of this job."""
        return self.__archived

    @property
    def start_time(self) -> str:
        """Get the start time of this job."""
        return self.__start_time

    @property
    def completion_time(self) -> str:
        """Get the completion time of this job."""
        return self.__completion_time

    @property
    def created_at(self) -> str:
        """Get the created datetime string of this job."""
        return self.__created_at

    @property
    def modified_at(self) -> str:
        """Get the modified datetime string of this job."""
        return self.__modified_at

    @property
    def job_definition(self) -> JobDefinition:
        """Get the job definition of this job."""
        if self.__job_definition is None:
            self.__job_definition = JobDefinitions(api=self.__api, organization_id=self.organization_id).get(name=self.job_definition_id)
        return self.__job_definition

    @property
    def job_definition_version(self) -> JobDefinitionVersion:
        """Get the job definition version of this job."""
        if self.__job_definition_version is None:
            self.__job_definition_version = JobDefinitionVersions(
                api=self.__api, job_definition=self.job_definition).get(
                    job_definition_version_id=self.job_definition_version_id)
        return self.__job_definition_version


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

    def list(self,
             filter_archived: Optional[bool] = None,
             offset: Optional[int] = None,
             limit: Optional[int] = None) -> SizedIterable[JobDefinition]:
        """Returns an iterator object that iterates training job definitions
        under the this object.

        This method returns an instance of :class:`SizedIterable`, so you can
        get the total number of training job definitions.

        Params:
            - **filter_archived** (bool): **[optional]** whether include archived ones or not. (default is not-filtered)
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


class JobDefinitionVersions():
    """The training job definition version adapter class.
    """

    def __init__(self, api: APIClient, job_definition: JobDefinition) -> None:
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

    def get(self, job_definition_version_id: int) -> JobDefinitionVersion:
        """Get a training job definition version.

        Request Syntax:
            .. code-block:: python

                version = versions.get(job_definition_version_id=5)

            Params:
            - **job_definition_version_id** (int): the version number

        Return type:
            :class:`JobDefinitionVersion` object

        """
        res = self.__api.get_training_job_definition_version(
            organization_id=self.organization_id,
            job_definition_name=self.job_definition_name,
            version_id=job_definition_version_id)

        return JobDefinitionVersion.from_response(
            api=self.__api,
            organization_id=self.organization_id,
            response=res,
            job_definition=self.__job_definition)

    def list(self, filter_archived: Optional[bool] = None) -> SizedIterable[JobDefinitionVersion]:
        """Returns an iterator object that iterates training job definition versions
        under the this object.

        This method returns an instance of :class:`SizedIterable`, so you can
        get the total number of training job definition versions.

        Params:
            - **filter_archived** (bool): **[optional]** whether include archived ones or not. (default is not-filtered)

        Return type:
            SizedIterable[JobDefinitionVersion]
        """
        res = self.__api.get_training_job_definition_versions(
            organization_id=self.organization_id,
            job_definition_name=self.job_definition_name,
            filter_archived=filter_archived)

        versions = [
            JobDefinitionVersion.from_response(
                api=self.__api,
                organization_id=self.organization_id,
                response=entry,
                job_definition=self.__job_definition)
            for entry in res['entries']]
        # Because the SizedIterator<T> is not a true "Intersection Type" but is
        # a new class, a list object will not be considered as adapted.
        return cast(SizedIterable[JobDefinitionVersion], versions)

    def create(self,
               source: Union[List[str], IO[AnyStr]],
               handler: str,
               image: Optional[str] = None,
               environment: Optional[Dict[str, Any]] = None,
               description: Optional[str] = None):
        """Create a new training job definition version.

        Request Syntax:
            .. code-block:: python

                version = versions.create(
                    source=['train.py'],
                    handler='train:handler',
                    image='abeja-inc/all-gpu:19.04',
                    environment={'key': 'value'},
                    description='new version')

            Params:
            - **source** (List[str] | IO): an input source for training code. It's one of:
              - zip or tar.gz archived file-like object.
              - a list of file paths.
            - **image** (Optional[str]): runtime environment
            - **environment** (Optional[dict]): user defined parameters set as environment variables
            - **description** (Optional[str]): description

        Return type:
            :class:`JobDefinitionVersion` object

        """
        if isinstance(source, io.IOBase):
            parameters = {'handler': handler}  # type: Dict[str, Any]
            if image is not None:
                parameters['image'] = image
            if environment is not None:
                parameters['environment'] = environment
            if description is not None:
                parameters['description'] = description

            res = self.__api.create_training_job_definition_version_native_api(
                organization_id=self.organization_id,
                job_definition_name=self.job_definition_name,
                source_code=cast(IO[AnyStr], source),
                parameters=parameters)

            return JobDefinitionVersion.from_response(
                api=self.__api,
                organization_id=self.organization_id,
                response=res,
                job_definition=self.__job_definition)
        else:
            res = self.__api.create_training_job_definition_version(
                organization_id=self.organization_id,
                job_definition_name=self.job_definition_name,
                filepaths=cast(List[str], source),
                handler=handler,
                image=image,
                environment=environment,
                description=description)
            return JobDefinitionVersion.from_response(
                api=self.__api,
                organization_id=self.organization_id,
                response=res,
                job_definition=self.__job_definition)

    def update(self, job_definition_version_id: int, description: str) -> JobDefinitionVersion:
        """Update a training job definition version.

        Request Syntax:
            .. code-block:: python

                version = versions.update(job_definition_version_id=5, description='new version')

            Params:
            - **job_definition_version_id** (int): the version number

        Return type:
            :class:`JobDefinitionVersion` object

        """
        res = self.__api.patch_training_job_definition_version(
            organization_id=self.organization_id,
            job_definition_name=self.job_definition_name,
            version_id=job_definition_version_id,
            description=description)

        return JobDefinitionVersion.from_response(
            api=self.__api,
            organization_id=self.organization_id,
            response=res,
            job_definition=self.__job_definition)

    def archive(self, job_definition_version_id: int):
        """Archive a training job definition version.

        Request Syntax:
            .. code-block:: python

                versions.archive(job_definition_version_id=5)

            Params:
            - **job_definition_version_id** (int): the version number
        """
        self.__api.archive_training_job_definition_version(
            organization_id=self.organization_id,
            job_definition_name=self.job_definition_name,
            version_id=job_definition_version_id)

    def unarchive(self, job_definition_version_id: int):
        """Unarchive a training job definition version.

        Request Syntax:
            .. code-block:: python

                versions.unarchive(job_definition_version_id=5)

            Params:
            - **job_definition_version_id** (int): the version number
        """
        self.__api.unarchive_training_job_definition_version(
            organization_id=self.organization_id,
            job_definition_name=self.job_definition_name,
            version_id=job_definition_version_id)

    def delete(self, job_definition_version_id: int):
        """Delete a training job definition version.

        Request Syntax:
            .. code-block:: python

                versions.delete(job_definition_version_id=5)

            Params:
            - **job_definition_version_id** (int): the version number
        """
        self.__api.delete_training_job_definition_version(
            organization_id=self.organization_id,
            job_definition_name=self.job_definition_name,
            version_id=job_definition_version_id)


class Jobs():
    """The training jobs adapter class.
    """

    def __init__(self, api: APIClient, job_definition: JobDefinition) -> None:
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

    def get(self, job_id: str) -> Job:
        """Get a training job.

        Request Syntax:
            .. code-block:: python

                job = jobs.get(job_id)

            Params:
            - **job_id** (int): Job ID

        Return type:
            :class:`Job` object

        """
        res = self.__api.get_training_job(
            organization_id=self.organization_id,
            job_definition_name=self.job_definition_name,
            training_job_id=job_id)

        return Job.from_response(
            api=self.__api,
            organization_id=self.organization_id,
            response=res,
            job_definition=self.__job_definition)

# Iterator classes


class JobDefinitionIterator(SizedIterable[JobDefinition]):

    def __init__(self, api: APIClient, organization_id: str,
                 filter_archived: Optional[bool],
                 offset: Optional[int],
                 limit: Optional[int]) -> None:
        self.__api = api
        self.__organization_id = organization_id
        self.__filter_archived = filter_archived
        self.__offset = offset if offset is not None else 0
        self.__limit = limit if limit is not None else 50
        self.__total = None  # type: Optional[int]
        self.__page = None  # type: Optional[Dict[str, Any]]

    def invoke_api(self) -> Dict[str, Any]:
        return self.__api.get_training_job_definitions(
            organization_id=self.organization_id,
            filter_archived=self.__filter_archived,
            offset=self.__offset,
            limit=self.__limit)

    @property
    def organization_id(self) -> str:
        """Get the organization ID."""
        return self.__organization_id

    def __len__(self) -> int:
        if self.__page is None:
            self.__page = self.invoke_api()
        return self.__page['total']

    def __iter__(self) -> Iterator[JobDefinition]:
        if self.__page is None:
            self.__page = self.invoke_api()

        while self.__page['entries']:
            for entry in self.__page["entries"]:
                yield JobDefinition.from_response(self.__api, self.organization_id, entry)
                self.__offset += 1
            if self.__offset < self.__page['total']:
                self.__page = self.invoke_api()
            else:
                break
