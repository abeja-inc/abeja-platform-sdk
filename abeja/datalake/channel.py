# -*- coding: utf-8 -*-
import os
import mimetypes
from io import BytesIO
from typing import Iterable
from concurrent.futures import ThreadPoolExecutor, as_completed

from abeja.common.config import UPLOAD_WORKER_COUNT
from abeja.common.logging import logger
from abeja.common.file_helpers import generate_path_iter
from .api.client import APIClient
from .file import DatalakeFile, Files, FileIterator


class Channel:
    """a model class for a channel

    Properties:
        - organization_id (str)
        - channel_id (str)
        - name (str)
        - display_name (str)
        - description (str)
        - archived (bool)
        - created_at (datetime)
        - updated_at (datetime)

    """

    def __init__(self, api: APIClient, organization_id: str, channel_id: str,
                 name: str=None, description: str=None, display_name: str=None,
                 storage_type: str=None, created_at: str=None,
                 updated_at: str=None, archived: bool=False) -> None:
        self._api = api
        self.organization_id = organization_id
        self.channel_id = channel_id
        self.name = name
        self.description = description
        self.display_name = display_name
        self.storage_type = storage_type
        self.created_at = created_at
        self.updated_at = updated_at
        self.archived = archived

    @property
    def files(self) -> Files:
        """Get datalake Files object

        Request syntax:
            .. code-block:: python

                channel = client.get_channel(channel_id='1230000000000')
                channel.files

        Returns:
            :class:`Files <abeja.datalake.file.Files>` object
        """
        return Files(self._api, self.organization_id, self.channel_id)

    def list_files(
            self,
            start: str=None,
            end: str=None,
            timezone: str=None,
            sort: str=None,
            next_page_token: str=None,
            limit: int=None,
            prefetch: bool=False,
            query: str=None) -> FileIterator:
        """get datalake files in the channel

        Request syntax:
            .. code-block:: python

                for f in channel.list_files():
                    pass

        Params:
            - **start** (str): start date of target uploaded files
            - **end** (str): end date of target uploaded files
            - **timezone** (str): timezone of specified start and end date
            - **query** (str):
                query to search.
                It is possible to filter what contain specific value by describing like "x-abeja-meta-filename:filename".
            - **sort** (str):
                the order of the file list.
                multiple items can be specified by separating with commas (,).
                It is possible to sort in descending order by specifying a hyphen (-) in front of the item.
                By default, the list is sorted by uploaded_at in ascending order.

        Return type:
            :class:`FileIterator <abeja.datalake.file.FileIterator>` object
        """
        return FileIterator(
            self._api,
            self.organization_id,
            self.channel_id,
            start=start,
            end=end,
            timezone=timezone,
            next_page_token=next_page_token,
            items_per_page=limit,
            sort=sort,
            prefetch=prefetch,
            query=query)

    def get_file(self, file_id: str) -> DatalakeFile:
        """get a datalake file in the channel

        Request syntax:
            .. code-block:: python

                file_id = '20180101T000000-00000000-1111-2222-3333-999999999999'
                datalake_file = channel.get_file(file_id=file_id)

        Params:
            - **file_id** (str): FILE_ID

        Return type:
            :class:`DatalakeFile <abeja.datalake.file.DatalakeFile>` object
        """
        download_info = self._api.get_channel_file_download(
            self.channel_id, file_id)

        return DatalakeFile(
            api=self._api,
            organization_id=self.organization_id,
            channel_id=self.channel_id,
            file_id=download_info.get('file_id'),
            content_type=download_info.get('content_type'),
            download_uri=download_info.get('download_uri'),
            metadata=download_info.get('metadata'),
            url_expires_on=download_info.get('url_expires_on'),
            uploaded_at=download_info.get('uploaded_at'),
            lifetime=download_info.get('lifetime'))

    def upload(self, file_obj: BytesIO, content_type: str, metadata: dict=None,
               lifetime: str=None, conflict_target: str=None) -> DatalakeFile:
        """upload a content to a channel with file-like object.

        Request syntax:
            .. code-block:: python

                content_type = 'image/jpeg'
                metadata = {
                    'label': 'example'
                }
                with open('example.csv') as f:
                    response = channel.upload(f, content_type, metadata=metadata)

        Params:
            - **file_obj** (a file-like object) : a file-like object to upload. It must implement the read method, and must return bytes.
            - **content_type** (str): MIME type of content.
            - **metadata** (dict): **[optional]** metadata to be added to uploaded file. Object can not be set to the key or value of dict. It must be a string.
            - **lifetime** (str): **[optional]** each one of `1day` / `1week` / `1month` / `6months`. the file will be deleted after the specified time.
            - **conflict_target** (str): **[optional]** return `409 Conflict` when the same value of specified key already exists in channel.

        Return type:
            :class:`DatalakeFile <abeja.datalake.file.DatalakeFile>` object

        Returns:
            a file uploaded to a channel
        """
        if not metadata:
            metadata = {}

        # ignore Content-Type in metadata
        metadata = {
            k: v for k,
            v in metadata.items() if k.lower() not in {
                'content_type',
                'content-type'}}

        # add x-abeja-meta- prefix
        metadata = {
            'x-abeja-meta-{}'.format(k): str(v) for k,
            v in metadata.items()}

        res = self._api.post_channel_file_upload(
            self.channel_id,
            file_obj,
            content_type,
            metadata=metadata,
            lifetime=lifetime,
            conflict_target=conflict_target)

        return DatalakeFile(
            api=self._api,
            organization_id=self.organization_id,
            channel_id=self.channel_id,
            file_id=res.get('file_id'),
            content_type=res.get('content_type'),
            metadata=res.get('metadata'),
            uploaded_at=res.get('uploaded_at'),
            lifetime=res.get('lifetime'))

    def upload_file(
            self, file_path: str, metadata: dict=None, content_type: str=None,
            lifetime: str=None, conflict_target: str=None) -> DatalakeFile:
        """upload a file to a channel.
        This method infers the content_type of given file if content_type is not specified,
        and set the filename as `x-abeja-meta-filename` in metadata.

        Request syntax:
            .. code-block:: python

                metadata = {
                    'label': 'example'
                }
                response = channel.upload('~/example.txt', metadata=metadata)

        Params:
            - **file_path** (str) : path to a file
            - **metadata** (dict): **[optional]** metadata to be added to uploaed file.
            - **content_type** (str): **[optional]** MIME type of content. Content-Type is assumed by the extension if not specified.
            - **lifetime** (str): **[optional]** each one of `1day` / `1week` / `1month` / `6months`. the file will be deleted after the specified time.
            - **conflict_target** (str): **[optional]** return `409 Conflict` when the same value of specified key already exists in channel.

        Return type:
            :class:`DatalakeFile <abeja.datalake.file.DatalakeFile>` object

        Returns:
            a file uploaded to a channel
        """
        if not content_type:
            mime_type, _ = mimetypes.guess_type(file_path)
            content_type = mime_type

        if not metadata:
            metadata = {}

        # keep the user defined "metadata" unchanged
        update_metadata = {**metadata}

        # add `x-abeja-meta-filename` if not defined
        if 'filename' not in metadata:
            update_metadata['filename'] = os.path.basename(file_path)

        with open(file_path, 'rb') as f:
            return self.upload(
                f,
                content_type,
                metadata=update_metadata,
                lifetime=lifetime,
                conflict_target=conflict_target)

    def upload_dir(
            self,
            dir_path: str,
            metadata: dict=None,
            content_type: str=None,
            lifetime: str=None,
            conflict_target: str=None,
            recursive: bool=False,
            use_thread: bool=True) -> Iterable[DatalakeFile]:
        """upload files in directory to a channel.
        This method infers the content_type of given file if content_type is not specified,
        and set the filename as `x-abeja-meta-filename` in metadata.

        Note: this method returns list ( not generator ) to make sure upload process will be done here.

        Request syntax:
            .. code-block:: python

                metadata = {
                    'label': 'example'
                }
                response = channel.upload_dir('./source_dir', metadata)

        Params:
            - **content** (file-like object) : contents to be uploaded
            - **metadata** (dict): metadata to be added to uploaed file. **[optional]**
            - **content_type** (str): MIME type of content. Content-Type is assumed by extensions if not specified **[optional]**
            - **lifetime** (str): **[optional]** each one of `1day` / `1week` / `1month` / `6months`. the file will be deleted after the specified time.
            - **conflict_target** (str): **[optional]** return `409 Conflict` when the same value of specified key already exists in channel.

        Return type:
            list of :class:`DatalakeFile <abeja.datalake.file.DatalakeFile>` object

        Returns:
            A list of DatalakeFile successfully uploaded.
        """
        file_path_iter = generate_path_iter(dir_path, recursive=recursive)
        if use_thread:
            upload_files_func = self._upload_files_threaded
        else:
            upload_files_func = self._upload_files_unthreaded
        return upload_files_func(
            file_path_iter,
            content_type=content_type,
            metadata=metadata,
            lifetime=lifetime,
            conflict_target=conflict_target)

    def _upload_files_threaded(
            self,
            file_paths: Iterable[str],
            content_type: str=None,
            metadata: dict=None,
            lifetime: str=None,
            conflict_target: str=None) -> Iterable[DatalakeFile]:
        """upload files asynchronously using thread
        this method does not return generator to avoid lazy evaluation.
        """
        files = []
        with ThreadPoolExecutor(max_workers=UPLOAD_WORKER_COUNT) as executor:
            futures = []
            for f in file_paths:
                futures.append(
                    executor.submit(
                        self.upload_file,
                        f,
                        metadata=metadata,
                        content_type=content_type,
                        lifetime=lifetime,
                        conflict_target=conflict_target))
            for f in as_completed(futures):
                try:
                    files.append(f.result())
                except Exception as e:
                    logger.error(e)
        return files

    def _upload_files_unthreaded(
            self,
            file_paths: Iterable[str],
            content_type: str=None,
            metadata: dict=None,
            lifetime: str=None,
            conflict_target: str=None) -> Iterable[DatalakeFile]:
        """upload files synchronously using thread
        this method does not return generator to avoid lazy evaluation.
        """
        files = []
        for file_path in file_paths:
            try:
                file = self.upload_file(
                    file_path,
                    content_type=content_type,
                    metadata=metadata,
                    lifetime=lifetime,
                    conflict_target=conflict_target)
                files.append(file)
            except Exception as e:
                logger.error(e)
        return files

    def list_datasources(self):
        raise NotImplementedError

    def add_datasource(self):
        raise NotImplementedError

    def remove_datasource(self):
        raise NotImplementedError


