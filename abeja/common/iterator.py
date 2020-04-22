from abc import ABCMeta, abstractmethod


class Iterator(metaclass=ABCMeta):
    """abstract class for page iterator"""

    def __iter__(self):
        return self._items_iter()

    def _items_iter(self):
        for page in self._page_iter():
            for item in page:
                yield item

    def _page_iter(self):
        page = self._page()
        while page:
            yield page
            page = self._page()

    @abstractmethod
    def _page(self):
        raise NotImplementedError
