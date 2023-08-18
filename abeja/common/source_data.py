from abc import abstractmethod
from typing import Dict


class SourceData:
    @abstractmethod
    def get_content(self, cache: bool = True) -> bytes:
        raise NotImplementedError

    @abstractmethod
    def to_source_data(self) -> Dict[str, str]:
        raise NotImplementedError
