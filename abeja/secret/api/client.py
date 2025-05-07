from __future__ import annotations
from typing import Optional
import base64
from abeja.common.api_client import BaseAPIClient
from abeja.exceptions import BadRequest
import re


class APIClient(BaseAPIClient):
    """A Low-Level client for Secret Manager API

    .. code-block:: python

       from abeja.secret import APIClient

       api_client = APIClient()
    """

    def get_secrets(
        self,
        organization_id: str,
        offset: Optional[int] = 0,
        limit: Optional[int] = 50
    ) -> dict:
        """get secrets

        API reference: GET /secret-manager/organizations/<organization_id>/secrets

        Request Syntax:
            .. code-block:: python

                organization_id = "1410000000000"
                offset = 0
                limit = 50
                response = api_client.get_secrets(organization_id, offset, limit)

        Params:
            - **organization_id** (str): organization identifier (required)
            - **offset** (int): **[optional]** offset of secrets (which starts from 0)
            - **limit** (int): **[optional]** max number of secrets to be returned (between 1 and 100)

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    "organization_id": "3617229248589",
                    "secrets": [
                        {
                            "created_at": "2025-05-01T04:13:32.861378Z",
                            "description": "",
                            "expired_at": "2025-05-29T04:13:00Z",
                            "id": "3354488798882",
                            "name": "test",
                            "organization_id": "3617229248589",
                            "properties": null,
                            "provider": "aws-secret-manager",
                            "rotation": false,
                            "updated_at": "2025-05-01T04:13:32.861380Z",
                            "user_id": "3614618482910",
                            "versions": [
                                {
                                    "created_at": "2025-05-01T04:14:20.657971Z",
                                    "id": "9960370863434",
                                    "organization_id": "3617229248589",
                                    "provider": "aws-secret-manager",
                                    "secret_id": "3354488798882",
                                    "status": "inactive",
                                    "updated_at": "2025-05-01T07:05:00.613985Z",
                                    "value": "test",
                                    "version": 1
                                }
                            ]
                        }
                    ],
                    "offset": 0,
                    "limit": 50,
                    "has_next": false
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
        params['return_secret_value'] = True

        path = '/secret-manager/organizations/{}/secrets'.format(
            organization_id,
        )
        result = self._connection.api_request(method='GET', path=path, params=params)

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
    ) -> dict:
        """get secret

        API reference: GET /secret-manager/organizations/<organization_id>/secrets/<secret_id>

        Request Syntax:
            .. code-block:: python

                organization_id = "1410000000000"
                secret_id = "3053595942757"
                response = api_client.get_secret(
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
                    "created_at": "2025-04-30T19:01:19.209973Z",
                    "description": "test",
                    "expired_at": "2025-05-21T19:01:00Z",
                    "id": "3471958194321",
                    "name": "test",
                    "organization_id": "3617229248589",
                    "properties": null,
                    "provider": "aws-secret-manager",
                    "rotation": false,
                    "updated_at": "2025-04-30T19:01:19.209975Z",
                    "user_id": "3614618482910",
                    "versions": [
                        {
                            "created_at": "2025-05-01T04:02:20.962352Z",
                            "id": "4914543680412",
                            "organization_id": "3617229248589",
                            "provider": "aws-secret-manager",
                            "secret_id": "3471958194321",
                            "status": "active",
                            "updated_at": "2025-05-01T07:10:00.646086Z",
                            "value": "test",
                            "version": 1
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
        params['return_secret_value'] = True

        path = '/secret-manager/organizations/{}/secrets/{}'.format(
            organization_id,
            secret_id,
        )
        result = self._connection.api_request(method='GET', path=path, params=params)

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
                description = "AWS access key"
                expired_at = "2024-12-15T16:50:33+09:00"
                response = api_client.create_secret(
                    organization_id, name, value, description, expired_at)

        Params:
            - **organization_id** (str): organization identifier (required)
            - **name** (str): secret name (required) The secret name can contain ASCII letters, numbers, and the following
              characters: `_-` Do not end your secret name with a hyphen followed by six characters. The secret name must
              be unique within the same organization.
            - **value** (str): secret value (required)
            - **description** (str): **[optional]** secret description
            - **expired_at** (str): **[optional]** expiration date (ISO 8601 format)

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    "created_at": "2025-05-01T07:12:23.319068Z",
                    "description": null,
                    "expired_at": null,
                    "id": "2372152227971",
                    "name": "test-1612",
                    "organization_id": "3617229248589",
                    "properties": null,
                    "provider": "aws-secret-manager",
                    "rotation": false,
                    "updated_at": "2025-05-01T07:12:23.319071Z",
                    "user_id": "3614618482910",
                    "versions": [
                        {
                            "created_at": "2025-05-01T07:12:23.321625Z",
                            "id": "1235028292438",
                            "organization_id": "3617229248589",
                            "provider": "aws-secret-manager",
                            "secret_id": "2372152227971",
                            "status": "active",
                            "updated_at": "2025-05-01T07:12:23.321628Z",
                            "value": "test",
                            "version": 1
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

        if not re.match(r'^[a-zA-Z0-9_-]+$', name):
            error_message = '"name" must contain only ASCII letters, numbers, and the following characters: _-'
            raise BadRequest(
                error=error_message,
                error_description=error_message,
                status_code=400
            )

        if re.match(r'.*-......$', name):
            error_message = '"name" must not end with a hyphen followed by six characters'
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

        path = '/secret-manager/organizations/{}/secrets'.format(
            organization_id,
        )

        return self._connection.api_request(method='POST', path=path, json=payload)

    def update_secret(
        self,
        organization_id: str,
        secret_id: str,
        description: Optional[str] = None,
        expired_at: Optional[str] = None,
    ) -> dict:
        """update a secret

        API reference: PATCH /secret-manager/organizations/<organization_id>/secrets/<secret_id>

        Request Syntax:
            .. code-block:: python

                organization_id = "1410000000000"
                secret_id = "3053595942757"
                description = "Updated AWS access key"
                expired_at = "2025-12-15T16:50:33+09:00"
                response = api_client.update_secret(
                    organization_id, secret_id, description, expired_at)

        Params:
            - **organization_id** (str): organization identifier (required)
            - **secret_id** (str): secret identifier (required)
            - **description** (str): **[optional]** secret description
            - **expired_at** (str): **[optional]** expiration date (ISO 8601 format)

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    "created_at": "2025-05-01T07:12:23.319068Z",
                    "description": "test",
                    "expired_at": null,
                    "id": "2372152227971",
                    "name": "test",
                    "organization_id": "3617229248589",
                    "properties": null,
                    "provider": "aws-secret-manager",
                    "rotation": false,
                    "updated_at": "2025-05-01T07:13:37.031149Z",
                    "user_id": "3614618482910",
                    "versions": [
                        {
                            "created_at": "2025-05-01T07:12:23.321625Z",
                            "id": "1235028292438",
                            "organization_id": "3617229248589",
                            "provider": "aws-secret-manager",
                            "secret_id": "2372152227971",
                            "status": "active",
                            "updated_at": "2025-05-01T07:12:23.321628Z",
                            "value": "test",
                            "version": 1
                        }
                    ]
                }

        Raises:
            - BadRequest: Invalid parameters (organization_id or secret_id is missing)
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        payload = {}

        if description:
            payload['description'] = description

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
                    "message": "secret_id 2372152227971 successfully deleted"
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
