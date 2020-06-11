# -*- coding: utf-8 -*-
import os
# import re
from typing import Any, Dict, List, Iterable, Generator, Optional
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from retrying import retry
from requests.models import Response

from abeja.common.config import DEFAULT_CHUNK_SIZE, FETCH_WORKER_COUNT, DOWNLOAD_RETRY_ATTEMPT_NUMBER
# from abeja.common.config import S3_CHUNK_SIZE
from abeja.common.iterator import Iterator
from abeja.common.connection import http_error_handler
from abeja.common.local_file import (
    use_binary_cache,
    use_text_cache,
    use_iter_content_cache,
    use_iter_lines_cache
)
from abeja.common.file_utils import FileMixin
# from abeja.common.s3etag import calc_s3etag
from abeja.exceptions import HttpError, EtagHashNotMatch
from abeja.datalake.api.client import APIClient
from .metadata import DatalakeMetadata


def retry_if_etag_hash_not_match(error):
    return isinstance(error, EtagHashNotMatch)


class DatalakeFile(FileMixin):
    """a model class for a datalake channel file

    if the file exists in local, get data from the file.
    unless, get data from remote, and save it in local.

    the file is saved in `./{channel_id}/{file_id}` by default.

    you can change the location by setting `ABEJA_STORAGE_DIR_PATH`
    as environment variable.
    then it will be saved in `${ABEJA_STORAGE_DIR_PATH}/{channel_id}/{file_id}`.

    Properties:
        - organization_id (str)
        - channel_id (str)
        - file_id (str)
        - uri (str)
        - type (str)
        - upload_url (str)
        - download_uri (str)
        - content_type (str)
        - metadata (dict)
        - url_expires_on (str)
        - uploaded_at (datetime)

    """

    LIFETIME = (
        '1day',
        '1week',
        '1month',
        '6months'
    )

    def __init__(
            self,
            api: APIClient,
            organization_id: str=None,
            channel_id: str=None,
            file_id: str=None,
            uri: str=None,
            type: str=None,
            upload_url: str=None,
            download_uri: str=None,
            content_type: str=None,
            url_expires_on: str=None,
            metadata: dict=None,
            uploaded_at: str=None,
            lifetime: str=None,
            **kwargs) -> None:
        super(DatalakeFile, self).__init__(api, uri, type, **kwargs)
        self.organization_id = organization_id
        if self.uri:
            pr = urlparse(self.uri)
            self.channel_id = pr.netloc
            self.file_id = self._convert_to_file_id(pr.path)
        else:
            self.channel_id = channel_id
            self.file_id = file_id
            self.uri = "datalake://{}/{}".format(self.channel_id, self.file_id)
        self.upload_url = upload_url
        self.download_url = kwargs.get('download_url')  # TODO: DEPRECATED
        self.download_uri = download_uri
        self.content_type = content_type
        self.url_expires_on = url_expires_on
        self.lifetime = lifetime
        self.metadata = DatalakeMetadata(api, channel_id, file_id, metadata)
        self.uploaded_at = uploaded_at

    @property
    def lifetime(self) -> str:
        return self._lifetime

    @lifetime.setter
    def lifetime(self, lifetime) -> None:
        # not allow to update with None if lifetime exists
        if hasattr(
                self,
                '_lifetime') and self._lifetime is not None and lifetime is None:
            raise RuntimeError(
                'lifetime cannot be updated with {}'.format(lifetime))
        if lifetime is not None and lifetime not in DatalakeFile.LIFETIME:
            raise RuntimeError(
                'lifetime should be one of {}.'.format(DatalakeFile.LIFETIME))
        self._lifetime = lifetime

    def get_content(self, cache: bool=True) -> bytes:
        """Get content from a binary file

        Request syntax:
            .. code-block:: python

                file_id = '20180101T000000-00000000-1111-2222-3333-999999999999'
                datalake_file = channel.get_file(file_id=file_id)
                content = datalake_file.get_content()

        Params:
            - **cache** (str):
                if True, read file saved in `[ABEJA_STORAGE_DIR_PATH]/[channel_id]/[file_id]`
                if exists, and if not, downloaded content will be saved in the path. By default, True.

        Return type:
            bytes
        """
        if cache:
            decorated = use_binary_cache(self._get_content_from_remote)
            return decorated(self)
        return self._get_content_from_remote()

    def get_iter_content(self,
                         cache: bool=True,
                         chunk_size: int=DEFAULT_CHUNK_SIZE) -> Generator[bytes,
                                                                          None,
                                                                          None]:
        """Get content iteratively from a binary file

        Request syntax:
            .. code-block:: python

                file_id = '20180101T000000-00000000-1111-2222-3333-999999999999'
                datalake_file = channel.get_file(file_id=file_id)
                content = datalake_file.get_iter_content()

        Params:
            - **cache** (str):
                if True, read file saved in `[ABEJA_STORAGE_DIR_PATH]/[channel_id]/[file_id]`
                if exists, and if not, downloaded content will be saved in the path. By default, True.
            - **chunk_size** (str):
                The number of bytes it should read into memory.
                default value : 1,048,576 ( = 1MB )

        Return type:
            generator
        """
        if cache:
            decorated = use_iter_content_cache(
                self._get_iter_content_from_remote)
            return decorated(self, chunk_size)
        return self._get_iter_content_from_remote(chunk_size)

    def get_text(
            self,
            cache: bool = True,
            encoding: Optional[str] = None) -> str:
        """Get content from a text file

        Request syntax:
            .. code-block:: python

                file_id = '20180101T000000-00000000-1111-2222-3333-999999999999'
                datalake_file = channel.get_file(file_id=file_id)
                content = datalake_file.get_text()

        Params:
            - **cache** (str):
                if True, read file saved in `[ABEJA_STORAGE_DIR_PATH]/[channel_id]/[file_id]`
                if exists, and if not, downloaded content will be saved in the path. By default, True.
            - **encoding** (str):
                Specify to get text encoded in other than ISO-8859-1.

        Return type:
            str
        """
        if cache:
            decorated = use_text_cache(self._get_text_from_remote)
            ret = decorated(self)
        else:
            ret = self._get_text_from_remote()
        if encoding:
            ret = ret.encode('iso-8859-1').decode('utf-8')
        return ret

    def get_json(self) -> dict:
        """Get json from a file

        Request syntax:
            .. code-block:: python

                file_id = '20180101T000000-00000000-1111-2222-3333-999999999999'
                datalake_file = channel.get_file(file_id=file_id)
                content = datalake_file.get_json()

        Return type:
            dict

        Raises:
            json.decoder.JSONDecodeError
        """
        return self._get_json_from_remote()

    def get_iter_lines(self, cache: bool=True) -> Generator[str, None, None]:
        """Get lines iteratively from a text file

        if the text file exists in local, get content from the file.
        unless, get content from remote, and save it in local.

        Request syntax:
            .. code-block:: python

                file_id = '20180101T000000-00000000-1111-2222-3333-999999999999'
                datalake_file = channel.get_file(file_id=file_id)
                content = datalake_file.get_iter_lines()

        Params:
            - **cache** (str):
                if True, read file saved in `[ABEJA_STORAGE_DIR_PATH]/[channel_id]/[file_id]`
                if exists, and if not, downloaded content will be saved in the path. By default, True.

        Return type:
            generator
        """
        if cache:
            decorated = use_iter_lines_cache(
                self._get_iter_lines_from_remote)
            return decorated(self)
        return self._get_iter_lines_from_remote()

    def get_file_info(self) -> dict:
        """Get information of a file

        Request syntax:
            .. code-block:: python

                file_id = '20180101T000000-00000000-1111-2222-3333-999999999999'
                datalake_file = channel.get_file(file_id=file_id)
                content = datalake_file.get_file_info()

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    "url_expires_on": "2017-12-20T17:08:26+00:00",
                    "uploaded_at": "2017-12-18T05:39:47+00:00",
                    "metadata": {
                        "x-abeja-meta-filename": "test.jpg"
                    },
                    "file_id": "20171218T053947-821bd0a3-3992-4320-bc1c-1ee8d0a0ad6b",
                    "download_uri": "...",
                    "content_type": "image/jpeg"
                }

        """
        path = os.path.join('/channels', self.channel_id, self.file_id)
        return self._api._connection.api_request(method='GET', path=path)

    def _validate_etag(self, res: Response) -> bytes:
        # Prior to the version 0.6.0, SDK automatically validates ETag response header,
        # but it causes the problem described in the issue https://github.com/abeja-inc/platform-planning/issues/3188
        # So we decided to disable the validation.
        #
        # TODO:
        # - Discuss how we achieve ETag validation without assuming constant chunk size
        # - Shouldn't we retry if HTTP 5xx from S3?
        #
        content = res.content
        # etag = res.headers.get('etag')
        # etag = re.sub('"', '', etag) if etag else None
        # if etag:
        #     chunk_size = S3_CHUNK_SIZE
        #     if '-' not in etag:
        #         chunk_size = len(content)
        #     md5sum = calc_s3etag(content, chunk_size)
        #     if etag != md5sum:
        #         raise EtagHashNotMatch('Etag is not match')
        return content

    @retry(stop_max_attempt_number=DOWNLOAD_RETRY_ATTEMPT_NUMBER,
           retry_on_exception=retry_if_etag_hash_not_match)
    def _get_content_from_remote(self) -> bytes:
        res = self._do_download()
        return self._validate_etag(res)

    def _get_iter_content_from_remote(
            self, chunk_size) -> Generator[bytes, None, None]:
        res = self._do_download(stream=True)
        return res.iter_content(chunk_size=chunk_size)

    @retry(stop_max_attempt_number=DOWNLOAD_RETRY_ATTEMPT_NUMBER,
           retry_on_exception=retry_if_etag_hash_not_match)
    def _get_text_from_remote(self) -> str:
        res = self._do_download()
        self._validate_etag(res)
        return res.text

    @retry(stop_max_attempt_number=DOWNLOAD_RETRY_ATTEMPT_NUMBER,
           retry_on_exception=retry_if_etag_hash_not_match)
    def _get_json_from_remote(self) -> dict:
        res = self._do_download()
        self._validate_etag(res)
        return res.json()

    def _get_iter_lines_from_remote(self) -> Generator[str, None, None]:
        res = self._do_download(stream=True)
        return res.iter_lines()

    def _convert_to_file_id(self, path: str) -> str:
        """path is like `/<file_id>`, convert it in valid format.

        :param path:
        :return:
        """
        return path.lstrip('/')

    def _get_download_uri(self) -> str:
        file_info = self.get_file_info()
        return file_info['download_uri']

    def _do_download(self, stream: bool=False) -> Response:
        url = self._get_download_uri()
        try:
            return self._api._connection.request('GET', url, stream=stream)
        except requests.exceptions.HTTPError as e:
            http_error_handler(e)

    def commit(self) -> bool:
        """reflect instance info into remote state.
        only **metadata**, **lifetime** are editable for now.

        Return Type:
            Optional[bool] : True if succeeded in update
        """
        # NOTE: currently there is no way to update instance info by a single request.
        # ( ex. to update both `lifetime` and `metadata`, need to call respective endpoints )
        # In the future, instance info can be reflected by a single request.
        file_info = self.get_file_info()

        # update metadata first because lifetime does not support deletion for
        # now.
        datalake_metadata = {
            'x-abeja-meta-{}'.format(k): v for k, v in self.metadata.items()}
        self._api.put_channel_file_metadata(
            self.channel_id, self.file_id, metadata=datalake_metadata)

        if self._lifetime:
            try:
                # update lifetime
                self._api.put_channel_file_lifetime(
                    self.channel_id, self.file_id, lifetime=self._lifetime)
            except HttpError:
                # if failed in updating lifetime, rollback metadata with previous value
                # NOTE: failure in this process causes partial changes
                self._api.put_channel_file_metadata(
                    self.channel_id, self.file_id, metadata=file_info.get('metadata'))
                raise
        return True


