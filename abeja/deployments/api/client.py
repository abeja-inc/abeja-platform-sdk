from typing import Dict, Optional

from abeja.common.api_client import BaseAPIClient
from abeja.common.utils import print_feature_deprecation
from abeja.exceptions import BadRequest


class APIClient(BaseAPIClient):
    """A low-level client for Deployment API

    .. code-block:: python

       from abeja.deployments import APIClient

       api_client = APIClient()
    """

    def create_deployment(
            self, organization_id: str, name: str = None,
            description: Optional[str] = '',
            default_environment: Optional[Dict[str, str]]=None) -> dict:
        """create a deployment

        API reference: POST /organizations/<organization_id>/deployments

        Request Syntax:
            .. code-block:: python

                organization_id = "1111111111111"
                deployment_name = "deployment_name"
                description = "description"
                default_environment = {
                    'SAMPLE_ENV': 'SAMPLE_VALUE'
                }

                response = api_client.create_deployment(organization_id, deployment_name, default_environment)

        Params:
            - **organization_id** (str): organization identifier
            - **name** (str): deploymnet name
            - **description** (str): description
            - **default_environment** (dict): default environment variables on the running environment

        Return type:
            dict
        Returns:
            Response Syntax:
                .. code-block:: json

                    {
                        "deployment_id": "1111111111111",
                        "name": "deployment_name",
                        "description": "description",
                        "creator": {
                            "display_name": null,
                            "email": "platform-support@abeja.asia",
                            "id": "1111111111111",
                            "is_registered": true,
                            "role": "admin",
                            "created_at": "2017-05-29T07:48:55Z",
                            "updated_at": "2017-11-29T10:21:24Z"
                        },
                        "default_environment": {},
                        "runs": [],
                        "services": [],
                        "triggers": [],
                        "created_at": "2018-06-05T08:52:02.428441Z",
                        "modified_at": "2018-06-05T08:52:02.428587Z"
                    }

        Raises:
            - BadRequest: the resource already exists or parameters is insufficient or invalid.
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        if not name:
            error_message = '"name" is necessary'
            raise BadRequest(
                error=error_message,
                error_description=error_message,
                status_code=400)

        payload = {
            'name': name,
            'description': description
        }
        if default_environment:
            print_feature_deprecation(
                target='default_environment',
                additional_message='new spec does not require "default_environment" on "create_deployment()", '
                                   'Please not to specify "default_environment" here.')
            payload.update({
                'default_environment': default_environment
            })
        path = '/organizations/{}/deployments'.format(organization_id)
        return self._connection.api_request(
            method='POST', path=path, json=payload)

    def get_deployment(self, organization_id: str, deployment_id: str) -> dict:
        """get a deployment

        API reference: GET /organizations/<organization_id>/deployments/<deployment_id>

        Request Syntax:
            .. code-block:: python

                response = api_client.get_deployment(organization_id='1111111111111', deployment_id='1111111111111')

        Params:
            - **organization_id** (str): organization_id
            - **deployment_id** (str): deployment_id of the requested model

        Return type:
            dict

        Returns:
            Response Syntax:
                .. code-block:: json

                    {
                        "deployment_id": "1111111111111",
                        "name": "deployment_name",
                        "creator": {
                            "display_name": null,
                            "email": "platform-support@abeja.asia",
                            "id": "1111111111111",
                            "is_registered": true,
                            "role": "admin",
                            "created_at": "2017-05-29T07:48:55Z",
                            "updated_at": "2017-11-29T10:21:24Z"
                        },
                        "default_environment": {},
                        "runs": [],
                        "services": [],
                        "triggers": [],
                        "created_at": "2018-06-05T08:52:02.428441Z",
                        "modified_at": "2018-06-05T08:52:02.428587Z",
                    }

        Raises:
          - NotFound: model not found
          - Unauthorized: Authentication failed
          - InternalServerError
        """

        path = '/organizations/{}/deployments/{}'.format(
            organization_id, deployment_id)
        return self._connection.api_request(method='GET', path=path)

    def get_deployments(self, organization_id: str) -> dict:
        """Get deployments entries

        API reference: GET /organizations/<organization_id>/deployments/

        Request syntax:
            .. code-block:: python

                response = api_client.get_deployments(organization_id='1102940376065')

        Params:
            - **organization_id** (str): organization_id

        Return type:
            dict

        Returns:
            Return syntax:
                .. code-block:: json

                    {
                        "entries": [
                            {
                                "deployment_id": "1111111111111",
                                "name": "deployment_name",
                                "creator": {
                                    "display_name": null,
                                    "email": "paltform-support@abeja.asia",
                                    "id": "1111111111111",
                                    "is_registered": true,
                                    "role": "admin",
                                    "created_at": "2017-05-29T07:48:55Z",
                                    "updated_at": "2017-11-29T10:21:24Z"
                                },
                                "default_environment": {},
                                "runs": [],
                                "services": [],
                                "triggers": [],
                                "created_at": "2018-06-05T08:52:02.428441Z",
                                "modified_at": "2018-06-05T08:52:02.428587Z"
                            }
                        ]
                    }

        Raises:
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        path = '/organizations/{}/deployments'.format(organization_id)
        return self._connection.api_request(method='GET', path=path)

    def delete_deployment(
            self,
            organization_id: str,
            deployment_id: str) -> dict:
        """delete a deployment

        API reference: DELETE /organizations/<organization_id>/deployments/<deployment_id>

        Request syntax:
            .. code-block:: python

                response = api_client.delete_deployment(organization_id='1111111111111', deployment_id='1111111111111')

        Params:
            - **organization_id** (str): ORGANIZATION_ID
            - **deployment_id** (str): deployment identifier

        Return type:
            dict

        Responses:
            Response syntax:
                .. code-block:: json

                    {
                        "message": "1111111111111 deleted"
                    }

        Raises:
          - NotFound: model not found
          - Unauthorized: Authentication failed
          - InternalServerError
        """
        path = '/organizations/{}/deployments/{}'.format(
            organization_id, deployment_id)
        return self._connection.api_request(method='DELETE', path=path)

    def patch_deployment(
            self, organization_id: str, deployment_id: str, name: str,
            default_environment: Optional[Dict[str, str]]=None):
        """update a deployment

        API reference: PATCH /organizations/<organization_id>/deployments/<deployment_id>

        Request syntax:
            .. code-block:: python

                organization_id = "1111111111111"
                deployment_name = "deployment_name"
                default_environment = {
                    'SAMPLE_ENV': 'SAMPLE_VALUE'
                }

                response = api_client.create_deployment(organization_id, deployment_name, default_environment)

        Params:
            - **organization_id** (str): organization identifier
            - **deployment_id** (str): deployment identifier
            - **name** (str): deploymnet name
            - **default_environment** (dict): default environment variables on the running environment

        Return type:
            dict
        Returns:
            Response Syntax:
                .. code-block:: json

                    {
                        "deployment_id": "1111111111111",
                        "name": "deployment_name",
                        "default_environment": {},
                        "runs": [],
                        "services": [],
                        "triggers": [],
                        "created_at": "2018-06-05T08:52:02.428441Z",
                        "modified_at": "2018-06-05T08:52:02.428587Z"
                    }

        Raises:
            - BadRequest: the resource already exists or parameters is insufficient or invalid.
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        payload = {
            'name': name
        }
        if default_environment is not None:
            payload.update({
                'default_environment': default_environment
            })
        path = '/organizations/{}/deployments/{}'.format(
            organization_id, deployment_id)
        return self._connection.api_request(
            method='PATCH', path=path, json=payload)

    # deployment code version
    def get_deployment_versions(
            self,
            organization_id: str,
            deployment_id: str) -> dict:
        """get a deployment code versions

        API reference: GET /organizations/<organization_id>/deployments/<deployment_id>/versions

        Request Syntax:
            .. code-block:: python

                response = api_client.get_deployment_versions(organization_id='1111111111111', deployment_id='1111111111111')

        Params:
            - **organization_id** (str): organization_id
            - **deployment_id** (str): deployment_id of the requested model

        Return type:
            dict

        Returns:
            Response Syntax:
                .. code-block:: json

                    {
                        "entries": [
                            {
                                "deployment_id": "1111111111111",
                                "creator": {
                                    "display_name": null,
                                    "email": "paltform-support@abeja.asia",
                                    "id": "1111111111111",
                                    "is_registered": true,
                                    "role": "admin",
                                    "created_at": "2017-05-29T07:48:55Z",
                                    "updated_at": "2017-11-29T10:21:24Z"
                                },
                                "version": "0.0.1",
                                "version_id": "ver-abc1111111111111",
                                "handler": "main:handler",
                                "image": "abeja-inc/all-cpu:18.10",
                                "user_parameters": {},
                                "created_at": "2018-06-05T08:52:02.428441Z",
                                "modified_at": "2018-06-05T08:52:02.428587Z"
                            }
                        ]
                    }

        Raises:
          - NotFound: model not found
          - Unauthorized: Authentication failed
          - InternalServerError
        """

        path = '/organizations/{}/deployments/{}/versions'.format(
            organization_id, deployment_id)
        return self._connection.api_request(method='GET', path=path)

    def create_deployment_version(
            self, organization_id: str, deployment_id: str, version: str, handler: str,
            image: str, user_parameters: Optional[Dict[str, str]]=None) -> dict:
        """create a deployment code version

        API reference: POST /organizations/<organization_id>/deployments/<deployment_id>/versions

        Request syntax:
            .. code-block:: python

               deployment_id = '1111111111111',
               version = '0.0.1'
               handler = 'main:handler'
               image = 'abeja-inc/all-cpu:18.10'
               user_parameters = {
                    'SAMPLE_ENV': 'SAMPLE_VALUE'
                }

               response = api_client.create_deployment_version(
                   organization_id, deployment_id, version, handler, image, user_parameters
               )

        Params:
            - **organization_id** (str): organization id
            - **deployment_id** (str): deployment id
            - **version** (str): version
            - **handler** (str) : handler path
            - **user_parameters** (dict): user defined parameters.

        Return type:
            dict

        Returns:
            Response syntax:
                .. code-block:: json

                   {
                       "deployment_id": "1111111111111",
                       "version": "0.0.1",
                       "version_id": "ver-abc1111111111111",
                       "handler": "main:handler",
                       "image": "abeja-inc/all-cpu:18.10",
                       "user_parameters": {},
                       "created_at": "2018-06-14T07:15:43.462664Z",
                       "modified_at": "2018-06-14T07:15:43.462824Z",
                       "upload_url": "https://abeja-model-api-src.s3.amazonaws.com/1462815098134/ver-/source.tgz?xxxxxx"
                   }

            Response Structure:
                - **deployment_id** (str) : deployment id
                - **version** (str) : version
                - **version_id** (str) : version id
                - **handler** (str) : handler path
                - **image** (str) : runtime enviornment
                - **user_parameters** (dict): user defined parameters.
                - **upload_url** (str) : url to upload archived file. **archived file should be uploaded after creating model version using this upload_url**

        Raises:
          - BadRequest: specified deployment id does not exist or deployment version already exist, parameters is insufficient or invalid,
          - Unauthorized: Authentication failed
          - InternalServerError
        """
        payload = {
            'version': version,
            'handler': handler,
            'image': image,
        }
        if user_parameters:
            payload.update({
                'user_parameters': user_parameters,
            })
        path = '/organizations/{}/deployments/{}/versions'.format(
            organization_id, deployment_id)
        return self._connection.api_request(
            method='POST', path=path, json=payload)

    def create_deployment_from_template(self,
                                        organization_id: str,
                                        deployment_id: str,
                                        template_id: int,
                                        version: str,
                                        handler: str,
                                        image: str,
                                        user_parameters: Optional[Dict[str,
                                                                       str]]=None) -> dict:
        """create a deployment from template

        API reference: POST /organizations/<organization_id>/deployments/<deployment_id>/code_templates

        Request syntax:
            .. code-block:: python

               deployment_id = '1111111111111',
               template_id = 1,
               version = '0.0.1'
               handler = 'main:handler'
               image = 'abeja-inc/all-cpu:18.10'
               user_parameters = {
                    'SAMPLE_ENV': 'SAMPLE_VALUE'
                }

               response = api_client.create_deployment_from_template(
                   organization_id, deployment_id, template_id, version, handler, image, user_parameters
               )

        Params:
            - **organization_id** (str): organization id
            - **deployment_id** (str): deployment id
            - **template_id** (int): template id
            - **version** (str): version
            - **handler** (str) : handler path
            - **user_parameters** (dict): user defined parameters.

        Return type:
            dict

        Returns:
            Response syntax:
                .. code-block:: json

                   {
                       "deployment_id": "1111111111111",
                       "version": "0.0.1",
                       "version_id": "ver-abc1111111111111",
                       "handler": "main:handler",
                       "image": "abeja-inc/all-cpu:18.10",
                       "user_parameters": {},
                       "created_at": "2018-06-14T07:15:43.462664Z",
                       "modified_at": "2018-06-14T07:15:43.462824Z"
                   }

            Response Structure:
                - **deployment_id** (str) : deployment id
                - **version** (str) : version
                - **version_id** (str) : version id
                - **handler** (str) : handler path
                - **image** (str) : runtime enviornment
                - **user_parameters** (dict): user defined parameters.
                - **upload_url** (str) : url to upload archived file. **archived file should be uploaded after creating model version using this upload_url**

        Raises:
          - BadRequest: specified deployment id does not exist or deployment version already exist, parameters is insufficient or invalid,
          - Unauthorized: Authentication failed
          - InternalServerError
        """
        payload = {
            'template_id': template_id,
            'version': version,
            'handler': handler,
            'image': image,
        }
        if user_parameters:
            payload.update({
                'user_parameters': user_parameters,
            })
        path = '/organizations/{}/deployments/{}/code_templates'.format(
            organization_id, deployment_id)
        return self._connection.api_request(
            method='POST', path=path, json=payload)

    def get_deployment_version(
            self,
            organization_id: str,
            deployment_id: str,
            version_id: str) -> dict:
        """get a version of a deployment

        API reference: GET /organizations/<organization_id>/deployments/<deployment_id>/versions/<version_id>

        Request syntax:
            .. code-block:: python

               response = api_client.get_deployment_version(organization_id='1111111111111',
                                                       deployment_id='2222222222222',
                                                       version_id='ver-abc3333333333333')

        Params:
            - **organization_id** (str): ORGANIZATION_ID
            - **deployment_id** (str): deployment id
            - **version_id** (str): deployment version id

        Return type:
            dict

        Returns:
            Response syntax:
                .. code-block:: json

                   {
                       "deployment_id": "1111111111111",
                       "version_id": "ver-abc1111111111111",
                       "version": "0.0.1",
                       "handler": "main:handler",
                       "image": "abeja-inc/all-cpu:18.10",
                       "user_parameters": {},
                       "created_at": "2018-04-26T01:12:05.771403Z",
                       "modified_at": "2018-04-26T01:12:05.771533Z"
                   }

            Response Structure:
                - **deployment_id** (str) : deployment id
                - **version** (str) : version
                - **version_id** (str) : version id
                - **handler** (str) : handler path
                - **image** (str) : runtime enviornment
                - **user_parameters** (dict): user defined parameters.

        Raises:
          - NotFound: deployment version not found
          - Unauthorized: Authentication failed
          - InternalServerError
        """
        path = '/organizations/{}/deployments/{}/versions/{}'.format(
            organization_id, deployment_id, version_id)
        return self._connection.api_request(method='GET', path=path)

    def delete_deployment_version(
            self,
            organization_id: str,
            deployment_id: str,
            version_id: str) -> None:
        """delete a version in a deployment

        API reference: DELETE /organizations/<organization_id>/deployments/<deployment_id>/versions/<version_id>

        Request syntax:
            .. code-block:: python

               api_client.delete_deployment_version(
                   organization_id='1111111111111',
                   deployment_id='1111111111111',
                   version_id='ver-abc3333333333333')

        Params:
            - **organization_id** (str): ORGANIZATION_ID
            - **deployment_id** (str): deployment id
            - **version_id** (str): deployment version id

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
          - NotFound: deployment version not found
          - Unauthorized: Authentication failed
          - InternalServerError
        """
        path = '/organizations/{}/deployments/{}/versions/{}'.format(
            organization_id, deployment_id, version_id)
        return self._connection.api_request(method='DELETE', path=path)

    def download_deployment_version(
            self,
            organization_id: str,
            deployment_id: str,
            version_id: str) -> dict:
        """download a deployment code version

        API reference: GET /organizations/<organization_id>/deployments/<deployment_id>/versions/<version_id>/download

        Request Syntax:
            .. code-block:: python

               response = api_client.download_deployment_version(
                   organization_id='1111111111111',
                   deployment_id='1111111111111',
                   version_id='ver-abc3333333333333')

        Params:
            - **organization_id** (str): ORGANIZATION_ID
            - **deployment_id** (str): deployment id
            - **version_id** (str): deployment version id

        Return type:
            dict

        Returns:
            Response Syntax:
                .. code-block:: json

                   {
                        "download_uri": "https://..."
                   }

            Response Structure:
                - **download_uri** (str) : presigned download link of the deployment code version

        Raises:
          - NotFound: deployment not found
          - Unauthorized: Authentication failed
          - InternalServerError
        """
        path = '/organizations/{}/deployments/{}/versions/{}/download'.format(
            organization_id, deployment_id, version_id)
        return self._connection.api_request(method='GET', path=path)
