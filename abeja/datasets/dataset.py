# -*- coding: utf-8 -*-
from typing import List, Optional
from abeja.datasets.base import DatasetBase
from abeja.datasets.api.client import APIClient
from abeja.datasets.dataset_item import DatasetItems


class Dataset(DatasetBase):
    """a model class for a dataset

    Properties:
        - organization_id (str)
        - dataset_id (str)
        - name (str)
        - type (str)
        - props (dict)
        - total_count (int)
        - created_at (datetime)
        - updated_at (datetime)

    """

    def __init__(
            self,
            api: APIClient,
            organization_id: str,
            dataset_id: str,
            name: Optional[str]=None,
            type: Optional[str]=None,
            props: Optional[dict]=None,
            total_count: Optional[int]=None,
            created_at: Optional[str]=None,
            updated_at: Optional[str]=None,
            **kwargs) -> None:
        self._api = api
        self.organization_id = organization_id
        self.dataset_id = dataset_id
        self.name = name
        self.type = type
        self.props = props
        self.total_count = total_count
        self.created_at = created_at
        self.updated_at = updated_at

    @property
    def dataset_items(self) -> DatasetItems:
        """Get dataset Items object

        Request syntax:
            .. code-block:: python

                dataset = client.get_dataset(dataset_id='1410805969256')
                dataset_items = dataset.dataset_items

        Returns:
            :class:`DatasetItem <abeja.datasets.dataset_item.DatasetItem>` object
        """
        return DatasetItems(self._api, self.organization_id, self.dataset_id)

    def __repr__(self):
        return "<{} organization_id:{} " \
               "dataset_id:{} name:{} type:{} " \
               "props:{} total_count:{} created_at:{} updated_at:{}".format(self.__class__.__name__,
                                                                            self.organization_id,
                                                                            self.dataset_id,
                                                                            self.name,
                                                                            self.type,
                                                                            self.props,
                                                                            self.total_count,
                                                                            self.created_at,
                                                                            self.updated_at)


class Datasets:
    """a class for handling datasets"""

    def __init__(self, api: APIClient, organization_id: str) -> None:
        self._api = api
        self.organization_id = organization_id

    def create(self, name: str, type: str, props: dict) -> Dataset:
        """create a dataset

        API reference: POST /organizations/<organization_id>/datasets/

        Request Syntax:
            .. code-block:: python

                name = "test-dataset"
                dataset_type = "classification"
                props = {
                    "categories": [
                        {
                            "labels": [
                                {
                                    "label_id": 1,
                                    "label": "dog"
                                },
                                {
                                    "label_id": 2,
                                    "label": "cat"
                                },
                                {
                                    "label_id": 3,
                                    "label": "others"
                                }
                            ],
                            "category_id": 1,
                            "name": "cats_dogs"
                        }
                    ]
                }
                response = datasets.create(name, dataset_type, props)

        Params:
            - **name** (str): dataset name
            - **type** (str): dataset types eg: classification, detection
            - **props** (dict): properties of dataset

        Return type:
            :class:`Dataset <abeja.datasets.dataset.Dataset>` object
        """
        res = self._api.create_dataset(self.organization_id,
                                       name, type, props)
        return Dataset(self._api, **res)

    def get(self, dataset_id: str) -> Dataset:
        """get a dataset

        Request syntax:
            .. code-block:: python

                response = datasets.get(dataset_id=1410805969256)

        Params:
            - **dataset_id** (str): dataset id

        Return type:
            :class:`Dataset <abeja.datasets.dataset.Dataset>` object
        """
        res = self._api.get_dataset(self.organization_id, dataset_id)
        return Dataset(self._api, **res)

    def list(self) -> List[Dataset]:
        """Get dataset list

        Request syntax:
            .. code-block:: python

                response = datasets.list()

        Response type:
            list of :class:`Dataset <abeja.datasets.dataset.Dataset>` object
        """
        res = self._api.list_datasets(self.organization_id)
        return [Dataset(self._api, **data) for data in res]

    def delete(self, dataset_id: str) -> Dataset:
        """delete a dataset

        Request syntax:
            .. code-block:: python

                response = datasets.delete(dataset_id='1377232365920')

        Params:
            - **dataset_id** (str): dataset id

        Response type:
            :class:`Dataset <abeja.datasets.dataset.Dataset>` object
        """
        res = self._api.delete_dataset(self.organization_id, dataset_id)
        return Dataset(self._api, **res)
