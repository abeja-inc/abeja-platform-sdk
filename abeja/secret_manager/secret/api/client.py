from __future__ import annotations
from typing import Optional
import base64
from abeja.common.api_client import BaseAPIClient
from abeja.exceptions import BadRequest


class APIClient(BaseAPIClient):
    """A Low-Level client for Secret Manager API

    .. code-block:: python

       from abeja.secret_manager.secret import APIClient

       api_client = APIClient()
    """

    def get_secrets(
        self,
        organization_id: str,
        offset: Optional[int] = 0,
        limit: Optional[int] = 50,
        return_secret_value: Optional[bool] = False,
    ) -> dict:
        """get secrets

        API reference: GET /secret-manager/organizations/<organization_id>/secrets

        Request Syntax:
            .. code-block:: python

                organization_id = "1410000000000"
                offset = 0
                limit = 50
                return_secret_value = False
                response = api_client.get_secrets(
                    organization_id, offset, limit, return_secret_value)

        Params:
            - **organization_id** (str): organization identifier (required)
            - **offset** (int): **[optional]** offset of secrets (which starts from 0)
            - **limit** (int): **[optional]** max number of secrets to be returned (between 1 and 100)
            - **return_secret_value** (bool): **[optional]** whether to return secret values

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    'organization_id': '1410000000000'
                    'secrets': [
                        {
                            'id': '3053595942757',
                            'organization_id': '1410000000000',
                            'name': 'AWS_ACCESS_KEY',
                            'description': 'AWS access key',
                            'rotation': false,
                            'created_at': '2023-12-15T16:50:33+09:00',
                            'updated_at': '2023-12-15T16:50:33+09:00',
                            'versions': [
                                {
                                    'id': '1234567890123',
                                    'secret_id': '3053595942757',
                                    'version': 1,
                                    'expired_at': '2024-12-15T16:50:33+09:00',
                                    'created_at': '2023-12-15T16:50:33+09:00'
                                }
                            ]
                        },
                        ...
                    ],
                    'offset': 0,
                    'limit': 50,
                    'has_next': False,
                }

        Raises:
            - BadRequest: Invalid parameters (organization_id is missing, offset < 0, limit < 1 or limit > 100)
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        if not organization_id:
            error_message = '"organization_id" is necessary'
            raise BadRequest(
                error=error_message,
                error_description=error_message,
                status_code=400
            )

        params = {}
        if offset is None:
            offset = 0
        elif offset < 0:
            error_message = '"offset" must be greater than or equal to 0'
            raise BadRequest(
                error=error_message,
                error_description=error_message,
                status_code=400
            )

        if limit is None:
            limit = 50
        elif limit < 1 or limit > 100:
            error_message = '"limit" must be between 1 and 100'
            raise BadRequest(
                error=error_message,
                error_description=error_message,
                status_code=400
            )

        params['offset'] = offset
        params['limit'] = limit
        params['return_secret_value'] = bool(return_secret_value)

        path = '/secret-manager/organizations/{}/secrets'.format(
            organization_id,
        )
        result = self._connection.api_request(method='GET', path=path, params=params)

        if return_secret_value:
            for secret in result.get('secrets', []):
                for version in secret.get('versions', []):
                    if 'value' in version:
                        try:
                            version['value'] = base64.b64decode(version['value']).decode('utf-8')
                        except Exception:
                            pass

        return result

    def get_secret(
        self,
        organization_id: str,
        secret_id: str,
        return_secret_value: Optional[bool] = False,
    ) -> dict:
        """get secret

        API reference: GET /secret-manager/organizations/<organization_id>/secrets/<secret_id>

        Request Syntax:
            .. code-block:: python

                organization_id = "1410000000000"
                secret_id = "3053595942757"
                return_secret_value = False
                response = api_client.get_secret(
                    organization_id, secret_id, return_secret_value)

        Params:
            - **organization_id** (str): organization identifier (required)
            - **secret_id** (str): secret identifier (required)
            - **return_secret_value** (bool): **[optional]** whether to return secret values

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    'id': '3053595942757',
                    'organization_id': '1410000000000',
                    'name': 'AWS_ACCESS_KEY',
                    'description': 'AWS access key',
                    'rotation': false,
                    'created_at': '2023-12-15T16:50:33+09:00',
                    'updated_at': '2023-12-15T16:50:33+09:00',
                    'versions': [
                        {
                            'id': '1234567890123',
                            'secret_id': '3053595942757',
                            'version': 1,
                            'expired_at': '2024-12-15T16:50:33+09:00',
                            'created_at': '2023-12-15T16:50:33+09:00'
                        }
                    ]
                }

        Raises:
            - BadRequest: Invalid parameters (organization_id or secret_id is missing)
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        if not organization_id:
            error_message = '"organization_id" is necessary'
            raise BadRequest(
                error=error_message,
                error_description=error_message,
                status_code=400
            )

        if not secret_id:
            error_message = '"secret_id" is necessary'
            raise BadRequest(
                error=error_message,
                error_description=error_message,
                status_code=400
            )

        params = {}
        params['return_secret_value'] = bool(return_secret_value)

        path = '/secret-manager/organizations/{}/secrets/{}'.format(
            organization_id,
            secret_id,
        )
        result = self._connection.api_request(method='GET', path=path, params=params)

        if return_secret_value:
            for version in result.get('versions', []):
                if 'value' in version:
                    try:
                        version['value'] = base64.b64decode(version['value']).decode('utf-8')
                    except Exception:
                        pass

        return result

    def create_secret(
        self,
        organization_id: str,
        name: str,
        value: str,
        rotation: bool = False,
        description: Optional[str] = None,
        expired_at: Optional[str] = None,
    ) -> dict:
        """create a secret

        API reference: POST /secret-manager/organizations/<organization_id>/secrets

        Request Syntax:
            .. code-block:: python

                organization_id = "1410000000000"
                name = "AWS_ACCESS_KEY"
                value = "AKIAIOSFODNN7EXAMPLE"
                rotation = False
                description = "AWS access key"
                expired_at = "2024-12-15T16:50:33+09:00"
                response = api_client.create_secret(
                    organization_id, name, value, rotation, description, expired_at)

        Params:
            - **organization_id** (str): organization identifier (required)
            - **name** (str): secret name (required)
            - **value** (str): secret value (required)
            - **rotation** (bool): **[optional]** whether to enable rotation
            - **description** (str): **[optional]** secret description
            - **expired_at** (str): **[optional]** expiration date (ISO 8601 format)

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    'id': '3053595942757',
                    'organization_id': '1410000000000',
                    'name': 'AWS_ACCESS_KEY',
                    'description': 'AWS access key',
                    'rotation': false,
                    'created_at': '2023-12-15T16:50:33+09:00',
                    'updated_at': '2023-12-15T16:50:33+09:00',
                    'versions': [
                        {
                            'id': '1234567890123',
                            'secret_id': '3053595942757',
                            'version': 1,
                            'value': 'AKIAIOSFODNN7EXAMPLE',
                            'expired_at': '2024-12-15T16:50:33+09:00',
                            'created_at': '2023-12-15T16:50:33+09:00'
                        }
                    ]
                }

        Raises:
            - BadRequest: Invalid parameters (organization_id, name, or value is missing)
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        if not organization_id:
            error_message = '"organization_id" is necessary'
            raise BadRequest(
                error=error_message,
                error_description=error_message,
                status_code=400
            )

        if not name:
            error_message = '"name" is necessary'
            raise BadRequest(
                error=error_message,
                error_description=error_message,
                status_code=400
            )

        if value is None or value == '':
            error_message = '"value" is necessary'
            raise BadRequest(
                error=error_message,
                error_description=error_message,
                status_code=400
            )

        encoded_value = base64.b64encode(value.encode('utf-8')).decode('utf-8')

        payload = {
            'name': name,
            'value': encoded_value,
        }

        if expired_at:
            payload['expired_at'] = expired_at

        if description:
            payload['description'] = description

        if rotation:
            payload['rotation'] = str(rotation).lower()

        path = '/secret-manager/organizations/{}/secrets'.format(
            organization_id,
        )

        result = self._connection.api_request(method='POST', path=path, json=payload)

        return result

    def update_secret(
        self,
        organization_id: str,
        secret_id: str,
        description: Optional[str] = None,
        rotation: Optional[bool] = False,
        expired_at: Optional[str] = None,
    ) -> dict:
        """update a secret

        API reference: PATCH /secret-manager/organizations/<organization_id>/secrets/<secret_id>

        Request Syntax:
            .. code-block:: python

                organization_id = "1410000000000"
                secret_id = "3053595942757"
                description = "Updated AWS access key"
                rotation = True
                expired_at = "2025-12-15T16:50:33+09:00"
                response = api_client.update_secret(
                    organization_id, secret_id, description, rotation, expired_at)

        Params:
            - **organization_id** (str): organization identifier (required)
            - **secret_id** (str): secret identifier (required)
            - **description** (str): **[optional]** secret description
            - **rotation** (bool): **[optional]** whether to enable rotation
            - **expired_at** (str): **[optional]** expiration date (ISO 8601 format)

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    'id': '3053595942757',
                    'organization_id': '1410000000000',
                    'name': 'AWS_ACCESS_KEY',
                    'description': 'Updated AWS access key',
                    'rotation': true,
                    'created_at': '2023-12-15T16:50:33+09:00',
                    'updated_at': '2024-04-30T10:30:00+09:00',
                    'versions': [
                        {
                            'id': '1234567890123',
                            'secret_id': '3053595942757',
                            'version': 1,
                            'expired_at': '2025-12-15T16:50:33+09:00',
                            'created_at': '2023-12-15T16:50:33+09:00'
                        }
                    ]
                }

        Raises:
            - BadRequest: Invalid parameters
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        payload = {}

        if description:
            payload['description'] = description

        if rotation:
            payload['rotation'] = str(rotation).lower()

        if expired_at:
            payload['expired_at'] = expired_at

        path = '/secret-manager/organizations/{}/secrets/{}'.format(
            organization_id,
            secret_id,
        )
        return self._connection.api_request(method='PATCH', path=path, json=payload)

    def delete_secret(
        self,
        organization_id: str,
        secret_id: str,
    ) -> dict:
        """delete a secret

        API reference: DELETE /secret-manager/organizations/<organization_id>/secrets/<secret_id>

        Request Syntax:
            .. code-block:: python

                organization_id = "1410000000000"
                secret_id = "3053595942757"
                response = api_client.delete_secret(
                    organization_id, secret_id)

        Params:
            - **organization_id** (str): organization identifier (required)
            - **secret_id** (str): secret identifier (required)

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    'id': '3053595942757',
                    'organization_id': '1410000000000',
                    'name': 'AWS_ACCESS_KEY',
                    'description': 'AWS access key',
                    'rotation': false,
                    'created_at': '2023-12-15T16:50:33+09:00',
                    'updated_at': '2023-12-15T16:50:33+09:00'
                }

        Raises:
            - BadRequest: Invalid parameters (organization_id or secret_id is missing)
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        if not organization_id:
            error_message = '"organization_id" is necessary'
            raise BadRequest(
                error=error_message,
                error_description=error_message,
                status_code=400
            )

        if not secret_id:
            error_message = '"secret_id" is necessary'
            raise BadRequest(
                error=error_message,
                error_description=error_message,
                status_code=400
            )

        path = '/secret-manager/organizations/{}/secrets/{}'.format(
            organization_id,
            secret_id,
        )
        return self._connection.api_request(method='DELETE', path=path)
