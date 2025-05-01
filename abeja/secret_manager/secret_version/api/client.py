from __future__ import annotations
from typing import Optional
import base64
from abeja.common.api_client import BaseAPIClient
from abeja.exceptions import BadRequest


class APIClient(BaseAPIClient):
    """A Low-Level client for Secret Version API

    .. code-block:: python

       from abeja.secret_manager.secret_version import APIClient

       api_client = APIClient()
    """

    def get_secret_versions(
        self,
        organization_id: str,
        secret_id: str,
        offset: Optional[int] = 0,
        limit: Optional[int] = 50,
    ) -> dict:
        """get secret versions

        API reference: GET /secret-manager/organizations/<organization_id>/secrets/<secret_id>/versions

        Request Syntax:
            .. code-block:: python

            organization_id = "1410000000000"
            secret_id = "3053595942757"
            offset = 0
            limit = 50
            response = api_client.get_secret_versions(
                organization_id, secret_id, offset, limit)

        Params:
            - **organization_id** (str): organization identifier
            - **secret_id** (str): secret identifier
            - **offset** (int): **[optional]** offset of versions ( which starts from 0 )
            - **limit** (int): **[optional]** max number of versions to be returned

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

            {
                "pagination": {
                    "count": 1,
                    "has_next": false,
                    "limit": 50,
                    "offset": 0
                },
                "versions": [
                    {
                        "created_at": "2025-04-30T19:01:19.216304Z",
                        "id": "3884379411160",
                        "organization_id": "3617229248589",
                        "provider": "aws-secret-manager",
                        "secret_id": "3471958194321",
                        "status": "active",
                        "updated_at": "2025-05-01T07:35:01.002633Z",
                        "value": "test",
                        "version": 1
                    }
                ]
            }

        Raises:
            - BadRequest
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

        path = '/secret-manager/organizations/{}/secrets/{}/versions'.format(
            organization_id,
            secret_id,
        )
        response = self._connection.api_request(method='GET', path=path, params=params)

        for version in response['versions']:
            if 'value' in version and version['value']:
                try:
                    version['value'] = base64.b64decode(version['value']).decode('utf-8')
                except Exception:
                    pass

        return response

    def get_secret_version(
        self,
        organization_id: str,
        secret_id: str,
        version_id: str,
    ) -> dict:
        """get secret version

        API reference: GET /secret-manager/organizations/<organization_id>/secrets/<secret_id>/versions/<version_id>

        Request Syntax:
            .. code-block:: python

            organization_id = "1410000000000"
            secret_id = "3053595942757"
            version_id = "1234567890123"
            response = api_client.get_secret_version(
                organization_id, secret_id, version_id)

        Params:
            - **organization_id** (str): organization identifier
            - **secret_id** (str): secret identifier
            - **version_id** (str): version identifier

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

            {
                "created_at": "2025-05-01T04:02:20.962352Z",
                "id": "4914543680412",
                "organization_id": "3617229248589",
                "provider": "aws-secret-manager",
                "secret_id": "3471958194321",
                "status": "active",
                "updated_at": "2025-05-01T07:40:00.204109Z",
                "value": "test",
                "version": 2
            }

        Raises:
            - BadRequest
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

        if not version_id:
            error_message = '"version_id" is necessary'
            raise BadRequest(
                error=error_message,
                error_description=error_message,
                status_code=400
            )

        params = {}
        params['return_secret_value'] = True

        path = '/secret-manager/organizations/{}/secrets/{}/versions/{}'.format(
            organization_id,
            secret_id,
            version_id,
        )
        response = self._connection.api_request(method='GET', path=path, params=params)

        if 'value' in response and response['value']:
            try:
                response['value'] = base64.b64decode(response['value']).decode('utf-8')
            except Exception:
                pass

        return response

    def create_secret_version(
        self,
        organization_id: str,
        secret_id: str,
        value: str,
    ) -> dict:
        """create a secret version

        API reference: POST /secret-manager/organizations/<organization_id>/secrets/<secret_id>/versions

        Request Syntax:
            .. code-block:: python

            organization_id = "1410000000000"
            secret_id = "3053595942757"
            value = "AKIAIOSFODNN7EXAMPLE"
            response = api_client.create_secret_version(
                organization_id, secret_id, value)

        Params:
            - **organization_id** (str): organization identifier
            - **secret_id** (str): secret identifier
            - **value** (str): secret value

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

            {
                "created_at": "2025-05-01T18:58:18.712607Z",
                "id": "7285296397904",
                "organization_id": "3617229248589",
                "provider": "aws-secret-manager",
                "secret_id": "9598242896082",
                "status": "active",
                "updated_at": "2025-05-01T18:58:18.712610Z",
                "value": "AKIAIOSFODNN7EXAMPLE",
                "version": 2
            }

        Raises:
            - BadRequest
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

        if value is None or value == '':
            error_message = '"value" is necessary'
            raise BadRequest(
                error=error_message,
                error_description=error_message,
                status_code=400
            )

        params = {}
        params['return_secret_value'] = True

        payload = {
            'value': value,
        }

        path = '/secret-manager/organizations/{}/secrets/{}/versions'.format(
            organization_id,
            secret_id,
        )

        return self._connection.api_request(method='POST', path=path, json=payload, params=params)

    def update_secret_version(
        self,
        organization_id: str,
        secret_id: str,
        version_id: str,
        status: str,
    ) -> dict:
        """update a secret version

        API reference: PATCH /secret-manager/organizations/<organization_id>/secrets/<secret_id>/versions/<version_id>

        Request Syntax:
            .. code-block:: python

            organization_id = "1410000000000"
            secret_id = "3053595942757"
            version_id = "1234567890123"
            status = "inactive"
            response = api_client.update_secret_version(
                organization_id, secret_id, version_id, status)

        Params:
            - **organization_id** (str): organization identifier
            - **secret_id** (str): secret identifier
            - **version_id** (str): version identifier
            - **status** (str): version status ('active' or 'inactive')

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

            {
                "created_at": "2025-05-01T18:58:18.712607Z",
                "id": "7285296397904",
                "organization_id": "3617229248589",
                "provider": "aws-secret-manager",
                "secret_id": "9598242896082",
                "status": "inactive",
                "updated_at": "2025-05-01T19:04:40.398828Z",
                "value": "test",
                "version": 2
            }

        Raises:
            - BadRequest
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

        if not version_id:
            error_message = '"version_id" is necessary'
            raise BadRequest(
                error=error_message,
                error_description=error_message,
                status_code=400
            )

        if not status:
            error_message = '"status" is necessary'
            raise BadRequest(
                error=error_message,
                error_description=error_message,
                status_code=400
            )

        if status not in ['active', 'inactive']:
            error_message = '"status" need to be "active" or "inactive"'
            raise BadRequest(
                error=error_message,
                error_description=error_message,
                status_code=400
            )

        payload = {
            'status': status,
        }

        path = '/secret-manager/organizations/{}/secrets/{}/versions/{}'.format(
            organization_id,
            secret_id,
            version_id,
        )
        return self._connection.api_request(method='PATCH', path=path, json=payload)

    def delete_secret_version(
        self,
        organization_id: str,
        secret_id: str,
        version_id: str,
    ) -> dict:
        """delete a secret version

        API reference: DELETE /secret-manager/organizations/<organization_id>/secrets/<secret_id>/versions/<version_id>

        Request Syntax:
            .. code-block:: python

            organization_id = "1410000000000"
            secret_id = "3053595942757"
            version_id = "1234567890123"
            response = api_client.delete_secret_version(
                organization_id, secret_id, version_id)

        Params:
            - **organization_id** (str): organization identifier
            - **secret_id** (str): secret identifier
            - **version_id** (str): version identifier

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

            {
                "message": "secret_version_id 1234567890123 successfully deleted"
            }

        Raises:
            - BadRequest
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

        if not version_id:
            error_message = '"version_id" is necessary'
            raise BadRequest(
                error=error_message,
                error_description=error_message,
                status_code=400
            )

        path = '/secret-manager/organizations/{}/secrets/{}/versions/{}'.format(
            organization_id,
            secret_id,
            version_id,
        )
        return self._connection.api_request(method='DELETE', path=path)
