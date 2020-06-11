from typing import Any, Dict, Optional
from .api.client import APIClient
from abeja.common.exec_env import ExecEnv
from abeja.user import User
from . import job_definition, job

# Entity class


class Model():
    """Training model object.
    """

    def __init__(self, api: APIClient,
                 organization_id: str,
                 job_definition_id: str,
                 job_id: str,
                 model_id: str,
                 description: Optional[str],
                 metrics: Dict[str, Any],
                 environment: Dict[str, str],
                 exec_env: ExecEnv,
                 creator: Optional[User],
                 archived: bool,
                 created_at: str,
                 modified_at: str,
                 job_definition: Optional['job_definition.JobDefinition'] = None,
                 job: Optional['job.Job'] = None) -> None:
        self.__api = api
        self.__organization_id = organization_id
        self.__job_definition_id = job_definition_id
        self.__job_id = job_id
        self.__model_id = model_id
        self.__description = description
        self.__metrics = metrics
        self.__environment = environment
        self.__exec_env = exec_env
        self.__creator = creator
        self.__archived = archived
        self.__created_at = created_at
        self.__modified_at = modified_at
        self.__job_definition = job_definition
        self.__job = job

    @classmethod
    def from_response(klass, api: APIClient,
                      organization_id: str,
                      response: Dict[str, Any],
                      job_definition: Optional['job_definition.JobDefinition'] = None,
                      job: Optional['job.Job'] = None) -> 'Model':
        """Construct an object from API response.

        NOTE: For convenient, this method DOES NOT validate the input response and
        always returns an object filled with default values.
        """
        creator = User.from_response(response.get('user'))

        return klass(
            api=api,
            organization_id=organization_id,
            job_definition_id=response.get('job_definition_id', ''),
            job_id=response.get('training_job_id', ''),
            model_id=response.get('id', ''),
            description=response.get('description', ''),
            metrics=(response.get('metrics') or {}),
            environment=(response.get('environment') or {}),
            exec_env=ExecEnv(str(response.get('exec_env'))),
            creator=creator,
            archived=bool(response.get('archived')),
            created_at=response.get('created_at', ''),
            modified_at=response.get('modified_at', ''),
            job_definition=job_definition,
            job=job)

    @property
    def organization_id(self) -> str:
        """Get the organization id of this model."""
        return self.__organization_id

    @property
    def job_definition_id(self) -> str:
        """Get the job definition id of this model."""
        return self.__job_definition_id

    @property
    def job_id(self) -> str:
        """Get the job_id of this model."""
        return self.__job_id

    @property
    def model_id(self) -> str:
        """Get the model_id of this model."""
        return self.__model_id

    @property
    def description(self) -> Optional[str]:
        """Get the description of this model."""
        return self.__description

    @property
    def metrics(self) -> Dict[str, Any]:
        """Get the metrics of this model."""
        return self.__metrics

    @property
    def environment(self) -> Dict[str, str]:
        """Get the environment of this model."""
        return self.__environment

    @property
    def exec_env(self) -> ExecEnv:
        """Get the exec_env of this model."""
        return self.__exec_env

    @property
    def creator(self) -> Optional[User]:
        """Get the creator of this model."""
        return self.__creator

    @property
    def archived(self) -> bool:
        """Get the archived of this model."""
        return self.__archived

    @property
    def created_at(self) -> str:
        """Get the created_at of this model."""
        return self.__created_at

    @property
    def modified_at(self) -> str:
        """Get the modified_at of this model."""
        return self.__modified_at

    @property
    def job_definition(self) -> 'job_definition.JobDefinition':
        """Get the job definition of this model."""
        if self.__job_definition is None:
            self.__job_definition = job_definition.JobDefinitions(
                api=self.__api, organization_id=self.organization_id).get(
                name=self.job_definition_id)
        return self.__job_definition

    @property
    def job(self) -> 'job.Job':
        """Get the job of this model."""
        if self.__job is None:
            self.__job = job.Jobs(
                api=self.__api, job_definition=self.job_definition).get(
                job_id=self.job_id)
        return self.__job

# Adapter class


class Models():
    """The training models adapter class.
    """

    def __init__(
            self,
            api: APIClient,
            job_definition: 'job_definition.JobDefinition') -> None:
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

    def get(self, model_id: str) -> Model:
        """Get a training model.

        Request Syntax:
            .. code-block:: python

                model = models.get(model_id)

        Params:
            - **model_id** (str): Model ID

        Return type:
            :class:`Model` object

        """
        res = self.__api.get_training_model(
            organization_id=self.organization_id,
            job_definition_name=self.job_definition_name,
            model_id=model_id)

        return Model.from_response(
            api=self.__api,
            organization_id=self.organization_id,
            response=res,
            job_definition=self.__job_definition)
