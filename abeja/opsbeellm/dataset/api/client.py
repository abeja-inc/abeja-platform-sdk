from __future__ import annotations
from typing import Optional, List, Dict
from abeja.common.api_client import BaseAPIClient
from abeja.exceptions import BadRequest


class APIClient(BaseAPIClient):
    """A Low-Level client for OpsBee LLM Dataset API

    .. code-block:: python

       from abeja.opsbeellm.dataset import APIClient

       api_client = APIClient()
    """

    def get_datasets(
        self,
        organization_id: str,
        offset: Optional[int] = 0,
        limit: Optional[int] = 1000,
    ) -> dict:
        """get datasets

        API reference: GET /opsbee-llm/organizations/<organization_id>/datasets

        Request Syntax:
            .. code-block:: python

                organization_id = "1410000000000"
                offset = 0
                limit = 1000
                response = api_client.get_datatsets(
                    organization_id, offset, limit)

        Params:
            - **organization_id** (str): organization identifier
            - **offset** (int): **[optional]** offset of datasets ( which starts from 0 )
            - **limit** (int): **[optional]** max number of datasets to be returned

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    'organization_id': '1410000000000'
                    'datasets': [
                        {
                            'id': '3053595942757',
                            'organization_id': '1410000000000',
                            'name': 'datasetA',
                            'description': 'datasetAの説明',
                            'type': 'qa',
                            'item_count': 100,
                            'created_at': '2023-12-15T16:50:33+09:00',
                            'updated_at': '2023-12-15T16:50:33+09:00'
                        },
                        {
                            'id': '9968625354849',
                            'organization_id': '1410000000000',
                            'name': 'datasetB',
                            'description': 'datasetBの説明',
                            'type': 'llm',
                            'item_count': 300,
                            'created_at': '2023-12-04T16:01:52+09:00',
                            'updated_at': '2023-12-04T16:01:52+09:00',
                        },
                        ...
                    ],
                    'offset': 0,
                    'limit': 1000,
                    'has_next': False,
                }

        Raises:
            - BadRequest
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        params = {}
        if offset is None:
            offset = 0
        if limit is None:
            limit = 1000
        params['offset'] = offset
        params['limit'] = limit

        path = '/opsbee-llm/organizations/{}/datasets?offset={}&limit={}'.format(
            organization_id,
            offset,
            limit,
        )
        return self._connection.api_request(method='GET', path=path, params=params)

    def get_dataset(
        self,
        organization_id: str,
        dataset_id: str,
    ) -> dict:
        """get dataset

        API reference: GET /opsbee-llm/organizations/<organization_id>/datasets/<dataset_id>

        Request Syntax:
            .. code-block:: python

                organization_id = "1410000000000"
                dataset_id = "3053595942757"
                response = api_client.get_datatset(
                    organization_id, dataset_id)

        Params:
            - **organization_id** (str): organization identifier
            - **dataset_id** (str): dataset identifier

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    'id': '3053595942757',
                    'organization_id': '1410000000000',
                    'name': 'datasetA',
                    'description': 'datasetAの説明',
                    'type': 'qa',
                    'item_count': 100,
                    'created_at': '2023-12-15T16:50:33+09:00',
                    'updated_at': '2023-12-15T16:50:33+09:00'
                }

        Raises:
            - BadRequest
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        path = '/opsbee-llm/organizations/{}/datasets/{}'.format(
            organization_id,
            dataset_id,
        )
        return self._connection.api_request(method='GET', path=path)

    def create_dataset(
        self,
        organization_id: str,
        name: str,
        type: str,
        description: Optional[str] = None,
    ) -> dict:
        """create a dataset

        API reference: POST /opsbee-llm/organizations/<organization_id>/datasets

        Request Syntax:
            .. code-block:: python

                organization_id = "1410000000000"
                name = "datasetA"
                description = "datasetA description"
                type = "qa"
                response = api_client.create_dataset(
                    organization_id, name, type, description)

        Params:
            - **organization_id** (str): organization identifier
            - **name** (str): dataset name
            - **type** (str): dataset type. available type are "qa" or "llm".
            - **description** (str): **[optional]** dataset description

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    'id': "1234567890123",
                    'organization_id': "1410000000000",
                    'name': "datasetA",
                    'description': "datasetA description",
                    'type': "qa",
                    'item_count': 0,
                    'created_at' : "2023-12-04T16:01:52+09:00",
                    'updated_at' : "2023-12-04T16:01:52+09:00",
                }

        Raises:
            - BadRequest
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        if not name:
            error_message = '"name" is necessary'
            raise BadRequest(
                error=error_message,
                error_description=error_message,
                status_code=400
            )
        if not type:
            error_message = '"type" is necessary'
            raise BadRequest(
                error=error_message,
                error_description=error_message,
                status_code=400
            )
        if type not in ['qa', 'llm']:
            error_message = '"type" need to "qa" or "llm"'
            raise BadRequest(
                error=error_message,
                error_description=error_message,
                status_code=400
            )

        path = '/opsbee-llm/organizations/{}/datasets'.format(
            organization_id,
        )
        payload = {
            'name': name,
            'type': type,
        }
        if description is not None:
            payload['description'] = description
        else:
            payload['description'] = ''

        return self._connection.api_request(method='POST', path=path, json=payload)

    def update_dataset(
        self,
        organization_id: str,
        dataset_id: str,
        name: str,
        description: Optional[str] = None,
    ) -> dict:
        """update a dataset

        API reference: PATCH /opsbee-llm/organizations/<organization_id>/datasets/<dataset_id>

        Request Syntax:
            .. code-block:: python

                organization_id = "1410000000000"
                dataset_id = "1234567890123"
                name = "datasetA"
                description = "datasetA description"
                response = api_client.update_dataset(
                    organization_id, dataset_id, name, description)

        Params:
            - **organization_id** (str): organization identifier
            - **dataset_id** (str): dataset identifier
            - **name** (str): dataset name
            - **description** (str): **[optional]** dataset description

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    'id': "1234567890123",
                    'organization_id': "1410000000000",
                    'name': "datasetA",
                    'description': "datasetA description",
                    'type': "qa",
                    'item_count': 0,
                    'created_at' : "2023-12-04T16:01:52+09:00",
                    'updated_at' : "2023-12-04T16:01:52+09:00",
                }

        Raises:
            - BadRequest
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        if not name:
            error_message = '"name" is necessary'
            raise BadRequest(
                error=error_message,
                error_description=error_message,
                status_code=400
            )

        path = '/opsbee-llm/organizations/{}/datasets/{}'.format(
            organization_id,
            dataset_id,
        )
        payload = {
            'name': name,
        }
        if description is not None:
            payload['description'] = description
        else:
            payload['description'] = ''

        return self._connection.api_request(method='PATCH', path=path, json=payload)

    def delete_dataset(
        self,
        organization_id: str,
        dataset_id: str,
    ) -> dict:
        """delete a dataset

        API reference: DELETE /opsbee-llm/organizations/<organization_id>/datasets/<dataset_id>

        Request Syntax:
            .. code-block:: python

                organization_id = "1410000000000"
                dataset_id = "1234567890123"
                response = api_client.delete_dataset(
                    organization_id, dataset_id)

        Params:
            - **organization_id** (str): organization identifier
            - **dataset_id** (str): dataset identifier

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    'id': "1234567890123",
                    'organization_id': "1410000000000",
                    'name': "datasetA",
                    'description': "datasetA description",
                    'type': "qa",
                    'item_count': 0,
                    'created_at' : "2023-12-04T16:01:52+09:00",
                    'updated_at' : "2023-12-04T16:01:52+09:00",
                }

        Raises:
            - BadRequest
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        path = '/opsbee-llm/organizations/{}/datasets/{}'.format(
            organization_id,
            dataset_id,
        )
        return self._connection.api_request(method='DELETE', path=path)

    def get_dataset_items(
        self,
        organization_id: str,
        dataset_id: str,
        search_query: Optional[str] = None,
        offset: Optional[int] = 0,
        limit: Optional[int] = 1000,
    ) -> dict:
        """get dataset items

        API reference: GET /opsbee-llm/organizations/<organization_id>/datasets/<dataset_id>/items

        Request Syntax:
            .. code-block:: python

                organization_id = "1410000000000"
                dataset_id = "1234567890123"
                offset = 0
                limit = 1000
                response = api_client.get_datatset_items(
                    organization_id, dataset_id, offset, limit)

        Params:
            - **organization_id** (str): organization identifier
            - **dataset_id** (str): dataset identifier
            - **search_query** (str): **[optional]** search query
                - available search keys is below:
                    - `item_id:`
                    - `input_keys:`
                    - `input_values:`
                    - `output_keys:`
                    - `output_values:`
                    - `tag_values:`
                    - `metadata_keys:`
                    - `metadata_values:`
                    - `created_at:`
                    - `updated_at:`
                - AND and OR operators are available for each keys.
                - `*` operators are available for `input_keys:`, `input_values:`, `output_keys:`, `output_values:` keys.
                - `<=`, `<`, `>=`, `>` operators are available for `created_at`, `updated_at` keys.
                example:
                    search_query='input_values:"ABEJA*" AND created_at:>="2024-09-17T00:00:00" AND metadata_keys:metadata1 AND metadata_keys:metadata2'
            - **offset** (int): **[optional]** offset of datasets ( which starts from 0 )
            - **limit** (int): **[optional]** max number of datasets to be returned

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    'organization_id': '1410000000000'
                    'dataset_id': '1234567890123',
                    'items': [
                        {
                            'id': '3053595942757',
                            'organization_id': '1410000000000',
                            'dataset_id': '1234567890123',
                            'inputs': [
                                {'input_text': 'ABEJAについて教えて'},
                                ...
                            ],
                            'outputs': [
                                {'output_text': 'ABEJAは、スペイン語で「ミツバチ」の意味であり、植物の受粉を手伝い、世界の食料生産を支える存在として社名になっています。'},
                                ...
                            ],
                            tags: [
                                "OK1", "OK2", ...
                            ],
                            matadata: [
                                { metadata1: "value1" },
                                { metadata2: "value2" },
                                ...
                            ]
                            'created_at': '2023-12-15T16:50:33+09:00',
                            'updated_at': '2023-12-15T16:50:33+09:00'
                        },
                        ...
                    ],
                    'offset': 0,
                    'limit': 1000,
                    'total': 10,
                    'has_next': False,
                }

        Raises:
            - BadRequest
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        params = {}
        if offset is None:
            offset = 0
        if limit is None:
            limit = 1000
        params['offset'] = offset
        params['limit'] = limit

        if search_query:
            path = '/opsbee-llm/organizations/{}/datasets/{}/items?search_query={}&offset={}&limit={}'.format(
                organization_id,
                dataset_id,
                search_query,
                offset,
                limit,
            )
        else:
            path = '/opsbee-llm/organizations/{}/datasets/{}/items?offset={}&limit={}'.format(
                organization_id,
                dataset_id,
                offset,
                limit,
            )

        return self._connection.api_request(method='GET', path=path, params=params)

    def get_dataset_item(
        self,
        organization_id: str,
        dataset_id: str,
        item_id: str,
    ) -> dict:
        """get dataset item

        API reference: GET /opsbee-llm/organizations/<organization_id>/datasets/<dataset_id>/items/<item_id>

        Request Syntax:
            .. code-block:: python

                organization_id = "1410000000000"
                dataset_id = "1234567890123"
                item_id = "3053595942757"
                response = api_client.get_datatset_item(
                    organization_id, dataset_id, item_id)

        Params:
            - **organization_id** (str): organization identifier
            - **dataset_id** (str): dataset identifier
            - **item_id** (str): item identifier

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    'id': '3053595942757',
                    'organization_id': '1410000000000',
                    'dataset_id': '1234567890123',
                    'inputs': [
                        {'input_text': 'ABEJAについて教えて'},
                        ...
                    ],
                    'outputs': [
                        {'output_text': 'ABEJAは、スペイン語で「ミツバチ」の意味であり、植物の受粉を手伝い、世界の食料生産を支える存在として社名になっています。'},
                        ...
                    ],
                    tags: [
                        "OK1", "OK2", ...
                    ],
                    matadata: [
                        { metadata1: "value1" },
                        { metadata2: "value2" },
                        ...
                    ]
                    'created_at': '2023-12-04T16:01:52+09:00',
                    'updated_at': '2023-12-04T16:01:52+09:00'
                }

        Raises:
            - BadRequest
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        path = '/opsbee-llm/organizations/{}/datasets/{}/items/{}'.format(
            organization_id,
            dataset_id,
            item_id,
        )
        return self._connection.api_request(method='GET', path=path)

    def create_dataset_item(
        self,
        organization_id: str,
        dataset_id: str,
        inputs: list[dict],
        outputs: list[dict],
        tags: Optional[list] = None,
        metadata: Optional[List[Dict]] = None,
    ) -> dict:
        """create dataset item

        API reference: POST /opsbee-llm/organizations/<organization_id>/datasets/<dataset_id>/items

        Request Syntax:
            .. code-block:: python

                organization_id = "1410000000000"
                dataset_id = "1234567890123"
                inputs = [{"thread_name": "スレッドA"}, {"input_text": "ABEJAについて教えて"}]
                outputs = [{"thread_name": "スレッドA"}, {"output_text": "ABEJAは、スペイン語で「ミツバチ」の意味であり、植物の受粉を手伝い、世界の食料生産を支える存在として社名になっています。"}]
                tags = ["OK1", "OK2"]
                metadata = [{"metadata1": "value1"}, {"metadata2": "value2"}]
                response = api_client.create_datatset_item(
                    organization_id, dataset_id, inputs, outputs, tags, metadata)

        Params:
            - **organization_id** (str): organization identifier
            - **dataset_id** (str): dataset identifier
            - **item_id** (str): item identifier
            - **inputs** (list[dict]): list of key-value input data.
            - **outputs** (list[dict]): list of key-value output data
            - **tags** (list): **[optional]** list of tags
            - **metadata** (list[dict]): **[optional]** list of key-value metadata

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    'id': '3053595942757',
                    'organization_id': '1410000000000',
                    'dataset_id': '1234567890123',
                    'inputs': [
                        {"thread_name": "スレッドA"},
                        {'input_text': 'ABEJAについて教えて'},
                    ],
                    'outputs': [
                        {"thread_name": "スレッドA"},
                        {'output_text': 'ABEJAは、スペイン語で「ミツバチ」の意味であり、植物の受粉を手伝い、世界の食料生産を支える存在として社名になっています。'},
                    ],
                    tags: [
                        "OK1", "OK2"
                    ],
                    matadata: [
                        { metadata1: "value1" },
                        { metadata2: "value2" },
                    ]
                    'created_at': '2023-12-15T16:50:33+09:00',
                    'updated_at': '2023-12-15T16:50:33+09:00'
                }

        Raises:
            - BadRequest
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        if not inputs or len(inputs) == 0:
            error_message = '"inputs" is necessary'
            raise BadRequest(
                error=error_message,
                error_description=error_message,
                status_code=400
            )
        if not outputs or len(outputs) == 0:
            error_message = '"outputs" is necessary'
            raise BadRequest(
                error=error_message,
                error_description=error_message,
                status_code=400
            )

        if isinstance(inputs, list):
            for input in inputs:
                if not isinstance(input, dict):
                    error_message = '"inputs" is list of dict'
                    raise BadRequest(
                        error=error_message,
                        error_description=error_message,
                        status_code=400
                    )
        if isinstance(outputs, list):
            for output in outputs:
                if not isinstance(output, dict):
                    error_message = '"outputs" is list of dict'
                    raise BadRequest(
                        error=error_message,
                        error_description=error_message,
                        status_code=400
                    )

        path = '/opsbee-llm/organizations/{}/datasets/{}/items'.format(
            organization_id,
            dataset_id,
        )

        payload = {
            'inputs': inputs,
            'outputs': outputs,
        }
        if tags is None:
            payload['tags'] = []
        else:
            payload['tags'] = tags
        if metadata is None:
            payload['metadata'] = []
        else:
            payload['metadata'] = metadata

        return self._connection.api_request(method='POST', path=path, json=payload)

    def delete_dataset_item(
        self,
        organization_id: str,
        dataset_id: str,
        item_id: str,
    ) -> dict:
        """delete dataset item

        API reference: DELETE /opsbee-llm/organizations/<organization_id>/datasets/<dataset_id>/items/<item_id>

        Request Syntax:
            .. code-block:: python

                organization_id = "1410000000000"
                dataset_id = "1234567890123"
                item_id = "3053595942757"
                response = api_client.delete_datatset_item(
                    organization_id, dataset_id, item_id)

        Params:
            - **organization_id** (str): organization identifier
            - **dataset_id** (str): dataset identifier
            - **item_id** (str): item identifier

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    'id': '3053595942757',
                    'organization_id': '1410000000000',
                    'dataset_id': '1234567890123',
                    'inputs': [
                        {'input_text': 'ABEJAについて教えて'},
                        ...
                    ],
                    'outputs': [
                        {'output_text': 'ABEJAは、スペイン語で「ミツバチ」の意味であり、植物の受粉を手伝い、世界の食料生産を支える存在として社名になっています。'},
                        ...
                    ],
                    tags: [
                        "OK1", "OK2", ...
                    ],
                    matadata: [
                        { metadata1: "value1" },
                        { metadata2: "value2" },
                        ...
                    ]
                    'created_at': '2023-12-15T16:50:33+09:00',
                    'updated_at': '2023-12-15T16:50:33+09:00'
                }

        Raises:
            - BadRequest
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        path = '/opsbee-llm/organizations/{}/datasets/{}/items/{}'.format(
            organization_id,
            dataset_id,
            item_id,
        )
        return self._connection.api_request(method='DELETE', path=path)