def _download_file_content(item: DatalakeFile) -> DatalakeFile:
    # download content and cache to local disk
    item.get_content(cache=True)
    return item


class FileIterator(Iterator):
    def __init__(
            self,
            api: APIClient,
            organization_id: str,
            channel_id: str,
            start: str=None,
            end: str=None,
            timezone: str=None,
            items_per_page: int=None,
            sort: str=None,
            next_page_token: str=None,
            prefetch=False,
            query: str=None) -> None:
        self._api = api
        self.organization_id = organization_id
        self.channel_id = channel_id
        self.start = start
        self.end = end
        self.timezone = timezone
        self.items_per_page = items_per_page
        self.sort = sort
        self.next_page_token = next_page_token
        self._is_first_page = True
        self._current_page = None
        self._current_page_file_idx = 0
        self.prefetch = prefetch
        self.query = query
        super().__init__()

    def __iter__(self):
        if self.prefetch:
            return self._items_iter_with_prefetch()
        else:
            return self._items_iter()

    def _items_iter_with_prefetch(self) -> Iterable[DatalakeFile]:
        page = self._page()
        with ThreadPoolExecutor(max_workers=FETCH_WORKER_COUNT) as executor:
            futures = []
            while page:
                futures += [executor.submit(_download_file_content, item)
                            for item in page]
                page = self._page()
            for f in as_completed(futures):
                download_item = f.result()
                yield download_item

    def __next__(self):
        if self._current_page is None or self._current_page_file_idx >= len(
                self._current_page):
            self._current_page_file_idx = 0
            self._current_page = self._page()

        if len(self._current_page) == 0:
            raise StopIteration

        item = self._current_page[self._current_page_file_idx]

        self._current_page_file_idx += 1

        return item

    def _create_datalake_file(self, item: Dict[str, Any]) -> DatalakeFile:
        """
        Creates and returns a newly created ``DatalakeFile`` instance with
        API response.
        """
        kwargs = item.copy()
        kwargs['api'] = self._api
        kwargs['client'] = self.channel_id
        kwargs['organization_id'] = self.organization_id
        kwargs['channel_id'] = self.channel_id

        return DatalakeFile(**kwargs)

    def _page(self) -> List[DatalakeFile]:
        """get a page of items in channel"""
        # if some items of a page are taken, the rest of items are return
        # this is because FileIterator class supports `__next__` method.
        if self._current_page_file_idx != 0:
            if self._current_page[self._current_page_file_idx:]:
                _current_page = self._current_page
                idx = self._current_page_file_idx
                self._current_page = None
                self._current_page_file_idx = 0
                return _current_page[idx:]

        # return empty list to stop iterating of `_items_iter` or `_items_iter_with_prefetch`
        # when reaching the end of pages.
        if self.next_page_token is None and not self._is_first_page:
            return []

        params = {}
        if self.next_page_token is not None:
            params['next_page_token'] = self.next_page_token
        else:
            # can not specify next_page_token with other query parameters
            if self.items_per_page:
                params['items_per_page'] = self.items_per_page
            if self.query:
                params['query'] = self.query
            # NOTE: do not check for the combination of start and end parameters,
            # and delegate it validation in list api.
            if self.start:
                params['start'] = self.start
            if self.end:
                params['end'] = self.end
            if self.sort:
                params['sort'] = self.sort

        res = self._api.list_channel_files(self.channel_id, **params)

        self.next_page_token = res.get('next_page_token')
        self._is_first_page = False

        return [self._create_datalake_file(item) for item in res['files']]


