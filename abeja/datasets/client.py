# -*- coding: utf-8 -*-
import os
from typing import Dict, Optional
from abeja.datasets.dataset import Dataset
from abeja.datasets.dataset import Datasets
from abeja.datasets.api.client import APIClient


class Client:
    """A High-Level client for Dataset API

    .. code-block:: python

       from abeja.datasets import Client

       client = Client()
    """

    def __init__(
            self, organization_id: Optional[str] = None,
            credential: Optional[Dict[str, str]] = None,
            timeout: Optional[int] = None) -> None:
        self.api = APIClient(credential=credential, timeout=timeout)
        self.organization_id = organization_id or os.environ.get(
            'ABEJA_ORGANIZATION_ID')

    def get_dataset(self, dataset_id: str) -> Dataset:
        """Get dataset for specific dataset_id

        Request syntax:
            .. code-block:: python

                response = client.get_dataset(dataset_id='1234567890123')

        Params:
            - **dataset_id** (str): dataset id

        Return type:
            :class:`Dataset <abeja.datasets.dataset.Dataset>`
        """
        datasets = Datasets(self.api, self.organization_id)
        return datasets.get(dataset_id)

    @property
    def datasets(self) -> Datasets:
        """Get datasets object

        Request syntax:
            .. code-block:: python

                datasets = client.datasets

        Returns:
            :meth:`Datasets <abeja.datasets.dataset.Datasets>`

        """
        return Datasets(self.api, self.organization_id)
