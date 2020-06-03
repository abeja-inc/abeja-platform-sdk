from typing import Any, Dict, Optional
from logging import getLogger
from .api.client import APIClient
from .common import SizedIterable, AbstractSizedIterator
from .statistics import Statistics
from .job_status import JobStatus
from abeja.common.exec_env import ExecEnv
from abeja.common.instance_type import InstanceType
from abeja.user import User
import abeja.exceptions
from . import job_definition, job_definition_version

# Entity class


class Job():
    """Training job object.
    """

    def __init__(self, api: APIClient,
                 organization_id: str,
                 job_definition_id: str,
                 job_definition_version_id: int,
                 job_id: str,
                 instance_type: InstanceType,
                 exec_env: ExecEnv,
                 environment: Dict[str, str],
                 statistics: Optional[Statistics],
                 status_message: Optional[str],
                 status: JobStatus,
                 description: str,
                 datasets: Dict[str, str],
                 creator: Optional[User],
                 archived: bool,
                 start_time: str,
                 completion_time: str,
                 created_at: str,
                 modified_at: str,
                 job_definition: Optional['job_definition.JobDefinition'] = None,
                 job_definition_version: Optional['job_definition_version.JobDefinitionVersion'] = None) -> None:
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

    @classmethod
    def from_response(klass, api: APIClient,
                      organization_id: str,
                      response: Dict[str, Any],
                      job_definition: Optional['job_definition.JobDefinition'] = None,
                      job_definition_version: Optional['job_definition_version.JobDefinitionVersion'] = None) -> 'Job':
        """Construct an object from API response.

        NOTE: For convenient, this method DOES NOT validate the input response and
        always returns an object filled with default values.
        """
        statistics = Statistics.from_response(response.get('statistics'))
        creator = User.from_response(response.get('creator'))

        return klass(
            api=api,
            organization_id=organization_id,
            job_definition_id=response.get('job_definition_id', ''),
            job_definition_version_id=response.get('job_definition_version', 0),
            job_id=response.get('id', response.get('training_job_id', '')),
            instance_type=InstanceType.parse(response.get('instance_type', '')),
            exec_env=ExecEnv(str(response.get('exec_env'))),
            environment=(response.get('environment') or {}),
            statistics=statistics,
            status_message=response.get('status_message', ''),
            status=JobStatus(str(response.get('status'))),
            description=response.get('description', ''),
            datasets=(response.get('datasets') or {}),
            creator=creator,
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
    def instance_type(self) -> InstanceType:
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
    def status(self) -> JobStatus:
        """Get the current status of this job."""
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
    def creator(self) -> Optional[User]:
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
    def job_definition(self) -> 'job_definition.JobDefinition':
        """Get the job definition of this job."""
        if self.__job_definition is None:
            self.__job_definition = job_definition.JobDefinitions(
                api=self.__api, organization_id=self.organization_id).get(
                name=self.job_definition_id)
        return self.__job_definition

    @property
    def job_definition_version(
            self) -> 'job_definition_version.JobDefinitionVersion':
        """Get the job definition version of this job."""
        if self.__job_definition_version is None:
            self.__job_definition_version = job_definition_version.JobDefinitionVersions(
                api=self.__api, job_definition=self.job_definition).get(
                    job_definition_version_id=self.job_definition_version_id)
        return self.__job_definition_version


class JobArtifacts:

    def __init__(self, download_uri: str) -> None:
        self.__download_uri = download_uri

    @classmethod
    def from_response(klass, response: Dict[str, Any]) -> 'JobArtifacts':
        if 'download_uri' in response:
            return klass(download_uri=response['download_uri'])
        else:
            return klass(download_uri=response['artifacts']['complete']['uri'])

    @property
    def download_uri(self) -> str:
        """Return the download URI where artifacts archive file exists."""
        return self.__download_uri

# Adapter class


class Jobs():
    """The training jobs adapter class.
    """

    def __init__(
            self,
            api: APIClient,
            job_definition: 'job_definition.JobDefinition') -> None:
        self.__api = api
        self.__job_definition = job_definition
        self.__logger = getLogger('train-api')

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

    def list(self,
             filter_archived: Optional[bool] = None,
             offset: Optional[int] = None,
             limit: Optional[int] = None) -> SizedIterable[Job]:
        """Returns an iterator object that iterates training jobs
        under this object.

        This method returns an instance of :class:`SizedIterable`, so you can
        get the total number of training jobs.

        Params:
            - **filter_archived** (bool): **[optional]** If ``true``, include archived jobs, otherwise exclude archived jobs. (default: ``false``)
            - **offset** (int): **[optional]** paging offset.
            - **limit** (int): **[optional]** paging limit.

        Return type:
            SizedIterable[Job]
        """
        return JobIterator(
            api=self.__api,
            organization_id=self.organization_id,
            job_definition=self.__job_definition,
            filter_archived=filter_archived,
            offset=offset,
            limit=limit)

    def create(self,
               job_definition_version_id: int,
               instance_type: InstanceType,
               datasets: Optional[Dict[str, str]] = None,
               environment: Optional[Dict[str, Any]] = None,
               description: Optional[str] = None) -> Job:
        """Create a new training job.

        Request Syntax:
            .. code-block:: python

                job = jobs.create(
                    job_definition_version_id=5,
                    instance_type=InstanceType.parse('gpu-1'))

        Params:
            - **job_definition_version_id** (int): training job version
            - **instance_type** (InstanceType): instance type of running environment
            - **datasets** (dict): **[optional]** datasets, combination of alias and dataset_id
            - **environment** (dict): **[optional]** user defined parameters set as environment variables
            - **description** (str): **[optional]** description of this job

        Return type:
            :class:`Job` object
        """
        res = self.__api.create_training_job(
            organization_id=self.organization_id,
            job_definition_name=self.job_definition_name,
            version_id=job_definition_version_id,
            datasets=datasets,
            instance_type=str(instance_type),
            environment=environment,
            description=description)

        return Job.from_response(
            api=self.__api,
            organization_id=self.organization_id,
            response=res,
            job_definition=self.__job_definition)

    def stop(self, job_id: str) -> None:
        """Stop a training job.

        Request Syntax:
            .. code-block:: python

                job = jobs.stop(job_id)

        Params:
            - **job_id** (str): Job ID
        """
        self.__api.stop_training_job(
            organization_id=self.organization_id,
            job_definition_name=self.job_definition_name,
            training_job_id=job_id)

    def archive(self, job_id: str) -> None:
        """Archive a training job.

        Request Syntax:
            .. code-block:: python

                job = jobs.archive(job_id)

        Params:
            - **job_id** (str): Job ID
        """
        self.__api.archive_training_job(
            organization_id=self.organization_id,
            job_definition_name=self.job_definition_name,
            training_job_id=job_id)

    def unarchive(self, job_id: str) -> None:
        """Unarchive a training job.

        Request Syntax:
            .. code-block:: python

                job = jobs.archive(job_id)

        Params:
            - **job_id** (str): Job ID
        """
        self.__api.unarchive_training_job(
            organization_id=self.organization_id,
            job_definition_name=self.job_definition_name,
            training_job_id=job_id)

    def get_artifacts(self, job_id: str) -> 'JobArtifacts':
        """Get artifacts object of this job.

        Request Syntax:
            .. code-block:: python

                job = jobs.get_artifacts(job_id)

        Params:
            - **job_id** (str): Job ID
        """
        res = self.__api.get_training_result(
            organization_id=self.organization_id,
            job_definition_name=self.job_definition_name,
            training_job_id=job_id)
        return JobArtifacts.from_response(res)

    def update_statistics(
            self,
            job_id: str,
            statistics: Optional[Statistics]) -> Optional[Job]:
        """ Notify a job statistics for ABEJA Platform.

        Request Syntax:
            .. code-block:: python

                from abeja.training import Statistics

                statistics = Statistics(num_epochs=10, epoch=1)
                statistics.add_stage(name=Statistics.STAGE_TRAIN, accuracy=90.0, loss=0.10)
                statistics.add_stage(name=Statistics.STAGE_VALIDATION, accuracy=75.0, loss=0.07)

                jobs.update_statistics(job_id, statistics)

        Params:
            - **job_id** (str): Job ID
            - **statistics** (:class:`Statistics`): statistics

        Return type:
            :class:`Job` object
        """
        if not statistics:
            self.__logger.warning('no statistics found.')
            return None

        raw_statistics = statistics.get_statistics()
        if not raw_statistics:
            self.__logger.warning('empty statistics found.')
            return None

        try:
            res = self.__api.update_statistics(
                organization_id=self.organization_id,
                job_definition_name=self.job_definition_name,
                training_job_id=job_id,
                statistics=raw_statistics)
            return Job.from_response(
                api=self.__api,
                organization_id=self.organization_id,
                response=res,
                job_definition=self.__job_definition)
        except abeja.exceptions.HttpError as e:
            self.__logger.warning(
                'update_statistics result was {}.'.format(
                    str(e)))
            return None
        except Exception:
            self.__logger.exception(
                'update_statistics result was unexpected error:')
            return None

# Iterator class


class JobIterator(AbstractSizedIterator[Job]):

    def __init__(self, api: APIClient,
                 organization_id: str,
                 job_definition: 'job_definition.JobDefinition',
                 filter_archived: Optional[bool],
                 offset: Optional[int],
                 limit: Optional[int]) -> None:
        super().__init__(api=api,
                         organization_id=organization_id,
                         filter_archived=filter_archived,
                         offset=offset,
                         limit=limit)
        self.__job_definition = job_definition

    def invoke_api(self, api: APIClient) -> Dict[str, Any]:
        return api.get_training_jobs(
            organization_id=self.organization_id,
            job_definition_name=self.__job_definition.name,
            filter_archived=self.filter_archived,
            offset=self.offset,
            limit=self.limit)

    def build_entry(self, api: APIClient, entry: Dict[str, Any]) -> Job:
        return Job.from_response(
            api,
            self.organization_id,
            job_definition=self.__job_definition,
            response=entry)
