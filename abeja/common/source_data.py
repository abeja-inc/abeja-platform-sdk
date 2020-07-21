from abc import abstractmethod
from typing import Dict

from typing_extensions import Protocol


class SourceData(Protocol):
    @abstractmethod
    def get_content(self, cache: bool = True) -> bytes:
        raise NotImplementedError

    @abstractmethod
    def to_source_data(self) -> Dict[str, str]:
        raise NotImplementedError
