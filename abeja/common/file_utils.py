from typing import Dict


class FileMixin:
    def __init__(self, api, uri: str, type: str, **kwargs):
        self._api = api
        self.uri = uri
        self.type = type
        for k, v in kwargs.items():
            setattr(self, k, v)

    def to_source_data(self) -> Dict[str, str]:
        """Convert to source data format

        Return type:
            dict
        """
        source_data = {'data_uri': self.uri}
        if self.type:
            source_data['data_type'] = self.type
        return source_data
