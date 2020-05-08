from typing import Sized, Iterable, Iterator, TypeVar, Optional, Any, Dict
from abc import ABC, abstractmethod
from .api.client import APIClient

T = TypeVar('T')


class SizedIterable(Sized, Iterable[T], ABC):
    @abstractmethod
    def __len__(self) -> int:
        pass

    @abstractmethod
    def __iter__(self) -> Iterator[T]:
        pass

# Iterator classes


class AbstractSizedIterator(SizedIterable[T]):

    def __init__(self, api: APIClient, organization_id: str,
                 filter_archived: Optional[bool],
                 offset: Optional[int],
                 limit: Optional[int]) -> None:
        self.__api = api
        self.__organization_id = organization_id
        self.__filter_archived = filter_archived
        self.__offset = offset if offset is not None else 0
        self.__limit = limit if limit is not None else 50
        self.__total = None  # type: Optional[int]
        self.__page = None  # type: Optional[Dict[str, Any]]

    @abstractmethod
    def invoke_api(self, api: APIClient) -> Dict[str, Any]:
        pass

    @abstractmethod
    def build_entry(self, api: APIClient, entry: Dict[str, Any]) -> T:
        pass

    @property
    def organization_id(self) -> str:
        return self.__organization_id

    @property
    def filter_archived(self) -> Optional[bool]:
        return self.__filter_archived

    @property
    def offset(self) -> Optional[int]:
        return self.__offset

    @property
    def limit(self) -> Optional[int]:
        return self.__limit

    def __len__(self) -> int:
        if self.__page is None:
            self.__page = self.invoke_api(self.__api)
        return self.__page['total']

    def __iter__(self) -> Iterator[T]:
        if self.__page is None:
            self.__page = self.invoke_api(self.__api)

        while self.__page['entries']:
            for entry in self.__page["entries"]:
                yield self.build_entry(self.__api, entry)
                self.__offset += 1
            if self.__offset < self.__page['total']:
                self.__page = self.invoke_api(self.__api)
            else:
                break
