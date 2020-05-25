# -*- coding: utf-8 -*-
import copy
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Tuple, Optional, List

from abeja.common.config import FETCH_WORKER_COUNT
from abeja.common.file_factory import file_factory
from abeja.common.iterator import Iterator
from abeja.datasets.base import DatasetBase
from abeja.datasets.api.client import APIClient
from abeja.exceptions import InvalidDataFormat


class DatasetItem(DatasetBase):
    """a model class for DatasetItem

    Properties:
        - organization_id (str)
        - dataset_id (str)
        - dataset_item_id (int)
        - attributes (dict)
        - created_at (datetime)
        - updated_at (datetime)
        - source_data (list)
    """

    def __init__(
            self, api: APIClient, organization_id: str, dataset_id: str,
            dataset_item_id: str, **kwargs) -> None:
        """

        :param api: dataset api client
        :param organization_id:
        :param dataset_id:
        :param dataset_item_id:
        :param attributes: meta data annotated to source data.
        :param source_data: (list) list of source data stored in external storage.
        :param created_at:
        :param updated_at:
        """
        self._api = api
        self.organization_id = organization_id
        self.dataset_id = dataset_id
        self.dataset_item_id = dataset_item_id
        self.attributes = kwargs.get('attributes')
        self.created_at = kwargs.get('created_at')
        self.updated_at = kwargs.get('updated_at')
        source_data = kwargs.get('source_data', [])
        self.source_data = []

        for item in source_data:
            data_uri, data_type, _source_data = self._parse_source_data(item)
            source_file = file_factory(
                api, data_uri, data_type, **_source_data)
            self.source_data.append(source_file)

    def __repr__(self):
        return "<{} organization_id:{} " \
               "dataset_id:{} dataset_item_id: {} " \
               "attributes:{} source_data:{}".format(self.__class__.__name__,
                                                     self.organization_id,
                                                     self.dataset_id,
                                                     self.dataset_item_id,
                                                     self.attributes,
                                                     self.source_data)

    def asdict(self):
        d = {
            'dataset_id': self.dataset_id,
            'dataset_item_id': self.dataset_item_id,
            'source_data': [sd.to_source_data() for sd in self.source_data],
            'attributes': copy.deepcopy(self.attributes)
        }
        if self.created_at:
            d['created_at'] = self.created_at
        if self.updated_at:
            d['updated_at'] = self.updated_at
        return d

    def _parse_source_data(self, source_data: dict) -> Tuple[str, str, dict]:
        """extract data_uri and data_type from data

        :param source_data:
        :return: str, str, dict
        :raises:
          - InvalidDataFormat: when data does not includes required keys.
        """
        data = copy.deepcopy(source_data)
        data_type = data.pop('data_type', None)
        try:
            data_uri = data.pop('data_uri')
        except KeyError as e:
            raise InvalidDataFormat('{} is missing'.format(e))
        return data_uri, data_type, data


def _download_item_content(item: DatasetItem) -> DatasetItem:
    # download content and cache to local disk
    for data in item.source_data:
        data.get_content()
    return item


class DatasetItemIterator(Iterator):
    """an iterator class for DatasetItem"""

    def __init__(
            self, api: APIClient, organization_id: str, dataset_id: str,
            next_page_token: Optional[str]=None, limit: Optional[int]=None,
            prefetch: bool=False) -> None:
        self._api = api
        self.organization_id = organization_id
        self.dataset_id = dataset_id
        self.next_page_token = next_page_token
        self.limit = limit
        self.prefetch = prefetch
        self._is_first_page = True
        self._current_page = None
        self._current_page_file_idx = 0
        super().__init__()

    def __iter__(self):
        if self.prefetch:
            return self._items_iter_with_prefetch()
        else:
            return self._items_iter()

    def _items_iter_with_prefetch(self):
        page = self._page()
        with ThreadPoolExecutor(max_workers=FETCH_WORKER_COUNT) as executor:
            futures = []
            while page:
                futures += [executor.submit(_download_item_content, item)
                            for item in page]
                page = self._page()
            for f in as_completed(futures):
                download_item = f.result()
                yield download_item

    def __next__(self):
        if self._current_page is None or self._current_page_file_idx >= len(
                self._current_page):
            self._current_page_file_idx = 0
            self._current_page = self._page()

        if len(self._current_page) == 0:
            raise StopIteration

        item = self._current_page[self._current_page_file_idx]

        self._current_page_file_idx += 1

        return item

    def _page(self):
        """get a page of items in dataset"""
        # if some items of a page are taken, the rest of items are return
        if self._current_page_file_idx != 0:
            if self._current_page[self._current_page_file_idx:]:
                _current_page = self._current_page
                idx = self._current_page_file_idx
                self._current_page = None
                self._current_page_file_idx = 0
                return _current_page[idx:]

        params = {}
        if self.next_page_token:
            params['next_page_token'] = self.next_page_token
        if self.limit:
            params['limit'] = self.limit
        res = self._api.list_dataset_items(
            self.organization_id, self.dataset_id, params=params)
        self.next_page_token = res.get('next_page_token')
        return [
            DatasetItem(
                self._api,
                self.organization_id,
                **_item) for _item in res['items']]


