from typing import Any, Dict, Optional, IO, AnyStr
from .api.client import APIClient
from abeja.common.exec_env import ExecEnv
from abeja.user import User
from .common import SizedIterable, AbstractSizedIterator
from . import job_definition, job

# Entity class


class Model():
    """Training model object.

    Training model object is a representation of a machine learning model file.

    - Training Job can generate single or multiple training models.
    - You can upload your local model files which are on the local machine.
    """

    def __init__(self, api: APIClient,
                 organization_id: str,
                 job_definition_id: str,
                 job_id: Optional[str],
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
            job_id=response.get('training_job_id'),
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
    def job_id(self) -> Optional[str]:
        """Get the Job ID of this model. Returns ``None`` if the model doesn't
        have a back reference to a job."""
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
    def job(self) -> Optional['job.Job']:
        """Get the job of this model."""
        if self.__job is None and self.job_id is not None:
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

    def list(self,
             filter_archived: Optional[bool] = None) -> SizedIterable[Model]:
        """Returns an iterator object that iterates training models
        under this object.

        This method returns an instance of :class:`SizedIterable`, so you can
        get the total number of training models.

        Params:
            - **filter_archived** (bool): **[optional]** If ``true``, include archived models, otherwise exclude archived models. (default: ``false``)

        Return type:
            SizedIterable[Model]
        """
        return ModelIterator(
            api=self.__api,
            organization_id=self.organization_id,
            job_definition=self.__job_definition,
            filter_archived=filter_archived)

    def create(self,
               model_data: IO[AnyStr],
               job_id: Optional[str] = None,
               environment: Optional[Dict[str, Any]] = None,
               metrics: Optional[Dict[str, Any]] = None,
               description: Optional[str] = None) -> Model:
        """Create a new training model.

        Request Syntax:
            .. code-block:: python

                model = models.create(
                    model_data,
                    environment={'BATCH_SIZE': 32, 'EPOCHS': 50},
                    metrics={'acc': 0.76, 'loss': 1.99})

        Params:
            - **model_data** (IO): An input source for ML model. It must be a zip archived file like object
            - **job_id** (str): **[optional]** job identifer
            - **environment** (dict): **[optional]** user defined parameters set as environment variables
            - **metrics** (dict): **[optional]** user defined metrics for this model
            - **description** (str): **[optional]** description

        Return type:
            :class:`Model` object
        """
        parameters = {}  # type: Dict[str, Any]

        if job_id is not None:
            parameters['training_job_id'] = job_id
        if environment is not None:
            parameters['user_parameters'] = environment
        if metrics is not None:
            parameters['metrics'] = metrics
        if description is not None:
            parameters['description'] = description

        res = self.__api.create_training_model(
            organization_id=self.organization_id,
            job_definition_name=self.job_definition_name,
            model_data=model_data,
            parameters=parameters)

        return Model.from_response(
            api=self.__api,
            organization_id=self.organization_id,
            response=res,
            job_definition=self.__job_definition)

    def update(self, model_id: str, description: str) -> Model:
        """Update a training model.

        Request Syntax:
            .. code-block:: python

                model = models.update(model_id, 'description')

        Params:
            - **model_id** (str): Model ID
            - **description** (str): description

        Return type:
            :class:`Model` object
        """
        res = self.__api.patch_training_model(
            organization_id=self.organization_id,
            job_definition_name=self.job_definition_name,
            model_id=model_id,
            description=description)

        return Model.from_response(
            api=self.__api,
            organization_id=self.organization_id,
            response=res,
            job_definition=self.__job_definition)

    def get_download_uri(self, model_id: str) -> str:
        """Get download URL for training model.

        Request Syntax:
            .. code-block:: python

                uri = models.get_download_uri(model_id)

        Params:
            - **model_id** (str): Model ID

        Return type:
            str
        """
        res = self.__api.download_training_model(
            organization_id=self.organization_id,
            job_definition_name=self.job_definition_name,
            model_id=model_id)

        return res['download_uri']

    def archive(self, model_id: str) -> None:
        """Archive a training model.

        Request Syntax:
            .. code-block:: python

                model = models.archive(model_id)

        Params:
            - **model_id** (str): Job ID
        """
        self.__api.archive_training_model(
            organization_id=self.organization_id,
            job_definition_name=self.job_definition_name,
            model_id=model_id)

    def unarchive(self, model_id: str) -> None:
        """Unarchive a training model.

        Request Syntax:
            .. code-block:: python

                model = models.unarchive(model_id)

        Params:
            - **model_id** (str): Job ID
        """
        self.__api.unarchive_training_model(
            organization_id=self.organization_id,
            job_definition_name=self.job_definition_name,
            model_id=model_id)

# Iterator class


class ModelIterator(AbstractSizedIterator[Model]):

    def __init__(self, api: APIClient,
                 organization_id: str,
                 job_definition: 'job_definition.JobDefinition',
                 filter_archived: Optional[bool]) -> None:
        super().__init__(api=api,
                         organization_id=organization_id,
                         filter_archived=filter_archived,
                         # offset and limit are dummy
                         offset=0,
                         limit=1000)
        self.__job_definition = job_definition

    def invoke_api(self, api: APIClient) -> Dict[str, Any]:
        return api.get_training_models(
            organization_id=self.organization_id,
            job_definition_name=self.__job_definition.name,
            filter_archived=self.filter_archived)

    def build_entry(self, api: APIClient, entry: Dict[str, Any]) -> Model:
        return Model.from_response(
            api,
            self.organization_id,
            job_definition=self.__job_definition,
            response=entry)
