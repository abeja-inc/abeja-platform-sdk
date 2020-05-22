import os
from logging import getLogger
from typing import Dict
from typing import Optional

from abeja.base_client import BaseClient
from abeja.common.file_helpers import extract_zipfile
from abeja.exceptions import (BadRequest, Forbidden, MethodNotAllowed,
                              NotFound, ResourceNotFound, Unauthorized)
from abeja.train.api.client import APIClient
from abeja.train.statistics import Statistics


class Client(BaseClient):
    """A High-Level client for Training API

    .. code-block:: python

        from abeja.train import Client

        client = Client(organization_id='1234567890123')

    Params:
        - **organization_id** (str): The organization ID. Takes from `os.environ['ABEJA_ORGANIZATION_ID']` if omitted.
        - **job_definition_name** (str): The job definition name. Takes from `os.environ['TRAINING_JOB_DEFINITION_NAME']` if omitted.
        - **training_job_id** (str): The training job ID. Takes from `os.environ['TRAINING_JOB_ID']` if omitted.
    """

    def __init__(self, organization_id: str = None,
                 job_definition_name: str = None,
                 training_job_id: str = None,
                 credential: Dict[str, str] = None,
                 timeout: Optional[int] = None,
                 max_retry_count: Optional[int] = None) -> None:
        super().__init__(organization_id, credential)
        self.api = APIClient(
            credential=credential,
            timeout=timeout,
            max_retry_count=max_retry_count)
        self.logger = getLogger('train-api')
        self.job_definition_name = job_definition_name or os.environ.get(
            'TRAINING_JOB_DEFINITION_NAME')
        self.training_job_id = training_job_id or os.environ.get(
            'TRAINING_JOB_ID')

    def download_training_result(
            self,
            training_job_id: str = None,
            path: str = None) -> None:
        """download training artifact that includes model file or logs.
        Training artifact itself is a zip file, this function extracts it.

        API reference: GET /organizations/<organization_id>/training/definitions/<job_definition_name>/jobs/<training_job_id>/result

        Request Syntax:
            .. code-block:: python

                training_job_id = '1600000000000'
                client.download_training_result(training_job_id)

        Params:
            - **path** (str): target path where result are extracted **[optional]**

        Raises:
            - abeja.exceptions.BadRequest
            - abeja.exceptions.Unauthorized
            - abeja.exceptions.Forbidden
            - abeja.exceptions.NotFound
            - abeja.exceptions.MethodNotAllowed
            - abeja.exceptions.InternalServerError
            - json.JSONDecodeError
            - PermissionError
            - ValueError
            - IOError
        """
        # To keep backward compatibility with the older SDK (<= 1.0.10),
        # we have to allow a case which either job definition or job id is
        # `None`.
        training_job_id = training_job_id or self.training_job_id or 'None'
        job_definition_name = self.job_definition_name or 'None'

        response = self.api.get_training_result(
            organization_id=self.organization_id,
            job_definition_name=job_definition_name,
            training_job_id=training_job_id)
        try:
            artifact_uri = response['artifacts']['complete']['uri']
        except KeyError:
            raise ResourceNotFound(
                'training result for training_id {} is not found'.format(training_job_id))
        content = self._get_content(artifact_uri)
        extract_zipfile(content, path=path)

    def _get_content(self, url: str) -> bytes:
        """get binary content from given url.

        :param url:
        :return:
        :raises: abeja.exceptions.BadRequest
                 abeja.exceptions.Unauthorized
                 abeja.exceptions.Forbidden
                 abeja.exceptions.NotFound
                 abeja.exceptions.MethodNotAllowed
                 abeja.exceptions.InternalServerError
                 json.JSONDecodeError
        """
        res = self.api._connection.request('GET', url)
        return res.content

    def update_statistics(self, statistics: Statistics) -> None:
        """ Notify a job statistics for ABEJA Platform.

        API reference: POST /organizations/<organization_id>/training/definitions/<job_definition_name>/jobs/<training_job_id>/statistics

        Request Syntax:
            .. code-block:: python

                from abeja.train import Client
                from abeja.train.statistics import Statistics as ABEJAStatistics

                client = Client()

                statistics = ABEJAStatistics(num_epochs=10, epoch=1)
                statistics.add_stage(name=ABEJAStatistics.STAGE_TRAIN, accuracy=90.0, loss=0.10)
                statistics.add_stage(name=ABEJAStatistics.STAGE_VALIDATION, accuracy=75.0, loss=0.07)

                client.update_statistics(statistics)

        Params:
            - **statistics** (:class:`abeja.train.statistics.Statistics`): job statistics to nofity

        Returns:
            None
        """
        # To keep backward compatibility with the older SDK (<= 1.0.10),
        # we have to allow a case which either job definition or job id is
        # `None`.
        training_job_id = self.training_job_id or 'None'
        job_definition_name = self.job_definition_name or 'None'

        if not statistics or not statistics.get_statistics():
            self.logger.warning('empty statistics found.')
            return

        try:
            response = self.api.update_statistics(
                organization_id=self.organization_id,
                job_definition_name=job_definition_name,
                training_job_id=training_job_id,
                statistics=statistics.get_statistics())
            self.logger.info('update_statistics result: %s', response)
        except (BadRequest, Unauthorized, Forbidden, NotFound, MethodNotAllowed) as e:
            self.logger.warning(
                'update_statistics result was {}.'.format(
                    str(e)))
        except Exception:
            self.logger.exception(
                'update_statistics result was unexpected error:')
