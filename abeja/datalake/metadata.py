import typing
from collections.abc import Mapping

from abeja.datalake.api.client import APIClient


class DatalakeMetadata(Mapping):
    def __init__(self, api: APIClient, channel_id: str, file_id: str,
                 metadata: typing.Optional[typing.Dict[str, str]]=None):
        self.channel_id = channel_id
        self.file_id = file_id
        self.__api = api
        if metadata is None:
            self.__dict = {}
        else:
            self.__dict = {
                k.replace(
                    'x-abeja-meta-',
                    ''): v for k,
                v in metadata.items() if k.startswith('x-abeja-meta-')}

    def __len__(self):
        return len(self.__dict)

    def __getitem__(self, key):
        return self.__dict[key]

    def __setitem__(self, key, value):
        self.__dict[key] = value

    def __contains__(self, key):
        return key in self.__dict

    def __repr__(self):
        return self.__dict.__repr__()

    def __iter__(self):
        return iter(self.__dict)

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def update(self, *args, **kwargs):
        metadata = dict(*args, **kwargs)
        # Construct metadata.
        metadata = {
            k: str(v) for k,
            v in metadata.items() if k.lower() not in {
                'content_type',
                'content-type'}}
        # Update local variable.
        self.__dict.update(metadata)
