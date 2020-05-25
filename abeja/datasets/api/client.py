from typing import List, Optional

from abeja.common.api_client import BaseAPIClient


class APIClient(BaseAPIClient):
    """A Low-Level client for Dataset API

    .. code-block:: python

       from abeja.datasets import APIClient

       api_client = APIClient()
    """

    def create_dataset(
            self,
            organization_id: str,
            name: str,
            type: str,
            props: dict) -> dict:
        """create a dataset

        API reference: POST /organizations/<organization_id>/datasets/

        Request Syntax:
            .. code-block:: python

                organization_id = "1102940376065"
                dataset_name = "test-dataset"
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
                response = api_client.create_dataset(organization_id, dataset_name, dataset_type, props)

        Params:
            - **organization_id** (str): ORGANIZATION_ID
            - **name** (str): dataset name
            - **type** (str): dataset types eg: classification, detection
            - **props** (dict): properties of dataset
                - **categories** (list): list of categories which are used as validation rules for dataset item
                    - **category_id** (int): identifier of category
                    - **name** (str): name of category
                    - **labels** (list):
                        - **label_id** (int): identifier of label
                        - **label** (str): name of label **[optional]**

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    "created_at": "2018-04-10T07:49:30.514794",
                    "dataset_id": "1410805969256",
                    "name": "test-dataset",
                    "organization_id": "1102940376065",
                    "props": {
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
                    },
                    "type": "classification",
                    "updated_at": "2018-04-10T07:49:30.514794"
                }

        Raises:
            - BadRequest: the resource already exists or parameters is insufficient or invalid.
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        params = {
            'name': name,
            'type': type,
            'props': props
        }
        path = '/organizations/{}/datasets'.format(organization_id)
        return self._connection.api_request(
            method='POST', path=path, json=params)

    def get_dataset(self, organization_id: str, dataset_id: str) -> dict:
        """get a dataset

        API reference: GET /organizations/<organization_id>/datasets/<dataset_id>

        Request Syntax:
            .. code-block:: python

                response = api_client.get_dataset(organization_id='1102940376065', dataset_id='1410805969256')
        Params:
            - **organization_id** (str): ORGANIZATION_ID
            - **dataset_id** (str): dataset_id of the requested dataset

        Return type:
            dict

        Returns:
            Response Syntax:
                .. code-block:: json

                    {
                        "created_at": "2018-04-10T07:49:30.514794",
                        "dataset_id": "1410805969256",
                        "total_count": 3670,
                        "name": "test-dataset",
                        "organization_id": "1102940376065",
                        "props": {
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
                        },
                        "type": "classification",
                        "updated_at": "2018-04-10T07:49:30.514794"
                    }

        Raises:
          - NotFound: dataset not found
          - Unauthorized: Authentication failed
          - InternalServerError
        """

        path = '/organizations/{}/datasets/{}'.format(
            organization_id, dataset_id)
        return self._connection.api_request(method='GET', path=path)

    def list_datasets(
            self, organization_id: str, max_results: Optional[int]=None,
            next_token: Optional[str]=None) -> List[dict]:
        """Get datasets list

        API reference: GET /organizations/<organization_id>/datasets/

        Request syntax:
            .. code-block:: python

                response = api_client.get_dataset(organization_id='1102940376065')

        Params:
            - **organization_id** (str): ORGANIZATION_ID
            - **max_results** (int): maximum number of datasets in case of passing **[optional]**
            - **next_token** (str): To get the next list of datasets **[optional]**

        Return type:
            list

        Returns:
            Return syntax:
                .. code-block:: python

                    [
                        {
                            "created_at": "2018-03-03T09:04:58.274324",
                            "dataset_id": "1377232365920",
                            "name": "cats-dogs",
                            "organization_id": "1102940376065",
                            "props": {
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
                            },
                            "type": "classification",
                            "updated_at": "2018-03-03T09:04:58.274324"
                        },
                        {
                            .....
                            .....
                        },
                        .....
                    ]


        Raises:
          - Unauthorized: Authentication failed
          - InternalServerError
        """
        params = {}
        if max_results:
            params['max_results'] = max_results
        if next_token:
            params['next_token'] = next_token
        path = '/organizations/{}/datasets'.format(organization_id)
        return self._connection.api_request(
            method='GET', path=path, params=params)

    def delete_dataset(self, organization_id: str, dataset_id: str) -> dict:
        """delete a dataset

        API reference: DELETE /organizations/<organization_id>/datasets/<dataset_id>

        Request syntax:
            .. code-block:: python

                response = api_client.delete_dataset(organization_id='1102940376065', dataset_id='1410805969256')

        Params:
            - **organization_id** (str): ORGANIZATION_ID
            - **dataset_id** (str): dataset id

        Return type:
            dict

        Responses:
            Response syntax:
                .. code-block:: python

                    {
                        "created_at": "2018-04-10T07:49:30.514794",
                        "dataset_id": "1410805969256",
                        "name": "test-dataset",
                        "organization_id": "1102940376065",
                        "props": {
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
                        },
                        "type": "classification",
                        "updated_at": "2018-04-10T07:49:30.514794"
                    }

        Raises:
          - NotFound: dataset not found
          - Unauthorized: Authentication failed
          - InternalServerError
        """
        path = '/organizations/{}/datasets/{}'.format(
            organization_id, dataset_id)
        return self._connection.api_request(method='DELETE', path=path)

    # dataset_item
    def create_dataset_item(
            self, organization_id: str, dataset_id: str,
            source_data: dict, attributes: Optional[dict]=None) -> dict:
        """create a item in a dataset

        API reference: POST /organizations/<organization_id>/datasets/<dataset_id>/items/

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
                    "custom": [
                        {
                            "anything": "something"
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
                        },
                    ]
                }
                response = api_client.create_dataset_item(
                    organization_id="1102940376065",
                    dataset_id="1410805969256",
                    source_data=source_data,
                    attributes=attributes
                )

        Params:
            - **organization_id** (str): ORGANIZATION_ID
            - **dataset_id** (str): dataset id
            - **source_data** (list): list of source data
                - **data_type** (str): MIME type of file
                - **data_uri** (str): reference identifier of the source file. ex) datalake://1200000000000/20170815T044617-f20dde80-1e3b-4496-bc06-1b63b026b872
                - **height** (int): height of image, if the source file is an image **[optional]**
                - **width** (int): width of image, if the source file is an image **[optional]**
            - **attributes** (dict): attribute of dataset item **[optional]**
                - **classification** (list): list of label, if dataset type is `classification`
                    - **category_id** (int): identifier of category
                    - **label_id** (int): identifier of label, registered in dataset.props
                    - **label** (str): name of label, registered in dataset.props **[optional]**
                - **detection** (list): list of label, if dataset type is `detection`
                    - **category_id** (int): identifier of category
                    - **label_id** (int): identifier of label, registered in dataset.props
                    - **label** (str): name of label, registered in dataset.props **[optional]**
                    - **rect** (dict): coordinates of bounding box
                        - **xmin** (int):
                        - **ymin** (int):
                        - **xmax** (int):
                        - **ymax** (int):
                - **segmentation** (list): list of label, if dataset type is `segmentation`
                - **custom** (any): any primitive type of objects, if dataset type is `custom`

        Return type:
            list
        Returns:
            Return syntax:
                .. code-block:: python

                    {
                        "attributes": {
                            "classification": [
                                {
                                    "category_id": 1,
                                    "label_id": 1
                                }
                            ],
                            "custom": [
                                {
                                    "anything": "something"
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
                                },
                            ]
                        },
                        "created_at": "2017-12-27T06:25:00.394026",
                        "dataset_id": "1410805969256",
                        "dataset_item_id": 0,
                        "source_data": [
                            {
                                "data_type": "image/jpeg",
                                "data_uri": "datalake://1200123803688/20170815T044617-f20dde80-1e3b-4496-bc06-1b63b026b872",
                                "height": 500,
                                "width": 200
                            }
                        ],
                        "organization_id": "1102940376065",
                        "updated_at": "2017-12-27T06:25:00.394026"
                    }

        Raises:
          - BadRequest: specified dataset id does not exist or dataset item id already exist,
                        parameters is insufficient or invalid,
                        input data exceeded the max limit
          - Unauthorized: Authentication failed
          - InternalServerError
        """
        params = {
            'source_data': source_data,
            'attributes': attributes
        }
        path = '/organizations/{}/datasets/{}/items'.format(organization_id,
                                                            dataset_id)
        return self._connection.api_request(method='POST',
                                            path=path,
                                            json=params)

    def get_dataset_item(
            self,
            organization_id: str,
            dataset_id: str,
            dataset_item_id: str) -> dict:
        """get a item in a dataset

        API reference: GET /organizations/<organization_id>/datasets/<dataset_id>/items/<dataset_item_id>

        Request syntax:
            .. code-block:: python

                response = api_client.get_dataset_item(organization_id='1102940376065',
                                                        dataset_id='1410805969256',
                                                        dataset_item_id=0
                                                    )


        Params:
            - **organization_id** (str): ORGANIZATION_ID
            - **dataset_id** (str): dataset id
            - **dataset_item_id** (int): dataset item id

        Return type:
            dict

        Returns:
            Return syntax:
                .. code-block:: python

                    {
                        "attributes": {
                            "classification": [
                                {
                                    "category_id": 1,
                                    "label_id": 1
                                }
                            ],
                            "custom": [
                                {
                                    "anything": "something"
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
                                },
                            ]
                        },
                        "created_at": "2017-12-27T06:25:00.394026",
                        "dataset_id": "1410805969256",
                        "dataset_item_id": 0,
                        "source_data": [
                            {
                                "data_type": "image/jpeg",
                                "data_uri": "datalake://1200123803688/20170815T044617-f20dde80-1e3b-4496-bc06-1b63b026b872",
                                "height": 500,
                                "width": 200
                            }
                        ],
                        "organization_id": "1102940376065",
                        "updated_at": "2017-12-27T06:25:00.394026"
                    }

        Raises:
          - NotFound: dataset not found
          - Unauthorized: Authentication failed
          - InternalServerError
        """
        path = '/organizations/{}/datasets/{}/items/{}'.format(organization_id,
                                                               dataset_id,
                                                               dataset_item_id)
        return self._connection.api_request(method='GET', path=path)

    def list_dataset_items(
            self, organization_id: str, dataset_id: str,
            params: Optional[dict]=None) -> List[dict]:
        """Get item list in a dataset

        API reference: GET /organizations/<organization_id>/datasets/<dataset_id>/items/

        Params:
            - **organization_id** (str): ORGANIZATION_ID
            - **dataset_id** (str): dataset id
            - **params** (dict): **[optional]**
                - **next_page_token** (str): token to get the next page
                - **q** (str): search query, ex) `label_id:1 AND label:dog OR tag:A`

        Return type:
            dict

        Returns:
            dataset item list

            Return syntax:
                .. code-block:: python

                    {
                        "items": [
                            {
                                "attributes": {
                                    "classification": [
                                        {
                                            "category_id": 1,
                                            "label_id": 1
                                        }
                                    ],
                                    "custom": [
                                        {
                                            "anything": "something"
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
                                        },
                                    ]
                                },
                                "created_at": "2017-12-27T06:25:00.394026",
                                "dataset_id": "1410805969256",
                                "dataset_item_id": 0,
                                "source_data": [
                                    {
                                        "data_type": "image/jpeg",
                                        "data_uri": "datalake://1200123803688/20170815T044617-f20dde80-1e3b-4496-bc06-1b63b026b872",
                                        "height": 500,
                                        "width": 200
                                    }
                                ],
                                "organization_id": "1102940376065",
                                "updated_at": "2017-12-27T06:25:00.394026"
                            },
                            ...
                        ],
                        "total_count": 1000,
                        "next_page_token": "xxx"
                    }

            - **items** (list): list of dataset item dict
            - **total_count** (int): total number of filtered dataset items
            - **next_page_token** (str): token to get the next page

        Raises:
          - NotFound: dataset not found
          - Unauthorized: Authentication failed
          - InternalServerError
        """
        path = '/organizations/{}/datasets/{}/items'.format(organization_id,
                                                            dataset_id)
        if not params:
            params = {}
        return self._connection.api_request(
            method='GET', path=path, params=params)

    def update_dataset_item(
            self, organization_id: str, dataset_id: str, dataset_item_id: str,
            attributes: Optional[dict] = None) -> dict:
        """update a item in a dataset

        API reference: PUT /organizations/<organization_id>/datasets/<dataset_id>/items/<dataset_item_id>

        Request syntax:
            .. code-block:: python

                attributes = {
                    "classification": [
                        {
                            "category_id": 1,
                            "label_id": 1,
                        }
                    ],
                    "custom": [
                        {
                            "anything": "something"
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
                        },
                    ]
                }
                api_client.update_dataset_item(
                    organization_id='1102940376065',
                    dataset_id='1410805969256',
                    dataset_item_id=0,
                    attributes=attributes)

        Params:
            - **organization_id** (str): ORGANIZATION_ID
            - **dataset_id** (str): dataset id
            - **dataset_item_id** (str): dataset item id
            - **attributes** (dict): attribute of dataset item **[optional]**
                - **classification** (list): list of label, if dataset type is `classification`
                    - **category_id** (int): identifier of category
                    - **label_id** (int): identifier of label, registered in dataset.props
                    - **label** (str): name of label, registered in dataset.props **[optional]**
                - **detection** (list): list of label, if dataset type is `detection`
                    - **category_id** (int): identifier of category
                    - **label_id** (int): identifier of label, registered in dataset.props
                    - **label** (str): name of label, registered in dataset.props **[optional]**
                    - **rect** (dict): coordinates of bounding box
                        - **xmin** (int):
                        - **ymin** (int):
                        - **xmax** (int):
                        - **ymax** (int):
                - **segmentation** (list): list of label, if dataset type is `segmentation`
                - **custom** (any): any primitive type of objects, if dataset type is `custom`

        Return type:
            list
        Returns:
            Return syntax:
                .. code-block:: python

                    {
                        "attributes": {
                            "classification": [
                                {
                                    "category_id": 1,
                                    "label_id": 1
                                }
                            ],
                            "custom": [
                                {
                                    "anything": "something"
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
                                },
                            ]
                        },
                        "created_at": "2017-12-27T06:25:00.394026",
                        "dataset_id": "1410805969256",
                        "dataset_item_id": 0,
                        "source_data": [
                            {
                                "data_type": "image/jpeg",
                                "data_uri": "datalake://1200123803688/20170815T044617-f20dde80-1e3b-4496-bc06-1b63b026b872",
                                "height": 500,
                                "width": 200
                            }
                        ],
                        "organization_id": "1102940376065",
                        "updated_at": "2017-12-27T06:25:00.394026"
                    }

        Raises:
          - BadRequest: specified dataset id does not exist
          - NotFound: dataset not found
          - Unauthorized: Authentication failed
          - InternalServerError
        """
        params = {
            'attributes': attributes
        }
        path = '/organizations/{}/datasets/{}/items/{}'.format(organization_id,
                                                               dataset_id,
                                                               dataset_item_id)
        return self._connection.api_request(
            method='PUT', path=path, json=params)

    def bulk_update_dataset_item(
            self, organization_id: str, dataset_id: str,
            bulk_attributes: Optional[dict] = None) -> dict:
        """update a item in a dataset

        API reference: PUT /organizations/<organization_id>/datasets/<dataset_id>/items

        Request syntax:

            .. code-block:: python

                bulk_attributes =  [
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
                api_client.bulk_update_dataset_item(organization_id='1102940376065',
                                                        dataset_id='1410805969256',
                                                        bulk_attributes=bulk_attributes
                                                    )

        Params:
            - **organization_id** (str): ORGANIZATION_ID
            - **dataset_id** (str): dataset id
            - **bulk_attributes** (dict): bulk_attribute of dataset item **[optional]**
                - **dataset_item_id** (list): list of dataset_item_id
                    - **classification** (list): list of label, if dataset type is `classification`
                        - **category_id** (int): identifier of category
                        - **label_id** (int): identifier of label, registered in dataset.props
                        - **label** (str): name of label, registered in dataset.props **[optional]**
                    - **detection** (list): list of label, if dataset type is `detection`
                        - **category_id** (int): identifier of category
                        - **label_id** (int): identifier of label, registered in dataset.props
                        - **label** (str): name of label, registered in dataset.props **[optional]**
                        - **rect** (dict): coordinates of bounding box
                            - **xmin** (int):
                            - **ymin** (int):
                            - **xmax** (int):
                            - **ymax** (int):
                    - **segmentation** (list): list of label, if dataset type is `segmentation`
                    - **custom** (any): any primitive type of objects, if dataset type is `custom`

        Return type:
            list
        Returns:
            Return syntax:
                .. code-block:: python

                    [
                        {
                            "organization_id": "1200000000000",
                            "dataset_id": "1440000000000",
                            "dataset_item_id": 101554,
                            "source_data": [
                                {
                                    "data_type": "image/jpeg",
                                    "data_uri": "datalake://1230000000000/20180520T133855-10051aa4-d7aa-43a1-8d5e-4d59dae5bb83"
                                }
                            ],
                            "attributes": {
                                "classification": {
                                    "category_id": 1,
                                    "label_id": 1
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
                            },
                            "created_at": "2018-05-20T13:51:16.010344",
                            "updated_at": "2018-05-20T13:51:16.010344"
                        }
                    ]

        Raises:
          - BadRequest: specified dataset id does not exist
          - Unauthorized: Authentication failed
          - InternalServerError
        """
        params = bulk_attributes
        path = '/organizations/{}/datasets/{}/items'.format(organization_id,
                                                            dataset_id)
        return self._connection.api_request(
            method='PUT', path=path, json=params)

    def delete_dataset_item(
            self,
            organization_id: str,
            dataset_id: str,
            dataset_item_id: str) -> dict:
        """delete a item in a dataset

        API reference: DELETE /organizations/<organization_id>/datasets/<dataset_id>/items/<dataset_item_id>

        Request syntax:
            .. code-block:: python

                api_client.delete_dataset_item(organization_id='1102940376065',
                                                        dataset_id='1410805969256',
                                                        dataset_item_id=0
                                                    )

        Params:
            - **organization_id** (str): ORGANIZATION_ID
            - **dataset_id** (str): dataset id
            - **dataset_item_id** (str): dataset item id

        Return type:
            dict

        Returns:
            deleted dataset item

        Raises:
          - NotFound: dataset not found
          - Unauthorized: Authentication failed
          - InternalServerError
        """
        path = '/organizations/{}/datasets/{}/items/{}'.format(organization_id,
                                                               dataset_id,
                                                               dataset_item_id)
        return self._connection.api_request(method='DELETE', path=path)
