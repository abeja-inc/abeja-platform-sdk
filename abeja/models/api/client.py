import json
from io import BytesIO
from typing import Optional, IO

from abeja.common.api_client import BaseAPIClient
from abeja.common.file_helpers import convert_to_zipfile_object
from abeja.common.utils import print_feature_deprecation, print_feature_new
from abeja.exceptions import BadRequest
from abeja.common.utils import get_filter_archived_applied_params


class APIClient(BaseAPIClient):
    """A low-level client for Model API

    .. code-block:: python

       from abeja.models import APIClient

       api_client = APIClient()
    """

    def create_model(self, organization_id: str, name: str, description: str) -> dict:
        """create a model

        API reference: POST /organizations/<organization_id>/models/

        Request Syntax:
            .. code-block:: python

               organization_id = "1111111111111"
               model_name = "model_name"
               model_description = "this is description of the model"

               response = api_client.create_model(organization_id, model_name, model_description)

        Params:
            - **organization_id** (str): organization identifier
            - **name** (str): model name
            - **description** (str): model description

        Return type:
            dict
        Returns:
            Response Syntax:
                .. code-block:: json

                   {
                       "model_id": "1111111111111",
                       "name": "model_name",
                       "description": "this is description of the model",
                       "created_at": "2018-01-01T00:00:00.00000Z",
                       "modified_at": "2018-01-01T00:00:00.00000Z",
                       "versions": []
                   }

            Response Structure:
                - **model_id** (str) : model id
                - **name** (str) : model name
                - **description** (str) : model description
                - **versions** (list) :

        Raises:
            - BadRequest: the resource already exists or parameters is insufficient or invalid.
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        print_feature_deprecation(
            target='create_model',
            additional_message='We will renew the terminology of "model" completely. New "model" '
                               'means machine learning model/graph/network file. '
                               'For this, you need to create a training_job_definition '
                               'to manage your "model" file. All models are stored under '
                               'training_job_definition. Please use "create_training_job_definition()" '
                               'instead.')
        payload = {
            'name': name,
            'description': description
        }
        path = '/organizations/{}/models'.format(organization_id)
        return self._connection.api_request(method='POST', path=path, json=payload)

    def get_model(self, organization_id: str, model_id: str) -> dict:
        """get a model

        API reference: GET /organizations/<organization_id>/models/<model_id>

        Request Syntax:
            .. code-block:: python

               response = api_client.get_model(organization_id='1111111111111', model_id='1111111111111')

        Params:
            - **organization_id** (str): organization_id
            - **model_id** (str): model_id of the requested model

        Return type:
            dict

        Returns:
            Response Syntax:
                .. code-block:: json

                   {
                       "model_id": "1111111111111",
                       "name": "model_name",
                       "description": "this is description of the model",
                       "created_at": "2018-01-01T00:00:00.00000Z",
                       "modified_at": "2018-01-01T00:00:00.00000Z",
                       "versions": []
                   }

            Response Structure:
                - **model_id** (str) : model id
                - **name** (str) : model name
                - **description** (str) : model description
                - **versions** (list) :

        Raises:
          - NotFound: model not found
          - Unauthorized: Authentication failed
          - InternalServerError
        """
        print_feature_deprecation(
            target='get_model',
            additional_message='We will renew the terminology of "model" completely. New "model" '
                               'means machine learning model/graph/network file. '
                               'If you want to see the "model" info, '
                               'please use "get_training_model()" instead.')
        path = '/organizations/{}/models/{}'.format(organization_id, model_id)
        return self._connection.api_request(method='GET', path=path)

    def get_models(self, organization_id: str) -> dict:
        """Get models entries

        API reference: GET /organizations/<organization_id>/models/

        Request syntax:
            .. code-block:: python

               response = api_client.list_models(organization_id='1102940376065')

        Params:
            - **organization_id** (str): organization_id

        Return type:
            dict

        Returns:
            Response syntax:
                .. code-block:: json

                   {
                       "entries": [
                           {
                               "model_id": "1111111111111",
                               "name": "model_name",
                               "description": "this is description of the model",
                               "created_at": "2018-01-01T00:00:00.00000Z",
                               "modified_at": "2018-01-01T00:00:00.00000Z",
                               "versions": []
                           }
                       ]
                   }

            Response Structure:
                - **entries** (list)
                    - (dict)
                        - **model_id** (str) : model id
                        - **name** (str) : model name
                        - **description** (str) : model description
                        - **versions** (list) :

        Raises:
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        print_feature_deprecation(
            target='get_models',
            additional_message='We will renew the terminology of "model" completely. New "model" '
                               'means machine learning model/graph/network file. '
                               'For this, All models are stored under training_job_definition. '
                               'If you want to see the list of "model", '
                               'please use "get_training_models()" instead.')
        path = '/organizations/{}/models'.format(organization_id)
        return self._connection.api_request(method='GET', path=path)

    def delete_model(self, organization_id: str, model_id: str) -> dict:
        """delete a model

        API reference: DELETE /organizations/<organization_id>/model/<model_id>

        Request syntax:
            .. code-block:: python

               response = api_client.delete_model(organization_id='1111111111111', model_id='1111111111111')

        Params:
            - **organization_id** (str): ORGANIZATION_ID
            - **model_id** (str): model id

        Return type:
            dict

        Returns:
            Response syntax:
                .. code-block:: json

                   {
                       "message": "1111111111111 deleted"
                   }

            Response Structure:
                - **message** (str) :

        Raises:
          - NotFound: model not found
          - Unauthorized: Authentication failed
          - InternalServerError
        """
        print_feature_deprecation(
            target='delete_model',
            additional_message='We will renew the terminology of "model" completely. New "model" '
                               'means machine learning model/graph/network file. '
                               'New spec does not allow you to delete your "model" file. '
                               'But you can archive/unarchive your "model" file instead.'
                               'If you want to archive your "model" file, '
                               'please use "archive_training_model()". '
                               'If you want to unarchive your "model" file, '
                               'please use "unarchive_training_model()".')
        path = '/organizations/{}/models/{}'.format(organization_id, model_id)
        return self._connection.api_request(method='DELETE', path=path)

    # model version
    def create_model_version(
            self, organization_id: str, model_id: str, version: str, handler: str,
            image: str, content_type: Optional[str]=None, job_definition_name: Optional[str]=None,
            training_job_id: Optional[str]=None) -> dict:
        """create a model version

        API reference: POST /organizations/<organization_id>/models/<model_id>/versions/

        Request syntax:
            .. code-block:: python

               model_id = '1111111111111',
               version = '0.0.1'
               handler = 'main:handler'
               image = 'abeja-inc/all-cpu:18.10'
               content_type = 'application/zip'

               response = api_client.create_model_version(
                   organization_id, model_id, version, handler, image, content_type
               )

        Params:
            - **organization_id** (str): organization id
            - **model_id** (str): model id
            - **version** (str): version
            - **handler** (str) : handler path
            - **content_type** (str) : Mime-type of content **[OPTIONAL]**
            - **job_definition_name** (str) : job definition name used in a model handler **[OPTIONAL]**
            - **training_job_id** (str) : job id **[OPTIONAL]**

        Return type:
            dict

        Returns:
            Response syntax:
                .. code-block:: json

                   {
                       "model_id": "1111111111111",
                       "version": "0.0.1",
                       "version_id": "ver-abc1111111111111",
                       "handler": "main:handler",
                       "image": "abeja-inc/all-cpu:18.10",
                       "created_at": "2018-06-14T07:15:43.462664Z",
                       "modified_at": "2018-06-14T07:15:43.462824Z",
                       "job_definition_id": null,
                       "job_definition_version": null,
                       "training_job_id": null,
                       "upload_url": "https://abeja-model-api-src.s3.amazonaws.com/1462815098134/ver-/source.tgz?xxxxxx"
                   }

            Response Structure:
                - **model_id** (str) : model id
                - **version** (str) : version
                - **version_id** (str) : version id
                - **handler** (str) : handler path
                - **image** (str) : runtime enviornment
                - **job_definition_id** (str) : job definition id
                - **job_definition_version** (str) : job definition version
                - **training_job_id** (str) : job id
                - **upload_url** (str) : url to upload archived file. **archived file should be uploaded after creating model version using this upload_url**

        Raises:
          - BadRequest: specified model id does not exist or model version already exist, parameters is insufficient or invalid,
          - Unauthorized: Authentication failed
          - InternalServerError
        """
        print_feature_deprecation(
            target='create_model_version',
            additional_message='We will renew the terminology of "model" completely. New "model" '
                               'means machine learning model/graph/network file. '
                               'In the new spec, serving/prediction/inference code will be '
                               'managed under "deployment". '
                               'And "model" file will be specified when new deployment is created. '
                               'Please use "create_deployment_version()" instead.')
        payload = {
            'version': version,
            'handler': handler,
            'image': image,
            'content_type': content_type,
        }
        if job_definition_name and training_job_id:
            payload.update({
                'job_definition_name': job_definition_name,
                'training_job_id': training_job_id,
            })
        # create model version
        path = '/organizations/{}/models/{}/versions'.format(organization_id, model_id)
        return self._connection.api_request(method='POST', path=path, json=payload)

    def get_model_version(self, organization_id: str, model_id: str, version_id: str) -> dict:
        """get a version of a model

        API reference: GET /organizations/<organization_id>/models/<model_id>/versions/<version_id>

        Request syntax:
            .. code-block:: python

               response = api_client.get_model_version(organization_id='1111111111111',
                                                       model_id='2222222222222',
                                                       version_id='ver-abc3333333333333')

        Params:
            - **organization_id** (str): ORGANIZATION_ID
            - **model_id** (str): model id
            - **version_id** (str): model version id

        Return type:
            dict

        Returns:
            Response syntax:
                .. code-block:: json

                   {
                       "model_id": "1111111111111",
                       "version_id": "ver-abc1111111111111",
                       "version": "0.0.1",
                       "handler": "main:handler",
                       "image": "abeja-inc/all-cpu:18.10",
                       "job_definition_id": null,
                       "job_definition_version": null,
                       "training_job_id": null,
                       "created_at": "2018-04-26T01:12:05.771403Z",
                       "modified_at": "2018-04-26T01:12:05.771533Z"
                   }

            Response Structure:
                - **model_id** (str) : model id
                - **version** (str) : version
                - **version_id** (str) : version id
                - **handler** (str) : handler path
                - **image** (str) : runtime enviornment
                - **job_definition_id** (str) : job definition id
                - **job_definition_version** (str) : job definition version
                - **training_job_id** (str) : job id

        Raises:
          - NotFound: model version not found
          - Unauthorized: Authentication failed
          - InternalServerError
        """
        print_feature_deprecation(
            target='get_model_version',
            additional_message='We will renew the terminology of "model" completely. New "model" '
                               'means machine learning model/graph/network file. '
                               'In the new spec, serving/prediction/inference code will be '
                               'managed under "deployment". '
                               'And "model" file will be specified when new deployment is created. '
                               'Please use "get_deployment_version()" instead.')
        path = '/organizations/{}/models/{}/versions/{}'.format(organization_id,
                                                                model_id,
                                                                version_id)
        return self._connection.api_request(method='GET', path=path)

    def get_model_versions(self, organization_id: str, model_id: str) -> dict:
        """Get version entries in a model

        API reference: GET /organizations/<organization_id>/models/<model_id>/versions/

        Params:
            - **organization_id** (str): ORGANIZATION_ID
            - **model_id** (str): model id

        Return type:
            dict

        Returns:
            Response syntax:
                .. code-block:: json

                   {
                       "entries": [
                           {
                               "model_id": "1111111111111",
                               "version_id": "ver-abc1111111111111",
                               "version": "0.0.1",
                               "handler": "main:handler",
                               "image": "abeja-inc/all-cpu:18.10",
                               "job_definition_id": null,
                               "job_definition_version": null,
                               "training_job_id": null,
                               "created_at": "2018-04-26T01:12:05.771403Z",
                               "modified_at": "2018-04-26T01:12:05.771533Z"
                           }
                       ]
                   }

            Response Structure:
                - **entries** (list)
                    - (dict)
                        - **model_id** (str) : model id
                        - **version** (str) : version
                        - **version_id** (str) : version id
                        - **handler** (str) : handler path
                        - **image** (str) : runtime enviornment
                        - **job_definition_id** (str) : job definition id
                        - **job_definition_version** (str) : job definition version
                        - **training_job_id** (str) : job id

        Raises:
          - NotFound: model not found
          - Unauthorized: Authentication failed
          - InternalServerError
        """
        print_feature_deprecation(
            target='get_model_versions',
            additional_message='We will renew the terminology of "model" completely. New "model" '
                               'means machine learning model/graph/network file. '
                               'In the new spec, serving/prediction/inference code will be '
                               'managed under "deployment". '
                               'And "model" file will be specified when new deployment is created. '
                               'Please use "get_deployment_versions()" instead.')
        path = '/organizations/{}/models/{}/versions'.format(organization_id, model_id)
        return self._connection.api_request(method='GET', path=path)

    def delete_model_version(self, organization_id: str, model_id: str, version_id: str) -> None:
        """delete a version in a model

        API reference: DELETE /organizations/<organization_id>/models/<model_id>/versions/<version_id>

        Request syntax:
            .. code-block:: python

               api_client.delete_model_version(organization_id='1111111111111',
                                               model_id='1111111111111',
                                               version_id='ver-abc3333333333333')

        Params:
            - **organization_id** (str): ORGANIZATION_ID
            - **model_id** (str): model id
            - **version** (str): model version id

        Return type:
            dict

        Returns:
            Response syntax:
                .. code-block:: json

                   {
                       "message": "ver-abc1111111111111 deleted"
                   }

            Response Structure:
                - **message** (str) :

        Raises:
          - NotFound: model version not found
          - Unauthorized: Authentication failed
          - InternalServerError
        """
        print_feature_deprecation(
            target='delete_model_version',
            additional_message='We will renew the terminology of "model" completely. New "model" '
                               'means machine learning model/graph/network file. '
                               'In the new spec, serving/prediction/inference code will be '
                               'managed under "deployment". '
                               'And "model" file will be specified when new deployment is created. '
                               'Please use "delete_deployment_version()" instead.')
        path = '/organizations/{}/models/{}/versions/{}'.format(organization_id, model_id, version_id)
        return self._connection.api_request(method='DELETE', path=path)

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
        print_feature_new(
            target='get_training_models',
            additional_message='We will renew the terminology of "model" completely. New "model" '
                               'means machine learning model/graph/network file.')
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
        print_feature_new(
            target='create_training_model',
            additional_message='We will renew the terminology of "model" completely. New "model" '
                               'means machine learning model/graph/network file.')
        if model_data is None:
            error_message = "model_data is necessary"
            raise BadRequest(error=error_message, error_description=error_message, status_code=400)
        if parameters is None:
            parameters = {}
        parameters = BytesIO(json.dumps(parameters).encode())
        model_data = convert_to_zipfile_object(model_data)
        files = {
            'model_data': ('model_data.zip', model_data, 'application/zip'),
            'parameters': ('params.json', parameters, 'application/json')
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
        print_feature_new(
            target='get_training_model',
            additional_message='We will renew the terminology of "model" completely. New "model" '
                               'means machine learning model/graph/network file.')
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
        print_feature_new(
            target='patch_training_model',
            additional_message='We will renew the terminology of "model" completely. New "model" '
                               'means machine learning model/graph/network file.')
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
        print_feature_new(
            target='download_training_model',
            additional_message='We will renew the terminology of "model" completely. New "model" '
                               'means machine learning model/graph/network file.')
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
        print_feature_new(
            target='archive_training_model',
            additional_message='We will renew the terminology of "model" completely. New "model" '
                               'means machine learning model/graph/network file.')
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
        print_feature_new(
            target='unarchive_training_model',
            additional_message='We will renew the terminology of "model" completely. New "model" '
                               'means machine learning model/graph/network file.')
        path = '/organizations/{}/training/definitions/{}/models/{}/unarchive'.format(
            organization_id, job_definition_name, model_id)
        return self._connection.api_request(method='POST', path=path)
