from typing import Any, Dict, Optional
from .api.client import APIClient
from abeja.common.exec_env import ExecEnv
from abeja.user import User
from .job_definition import JobDefinition
from .job import Job

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
                 job_definition: Optional[JobDefinition] = None,
                 job: Optional[Job] = None) -> None:
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
                      job_definition: Optional[JobDefinition] = None,
                      job: Optional[Job] = None) -> 'Model':
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
