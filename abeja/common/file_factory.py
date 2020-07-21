from urllib.parse import urlparse

from abeja.common.http_file import HTTPFile
from abeja.common.source_data import SourceData
from abeja.datalake.api.client import APIClient
from abeja.datalake.file import DatalakeFile
from abeja.exceptions import UnsupportedURI


def file_factory(
        client: APIClient,
        uri: str,
        type: str,
        **kwargs) -> SourceData:
    """generate file for the given uri

    :param client:
    :param uri:
    :param type:
    :param kwargs:
    :return:
    :raises: UnsupportedURI if given uri is not supported
    """
    pr = urlparse(uri)
    if pr.scheme == 'datalake':
        return DatalakeFile(client, uri=uri, type=type, **kwargs)
    elif pr.scheme == "http" or pr.scheme == "https":
        return HTTPFile(client, uri=uri)
    raise UnsupportedURI('{} is not supported.'.format(uri))
