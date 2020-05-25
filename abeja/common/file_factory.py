from urllib.parse import urlparse

from abeja.datalake.api.client import APIClient
from abeja.datalake.file import DatalakeFile
from abeja.exceptions import UnsupportedURI


def file_factory(
        client: APIClient,
        uri: str,
        type: str,
        **kwargs) -> DatalakeFile:
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
    raise UnsupportedURI('{} is not supported.'.format(uri))
