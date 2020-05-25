from typing import Optional

from abeja.common.api_client import BaseAPIClient


class APIClient(BaseAPIClient):
    """A Low-Level client for Registry API

    .. code-block:: python

       from abeja.registry import APIClient

       api_client = APIClient()
    """

    def create_repository(
            self, organization_id: str, name: str,
            description: Optional[str] = None) -> dict:
        """create a docker repository

        API reference: POST /organizations/<organization_id>/registry/repositories

        Request Syntax:
            .. code-block:: python

                organization_id = "1410000000000"
                name = "sample_repository"
                description = "this is sample repository"
                response = api_client.create_repository(
                    organization_id, name, description)

        Params:
            - **organization_id** (str): ORGANIZATION_ID
            - **name** (str): repository name
            - **description** (str): description for this repository

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: python

                {
                    "id": "1234567890123",
                    "organization_id": "1410000000000",
                    "name": "sample_repository",
                    "description": "this is sample repository",
                    "tags": [],
                    "creator": {
                        "updated_at": "2018-01-04T03:02:12Z",
                        "role": "admin",
                        "is_registered": True,
                        "id": "1122334455660",
                        "email": "test@abeja.asia",
                        "display_name": None,
                        "created_at": "2017-05-26T01:38:46Z"
                    },
                    "created_at": "2018-06-07T04:42:34.913644Z",
                    "updated_at": "2018-06-07T04:42:34.913726Z"
                }

        Raises:
            - BadRequest
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        payload = {
            'name': name
        }
        if description is not None:
            payload['description'] = description
        path = '/organizations/{}/registry/repositories'.format(
            organization_id)
        return self._connection.api_request(
            method='POST', path=path, json=payload)

    def get_repositories(
            self, organization_id: str,
            limit: Optional[int] = None,
            offset: Optional[int] = None) -> dict:
        """get repositories

        API reference: GET /organizations/<organization_id>/registry/repositories

        Request Syntax:
            .. code-block:: python

                organization_id = "1410000000000"
                response = api_client.get_repositories(organization_id)

        Params:
            - **organization_id** (str): ORGANIZATION_ID
            - **limit** (int): max number of repositories to be returned **[optional]**
            - **offset** (int): offset of repositories ( which starts from 0 ) **[optional]**

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: python

                {
                    "offset": 0,
                    "limit": 10,
                    "has_next": False,
                    "organization_name": "test-org",
                    "organization_id": 1410000000000,
                    "created_at": "2019-05-23T05:13:13Z",
                    "updated_at": "2019-05-23T05:13:15Z",
                    "registry_repositories": [
                        {
                            "id": "1234567890123",
                            "organization_id": "1410000000000",
                            "name": "sample_repository",
                            "description": None,
                            "creator": {
                                "updated_at": "2018-01-04T03:02:12Z",
                                "role": "admin",
                                "is_registered": True,
                                "id": "1122334455660",
                                "email": "test@abeja.asia",
                                "display_name": None,
                                "created_at": "2017-05-26T01:38:46Z"
                            },
                            "created_at": "2018-06-07T04:42:34.913644Z",
                            "updated_at": "2018-06-07T04:42:34.913726Z"
                        }
                    ]
                }

        Raises:
            - BadRequest
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        params = {}
        if limit is not None:
            params['limit'] = limit
        if offset is not None:
            params['offset'] = offset
        path = '/organizations/{}/registry/repositories'.format(
            organization_id)
        return self._connection.api_request(
            method='GET', path=path, params=params)

    def get_repository(
            self, organization_id: str,
            repository_id: str) -> dict:
        """get repository

        API reference: GET /organizations/<organization_id>/registry/repositories/<repository_id>

        Request Syntax:
            .. code-block:: python

                organization_id = "1410000000000"
                repository_id = "1510000000000"
                response = api_client.get_repository(organization_id, repository_id)

        Params:
            - **organization_id** (str): ORGANIZATION_ID
            - **repository** (str): REPOSITORY_ID

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: python

                {
                    "id": "1234567890123",
                    "organization_id": "1410000000000",
                    "name": "sample_repository",
                    "description": None,
                    "tags": [],
                    "creator": {
                        "updated_at": "2018-01-04T03:02:12Z",
                        "role": "admin",
                        "is_registered": True,
                        "id": "1122334455660",
                        "email": "test@abeja.asia",
                        "display_name": None,
                        "created_at": "2017-05-26T01:38:46Z"
                    },
                    "created_at": "2018-06-07T04:42:34.913644Z",
                    "updated_at": "2018-06-07T04:42:34.913726Z"
                }

        Raises:
            - BadRequest
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        path = '/organizations/{}/registry/repositories/{}'.format(
            organization_id, repository_id)
        return self._connection.api_request(method='GET', path=path)

    def delete_repository(
            self, organization_id: str,
            repository_id: str) -> dict:
        """delete repository

        API reference: DELETE /organizations/<organization_id>/registry/repositories/<repository_id>

        Request Syntax:
            .. code-block:: python

                organization_id = "1410000000000"
                repository_id = "1510000000000"
                response = api_client.delete_repository(organization_id, repository_id)

        Params:
            - **organization_id** (str): ORGANIZATION_ID
            - **repository** (str): REPOSITORY_ID

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: python

                {
                    "id": "1234567890123",
                    "organization_id": "1410000000000",
                    "name": "sample_repository",
                    "description": None,
                    "tags": [],
                    "creator": {
                        "updated_at": "2018-01-04T03:02:12Z",
                        "role": "admin",
                        "is_registered": True,
                        "id": "1122334455660",
                        "email": "test@abeja.asia",
                        "display_name": None,
                        "created_at": "2017-05-26T01:38:46Z"
                    },
                    "created_at": "2018-06-07T04:42:34.913644Z",
                    "updated_at": "2018-06-07T04:42:34.913726Z"
                }

        Raises:
            - BadRequest
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        path = '/organizations/{}/registry/repositories/{}'.format(
            organization_id, repository_id)
        return self._connection.api_request(method='DELETE', path=path)

    def get_repository_tags(
            self, organization_id: str,
            repository_id: str,
            limit: Optional[int] = None,
            offset: Optional[int] = None) -> dict:
        """get tags of repository

        API reference: GET /organizations/<organization_id>/registry/repositories/<repository_id>/tags

        Request Syntax:
            .. code-block:: python

                organization_id = "1410000000000"
                repository_id = "1510000000000"
                response = api_client.get_repository_tags(organization_id, repository_id)

        Params:
            - **organization_id** (str): ORGANIZATION_ID
            - **repository** (str): REPOSITORY_ID
            - **limit** (int): max number of tags of repository to be returned **[optional]**
            - **offset** (int): offset of tags of repository ( which starts from 0 ) **[optional]**

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: python

                {
                    "offset": 0,
                    "limit": 10,
                    "has_next": False,
                    "registry_repository_id": "1700000000000",
                    "organization_name": "test-org",
                    "organization_id": "1410000000000",
                    "created_at": "2019-05-23T05:13:13Z",
                    "updated_at": "2019-05-23T05:13:15Z",
                    "tags": [
                        {
                            "size": 2757009,
                            "name": "0.0.4",
                            "media_type": "application/vnd.docker.distribution.manifest.v2+json",
                            "id": 1771682238503,
                            "digest": "sha256:5c40b3c27b9f13c873fefb2139765c56ce97fd50230f1f2d5c91e55dec171907",
                            "creator": {
                                "updated_at": "2018-01-04T03:02:12Z",
                                "role": "admin",
                                "is_registered": True,
                                "id": "1122334455660",
                                "email": "test@abeja.asia",
                                "display_name": None,
                                "created_at": "2017-05-26T01:38:46Z"
                            },
                            "created_at": "2019-05-23T05:13:13Z",
                            "updated_at": "2019-05-23T05:13:15Z"
                        }
                    ]
                }

        Raises:
            - BadRequest
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        params = {}
        if limit is not None:
            params['limit'] = limit
        if offset is not None:
            params['offset'] = offset
        path = '/organizations/{}/registry/repositories/{}/tags'.format(
            organization_id, repository_id)
        return self._connection.api_request(
            method='GET', path=path, params=params)
