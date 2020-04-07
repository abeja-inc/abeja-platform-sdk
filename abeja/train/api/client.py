import json
import tempfile
import zipfile
from io import BytesIO
from pathlib import Path
from typing import Optional

from abeja.common.api_client import BaseAPIClient
from abeja.common.utils import print_feature_deprecation
from abeja.train.instance_type import InstanceType
from abeja.common.utils import get_filter_archived_applied_params


class APIClient(BaseAPIClient):
    """A Low-Level client for Training API

    .. code-block:: python

       from abeja.train import APIClient

       api_client = APIClient()
    """

    def create_training_job_definition(self, organization_id: str, job_definition_name: str) -> dict:
        """create a training job definition

        API reference: POST /organizations/<organization_id>/training/definitions

        Request Syntax:
            .. code-block:: python

                organization_id = "1102940376065"
                job_definition_name = "test"
                response = api_client.create_training_job_definition(organization_id,
                                                                     job_definition_name)

        Params:
            - **organization_id** (str): ORGANIZATION_ID
            - **job_definition_name** (str): training job definition name

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    "job_definition_id": "1443334816413",
                    "versions": [],
                    "organization_id": "1200123565071",
                    "modified_at": "2018-05-17T02:13:35.726812Z",
                    "created_at": "2018-05-17T02:13:35.726691Z",
                    "version_count": 0,
                    "name": "test"
                }

        Raises:
            - BadRequest
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        data = {'name': job_definition_name}
        path = '/organizations/{}/training/definitions/'.format(organization_id)
        return self._connection.api_request(method='POST', path=path, json=data)

    def get_training_job_definitions(self, organization_id: str, filter_archived: Optional[bool] = None) -> dict:
        """get training job definitions

        API reference: GET /organizations/<organization_id>/training/definitions

        Request Syntax:
            .. code-block:: python

                organization_id = "1102940376065"
                response = api_client.get_training_job_definitions(organization_id)

        Params:
            - **organization_id** (str): ORGANIZATION_ID
            - **filter_archived** (bool): **[optional]** whether include archived ones or not. (default is not-filtered)

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    "entries": [
                        {
                            "version_count": 1,
                            "created_at": "2018-03-08T00:46:50.791787Z",
                            "organization_id": "1200123565071",
                            "versions": [
                                {
                                    "job_definition_version": 1,
                                    "user_parameters": {},
                                    "handler": "train:handler",
                                    "image": "abeja-inc/all-gpu:19.04",
                                    "modified_at": "2018-03-08T00:48:12.207883Z",
                                    "datasets": {
                                        "train": "1376063797251"
                                    },
                                    "created_at": "2018-03-08T00:48:12.132471Z",
                                    "job_definition_id": "1381349997580"
                                }
                            ],
                            "name": "test",
                            "archived": false,
                            "modified_at": "2018-03-08T00:46:50.791946Z",
                            "job_definition_id": "1381349997580"
                        }
                    ]
                }

        Raises:
            - BadRequest
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        params = None if filter_archived is None else get_filter_archived_applied_params({}, filter_archived)
        path = '/organizations/{}/training/definitions/'.format(organization_id)
        return self._connection.api_request(method='GET', path=path, params=params)

    def get_training_job_definition(self, organization_id: str, job_definition_name: str, include_jobs: Optional[bool] = None) -> dict:
        """get a training job definition.

        API reference: GET /organizations/<organization_id>/training/definitions/<job_definition_name>

        Request Syntax:
            .. code-block:: python

                organization_id = "1102940376065"
                job_definition_name = 'test'
                response = api_client.get_training_job_definition(organization_id, job_definition_name)

        Params:
            - **organization_id** (str): ORGANIZATION_ID
            - **job_definition_name** (str): training job definition name
            - **include_jobs** (bool): If ``True``, also returns training jobs in response. By historical reason,
                                       the default value is **True**, but you should specify False because it degrades
                                       API performance if you have a massive amount of jobs in the target training
                                       job definition.

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    "modified_at": "2018-05-17T02:13:35.726812Z",
                    "organization_id": "1200123565071",
                    "created_at": "2018-05-17T02:13:35.726691Z",
                    "job_definition_id": "1443334816413",
                    "name": "test",
                    "archived": false,
                    "versions": [],
                    "version_count": 0
                }

        Raises:
            - BadRequest
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        path = '/organizations/{}/training/definitions/{}'.format(organization_id, job_definition_name)

        # parameters
        params = {}

        if include_jobs is None:
            pass
        elif include_jobs:
            params['include_jobs'] = 'true'
        else:
            params['include_jobs'] = 'false'

        if len(params) == 0:
            params = None

        return self._connection.api_request(method='GET', path=path, params=params)

    def delete_training_job_definition(self, organization_id: str, job_definition_name: str) -> dict:
        """delete a training job definition.

        API reference: DELETE /organizations/<organization_id>/training/definitions/<job_definition_name>

        Request Syntax:
            .. code-block:: python

                organization_id = "1102940376065"
                job_definition_name = 'test'
                response = api_client.delete_training_job_definition(organization_id, job_definition_name)

        Params:
            - **organization_id** (str): ORGANIZATION_ID
            - **job_definition_name** (str): training job definition name

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    "message": "test deleted"
                }

        Raises:
            - BadRequest
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        path = '/organizations/{}/training/definitions/{}'.format(organization_id, job_definition_name)
        return self._connection.api_request(method='DELETE', path=path)

    def create_training_job_definition_version(
            self, organization_id: str, job_definition_name: str, params: Optional[dict] = None,
            filepaths: Optional[list] = None, handler: Optional[str] = None,
            image: Optional[str] = None, environment: Optional[dict] = None,
            description: Optional[str] = None) -> dict:
        """create a training job definition version.

        API reference: POST /organizations/<organization_id>/training/definitions/<job_definition_name>/versions

        Request Syntax:
            .. code-block:: python

                organization_id = "1102940376065"
                job_definition_name = "test_job_definition"
                filepaths = ["./requirements.txt", "./train.py"]
                handler = "train:handler"
                image = "abeja-inc/all-gpu:19.04"
                environment = {"key": "value"}
                description = "description"
                params = {
                    "handler": "train:handler",
                    "datasets": {
                        "mnist": "1111111111111"
                    },
                    "image": "abeja-inc/all-gpu:19.04",
                    "source_code_base64": "....",
                    "user_parameters": {}
                }
                response = api_client.create_training_job_definition_version(organization_id, job_definition_name, params)

        Params:
            - **organization_id** (str): ORGANIZATION_ID
            - **job_definition_name** (str): training job definition name
            - **filepaths** (list): file list to run training job
            - **handler** (str): path to handler (ex. train:handler )
            - **image** (Optional[str]): runtime enviornment
            - **environment** (Optional[dict]): user defined parameters set as environment variables
            - **description** (Optional[str]): description
            - (DEPRECATED) **params** (dict): parameters for training job definition version
                - **handler** (str): path to handler (ex. train:handler )
                - (DEPRECATED) **datasets** (Optional[str]): (**deprecated!!**) datasets, combination of alias and dataset_id
                - **image** (Optional[str]): runtime enviornment
                - **source_code_base64** (str): base64 encoded source code
                - **user_parameters** (Optional[dict]): user defined parameters set as environment variables.

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    "job_definition_version": 1,
                    "user_parameters": {},
                    "environment": {},
                    "description": "description",
                    "datasets": {
                        "mnist": "1111111111111"
                    },
                    "modified_at": "2018-05-17T12:34:46.344076Z",
                    "job_definition_id": "1443714239154",
                    "handler": "train:handler",
                    "created_at": "2018-05-17T12:34:46.296488Z",
                    "image": "abeja-inc/all-gpu:19.04"
                }

        Raises:
            - BadRequest
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        path = '/organizations/{}/training/definitions/{}/versions'.format(organization_id, job_definition_name)
        if params:
            print_feature_deprecation(
                target='params',
                additional_message='please set "filepaths", "handler", "image", '
                                   '"environment" and "description" instead.')
            if 'datasets' in params:
                print_feature_deprecation(
                    target='datasets',
                    additional_message='please set datasets when you create training job.')
            return self._connection.api_request(method='POST', path=path, json=params)
        else:
            try:
                source_code = tempfile.NamedTemporaryFile(suffix='.zip')
                with zipfile.ZipFile(source_code.name, 'w', compression=zipfile.ZIP_DEFLATED) as new_zip:
                    for filepath in filepaths:
                        path_obj = Path(filepath)
                        new_zip.write(filepath, path_obj.name)
                source_code.seek(0)

                parameters = {'handler': handler}
                if image:
                    parameters['image'] = image
                if environment:
                    parameters['environment'] = environment
                if description:
                    parameters['description'] = description
                parameters = BytesIO(json.dumps(parameters).encode())
                files = {
                    'source_code': ('source_code.zip', source_code, 'application/zip'),
                    'parameters': ('params.json', parameters, 'application/json'),
                }
                return self._connection.api_request(method='POST', path=path, files=files)
            finally:
                if source_code:
                    source_code.close()

    def get_training_job_definition_versions(
            self, organization_id: str, job_definition_name: str,
            filter_archived: Optional[bool] = None) -> dict:
        """get training job definition versions.

        API reference: GET /organizations/<organization_id>/training/definitions/<job_definition_name>/versions

        Request Syntax:
            .. code-block:: python

                organization_id = "1102940376065"
                job_definition_name = 'test_job_definition'
                response = api_client.get_training_job_definition_versions(organization_id, job_definition_name)

        Params:
            - **organization_id** (str): ORGANIZATION_ID
            - **job_definition_name** (str): training job definition name
            - **filter_archived** (bool): **[optional]** whether include archived ones or not. (default is not-filtered)

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    "entries": [
                        {
                            "job_definition_version": 1,
                            "user_parameters": {},
                            "datasets": {
                                "mnist": "1111111111111"
                            },
                            "modified_at": "2018-05-17T12:34:46.344076Z",
                            "job_definition_id": "1443714239154",
                            "handler": "train:handler",
                            "created_at": "2018-05-17T12:34:46.296488Z",
                            "image": "abeja-inc/all-gpu:19.04",
                            "archived": false
                        }
                    ]
                }

        Raises:
            - BadRequest
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        params = None if filter_archived is None else get_filter_archived_applied_params({}, filter_archived)
        path = '/organizations/{}/training/definitions/{}/versions'.format(
            organization_id, job_definition_name)
        return self._connection.api_request(method='GET', path=path, params=params)

    def get_training_job_definition_version(
            self, organization_id: str, job_definition_name: str, version_id: int) -> dict:
        """get a training job definition version

        API reference: GET /organizations/<organization_id>/training/definitions/<job_definition_name>/versions/<version_id>

        Request Syntax:
            .. code-block:: python

                organization_id = "1102940376065"
                job_definition_name = "test_job_definition"
                version_id = 1
                response = api_client.get_training_job_definition_version(organization_id, job_definition_name, version_id)

        Params:
            - **organization_id** (str): ORGANIZATION_ID
            - **job_definition_name** (str): training job definition name
            - **version_id** (int): training job version

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    "job_definition_version": 1,
                    "user_parameters": {},
                    "datasets": {
                        "mnist": "1111111111111"
                    },
                    "modified_at": "2018-05-17T12:34:46.344076Z",
                    "job_definition_id": "1443714239154",
                    "handler": "train:handler",
                    "created_at": "2018-05-17T12:34:46.296488Z",
                    "image": "abeja-inc/all-gpu:19.04",
                    "archived": false
                }

        Raises:
            - BadRequest
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        path = '/organizations/{}/training/definitions/{}/versions/{}'.format(
            organization_id, job_definition_name, version_id)
        return self._connection.api_request(method='GET', path=path)

    def delete_training_job_definition_version(
            self, organization_id: str, job_definition_name: str, version_id: int) -> dict:
        """delete a training job definition version

        API reference: DELETE /organizations/<organization_id>/training/definitions/<job_definition_name>/versions/<version_id>

        Request Syntax:
            .. code-block:: python

                organization_id = "1102940376065"
                job_definition_name = "test_job_definition"
                version_id = 1
                response = api_client.delete_training_job_definition_version(organization_id, job_definition_name, version_id)

        Params:
            - **organization_id** (str): ORGANIZATION_ID
            - **job_definition_name** (str): training job definition name
            - **version_id** (int): training job version

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    "job_definition_version": 1,
                    "user_parameters": {},
                    "datasets": {
                        "mnist": "1111111111111"
                    },
                    "modified_at": "2018-05-17T12:34:46.344076Z",
                    "job_definition_id": "1443714239154",
                    "handler": "train:handler",
                    "created_at": "2018-05-17T12:34:46.296488Z",
                    "image": "abeja-inc/all-gpu:19.04"
                }

        Raises:
            - BadRequest
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        path = '/organizations/{}/training/definitions/{}/versions/{}'.format(
            organization_id, job_definition_name, version_id)
        return self._connection.api_request(method='DELETE', path=path)

    def create_training_job(
            self, organization_id: str, job_definition_name: str,
            version_id: int, user_parameters: Optional[dict] = None,
            datasets: Optional[dict] = None, instance_type: Optional[str] = None,
            environment: Optional[dict] = None, description: Optional[str] = None) -> dict:
        """create a training job

        API reference: POST /organizations/<organization_id>/training/definitions/<job_definition_name>/versions/<version_id>/jobs

        Request Syntax:
            .. code-block:: python

                organization_id = "1102940376065"
                job_definition_name = "test_job_definition"
                version_id = 1
                user_parameters = {
                    'BATCH_SIZE': 50
                }
                datasets = {
                    "mnist": "1111111111111"
                }
                response = api_client.create_training_job(
                    organization_id, job_definition_name, version_id, user_parameters, datasets)

        Params:
            - **organization_id** (str): ORGANIZATION_ID
            - **job_definition_name** (str): training job definition name
            - **version_id** (int): training job version
            - **user_parameters** (dict): (**deprecated!!**) user defined parameters set as environment variables. use ``environment`` instead.
            - **datasets** (dict): **[optional]** datasets, combination of alias and dataset_id
            - **instance_type** (str): **[optional]** instance type of running environment
            - **environment** (dict): **[optional]** user defined parameters set as environment variables
            - **description** (str): **[optional]** description of this job

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    "job_definition_id": "1443714239154",
                    "user_parameters": {},
                    "start_time": null,
                    "created_at": "2018-05-17T12:43:59.322367Z",
                    "job_definition_version": 1,
                    "completion_time": null,
                    "status": "Pending",
                    "instance_type": "cpu-1",
                    "modified_at": "2018-05-17T12:43:59.322673Z",
                    "training_job_id": "1443722127663",
                    "creator": {
                        "email": "test@abeja.asia",
                        "is_registered": true,
                        "created_at": "2017-05-26T01:38:46Z",
                        "id": "1128347408389",
                        "display_name": null,
                        "updated_at": "2018-01-04T03:02:12Z",
                        "role": "admin"
                    },
                    "description": null,
                    "statistics": null
                }

        Raises:
            - BadRequest
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        data = {}
        if environment is not None:
            data['environment'] = environment
        elif user_parameters is not None:
            data['environment'] = user_parameters
        if datasets is not None:
            data['datasets'] = datasets
        if instance_type is not None and InstanceType.to_enum(instance_type):
            data['instance_type'] = instance_type
        if description is not None:
            data['description'] = description
        path = '/organizations/{}/training/definitions/{}/versions/{}/jobs'.format(
            organization_id, job_definition_name, version_id)
        return self._connection.api_request(method='POST', path=path, json=data)

    def get_training_jobs(
            self, organization_id: str, job_definition_name: str,
            limit: Optional[int]=None, offset: Optional[int]=None,
            filter_archived: Optional[bool] = None) -> dict:
        """get training jobs

        API reference: GET /organizations/<organization_id>/training/definitions/<job_definition_name>/jobs

        Request Syntax:
            .. code-block:: python

                organization_id = "1102940376065"
                job_definition_name = "test_job_definition"
                response = api_client.get_training_jobs(organization_id, job_definition_name)

        Params:
            - **organization_id** (str): ORGANIZATION_ID
            - **job_definition_name** (str): training job definition name
            - **limit** (int): **[optional]** max number of jobs to be returned (default: 10)
            - **offset** (int): **[optional]** offset of jobs ( which starts from 0 )
            - **filter_archived** (bool): **[optional]** whether include archived ones or not. (default is not-filtered)

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    "entries": [
                        {
                            "user_parameters": {},
                            "start_time": null,
                            "training_job_id": "1443722127663",
                            "created_at": "2018-05-17T12:43:59.322367Z",
                            "completion_time": null,
                            "id": "1443722127663",
                            "job_definition_version": 1,
                            "description": null,
                            "statistics": null,
                            "job_definition_id": "1443714239154",
                            "modified_at": "2018-05-17T12:43:59.322673Z",
                            "status": "Pending",
                            "archived": false,
                            "creator": {
                                "email": "test@abeja.asia",
                                "created_at": "2017-05-26T01:38:46Z",
                                "id": "1128347408389",
                                "role": "admin",
                                "display_name": null,
                                "updated_at": "2018-01-04T03:02:12Z",
                                "is_registered": true
                            }
                        }
                    ],
                    "limit": 10,
                    "offset": 0,
                    "total": 1
                }

        Raises:
            - BadRequest
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        params = {} if filter_archived is None else get_filter_archived_applied_params({}, filter_archived)
        if limit is not None:
            params['limit'] = limit
        if offset is not None:
            params['offset'] = offset
        path = '/organizations/{}/training/definitions/{}/jobs'.format(
            organization_id, job_definition_name)
        return self._connection.api_request(method='GET', path=path, params=params)

    def get_training_job(
            self, organization_id: str, job_definition_name: str, training_job_id: str) -> dict:
        """get a training job

        API reference: GET /organizations/<organization_id>/training/definitions/<job_definition_name>/jobs/<training_job_id>

        Request Syntax:
            .. code-block:: python

                organization_id = "1102940376065"
                job_definition_name = "test_job_definition"
                training_job_id = "1443722127663"
                response = api_client.get_training_job(organization_id, job_definition_name, training_job_id)

        Params:
            - **organization_id** (str): ORGANIZATION_ID
            - **job_definition_name** (str): training job definition name
            - **training_job_id** (str): TRAINING_JOB_ID

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    "job_definition_id": "1443714239154",
                    "user_parameters": {},
                    "start_time": null,
                    "created_at": "2018-05-17T12:43:59.322367Z",
                    "job_definition_version": 1,
                    "completion_time": null,
                    "status": "Pending",
                    "modified_at": "2018-05-17T12:43:59.322673Z",
                    "training_job_id": "1443722127663",
                    "archived": false,
                    "creator": {
                        "email": "test@abeja.asia",
                        "is_registered": true,
                        "created_at": "2017-05-26T01:38:46Z",
                        "id": "1128347408389",
                        "display_name": null,
                        "updated_at": "2018-01-04T03:02:12Z",
                        "role": "admin"
                    },
                    "description": null,
                    "statistics": null
                }

        Raises:
            - BadRequest
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        path = '/organizations/{}/training/definitions/{}/jobs/{}'.format(
            organization_id, job_definition_name, training_job_id)
        return self._connection.api_request(method='GET', path=path)

    def delete_training_job(
            self, organization_id: str, job_definition_name: str, training_job_id: str) -> dict:
        """delete a training job

        API reference: DELETE /organizations/<organization_id>/training/definitions/<job_definition_name>/jobs/<training_job_id>

        Request Syntax:
            .. code-block:: python

                organization_id = "1102940376065"
                job_definition_name = "test_job_definition"
                training_job_id = "1443722127663"
                response = api_client.delete_training_job_definition_version(organization_id,
                                                                             job_definition_name,
                                                                             training_job_id)

        Params:
            - **organization_id** (str): ORGANIZATION_ID
            - **job_definition_name** (str): training job definition name
            - **training_job_id** (str): TRAINING_JOB_ID

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    "message": "test_job_definition:1443722127663 deleted"
                }

        Raises:
            - BadRequest
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        path = '/organizations/{}/training/definitions/{}/jobs/{}'.format(
            organization_id, job_definition_name, training_job_id)
        return self._connection.api_request(method='DELETE', path=path)

    def get_training_result(
            self, organization_id: str, job_definition_name: str, training_job_id: str) -> dict:
        """get a training job result

        API reference: GET /organizations/<organization_id>/training/definitions/<job_definition_name>/jobs/<training_job_id>/result

        Request Syntax:
            .. code-block:: python

                organization_id = "1102940376065"
                job_definition_name = "test_job_definition"
                training_job_id = "1443722127663"
                response = api_client.get_training_result(organization_id, job_definition_name,
                                                          training_job_id)

        Params:
            - **organization_id** (str): ORGANIZATION_ID
            - **job_definition_name** (str): training job definition name
            - **training_job_id** (str): TRAINING_JOB_ID

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    "artifacts": {
                        "complete": {
                            "uri": "dummy_url",
                        }
                    }
                }

        Raises:
            - BadRequest
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        path = '/organizations/{}/training/definitions/{}/jobs/{}/result'.format(
            organization_id, job_definition_name, training_job_id)
        return self._connection.api_request(method='GET', path=path)

    def update_statistics(self, organization_id: str, job_definition_name: str, training_job_id: str,
                          statistics: dict) -> dict:
        """update a training job statistics

        API reference: POST /organizations/<organization_id>/training/definitions/<job_definition_name>/jobs/<training_job_id>/statistics

        Request Syntax:
            .. code-block:: python

                from abeja.train.statistics import Statistics

                statistics = Statistics(progress_percentage=0.5, epoch=1, num_epochs=5, key1='value1')
                statistics.add_stage(name=Statistics.STAGE_TRAIN, accuracy=0.9, loss=0.05)
                statistics.add_stage(name=Statistics.STAGE_VALIDATION, accuracy=0.8, loss=0.1, key2=2)

                response = api_client.update_statistics(statistics)

        Params:
            - **statistics** (str): statistics needs to be saved and updated

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                  "statistics": {
                    "num_epochs": 5,
                    "epoch": 1,
                    "progress_percentage": 0.5,
                    "stages": {
                      "train": {
                        "accuracy": 0.9,
                        "loss": 0.05
                      },
                      "validation": {
                        "accuracy": 0.8,
                        "loss": 0.1,
                        "key2": 2
                      }
                    },
                    "key1": "value1"
                  }
                }

        Raises:
            - BadRequest
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        data = {
            'statistics': statistics
        }
        path = '/organizations/{}/training/definitions/{}/jobs/{}/statistics'.format(
            organization_id, job_definition_name, training_job_id)
        return self._connection.api_request(method='POST', path=path, json=data)
