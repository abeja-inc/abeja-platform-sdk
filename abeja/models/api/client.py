import json
from io import BytesIO
from typing import Optional, IO

from abeja.common.api_client import BaseAPIClient
from abeja.common.file_helpers import convert_to_zipfile_object
from abeja.exceptions import BadRequest
from abeja.common.utils import get_filter_archived_applied_params


class APIClient(BaseAPIClient):
    """A low-level client for Model API

    .. code-block:: python

       from abeja.models import APIClient

       api_client = APIClient()
    """

    def get_training_models(
            self, organization_id: str, job_definition_name: str,
            filter_archived: Optional[bool] = None) -> dict:
        """Get models entries

        API reference: GET /organizations/<organization_id>/training/definitions/<job_definition_name>/models

        Request syntax:
            .. code-block:: python

               response = api_client.list_models(organization_id='1102940376065')

        Params:
            - **organization_id** (str): organization_id
            - **job_definition_name** (str): training job definition name
            - **filter_archived** (bool): **[optional]** whether include archived ones or not. (default is not-filtered)

        Return type:
            dict

        Returns:
            Response syntax:
                .. code-block:: json

                   {
                       "entries": [
                           {
                               "training_model_id": "1111111111111",
                               "job_definition_id": "1111111111111",
                               "training_job_id": "1111111111111",
                               "user_parameters": {},
                               "description": "this is description of the model",
                               "archived": false,
                               "exec_env": "cloud",
                               "archived": false,
                               "created_at": "2018-01-01T00:00:00.00000Z",
                               "modified_at": "2018-01-01T00:00:00.00000Z"
                           }
                       ]
                   }

            Response Structure:
                - **entries** (list)
                    - (dict)
                        - **training_model_id** (str) : training model id
                        - **job_definition_id** (str) : job definition id
                        - **training_job_id** (str) : training job id
                        - **user_parameters** (dict): user defined parameters.
                        - **description** (str) : model description.
                        - **archived** (bool) : archived or not.
                        - **exec_env** (enum) : Executed environment. One of [cloud, local, none].

        Raises:
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        params = None if filter_archived is None else get_filter_archived_applied_params({}, filter_archived)
        path = '/organizations/{}/training/definitions/{}/models'.format(organization_id, job_definition_name)
        return self._connection.api_request(method='GET', path=path, params=params)

    def create_training_model(
            self, organization_id: str, job_definition_name: str,
            model_data: IO, parameters: Optional[dict] = None) -> dict:
        """create a training model.

        API reference: POST /organizations/<organization_id>/training/definitions/<job_definition_name>/models

        Request Syntax:
            .. code-block:: python

                organization_id = "1102940376065"
                job_definition_name = 'test_job_definition'
                model_data = '....'
                parameters = {
                    "description": "description",
                    "user_parameters": {}
                }
                response = api_client.create_training_model(
                    organization_id, job_definition_name, model_data, parameters)

        Params:
            - **organization_id** (str): ORGANIZATION_ID
            - **job_definition_name** (str): training job definition name
            - **model_data** (IO): model data
            - **parameters** (dict): parameters for creating training model
                - **description** (str): Description
                - **user_parameters** (dict): user defined parameters.

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    "training_model_id": "1111111111111",
                    "job_definition_id": "1111111111111",
                    "training_job_id": "1111111111111",
                    "user_parameters": {},
                    "description": "this is description of the model",
                    "archived": false,
                    "exec_env": "cloud",
                    "created_at": "2018-01-01T00:00:00.00000Z",
                    "modified_at": "2018-01-01T00:00:00.00000Z"
                }

        Raises:
            - InvalidDataFormat
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        if model_data is None:
            error_message = "model_data is necessary"
            raise BadRequest(error=error_message, error_description=error_message, status_code=400)
        if parameters is None:
            parameters = {}
        model_data = convert_to_zipfile_object(model_data)
        files = {
            'model_data': ('model_data.zip', model_data, 'application/zip'),
            'parameters': ('params.json', BytesIO(json.dumps(parameters).encode()), 'application/json')
        }
        path = '/organizations/{}/training/definitions/{}/models'.format(organization_id, job_definition_name)
        return self._connection.api_request(method='POST', path=path, files=files)

    def get_training_model(self, organization_id: str, job_definition_name: str, model_id: str) -> dict:
        """get a training model

        API reference: GET /organizations/<organization_id>/training/definitions/<job_definition_name>/models/<model_id>

        Request Syntax:
            .. code-block:: python

               response = api_client.get_training_model(
                   organization_id='1111111111111', job_definition_name='1111111111111', model_id='1111111111111')

        Params:
            - **organization_id** (str): organization_id
            - **job_definition_name** (str): training job definition name
            - **model_id** (str): model_id of the requested model

        Return type:
            dict

        Returns:
            Response Syntax:
                .. code-block:: json

                   {
                        "training_model_id": "1111111111111",
                        "job_definition_id": "1111111111111",
                        "training_job_id": "1111111111111",
                        "user_parameters": {},
                        "description": "this is description of the model",
                        "archived": false,
                        "exec_env": "cloud",
                        "archived": false,
                        "created_at": "2018-01-01T00:00:00.00000Z",
                        "modified_at": "2018-01-01T00:00:00.00000Z"
                   }

            Response Structure:
                - **training_model_id** (str) : training model id
                - **job_definition_id** (str) : job definition id
                - **training_job_id** (str) : training job id
                - **user_parameters** (dict): user defined parameters.
                - **description** (str) : model description.
                - **archived** (bool) : archived or not.
                - **exec_env** (enum) : Executed environment. One of [cloud, local, none].

        Raises:
          - NotFound: model not found
          - Unauthorized: Authentication failed
          - InternalServerError
        """
        path = '/organizations/{}/training/definitions/{}/models/{}'.format(
            organization_id, job_definition_name, model_id)
        return self._connection.api_request(method='GET', path=path)

    def patch_training_model(
            self, organization_id: str, job_definition_name: str, model_id: str, description: str) -> dict:
        """patch a training model

        API reference: PATCH /organizations/<organization_id>/training/definitions/<job_definition_name>/models/<model_id>

        Request Syntax:
            .. code-block:: python

               response = api_client.patch_training_model(
                   organization_id='1111111111111', job_definition_name='1111111111111',
                   model_id='1111111111111', description='new description')

        Params:
            - **organization_id** (str): organization_id
            - **job_definition_name** (str): training job definition name
            - **model_id** (str): model_id of the requested model
            - **description** (str): description

        Return type:
            dict

        Returns:
            Response Syntax:
                .. code-block:: json

                   {
                        "training_model_id": "1111111111111",
                        "job_definition_id": "1111111111111",
                        "training_job_id": "1111111111111",
                        "user_parameters": {},
                        "description": "this is description of the model",
                        "archived": false,
                        "exec_env": "cloud",
                        "created_at": "2018-01-01T00:00:00.00000Z",
                        "modified_at": "2018-01-01T00:00:00.00000Z"
                   }

            Response Structure:
                - **training_model_id** (str) : training model id
                - **job_definition_id** (str) : job definition id
                - **training_job_id** (str) : training job id
                - **user_parameters** (dict): user defined parameters.
                - **description** (str) : model description.
                - **archived** (bool) : archived or not.
                - **exec_env** (enum) : Executed environment. One of [cloud, local, none].

        Raises:
          - NotFound: model not found
          - Unauthorized: Authentication failed
          - InternalServerError
        """
        params = {
            'description': description
        }
        path = '/organizations/{}/training/definitions/{}/models/{}'.format(
            organization_id, job_definition_name, model_id)
        return self._connection.api_request(method='PATCH', path=path, json=params)

    def download_training_model(self, organization_id: str, job_definition_name: str, model_id: str) -> dict:
        """download a training model

        API reference: GET /organizations/<organization_id>/training/definitions/<job_definition_name>/models/<model_id>/download

        Request Syntax:
            .. code-block:: python

               response = api_client.download_training_model(
                   organization_id='1111111111111', job_definition_name='1111111111111', model_id='1111111111111')

        Params:
            - **organization_id** (str): organization_id
            - **job_definition_name** (str): training job definition name
            - **model_id** (str): model_id of the requested model

        Return type:
            dict

        Returns:
            Response Syntax:
                .. code-block:: json

                   {
                        "download_uri": "https://..."
                   }

            Response Structure:
                - **download_uri** (str) : presigned download link of the training model

        Raises:
          - NotFound: model not found
          - Unauthorized: Authentication failed
          - InternalServerError
        """
        path = '/organizations/{}/training/definitions/{}/models/{}/download'.format(
            organization_id, job_definition_name, model_id)
        return self._connection.api_request(method='GET', path=path)

    def archive_training_model(self, organization_id: str, job_definition_name: str, model_id: str) -> dict:
        """archive a training model

        API reference: POST /organizations/<organization_id>/training/definitions/<job_definition_name>/models/<model_id>/archive

        Request Syntax:
            .. code-block:: python

               response = api_client.archive_training_model(
                   organization_id='1111111111111', job_definition_name='1111111111111', model_id='1111111111111')

        Params:
            - **organization_id** (str): organization_id
            - **job_definition_name** (str): training job definition name
            - **model_id** (str): model_id of the requested model

        Return type:
            dict

        Returns:
            Response Syntax:
                .. code-block:: json

                   {
                        "message": "{job_definition_name}:{model_id} archived"
                   }

            Response Structure:
                - **message** (str) : message

        Raises:
          - NotFound: model not found
          - Unauthorized: Authentication failed
          - InternalServerError
        """
        path = '/organizations/{}/training/definitions/{}/models/{}/archive'.format(
            organization_id, job_definition_name, model_id)
        return self._connection.api_request(method='POST', path=path)

    def unarchive_training_model(self, organization_id: str, job_definition_name: str, model_id: str) -> dict:
        """unarchive a training model

        API reference: POST /organizations/<organization_id>/training/definitions/<job_definition_name>/models/<model_id>/unarchive

        Request Syntax:
            .. code-block:: python

               response = api_client.unarchive_training_model(
                   organization_id='1111111111111', job_definition_name='1111111111111', model_id='1111111111111')

        Params:
            - **organization_id** (str): organization_id
            - **job_definition_name** (str): training job definition name
            - **model_id** (str): model_id of the requested model

        Return type:
            dict

        Returns:
            Response Syntax:
                .. code-block:: json

                   {
                        "message": "{job_definition_name}:{model_id} unarchived"
                   }

            Response Structure:
                - **message** (str) : message

        Raises:
          - NotFound: model not found
          - Unauthorized: Authentication failed
          - InternalServerError
        """
        path = '/organizations/{}/training/definitions/{}/models/{}/unarchive'.format(
            organization_id, job_definition_name, model_id)
        return self._connection.api_request(method='POST', path=path)