class Channels:
    """a class for handling channels"""

    def __init__(self, api: APIClient, organization_id: str) -> None:
        self._api = api
        self.organization_id = organization_id

    def create(
            self,
            name: str,
            description: str,
            storage_type: str) -> Channel:
        """create a channel

        API reference: POST /organizations/<organization_id>/channels/

        Request Syntax:
            .. code-block:: python

                params = {
                    "name": "test-channel",
                    "description": "test channel",
                    "storage_type": "datalake"
                }
                channel = channels.create(**params)

        Params:
            - **name** (str): channel name
            - **description** (str): channel description
            - **storage_type** (str): type of storage, datalake or file

        Return type:
            :class:`Channel <abeja.datalake.channel.Channel>` object

        """
        res = self._api.create_channel(
            self.organization_id, name, description, storage_type)

        channel_info = res.get('channel', {})

        return Channel(
            self._api,
            organization_id=self.organization_id,
            channel_id=channel_info.get('channel_id'),
            name=channel_info.get('name'),
            display_name=channel_info.get('display_name'),
            description=channel_info.get('description'),
            storage_type=channel_info.get('storage_type'),
            archived=channel_info.get('archived', False),
            created_at=channel_info.get('created_at'),
            updated_at=channel_info.get('updated_at'))

    def list(self, limit: int=None, offset: int=None) -> Iterable[Channel]:
        """list channels

        API reference: GET /organizations/<organization_id>/channels/

        Request Syntax:
            .. code-block:: python

                channel = channels.list()

        Return type:
            generator of :class:`Channel <abeja.datalake.channel.Channel>` objects

        """
        res = self._api.list_channels(
            self.organization_id, limit=limit, offset=offset)
        for item in res['channels']:

            yield Channel(
                self._api,
                organization_id=self.organization_id,
                channel_id=item.get('channel_id'),
                name=item.get('name'),
                display_name=item.get('display_name'),
                description=item.get('description'),
                storage_type=item.get('storage_type'),
                archived=item.get('archived', False),
                created_at=item.get('created_at'),
                updated_at=item.get('updated_at'))

    def get(self, channel_id: str) -> Channel:
        """get a channel

        API reference: GET /organizations/<organization_id>/channels/<channel_id>

        Request Syntax:
            .. code-block:: python

                channel_id = '1234567890123'
                channel = channels.get(channel_id=channel_id)

        Params:
            - **channel_id** (str): identifier of channel

        Return type:
            :class:`Channel <abeja.datalake.channel.Channel>` object

        """
        res = self._api.get_channel(self.organization_id, channel_id)

        channel_info = res.get('channel', {})

        return Channel(
            self._api,
            organization_id=self.organization_id,
            channel_id=channel_info.get('channel_id'),
            name=channel_info.get('name'),
            display_name=channel_info.get('display_name'),
            description=channel_info.get('description'),
            storage_type=channel_info.get('storage_type'),
            archived=channel_info.get('archived', False),
            created_at=channel_info.get('created_at'),
            updated_at=channel_info.get('updated_at'))

    def patch(
            self,
            channel_id: str,
            name: str=None,
            description: str=None) -> Channel:
        """patch a channel

        API reference: PATCH /organizations/<organization_id>/channels/<channel_id>

        Request Syntax:
            .. code-block:: python

                params = {
                    "channel_id": "1234567890123",
                    "name": "updated_name",
                    "description": "updated description"
                }
                channel = channels.patch(**params)

        Params:
            - **channel_id** (str): identifier of channel
            - **name** (str): channel name
            - **description** (str): channel description

        Return type:
            :class:`Channel <abeja.datalake.channel.Channel>` object

        """
        res = self._api.patch_channel(
            self.organization_id, channel_id, name, description)

        channel_info = res.get('channel', {})

        return Channel(
            self._api,
            organization_id=self.organization_id,
            channel_id=channel_info.get('channel_id'),
            name=channel_info.get('name'),
            display_name=channel_info.get('display_name'),
            description=channel_info.get('description'),
            storage_type=channel_info.get('storage_type'),
            archived=channel_info.get('archived', False),
            created_at=channel_info.get('created_at'),
            updated_at=channel_info.get('updated_at'))
