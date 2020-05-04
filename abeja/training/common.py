from typing import Sized, Iterable, Iterator, TypeVar
from abc import ABC, abstractmethod

T = TypeVar('T')


class SizedIterable(Sized, Iterable[T], ABC):
    @abstractmethod
    def __len__(self) -> int:
        pass

    @abstractmethod
    def __iter__(self) -> Iterator[T]:
        pass
