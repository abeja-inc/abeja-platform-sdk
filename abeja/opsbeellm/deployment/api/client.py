from typing import Optional

from abeja.opsbeellm.common.api_client import OpsBeeLLMBaseAPIClient
from abeja.exceptions import BadRequest


class APIClient(OpsBeeLLMBaseAPIClient):
    """A Low-Level client for OpsBee LLM Deployment API

    .. code-block:: python

       from abeja.opsbeellm.deployment import APIClient

       api_client = APIClient()
    """

    def get_deployments(
        self,
        account_id: str,
        organization_id: str,
        offset: Optional[int] = 0,
        limit: Optional[int] = 1000,
    ) -> dict:
        """get deployments

        API reference: GET /accounts/<account_id>/organizations/<organization_id>/deployments

        Request Syntax:
            .. code-block:: python

                account_id = "1122334455660"
                organization_id = "1410000000000"
                offset = 0
                limit = 1000
                response = api_client.get_deployments(
                    account_id, organization_id, offset, limit)

        Params:
            - **account_id** (str): account identifier
            - **organization_id** (str): organization identifier
            - **offset** (int): **[optional]** offset of deployments ( which starts from 0 )
            - **limit** (int): **[optional]** max number of deployments to be returned

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: python
                {
                    'account_id': '3214751235078',
                    'organization_id': '3208401525829'
                    'deployments': [
                        {
                            'id': '3053595942757',
                            'account_id': '3214751235078',
                            'organization_id': '3208401525829',
                            'name': 'deploymentA',
                            'description': 'deploymentAの説明',
                            'type': 'qa',
                            'history_count': 0,
                            'created_at': '2023-12-15T16:50:33+09:00',
                            'updated_at': '2023-12-15T16:50:33+09:00'
                        },
                        {
                            'id': '9968625354849',
                            'account_id': '3214751235078',
                            'organization_id': '3208401525829',
                            'name': 'deployment-chat-gpt35-turbo',
                            'description': 'Chat用デプロイメント',
                            'type': 'chat',
                            'history_count': 3,
                            'created_at': '2023-12-04T16:01:52+09:00',
                            'updated_at': '2023-12-04T16:01:52+09:00',
                        },
                        ...
                    ],
                    'offset': 0,
                    'limit': 1000,
                    'has_next': False,
                }

        Raises:
            - BadRequest
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        params = {}
        if offset is None:
            offset = 0
        if limit is None:
            limit = 1000
        params['offset'] = offset
        params['limit'] = limit

        path = '/accounts/{}/organizations/{}/deployments?offset={}&limit={}'.format(
            account_id,
            organization_id,
            offset,
            limit,
        )
        return self._connection.api_request(method='GET', path=path, params=params)

    def get_deployment(
        self,
        account_id: str,
        organization_id: str,
        deployment_id: str,
    ) -> dict:
        """get deployments

        API reference: GET /accounts/<account_id>/organizations/<organization_id>/deployments

        Request Syntax:
            .. code-block:: python

                account_id = "1122334455660"
                organization_id = "1410000000000"
                deployment_id = "9968625354849"
                response = api_client.get_deployment(
                    account_id, organization_id, deployment_id)

        Params:
            - **account_id** (str): account identifier
            - **organization_id** (str): organization identifier
            - **deployment_id** (str): deployment identifier

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: python
                {
                    'id': '9968625354849',
                    'account_id': '3214751235078',
                    'organization_id': '3208401525829',
                    'name': 'deployment-chat-gpt35-turbo',
                    'description': 'Chat用デプロイメント',
                    'type': 'chat',
                    'history_count': 3,
                    'created_at': '2023-12-04T16:01:52+09:00',
                    'updated_at': '2023-12-04T16:01:52+09:00',
                },

        Raises:
            - BadRequest
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        path = '/accounts/{}/organizations/{}/deployments/{}'.format(
            account_id,
            organization_id,
            deployment_id,
        )
        return self._connection.api_request(method='GET', path=path)

    def create_deployment(
        self,
        account_id: str,
        organization_id: str,
        name: str,
        type: str,
        description: Optional[str] = None,
    ) -> dict:
        """create a deployment

        API reference: POST /accounts/<account_id>/organizations/<organization_id>/deployments/

        Request Syntax:
            .. code-block:: python

                account_id = "1122334455660"
                organization_id = "1410000000000"
                name = "deployment name"
                description = "deployment description"
                type = "qa"
                response = api_client.create_deployment(
                    account_id, organization_id, name, type, description)

        Params:
            - **account_id** (str): account identifier
            - **organization_id** (str): organization identifier
            - **name** (str): deployment name
            - **description** (str): **[optional]** deployment description
            - **type** (str): deployment type. available type are "qa" or "chat".

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: python
                {
                    'id': "1234567890123",
                    'account_id': "1122334455660",
                    'organization_id': "1410000000000",
                    'name': "deployment name",
                    'description': "deployment description",
                    'type': "qa",
                    'created_at' : "2023-12-13T04:42:34.913644Z",
                    'updated_at' : "2023-12-13T04:42:34.913644Z",
                }

        Raises:
            - BadRequest
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        if not name:
            error_message = '"name" is necessary'
            raise BadRequest(
                error=error_message,
                error_description=error_message,
                status_code=400
            )
        if not type:
            error_message = '"type" is necessary'
            raise BadRequest(
                error=error_message,
                error_description=error_message,
                status_code=400
            )
        if type not in ['qa', 'chat']:
            error_message = '"type" need to "qa" or "chat"'
            raise BadRequest(
                error=error_message,
                error_description=error_message,
                status_code=400
            )

        path = '/accounts/{}/organizations/{}/deployments'.format(
            account_id,
            organization_id,
        )

        payload = {
            'name': name,
            'type': type,
        }
        if description is not None:
            payload['description'] = description
        else:
            payload['description'] = ''

        return self._connection.api_request(method='POST', path=path, json=payload)

    def update_deployment(
        self,
        account_id: str,
        organization_id: str,
        deployment_id: str,
        name: str,
        description: Optional[str] = None,
    ) -> dict:
        """update a deployment

        API reference: PATCH /accounts/<account_id>/organizations/<organization_id>/deployments/<deployment_id>

        Request Syntax:
            .. code-block:: python

                account_id = "1122334455660"
                organization_id = "1410000000000"
                deployment_id = "9968625354849"
                name = "deployment name"
                description = "deployment description"
                response = api_client.update_deployment(
                    account_id, organization_id, deployment_id, name, description)

        Params:
            - **account_id** (str): account identifier
            - **organization_id** (str): organization identifier
            - **deployment_id** (str): deployment identifier
            - **name** (str): deployment name
            - **description** (str): **[optional]** deployment description

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: python
                {
                    'id': "1234567890123",
                    'account_id': "1122334455660",
                    'organization_id': "1410000000000",
                    'name': "deployment name",
                    'description': "deployment description",
                    'type': "qa",
                    'created_at' : "2023-12-13T04:42:34.913644Z",
                    'updated_at' : "2023-12-14T04:42:34.913644Z",
                }

        Raises:
            - BadRequest
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        if not name:
            error_message = '"name" is necessary'
            raise BadRequest(
                error=error_message,
                error_description=error_message,
                status_code=400
            )

        path = '/accounts/{}/organizations/{}/deployments/{}'.format(
            account_id,
            organization_id,
            deployment_id,
        )

        payload = {
            'name': name,
        }
        if description is not None:
            payload['description'] = description
        else:
            payload['description'] = ''

        return self._connection.api_request(method='PATCH', path=path, json=payload)

    def delete_deployment(
        self,
        account_id: str,
        organization_id: str,
        deployment_id: str,
    ) -> dict:
        """delete a deployment

        API reference: DELETE /accounts/<account_id>/organizations/<organization_id>/deployments/<deployment_id>

        Request Syntax:
            .. code-block:: python

                account_id = "1122334455660"
                organization_id = "1410000000000"
                deployment_id = "9968625354849"
                response = api_client.delete_deployment(
                    account_id, organization_id, deployment_id)

        Params:
            - **account_id** (str): account identifier
            - **organization_id** (str): organization identifier
            - **deployment_id** (str): deployment identifier

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: python
                {
                    'message': f'deployment 9968625354849 was deleted.
                }

        Raises:
            - BadRequest
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        path = '/accounts/{}/organizations/{}/deployments/{}'.format(
            account_id,
            organization_id,
            deployment_id,
        )
        return self._connection.api_request(method='DELETE', path=path)
