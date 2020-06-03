from io import BytesIO
import json
import mimetypes
import os
from pathlib import Path
from typing import Dict, IO, Optional
import urllib.parse

from abeja.common.api_client import BaseAPIClient
from abeja.common.file_helpers import convert_to_valid_path
from abeja.exceptions import BadRequest, Unauthorized, NotFound, Forbidden, InternalServerError
from abeja.common.utils import get_filter_archived_applied_params


def encode_metadata(metadata: dict) -> Dict[str, str]:
    encoded = {}
    for key, value in metadata.items():
        key = urllib.parse.quote(str(key), encoding='utf-8')
        value = urllib.parse.quote(str(value), encoding='utf-8')
        encoded[key] = value
    return encoded


def decode_metadata(encoded_metadata: Dict[str, str]) -> Dict[str, str]:
    decoded = {}
    for key, value in encoded_metadata.items():
        key = urllib.parse.unquote(key, encoding='utf-8')
        value = urllib.parse.unquote(value, encoding='utf-8')
        decoded[key] = value
    return decoded


def decode_file_metadata_if_exist(file: dict) -> dict:
    if file.get('metadata'):
        return {
            **file,
            'metadata': decode_metadata(file['metadata'])
        }
    return file


class APIClient(BaseAPIClient):
    """A low-level client for Datalake API

    .. code-block:: python

        from abeja.datalake import APIClient

        api_client = APIClient()
    """

    def create_channel(self, organization_id: str, name: str,
                       description: str, storage_type: str) -> dict:
        """create a channel

        API reference: POST /organizations/<organization_id>/channels/

        Request Syntax:
            .. code-block:: python

                organization_id = "1234567890123"
                name = "sample channel"
                description = "sample channel description"
                storage_type = "datalake"
                response = api_client.create_channel(
                    organization_id, name, description, storage_type)

        Params:
            - **organization_id** (str): ORGANIZATION_ID
            - **name** (str): channel name
            - **description** (str): channel description
            - **storage_type** (str): datalake or file

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    "organization_id": "1234567890123",
                    "updated_at": "2017-09-12T10:11:46Z",
                    "organization_name": "abeja-inc",
                    "channel": {
                        "updated_at": "2018-05-15T17:14:03Z",
                        "created_at": "2018-05-15T17:14:02Z",
                        "storage_type": "datalake",
                        "name": "test",
                        "description": "test",
                        "display_name": "test",
                        "channel_id": "1230000000000"
                    },
                    "created_at": "2017-09-12T10:11:46Z"
                }

        Raises:
            - BadRequest
            - Unauthorized
            - Forbidden
            - InternalServerError
        """
        params = {
            'name': name,
            'description': description,
            'storage_type': storage_type
        }
        path = '/organizations/{}/channels'.format(organization_id)
        return self._connection.api_request(
            method='POST', path=path, json=params)

    def list_channels(
            self,
            organization_id: str,
            limit: Optional[int]=None,
            offset: Optional[int]=None,
            filter_archived: Optional[bool] = None) -> dict:
        """get channels

        API reference: GET /organizations/<organization_id>/channels/

        Request Syntax:
            .. code-block:: python

                organization_id = "1234567890123"
                response = api_client.list_channels(organization_id)

        Params:
            - **organization_id** (str): ORGANIZATION_ID
            - **limit** (int): **[optional]** max number of channels to be returned
            - **offset** (int): **[optional]** offset of channels ( which starts from 0 )
            - **filter_archived** (bool): **[optional]** If ``true``, include archived jobs, otherwise exclude archived jobs. (default: ``false``)

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    "updated_at": "2017-09-12T10:11:46Z",
                    "channels": [
                        {
                            "updated_at": "2018-05-15T17:14:03Z",
                            "display_name": "test",
                            "description": "test",
                            "name": "test",
                            "channel_id": "1230000000000",
                            "created_at": "2018-05-15T17:14:02Z",
                            "storage_type": "datalake",
                            "archived": false
                        },
                    ],
                    "limit": 50,
                    "has_next": true,
                    "organization_name": "abeja-inc",
                    "offset": 0,
                    "created_at": "2017-09-12T10:11:46Z",
                    "organization_id": "1234567890123"
                }

        Raises:
            - Unauthorized: Authentication failed
            - NotFound: channel not found
            - Forbidden
            - InternalServerError
        """
        params = {}
        if limit is not None:
            params['limit'] = limit
        if offset is not None:
            params['offset'] = offset

        params = get_filter_archived_applied_params(params, filter_archived)

        path = '/organizations/{}/channels'.format(organization_id)
        return self._connection.api_request(
            method='GET', path=path, params=params)

    def get_channel(self, organization_id: str, channel_id: str) -> dict:
        """get a channel

        API reference: GET /organizations/<organization_id>/channels/<channel_id>

        Request Syntax:
            .. code-block:: python

                organization_id = "1234567890123"
                channel_id = "1230000000000"
                response = api_client.get_channel(organization_id, channel_id)

        Params:
            - **organization_id** (str): ORGANIZATION_ID
            - **channel_id** (str): CHANNEL_ID

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    "updated_at": "2017-09-12T10:11:46Z",
                    "created_at": "2017-09-12T10:11:46Z",
                    "channel": {
                        "created_at": "2018-05-15T17:14:02Z",
                        "name": "test",
                        "updated_at": "2018-05-15T17:14:03Z",
                        "channel_id": "1230000000000",
                        "storage_type": "datalake",
                        "display_name": "test",
                        "description": "test",
                        "archived": false
                    },
                    "organization_id": "1234567890123",
                    "organization_name": "abeja-inc"
                }

        Raises:
            - Unauthorized: Authentication failed
            - NotFound: channel not found
            - Forbidden
            - InternalServerError
        """
        path = '/organizations/{}/channels/{}'.format(
            organization_id, channel_id)
        return self._connection.api_request(method='GET', path=path)

    def patch_channel(self, organization_id: str, channel_id: str,
                      name: str=None, description: str=None) -> dict:
        """edit a channel

        API reference: PATCH /organizations/<organization_id>/channels/<channel_id>

        Request Syntax:
            .. code-block:: python

                organization_id = "1234567890123"
                channel_id = "1230000000000"
                name = 'updated_name'
                description = 'updated_description'
                response = api_client.patch_channel(organization_id, channel_id, name, description)

        Params:
            - **organization_id** (str): ORGANIZATION_ID
            - **channel_id** (str): CHANNEL_ID
            - **name** (str): channel name
            - **description** (str): channel description

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    "channel": {
                        "storage_type": "datalake",
                        "description": "updated_description",
                        "updated_at": "2018-05-15T17:30:21Z",
                        "created_at": "2018-05-15T17:14:02Z",
                        "display_name": "updated_description",
                        "channel_id": "1230000000000",
                        "name": "updated_name"
                    },
                    "organization_name": "abeja-inc",
                    "updated_at": "2017-09-12T10:11:46Z",
                    "created_at": "2017-09-12T10:11:46Z",
                    "organization_id": "1234567890123"
                }

        Raises:
            - BadRequest
            - Unauthorized: Authentication failed
            - Forbidden
            - NotFound: channel not found
            - InternalServerError
        """
        params = {}
        if name:
            params['name'] = name
        if description:
            params['description'] = description
        path = '/organizations/{}/channels/{}'.format(
            organization_id, channel_id)
        return self._connection.api_request(
            method='PATCH', path=path, json=params)

    def put_channel_datasource(self, organization_id: str, channel_id: str,
                               datasource_id: str) -> dict:
        """connect a datasource with a channel

        API reference: PUT /organizations/<organization_id>/channels/<channel_id>/datasources/<datasource_id>

        Request Syntax:
            .. code-block:: python

                organization_id = "1234567890123"
                channel_id = "1230000000000"
                datasource_id = "1442132811920"
                response = api_client.put_channel_datasource(organization_id,
                                                             channel_id, datasource_id)

        Params:
            - **organization_id** (str): ORGANIZATION_ID
            - **channel_id** (str): CHANNEL_ID
            - **datasource_id** (str): DATASOURCE_ID

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    "organization_id": "1234567890123",
                    "datasource": {
                        "datasource_id": "1442132811920",
                        "created_at": "2018-05-15T10:33:00Z",
                        "display_name": "test",
                        "secret": "c78cc952d6aa021b1701c3a7e68205cc84c4eddd",
                        "updated_at": "2018-05-15T10:33:00Z"
                    },
                    "organization_name": "abeja-inc",
                    "created_at": "2017-09-12T10:11:46Z",
                    "updated_at": "2017-09-12T10:11:46Z"
                }

        Raises:
            - Unauthorized: Authentication failed
            - Forbidden
            - NotFound: channel not found
            - Conflict
            - InternalServerError
        """
        path = '/organizations/{}/channels/{}/datasources/{}'.format(
            organization_id, channel_id, datasource_id)
        return self._connection.api_request(method='PUT', path=path)

    def list_channel_datasources(
            self,
            organization_id: str,
            channel_id: str) -> dict:
        """get datasources of a channel

        API reference: GET /organizations/<organization_id>/channels/<channel_id>/datasources

        Request Syntax:
            .. code-block:: python

                organization_id = "1234567890123"
                channel_id = "1230000000000"
                response = api_client.list_channel_datasources(organization_id, channel_id)

        Params:
            - **organization_id** (str): ORGANIZATION_ID
            - **channel_id** (str): CHANNEL_ID

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    "limit": 50,
                    "has_next": false,
                    "updated_at": "2017-09-12T10:11:46Z",
                    "datasources": [
                        {
                            "created_at": "2018-05-15T17:37:12Z",
                            "datasource_id": "1442132811920",
                            "secret": "c123aa2751dc123235156040ed160103877b9aaa",
                            "updated_at": "2018-05-15T17:37:12Z",
                            "display_name": "test_datasource"
                        }
                    ],
                    "organization_name": "abeja-inc",
                    "created_at": "2017-09-12T10:11:46Z",
                    "offset": 0,
                    "organization_id": "1234567890123"
                }

        Raises:
            - Unauthorized: Authentication failed
            - NotFound: channel not found
            - Forbidden
            - InternalServerError
        """
        path = '/organizations/{}/channels/{}/datasources'.format(
            organization_id, channel_id)
        return self._connection.api_request(method='GET', path=path)

    def delete_channel_datasource(self, organization_id: str, channel_id: str,
                                  datasource_id: str):
        """delete datasource of a channel

        API reference: DELETE /organizations/<organization_id>/channels/<channel_id>/datasources/<datasource_id>

        Request Syntax:
            .. code-block:: python

                organization_id = "1234567890123"
                channel_id = "1230000000000"
                datasource_id = "1442132811920"
                response = api_client.delete_channel_datasource(
                    organization_id, channel_id, datasource_id)

        Params:
            - **organization_id** (str): ORGANIZATION_ID
            - **channel_id** (str): CHANNEL_ID
            - **datasource_id** (str): DATASOURCE_ID

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    "organization_id": "1234567890123",
                    "datasource": {
                        "secret": "c78cc952d6aa021b1701c3a7e68205cc84c4eddd",
                        "created_at": "2018-05-15T10:33:00Z",
                        "display_name": "test",
                        "updated_at": "2018-05-15T10:33:00Z",
                        "datasource_id": "1442132811920"
                    },
                    "organization_name": "abeja-inc",
                    "created_at": "2017-09-12T10:11:46Z",
                    "updated_at": "2017-09-12T10:11:46Z"
                }

        Raises:
            - Unauthorized: Authentication failed
            - NotFound: channel not found
            - Forbidden
            - InternalServerError
        """
        path = '/organizations/{}/channels/{}/datasources/{}'.format(
            organization_id, channel_id, datasource_id)
        return self._connection.api_request(method='DELETE', path=path)

    def archive_channel(self, organization_id: str, channel_id: str):
        """archive a channel

        API reference: POST /organizations/<organization_id>/channels/<channel_id>/archive

        Request Syntax:
            .. code-block:: python

                organization_id = "1234567890123"
                channel_id = "1230000000000"
                response = api_client.archive_channel(
                    organization_id, channel_id)

        Params:
            - **organization_id** (str): ORGANIZATION_ID
            - **channel_id** (str): CHANNEL_ID

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    "organization_id": "1234567890123",
                    "channel": {
                        "updated_at": "2018-06-06T09:43:34Z",
                        "storage_type": "datalake",
                        "security_method": "organization",
                        "name": "example-channel",
                        "display_name": "example-channel",
                        "description": "this is sample channel",
                        "created_at": "2018-05-30T10:44:28Z",
                        "channel_id": "1234567890123",
                        "archived": true
                    },
                    "organization_name": "abeja-inc",
                    "created_at": "2017-09-12T10:11:46Z",
                    "updated_at": "2017-09-12T10:11:46Z"
                }

        Raises:
            - Unauthorized: Authentication failed
            - NotFound: channel not found
            - Forbidden
            - InternalServerError
        """
        path = '/organizations/{}/channels/{}/archive'.format(
            organization_id, channel_id)
        return self._connection.api_request(method='POST', path=path)

    def unarchive_channel(self, organization_id: str, channel_id: str):
        """unarchive a channel

        API reference: POST /organizations/<organization_id>/channels/<channel_id>/unarchive

        Request Syntax:
            .. code-block:: python

                organization_id = "1234567890123"
                channel_id = "1230000000000"
                response = api_client.unarchive_channel(
                    organization_id, channel_id)

        Params:
            - **organization_id** (str): ORGANIZATION_ID
            - **channel_id** (str): CHANNEL_ID

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    "organization_id": "1234567890123",
                    "channel": {
                        "updated_at": "2018-06-06T09:43:34Z",
                        "storage_type": "datalake",
                        "security_method": "organization",
                        "name": "example-channel",
                        "display_name": "example-channel",
                        "description": "this is sample channel",
                        "created_at": "2018-05-30T10:44:28Z",
                        "channel_id": "1234567890123",
                        "archived": false
                    },
                    "organization_name": "abeja-inc",
                    "created_at": "2017-09-12T10:11:46Z",
                    "updated_at": "2017-09-12T10:11:46Z"
                }

        Raises:
            - Unauthorized: Authentication failed
            - NotFound: channel not found
            - Forbidden
            - InternalServerError
        """
        path = '/organizations/{}/channels/{}/unarchive'.format(
            organization_id, channel_id)
        return self._connection.api_request(method='POST', path=path)

    def get_channel_file_upload(self, channel_id: str, content_type: str,
                                metadata: dict=None) -> dict:
        """get upload info for a channel.

        API reference: POST /channels/<channel_id>/

        Request Syntax:
            .. code-block:: python

                channel_id = "1230000000000"
                content_type = "image/jpeg"
                metadata = {
                    "x-abeja-meta-filename": "sample.jpg"
                }
                response = api_client.get_channel_file_upload(
                    channel_id, content_type, metadata)

        Params:
            - **channel_id** (str): CHANNEL_ID
            - **content_type** (str): content type of a file to be uploaded
            - **metadata** (dict): key-value pair of metadata for the file

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    "url_expires_on": "2018-05-15T19:06:05+00:00",
                    "upload_url": "...",
                    "uploaded_at": null,
                    "metadata": {},
                    "content_type": "image/jpeg",
                    "file_id": "20180515T180605-f4acc798-9afa-40a1-b500-ebce42a4fa3f"
                }

        Raises:
            - Unauthorized: Authentication failed
            - NotFound: channel not found
            - Forbidden
            - InternalServerError
        """
        path = '/channels/{}'.format(channel_id)
        if not metadata:
            metadata = {}
        headers = {
            'Content-Type': content_type
        }
        encoded_metadata = encode_metadata(metadata)
        headers.update(encoded_metadata)
        res = self._connection.api_request(
            method='POST', headers=headers, path=path)
        return decode_file_metadata_if_exist(res)

    def post_channel_file_upload(
            self,
            channel_id: str,
            file_obj: IO,
            content_type: str,
            metadata: dict=None,
            lifetime: str=None,
            conflict_target: str=None) -> dict:
        """upload a file to a channel.

        API reference: POST /channels/<channel_id>/upload

        Request Syntax:
            .. code-block:: python

                channel_id = "1230000000000"
                content_type = "image/jpeg"
                metadata = {
                    "x-abeja-meta-filename": "sample.jpg"
                }
                with open('sample.jpg', 'rb') as f:
                    response = api_client.post_channel_file_upload(
                        channel_id, f, content_type, metadata=metadata)

        Params:
            - **channel_id** (str): CHANNEL_ID
            - **file_obj** (a file-like object) : a file-like object to upload. It must implement the read method, and must return bytes.
            - **content_type** (str): content type of a file to be uploaded
            - **metadata** (dict): **[optional]** key-value pair of metadata for the file
            - **lifetime** (str): **[optional]** each one of `1day` / `1week` / `1month` / `6months`. the file will be deleted after the specified time.
            - **conflict_target** (str): **[optional]** return `409 Conflict` when the same value of specified key already exists in channel.

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    "uploaded_at": null,
                    "metadata": {
                        "x-abeja-meta-filename": "sample.jpg"
                    },
                    "lifetime": "1day",
                    "content_type": "image/jpeg",
                    "file_id": "20180515T180605-f4acc798-9afa-40a1-b500-ebce42a4fa3f"
                }

        Raises:
            - BadRequest: given parameters are invalid
            - Unauthorized: Authentication failed
            - NotFound: channel not found
            - Forbidden
            - InternalServerError
        """
        path = '/channels/{}/upload'.format(channel_id)
        if not metadata:
            metadata = {}
        headers = {
            'Content-Type': content_type
        }
        encoded_metadata = encode_metadata(metadata)
        headers.update(encoded_metadata)

        params = {}
        if lifetime is not None:
            params['lifetime'] = lifetime
        if conflict_target is not None:
            params['conflict_target'] = conflict_target
        res = self._connection.api_request(
            method='POST',
            headers=headers,
            path=path,
            params=params,
            data=file_obj)
        return decode_file_metadata_if_exist(res)

    def list_channel_files(
            self, channel_id: str, start: str=None, end: str=None,
            timezone: str=None, items_per_page: int=None, sort: str=None,
            next_page_token: str=None, query: str=None) -> dict:
        """get files in a channel.

        API reference: GET /channels/<channel_id>/

        Request Syntax:
            .. code-block:: python

                channel_id = "1230000000000"
                response = api_client.list_channel_files(channel_id)

        Params:
            - **channel_id** (str): CHANNEL_ID
            - **start** (str): start date of target uploaded files
            - **end** (str): end date of target uploaded files
            - **timezone** (str): timezone of specified start and end date
            - **items_per_page** (int): max number of files to be returned
            - **sort** (str):
                the order of the file list.
                multiple items can be specified by separating with commas (,).
                It is possible to sort in descending order by specifying a hyphen (-) in front of the item.
                By default, the list is sorted by uploaded_at in ascending order.
            - **next_page_token** (str):
                token for offset of files.
                other params should not be used with next_page_token.
            - **query** (str):
                query to search.
                It is possible to filter what contain specific value by describing like "x-abeja-meta-filename:filename".

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    "next_page_token": null,
                    "files": [
                        {
                            "content_type": "image/jpeg",
                            "metadata": {
                                "x-abeja-meta-filename": "000000006197.jpg"
                            },
                            "uploaded_at": "2018-05-10T11:02:08+00:00",
                            "url_expires_on": "2018-05-15T18:54:37+00:00",
                            "download_uri": "...",
                            "file_id": "20180510T110208-193d0d17-f0b1-4549-96df-651c02ccb8c9"
                        },
                    ]
                }

        Raises:
            - Unauthorized: Authentication failed
            - NotFound: channel not found
            - Forbidden
            - InternalServerError
        """
        params = {}
        if start is not None:
            params['start'] = start
        if end is not None:
            params['end'] = end
        if (start or end) and timezone is not None:
            params['timezone'] = timezone
        if items_per_page is not None:
            params['items_per_page'] = items_per_page
        if sort is not None:
            params['sort'] = sort
        if next_page_token is not None:
            params['next_page_token'] = next_page_token
        if query is not None:
            assert isinstance(
                query, str), 'Unexpected query type: {}'.format(
                type(query))
            params['q'] = query
        path = '/channels/{}'.format(channel_id)
        res = self._connection.api_request(
            method='GET', path=path, params=params)

        if res.get('files'):
            res['files'] = [
                decode_file_metadata_if_exist(f)
                for f in res['files']
            ]
        return res

    def get_channel_file_download(self, channel_id: str, file_id: str) -> dict:
        """get a file info in a channel.

        API reference: GET /channels/<channel_id>/<file_id>

        Request Syntax:
            .. code-block:: python

                channel_id = "1230000000000"
                file_id = "20180510T110208-193d0d17-f0b1-4549-96df-651c02ccb8c9"
                response = api_client.get_channel_file_download(channel_id, file_id)

        Params:
            - **channel_id** (str): CHANNEL_ID
            - **file_id** (str): FILE_ID

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    "download_uri": "...",
                    "url_expires_on": "2018-05-15T18:57:03+00:00",
                    "metadata": {
                        "x-abeja-meta-filename": "000000009851.jpg"
                    },
                    "file_id": "20180510T110210-a2d3a218-5357-4919-8218-9090acaa147e",
                    "content_type": "image/jpeg",
                    "uploaded_at": "2018-05-10T11:02:10+00:00"
                }

        Raises:
            - Unauthorized: Authentication failed
            - NotFound: channel not found
            - Forbidden
            - InternalServerError
        """
        path = '/channels/{}/{}'.format(channel_id, file_id)
        res = self._connection.api_request(method='GET', path=path)
        return decode_file_metadata_if_exist(res)

    def delete_channel_file(self, channel_id: str, file_id: str) -> dict:
        """delete a file in a channel.

        API reference: DELETE /channels/<channel_id>/<file_id>

        Request Syntax:
            .. code-block:: python

                channel_id = "1230000000000"
                file_id = "20180510T110208-193d0d17-f0b1-4549-96df-651c02ccb8c9"
                response = api_client.delete_channel_file(channel_id, file_id)

        Params:
            - **channel_id** (str): CHANNEL_ID
            - **file_id** (str): FILE_ID

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    "message": "deleted file (20180510T110208-193d0d17-f0b1-4549-96df-651c02ccb8c9)"
                }

        Raises:
            - Unauthorized: Authentication failed
            - NotFound: channel not found
            - Forbidden
            - InternalServerError
        """
        path = '/channels/{}/{}'.format(channel_id, file_id)
        return self._connection.api_request(method='DELETE', path=path)

    def put_channel_file_metadata(
            self,
            channel_id: str,
            file_id: str,
            metadata: dict=None) -> dict:
        """update a file metadata in a channel.

        API reference: PUT /channels/<channel_id>/<file_id>/metadata

        Request Syntax:
            .. code-block:: python

                channel_id = "1230000000000"
                file_id = "20180510T110208-193d0d17-f0b1-4549-96df-651c02ccb8c9"
                metadata = {
                    "x-abeja-meta-filename": "test.csv"
                }
                response = api_client.put_channel_file_metadata(channel_id, file_id, metadata)

        Params:
            - **channel_id** (str): CHANNEL_ID
            - **file_id** (str): FILE_ID
            - **metadata** (dict): key-value pair of metadata for the file

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    "uploaded_at": "2018-05-10T11:02:10+00:00"
                    "download_uri": "...",
                    "url_expires_on": "2018-05-15T18:57:03+00:00",
                    "metadata": {
                        "x-abeja-sys-meta-organizationid": "1200123565071",
                        "x-abeja-meta-filename": "test.csv"
                    },
                    "file_id": "20180510T110208-193d0d17-f0b1-4549-96df-651c02ccb8c9",
                    "content_type": "text/csv",
                }

        Raises:
            - BadRequest
            - Unauthorized: Authentication failed
            - NotFound: file not found
            - Forbidden
            - InternalServerError
        """
        path = '/channels/{}/{}/metadata'.format(channel_id, file_id)
        if metadata is None:
            metadata = {}
        encoded_metadata = encode_metadata(metadata)
        res = self._connection.api_request(
            method='PUT', path=path, json=encoded_metadata)
        return decode_file_metadata_if_exist(res)

    def put_channel_file_lifetime(
            self,
            channel_id: str,
            file_id: str,
            lifetime: str) -> dict:
        """update a file lifetime in a channel.

        API reference: PUT /channels/<channel_id>/<file_id>/lifetime

        Request Syntax:
            .. code-block:: python

                channel_id = "1230000000000"
                file_id = "20180510T110208-193d0d17-f0b1-4549-96df-651c02ccb8c9"
                lifetime = "1week"
                response = api_client.put_channel_file_life(channel_id, file_id, life)

        Params:
            - **channel_id** (str): CHANNEL_ID
            - **file_id** (str): FILE_ID
            - **lifetime** (str): string value of file lifetime

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    "channel_id": "1230000000000",
                    "file_id": "20180510T110208-193d0d17-f0b1-4549-96df-651c02ccb8c9",
                    "lifetime": "1week"
                }

        Raises:
            - BadRequest
            - Unauthorized: Authentication failed
            - NotFound: file not found
            - Forbidden
            - InternalServerError
        """
        params = {
            'lifetime': lifetime
        }
        path = '/channels/{}/{}/lifetime'.format(channel_id, file_id)
        return self._connection.api_request(
            method='PUT', path=path, json=params)

    def create_bucket(
            self,
            organization_id: str,
            name: str,
            description: str) -> dict:
        """create a bucket

        API reference: POST /organizations/<organization_id>/buckets

        Request Syntax:
            .. code-block:: python

                organization_id = "1234567890123"
                name = "sample bucket"
                description = "sample bucket description"
                response = api_client.create_bucket(organization_id, name, description)

        Params:
            - **organization_id** (str): ORGANIZATION_ID
            - **name** (str): bucket name
            - **description** (str): bucket description

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    "organization_id": "1234567890123",
                    "updated_at": "2017-09-12T10:11:46Z",
                    "organization_name": "abeja-inc",
                    "bucket": {
                        "updated_at": "2018-05-15T17:14:03Z",
                        "created_at": "2018-05-15T17:14:02Z",
                        "name": "test",
                        "description": "test",
                        "display_name": "test",
                        "bucket_id": "1230000000000"
                    },
                    "created_at": "2017-09-12T10:11:46Z"
                }

        Raises:
            - BadRequest
            - Unauthorized
            - Forbidden
            - InternalServerError
        """
        params = {
            'name': name,
            'description': description
        }
        path = '/organizations/{}/buckets'.format(organization_id)
        return self._connection.api_request(
            method='POST', path=path, json=params)

    def list_buckets(
            self,
            organization_id: str,
            limit: int=None,
            offset: int=None) -> dict:
        """get buckets

        API reference: GET /organizations/<organization_id>/buckets/

        Request Syntax:
            .. code-block:: python

                organization_id = "1234567890123"
                response = api_client.list_buckets(organization_id)

        Params:
            - **organization_id** (str): ORGANIZATION_ID
            - **limit** (int): max number of buckets to be returned
            - **offset** (int): offset of buckets ( which starts from 0 )

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    "updated_at": "2017-09-12T10:11:46Z",
                    "buckets": [
                        {
                            "updated_at": "2018-05-15T17:14:03Z",
                            "display_name": "test",
                            "description": "test",
                            "name": "test",
                            "bucket_id": "1230000000000",
                            "created_at": "2018-05-15T17:14:02Z",
                        },
                    ],
                    "limit": 50,
                    "has_next": true,
                    "organization_name": "abeja-inc",
                    "offset": 0,
                    "created_at": "2017-09-12T10:11:46Z",
                    "organization_id": "1234567890123"
                }

        Raises:
            - Unauthorized: Authentication failed
            - NotFound: bucket not found
            - Forbidden
            - InternalServerError
        """
        params = {}
        if limit is not None:
            params['limit'] = limit
        if offset is not None:
            params['offset'] = offset
        path = '/organizations/{}/buckets'.format(organization_id)
        return self._connection.api_request(
            method='GET', path=path, params=params)

    def get_bucket(self, organization_id: str, bucket_id: str) -> dict:
        """get a bucket

        API reference: GET /organizations/<organization_id>/buckets/<bucket_id>

        Request Syntax:
            .. code-block:: python

                organization_id = "1234567890123"
                bucket_id = "1230000000000"
                response = api_client.get_bucket(organization_id, bucket_id)

        Params:
            - **organization_id** (str): ORGANIZATION_ID
            - **bucket_id** (str): BUCKET_ID

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    "updated_at": "2017-09-12T10:11:46Z",
                    "created_at": "2017-09-12T10:11:46Z",
                    "bucket": {
                        "created_at": "2018-05-15T17:14:02Z",
                        "name": "test",
                        "updated_at": "2018-05-15T17:14:03Z",
                        "bucket_id": "1230000000000",
                        "display_name": "test",
                        "description": "test"
                    },
                    "organization_id": "1234567890123",
                    "organization_name": "abeja-inc"
                }

        Raises:
            - Unauthorized: Authentication failed
            - NotFound: bucket not found
            - Forbidden
            - InternalServerError
        """
        path = '/organizations/{}/buckets/{}'.format(
            organization_id, bucket_id)
        return self._connection.api_request(method='GET', path=path)

    def patch_bucket(
            self,
            organization_id: str,
            bucket_id: str,
            name: str=None,
            description: str=None) -> dict:
        """edit a bucket

        API reference: PATCH /organizations/<organization_id>/buckets/<bucket_id>

        Request Syntax:
            .. code-block:: python

                organization_id = "1234567890123"
                bucket_id = "1230000000000"
                name = 'updated_name'
                description = 'updated_description'
                response = api_client.patch_bucket(organization_id, bucket_id, name, description)

        Params:
            - **organization_id** (str): ORGANIZATION_ID
            - **bucket_id** (str): BUCKET_ID
            - **name** (str): bucket name
            - **description** (str): bucket description

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    "bucket": {
                        "description": "updated_description",
                        "updated_at": "2018-05-15T17:30:21Z",
                        "created_at": "2018-05-15T17:14:02Z",
                        "display_name": "updated_description",
                        "bucket_id": "1230000000000",
                        "name": "updated_name"
                    },
                    "organization_name": "abeja-inc",
                    "updated_at": "2017-09-12T10:11:46Z",
                    "created_at": "2017-09-12T10:11:46Z",
                    "organization_id": "1234567890123"
                }

        Raises:
            - BadRequest
            - Unauthorized: Authentication failed
            - Forbidden
            - NotFound: bucket not found
            - InternalServerError
        """
        params = {}
        if name:
            params['name'] = name
        if description:
            params['description'] = description
        path = '/organizations/{}/buckets/{}'.format(
            organization_id, bucket_id)
        return self._connection.api_request(
            method='PATCH', path=path, json=params)

    def archive_bucket(self, organization_id: str, bucket_id: str):
        """archive a bucket

        API reference: POST /organizations/<organization_id>/buckets/<bucket_id>/archive

        Request Syntax:
            .. code-block:: python

                organization_id = "1234567890123"
                bucket_id = "1230000000000"
                response = api_client.archive_bucket(
                    organization_id, bucket_id)

        Params:
            - **organization_id** (str): ORGANIZATION_ID
            - **bucket_id** (str): BUCKET_ID

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    "organization_id": "1234567890123",
                    "bucket": {
                        "updated_at": "2018-06-06T09:43:34Z",
                        "security_method": "organization",
                        "name": "example-bucket",
                        "display_name": "example-bucket",
                        "description": "this is sample bucket",
                        "created_at": "2018-05-30T10:44:28Z",
                        "bucket_id": "1234567890123",
                        "archived": true
                    },
                    "organization_name": "abeja-inc",
                    "created_at": "2017-09-12T10:11:46Z",
                    "updated_at": "2017-09-12T10:11:46Z"
                }

        Raises:
            - Unauthorized: Authentication failed
            - NotFound: bucket not found
            - Forbidden
            - InternalServerError
        """
        path = '/organizations/{}/buckets/{}/archive'.format(
            organization_id, bucket_id)
        return self._connection.api_request(method='POST', path=path)

    def unarchive_bucket(self, organization_id: str, bucket_id: str):
        """unarchive a bucket

        API reference: POST /organizations/<organization_id>/buckets/<bucket_id>/unarchive

        Request Syntax:
            .. code-block:: python

                organization_id = "1234567890123"
                bucket_id = "1230000000000"
                response = api_client.unarchive_bucket(
                    organization_id, bucket_id)

        Params:
            - **organization_id** (str): ORGANIZATION_ID
            - **bucket_id** (str): BUCKET_ID

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    "organization_id": "1234567890123",
                    "bucket": {
                        "updated_at": "2018-06-06T09:43:34Z",
                        "security_method": "organization",
                        "name": "example-bucket",
                        "display_name": "example-bucket",
                        "description": "this is sample bucket",
                        "created_at": "2018-05-30T10:44:28Z",
                        "bucket_id": "1234567890123",
                        "archived": false
                    },
                    "organization_name": "abeja-inc",
                    "created_at": "2017-09-12T10:11:46Z",
                    "updated_at": "2017-09-12T10:11:46Z"
                }

        Raises:
            - Unauthorized: Authentication failed
            - NotFound: bucket not found
            - Forbidden
            - InternalServerError
        """
        path = '/organizations/{}/buckets/{}/unarchive'.format(
            organization_id, bucket_id)
        return self._connection.api_request(method='POST', path=path)

    def upload_bucket_file(
            self, organization_id: str, bucket_id: str, file_obj: IO,
            file_location: str, content_type: str,
            metadata: dict=None, lifetime: str=None) -> dict:
        """upload a file to a bucket.

        API reference: POST /organizations/<organization_id>/buckets/<bucket_id>/files

        Request Syntax:
            .. code-block:: python

                organization_id = "1234567890123"
                bucket_id = "1230000000000"
                file_location = "target/sample.jpg"
                content_type = "image/jpeg"
                metadata = {
                    "x-abeja-meta-filename": "target/sample.jpg"
                }
                with open('sample.jpg', 'rb') as f:
                    response = api_client.upload_bucket_file(
                        bucket_id, f, content_type, metadata=metadata)

        Params:
            - **organization_id** (str): ORGANIZATION_ID
            - **bucket_id** (str): BUCKET_ID
            - **file_obj** (a file-like object) : a file-like object to upload. It must implement the read method, and must return bytes.
            - **file_location** (str): file location to store
            - **content_type** (str): content type of a file to be uploaded
            - **metadata** (dict): **[optional]** key-value pair of metadata for the file
            - **lifetime** (str): **[optional]** each one of `1day` / `1week` / `1month` / `6months`. the file will be deleted after the specified time.

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    "uploaded_at": null,
                    "metadata": {
                        "x-abeja-meta-filename": "sample.jpg"
                    },
                    "lifetime": "1day",
                    "content_type": "image/jpeg",
                    "file_id": "20180515T180605-f4acc798-9afa-40a1-b500-ebce42a4fa3f"
                }

        Raises:
            - BadRequest: given parameters are invalid
            - Unauthorized: Authentication failed
            - NotFound: channel not found
            - Forbidden
            - InternalServerError
        """
        path = '/organizations/{}/buckets/{}/files'.format(
            organization_id, bucket_id)

        if str(convert_to_valid_path(file_location)) != file_location:
            error_message = "'file_location' must not start with '/' and must not include " \
                            "a relative path of '..' and '.'. '{}'".format(file_location)
            raise BadRequest(
                error=error_message,
                error_description=error_message,
                status_code=400)

        if not metadata:
            metadata = {}
        encoded_metadata = encode_metadata(metadata)
        headers = dict()
        headers.update(encoded_metadata)

        params = {}
        if lifetime:
            params['lifetime'] = lifetime
        params = BytesIO(json.dumps(params).encode())

        files = {
            'file': (file_location, file_obj, content_type),
            'parameters': ('params.json', params, 'application/json')
        }
        res = self._connection.api_request(
            method='POST', headers=headers, path=path, files=files)
        return decode_file_metadata_if_exist(res)

    def upload_bucket_files(
            self,
            organization_id: str,
            bucket_id: str,
            target_dir: str,
            lifetime: str=None) -> dict:
        """upload files on your specified directory to a bucket.

        API reference: POST /organizations/<organization_id>/buckets/<bucket_id>/files

        Request Syntax:
            .. code-block:: python

                organization_id = "1234567890123"
                bucket_id = "1230000000000"
                target_dir = "./data"

                response = api_client.upload_bucket_files(organization_id, bucket_id, target_dir)

        Params:
            - **organization_id** (str): ORGANIZATION_ID
            - **bucket_id** (str): BUCKET_ID
            - **target_dir** (str) : a directory to upload. Directory structure will be kept on a bucket.
            - **lifetime** (str): **[optional]** each one of `1day` / `1week` / `1month` / `6months`. the file will be deleted after the specified time.

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    "messages": [
                        { "message": "Upload failed. file (20180510T110208-193d0d17-f0b1-4549-96df-651c02ccb8c9)" },
                    ]
                }

        Raises:
            - BadRequest: given parameters are invalid
            - Unauthorized: Authentication failed
            - NotFound: bucket not found
            - Forbidden
            - InternalServerError
        """
        messages = list()
        response = {"error_messages": messages}

        target_dir_path = '{}/'.format(str(Path(target_dir).absolute()))
        for root, dirs, files in os.walk(target_dir):
            for dirname in dirs[:]:
                if dirname.startswith('.'):
                    dirs.remove(dirname)

            for filename in files:
                if filename.startswith('.'):
                    continue
                filepath = Path(root, filename)
                file_location = str(
                    filepath.absolute()).replace(
                    target_dir_path, '', 1)
                content_type, _ = mimetypes.guess_type(str(filepath))
                metadata = {
                    "x-abeja-meta-filename": file_location
                }
                with open(str(filepath), 'rb') as f:
                    try:
                        self.upload_bucket_file(
                            organization_id,
                            bucket_id,
                            f,
                            file_location,
                            content_type,
                            metadata=metadata,
                            lifetime=lifetime)
                    except (BadRequest, Unauthorized, NotFound, Forbidden, InternalServerError) as e:
                        messages.append({
                            "message": 'Upload failed file({}), {}: {}'.format(
                                filepath, e.__class__.__name__, str(e))
                        })
        response["status"] = False if messages else True
        return response

    def list_bucket_files(
            self,
            organization_id: str,
            bucket_id: str,
            target_dir: str="/",
            items_per_page: int=None,
            last_file_id: str=None,
            query: str=None) -> dict:
        """get files in a bucket.

        API reference: GET /organizations/<organization_id>/buckets/<bucket_id>/files

        Request Syntax:
            .. code-block:: python

                organization_id = "1234567890123"
                bucket_id = "1230000000000"
                response = api_client.list_bucket_files(bucket_id)

        Params:
            - **organization_id** (str): ORGANIZATION_ID
            - **bucket_id** (str): BUCKET_ID
            - **target_dir** (str): Bucket target directory name
            - **items_per_page** (int): max number of files to be returned
            - **last_file_id** (str):
                API response includes file list after `last_file_id`.
            - **query** (str):
                query to search. JMESPATH format is available.
                Please refer to https://boto3.amazonaws.com/v1/documentation/api/latest/guide/paginators.html#filtering-results-with-jmespath

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    "last_file_id": "/aaa/bbb/ccc",
                    "files": [
                        {
                            "size": 4,
                            "etag": "xxx",
                            "is_file": true,
                            "metadata": {
                                "x-abeja-meta-filename": "000000006197.jpg"
                            },
                            "last_modified": "2018-05-10T11:02:08+00:00",
                            "uploaded_at": "2018-05-10T11:02:08+00:00",
                            "url_expires_on": "2018-05-15T18:54:37+00:00",
                            "download_uri": "...",
                            "file_id": "/aaa/bbb/ddd"
                        },
                    ]
                }

        Raises:
            - Unauthorized: Authentication failed
            - NotFound: bucket not found
            - Forbidden
            - InternalServerError
        """
        params = {
            'target_dir': target_dir
        }
        if items_per_page is not None:
            params['items_per_page'] = items_per_page
        if last_file_id is not None:
            params['last_file_id'] = last_file_id
        if query is not None:
            assert isinstance(
                query, str), 'Unexpected query type: {}'.format(
                type(query))
            params['q'] = query
        path = '/organizations/{}/buckets/{}/files'.format(
            organization_id, bucket_id)
        res = self._connection.api_request(
            method='GET', path=path, params=params)

        if res.get('files'):
            res['files'] = [
                decode_file_metadata_if_exist(f)
                for f in res['files']
            ]
        return res

    def get_bucket_file(
            self,
            organization_id: str,
            bucket_id: str,
            file_id: str) -> dict:
        """get a file in a bucket.

        API reference: GET /organizations/<organization_id>/buckets/<bucket_id>/files/<file_id>

        Request Syntax:
            .. code-block:: python

                organization_id = "1234567890123"
                bucket_id = "1230000000000"
                file_id = "aaa/bbb"
                response = api_client.get_bucket_file(organization_id, bucket_id, file_id)

        Params:
            - **organization_id** (str): ORGANIZATION_ID
            - **bucket_id** (str): BUCKET_ID
            - **file_id** (str): FILE_ID in a bucket

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    "size": 4,
                    "etag": "xxx",
                    "is_file": true,
                    "metadata": {
                        "x-abeja-meta-filename": "000000006197.jpg"
                    },
                    "last_modified": "2018-05-10T11:02:08+00:00",
                    "uploaded_at": "2018-05-10T11:02:08+00:00",
                    "url_expires_on": "2018-05-15T18:54:37+00:00",
                    "download_uri": "...",
                    "file_id": "/aaa/bbb/ddd"
                }

        Raises:
            - Unauthorized: Authentication failed
            - NotFound: bucket not found
            - Forbidden
            - InternalServerError
        """
        path = '/organizations/{}/buckets/{}/files/{}'.format(
            organization_id, bucket_id, file_id)
        res = self._connection.api_request(method='GET', path=path)
        return res
