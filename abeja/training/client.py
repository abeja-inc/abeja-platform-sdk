from logging import getLogger
from typing import Dict, Optional

from abeja.base_client import BaseClient
from .api.client import APIClient
from .job_definition import JobDefinitions, JobDefinition


class Client(BaseClient):
    """A High-Level client for Training API

    .. code-block:: python

        from abeja.training import Client

        client = Client(organization_id='1234567890123')

    Params:
        - **organization_id** (str): The organization ID. Takes from ``os.environ['ABEJA_ORGANIZATION_ID']`` if omitted.
        - **credential** (dict):  **[optional]** This parameter will be passed to its undering :mod:`APIClient <abeja.training.APIClient>`.
          See the section :ref:`authentication_client_parameter` for more details about how to specify this parameter.
        - **timeout** (int):  **[optional]** This parameter will be passed to its undering :mod:`APIClient <abeja.training.APIClient>`.
        - **max_retry_count** (int):  **[optional]** This parameter will be passed to its undering :mod:`APIClient <abeja.training.APIClient>`.
    """

    def __init__(self, organization_id: str = None,
                 credential: Dict[str, str] = None,
                 timeout: Optional[int] = None,
                 max_retry_count: Optional[int] = None) -> None:
        super().__init__(organization_id, credential)
        self.api = APIClient(credential=credential, timeout=timeout, max_retry_count=max_retry_count)
        self.logger = getLogger('train-api')

    def get_job_definition(self, job_definition_name: str) -> JobDefinition:
        """Get a training job definition for specific ``job_definition_name``.

        Request syntax:
            .. code-block:: python

                definition = client.get_job_definition(job_definition_name)

        Params:
            - **job_definition_name** (str): Training Job Definition name

        Return type:
            :class:`JobDefinition <abeja.training.JobDefinition>` object
        """
        definitions = JobDefinitions(api=self.api, organization_id=self.organization_id)
        return definitions.get(job_definition_name)
