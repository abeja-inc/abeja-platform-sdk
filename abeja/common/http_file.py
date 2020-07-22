import requests

from abeja.common.connection import http_error_handler
from abeja.common.local_file import use_binary_cache
from abeja.common.source_data import SourceData
from abeja.datalake.api.client import APIClient


class HTTPFile(SourceData):
    def __init__(self, api: APIClient, uri: str) -> None:
        self.__api = api
        self.uri = uri

    def get_content(self, cache: bool = True) -> bytes:
        if cache:
            decorated = use_binary_cache(self._get_content_from_remote)
            return decorated(self)
        return self._get_content_from_remote()

    def _get_content_from_remote(self):
        try:
            res = self.__api._connection.request("GET", self.uri)
            return res.content
        except requests.exceptions.HTTPError as e:
            raise http_error_handler(e)

    def to_source_data(self):
        return {
            "data_uri": self.uri,
        }