class DatasetItems:
    """a class for a dataset item

        .. code-block:: python

            from abeja.datasets import Client

            client = Client()
            dataset = client.get_dataset(dataset_id='1410805969256')
            dataset_items = dataset.dataset_items

    """

    def __init__(
            self,
            api: APIClient,
            organization_id: str,
            dataset_id: str) -> None:
        self._api = api
        self.organization_id = organization_id
        self.dataset_id = dataset_id

    def create(self, source_data: List[dict], attributes: dict) -> DatasetItem:
        """create a item in dataset

        Request syntax:
            .. code-block:: python

                source_data = [
                    {
                        "data_type": "image/jpeg",
                        "data_uri": "datalake://1200123803688/20170815T044617-f20dde80-1e3b-4496-bc06-1b63b026b872",
                        "height": 500,
                        "width": 200
                    }
                ]

                attributes = {
                    "classification": [
                        {
                            "category_id": 1,
                            "label_id": 1,
                        }
                    ],
                    "detection": [
                        {
                            "category_id": 1,
                            "label_id": 2,
                            "rect": {
                                "xmin": 22,
                                "ymin": 145,
                                "xmax": 140,
                                "ymax": 220
                            }
                        }
                    ]
                    "custom": [
                        {
                            "anything": "something"
                        }
                    ]
                }

                response = dataset_items.create(source_data=source_data, attributes=attributes)

        Params:
            - **source_data** (list): meta data annotated to source data.
            - **attribute** (dict): list of source data stored in external storage.

        Return type:
            :class:`DatasetItem <abeja.datasets.dataset_item.DatasetItem>` object

        """
        res = self._api.create_dataset_item(
            self.organization_id, self.dataset_id, source_data, attributes)
        return DatasetItem(self._api, self.organization_id, **res)

    def get(self, dataset_item_id: str) -> DatasetItem:
        """get a item in dataset

        Request syntax:
            .. code-block:: python

                response = dataset_items.get(dataset_item_id=0)

        Params:
            - **dataset_item_id** (int): dataset item id

        Return type:
            :class:`DatasetItem <abeja.datasets.dataset_item.DatasetItem>` object
        """
        res = self._api.get_dataset_item(
            self.organization_id, self.dataset_id, dataset_item_id)
        return DatasetItem(self._api, self.organization_id, **res)

    def list(
            self,
            next_page_token: Optional[str]=None,
            limit: Optional[int]=None,
            prefetch: bool=False) -> DatasetItemIterator:
        """generate all dataset_items in a dataset

        Request syntax:
            .. code-block:: python

                dataset_item_iter = dataset_items.list()

                # list all dataset items
                dataset_items = list(dataset_item_iter)

                # or get the first dataset item
                dataset_item = next(dataset_item_iter)

        Params:
            - **next_page_token** (str) : next page token to get the next items. **[optional]**
            - **limit** (int): limit of items. **[optional]**
            - **prefetch** (bool) : False by default. if True, download source_data of all dataset_item
              concurrently (therefore the order of dataset_items can be changed) and save them in
              the path specified in environment variable as ``ABEJA_STORAGE_DIR_PATH`` or current
              directory by default. **[optional]**

        Return type:
            :class:`DatasetItemIterator <abeja.datasets.dataset_item.DatasetItemIterator>` object

        """
        return DatasetItemIterator(
            self._api,
            self.organization_id,
            self.dataset_id,
            next_page_token,
            limit,
            prefetch)

    def update(self, dataset_item_id: str, attributes: dict) -> DatasetItem:
        """Update a datset item.

        Request syntax:
            .. code-block:: python

                attributes = {
                    "classification": [
                        {
                            "category_id": 1,
                            "label_id": 1,
                        }
                    ],
                    "detection": [
                        {
                            "category_id": 1,
                            "label_id": 2,
                            "rect": {
                                "xmin": 22,
                                "ymin": 145,
                                "xmax": 140,
                                "ymax": 220
                            }
                        }
                    ]
                    "custom": [
                        {
                            "anything": "something"
                        }
                    ]
                }

                response = dataset_items.update(dataset_item_id=0, attributes=attributes)

        Params:
            - **dataset_item_id** (int): dataset item id
            - **attribute** (dict): list of source data stored in external storage.

        Return type:
            return the updated dataset item
            :class:`DatasetItem <abeja.datasets.dataset_item.DatasetItem>` object
        """
        res = self._api.update_dataset_item(
            self.organization_id,
            self.dataset_id,
            dataset_item_id,
            attributes)
        return DatasetItem(self._api, self.organization_id, **res)

    def bulk_update(self, bulk_attributes: dict) -> DatasetItem:
        """Update a datset item in bulk.

        Request syntax:
            .. code-block:: python

                bulk_attributes = [
                    {
                        "dataset_item_id": 1111111111111,
                        "attributes": {
                            "classification": [
                                {
                                    "category_id": 1,
                                    "label_id": 1
                                }
                            ],
                            "custom_format": {
                                "anything": "something"
                                   },
                            "detection": [
                                {
                                    "category_id": 1,
                                    "label_id": 2,
                                    "rect": {
                                        "xmin": 22,
                                        "ymin": 145,
                                        "xmax": 140,
                                        "ymax": 220
                                    }
                                }
                            ]
                        }
                    }
                ]

                response = dataset_items.bulk_update(bulk_attributes=bulk_attributes)

        Params:
            - **bulk_attributes** (dict): list of attributes.

        Return type:
            return the updated dataset item list
            :class:`DatasetItem <abeja.datasets.dataset_item.DatasetItem>` object
        """
        res = self._api.bulk_update_dataset_item(
            self.organization_id, self.dataset_id, bulk_attributes)
        return [
            DatasetItem(
                self._api,
                self.organization_id,
                **_item) for _item in res]

    def delete(self, dataset_item_id: str) -> DatasetItem:
        """Delete a datset item.

        Request syntax:
            .. code-block:: python

                response = dataset_items.delete(dataset_item_id=0)

        Params:
            -**dataset_item_id** (int): dataset item id

        Return type:
            return the deleted dataset item
            :class:`DatasetItem <abeja.datasets.dataset_item.DatasetItem>` object
        """
        res = self._api.delete_dataset_item(
            self.organization_id, self.dataset_id, dataset_item_id)
        return DatasetItem(self._api, self.organization_id, **res)