class Files:
    def __init__(
            self,
            api: APIClient,
            organization_id: str,
            channel_id: str) -> None:
        self._api = api
        self.organization_id = organization_id
        self.channel_id = channel_id

    def list(self, start: str=None, end: str=None, timezone: str=None,
             sort: str = None, next_page_token: str=None,
             limit: int=None, prefetch: bool=False) -> FileIterator:
        """return iterator for all datalake files in a channel

        Request syntax:
            .. code-block:: python

                file_iterator = files.list()

                # take a first file
                file_1 = next(file_iterator)

                # get all files in a channel
                files = list(file_iterator)

        Params:
            - **start** (str): start date of target uploaded files
            - **end** (str): end date of target uploaded files
            - **timezone** (str): timezone of specified start and end date
            - **sort** (str):
                the order of the file list.
                multiple items can be specified by separating with commas (,).
                It is possible to sort in descending order by specifying a hyphen (-) in front of the item.
                By default, the list is sorted by uploaded_at in ascending order.
            - **next_page_token** (str) : next page token to get the next items. **[optional]**
            - **limit** (int): limit of items. **[optional]**
            - **prefetch** :(bool)**[optional]**

        Return type:
            :class:`FileIterator <abeja.datalake.file.FileIterator>`
        """
        return FileIterator(
            self._api,
            self.organization_id,
            self.channel_id,
            start=start,
            end=end,
            timezone=timezone,
            sort=sort,
            next_page_token=next_page_token,
            items_per_page=limit,
            prefetch=prefetch)
