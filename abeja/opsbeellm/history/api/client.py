from __future__ import annotations
from typing import Optional, List, Dict

from abeja.common.api_client import BaseAPIClient
from abeja.exceptions import BadRequest


class APIClient(BaseAPIClient):
    """A Low-Level client for OpsBee LLM History API

    .. code-block:: python

       from abeja.opsbeellm.history import APIClient

       api_client = APIClient()
    """

    def get_threads(
        self,
        organization_id: str,
        deployment_id: str,
        offset: Optional[int] = 0,
        limit: Optional[int] = 1000,
    ) -> dict:
        """get threads

        API reference: GET /opsbee-llm/organizations/<organization_id>/deployments/<deployment_id>/threads

        Request Syntax:
            .. code-block:: python

                organization_id = "1410000000000"
                deployment_id = "1234567890123"
                offset = 0
                limit = 1000
                response = api_client.get_threads(
                    organization_id, deployment_id, offset, limit)

        Params:
            - **organization_id** (str): organization identifier
            - **deployment_id** (str): deployment identifier for OpsBee LLM
            - **offset** (int): **[optional]** offset of threads ( which starts from 0 )
            - **limit** (int): **[optional]** max number of threads to be returned

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    'organization_id': '1410000000000'
                    'deployment_id': '1234567890123',
                    'threads': [
                        {
                            'id': "1234567890124",
                            'organization_id': "1410000000000",
                            'deployment_id': "1234567890123",
                            'name': "thread A to B",
                            'description': "A さんと B さんのチャット",
                            'created_at' : 2023-12-04T16:01:52+09:00,
                            'updated_at' : 2023-12-04T16:01:52+09:00,
                        },
                        {
                            'id': "1234567890125",
                            'organization_id': "1410000000000",
                            'deployment_id': "1234567890123",
                            'name': "thread A to C",
                            'description': "A さんと C さんのチャット",
                            'created_at' : "2023-12-04T16:01:52+09:00",
                            'updated_at' : "2023-12-04T16:01:52+09:00",
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

        path = '/opsbee-llm/organizations/{}/deployments/{}/threads?offset={}&limit={}'.format(
            organization_id,
            deployment_id,
            offset,
            limit,
        )
        return self._connection.api_request(method='GET', path=path, params=params)

    def get_thread(
        self,
        organization_id: str,
        deployment_id: str,
        thread_id: str,
    ) -> dict:
        """get thread

        API reference: GET /opsbee-llm/organizations/<organization_id>/deployments/<deployment_id>/threads/<thread_id>

        Request Syntax:
            .. code-block:: python

                organization_id = "1410000000000"
                deployment_id = "1234567890123"
                thread_id = "1234567890125"
                response = api_client.get_thread(
                    organization_id, deployment_id, thread_id)

        Params:
            - **organization_id** (str): organization identifier
            - **deployment_id** (str): deployment identifier for OpsBee LLM
            - **thread_id** (str): thread identifier

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    'id': "1234567890125",
                    'organization_id': "1410000000000",
                    'deployment_id': "1234567890123",
                    'name': "thread A to B",
                    'description': "threadA description",
                    'created_at' : 2023-12-13T04:42:34.913644Z,
                    'updated_at' : 2023-12-13T04:42:34.913644Z,
                }

        Raises:
            - BadRequest
            - Unauthorized: Authentication failed
            - InternalServerError
        """

        path = '/opsbee-llm/organizations/{}/deployments/{}/threads/{}'.format(
            organization_id,
            deployment_id,
            thread_id,
        )
        return self._connection.api_request(method='GET', path=path)

    def create_thread(
        self,
        organization_id: str,
        deployment_id: str,
        name: str,
        description: Optional[str] = None,
    ) -> dict:
        """create a thread

        API reference: POST /opsbee-llm/organizations/<organization_id>/deployments/<deployment_id>/threads

        Request Syntax:
            .. code-block:: python

                organization_id = "1410000000000"
                deployment_id = "1234567890123"
                name = "thread A to B"
                description = "A さんと B さんのチャット"
                response = api_client.create_thread(
                    organization_id, deployment_id, name, description)

        Params:
            - **organization_id** (str): organization identifier
            - **deployment_id** (str): deployment identifier for OpsBee LLM
            - **name** (str): thread name
            - **description** (str): **[optional]** thread description

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    'id': "1234567890123",
                    'organization_id': "1410000000000",
                    'deployment_id': "1234567890123",
                    'name': "thread A to B",
                    'description': "A さんと B さんのチャット",
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

        path = '/opsbee-llm/organizations/{}/deployments/{}/threads'.format(
            organization_id,
            deployment_id,
        )

        payload = {
            'name': name,
        }
        if description is not None:
            payload['description'] = description
        else:
            payload['description'] = ''

        return self._connection.api_request(method='POST', path=path, json=payload)

    def update_thread(
        self,
        organization_id: str,
        deployment_id: str,
        thread_id: str,
        name: str,
        description: Optional[str] = None,
    ) -> dict:
        """update a thread

        API reference: PATCH /opsbee-llm/organizations/<organization_id>/deployments/<deployment_id>/threads/<thread_id>

        Request Syntax:
            .. code-block:: python

                organization_id = "1410000000000"
                deployment_id = "1234567890123"
                thread_id = "1234567890125"
                name = "thread A to B"
                description = "A さんと B さんのチャット"
                response = api_client.update_thread(
                    organization_id, deployment_id, thread_id, name, description)

        Params:
            - **organization_id** (str): organization identifier
            - **deployment_id** (str): deployment identifier for OpsBee LLM
            - **thread_id** (str): thread identifier
            - **name** (str): thread name
            - **description** (str): **[optional]** thread description

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    'id': "1234567890125",
                    'organization_id': "1410000000000",
                    'deployment_id': "1234567890123",
                    'name': "thread A to B",
                    'description': "A さんと B さんのチャット",
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

        path = '/opsbee-llm/organizations/{}/deployments/{}/threads/{}'.format(
            organization_id,
            deployment_id,
            thread_id
        )

        payload = {
            'name': name,
        }
        if description is not None:
            payload['description'] = description
        else:
            payload['description'] = ''

        return self._connection.api_request(method='PATCH', path=path, json=payload)

    def delete_thread(
        self,
        organization_id: str,
        deployment_id: str,
        thread_id: str,
    ) -> dict:
        """delete a thread

        API reference: DELETE /opsbee-llm/organizations/<organization_id>/deployments/<deployment_id>/threads/<thread_id>

        Request Syntax:
            .. code-block:: python

                organization_id = "1410000000000"
                deployment_id = "9968625354849"
                thread_id = "1234567890125"
                response = api_client.delete_thread(
                    organization_id, deployment_id, thread_id)

        Params:
            - **organization_id** (str): organization identifier
            - **deployment_id** (str): deployment identifier
            - **thread_id** (str): thread identifier

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    'message': 'thread 9968625354849 was deleted.
                }

        Raises:
            - BadRequest
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        path = '/opsbee-llm/organizations/{}/deployments/{}/threads/{}'.format(
            organization_id,
            deployment_id,
            thread_id
        )
        return self._connection.api_request(method='DELETE', path=path)

    def get_qa_histories(
        self,
        organization_id: str,
        deployment_id: str,
        search_query: Optional[str] = None,
        offset: Optional[int] = 0,
        limit: Optional[int] = 1000,
    ) -> dict:
        """get qa histories

        API reference: GET /opsbee-llm/organizations/<organization_id>/deployments/<deployment_id>/qa_histories

        Request Syntax:
            .. code-block:: python

                organization_id = "1410000000000"
                deployment_id = "1234567890123"
                offset = 0
                limit = 1000
                response = api_client.get_qa_histories(
                    organization_id, deployment_id, offset, limit)

        Params:
            - **organization_id** (str): organization identifier
            - **deployment_id** (str): deployment identifier for OpsBee LLM
            - **search_query** (str): **[optional]** search query
                - available search keys is below:
                    - `history_id:`
                    - `input_text:`
                    - `output_text:`
                    - `input_token_count:`
                    - `output_token_count:`
                    - `tag_id:`
                    - `tag_name:`
                    - `metadata_id:`
                    - `metadata_key:`
                    - `metadata_value:`
                    - `created_at:`
                    - `updated_at:`
                - AND and OR operators are available for each keys.
                - `*` operators are available for `input_text:`, `output_text:` keys.
                - `<=`, `<`, `>=`, `>` operators are available for `input_token_count:`, `output_token_count:`, `created_at`, `updated_at` keys.
                example:
                    search_query='input_text:"ABEJA*" AND input_token_count:>=10 AND metadata_key:metadata1 AND metadata_key:metadata2'
            - **offset** (int): **[optional]** offset of histories ( which starts from 0 )
            - **limit** (int): **[optional]** max number of histories to be returned

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    'organization_id': '1410000000000'
                    'deployment_id': '1234567890123',
                    'thread_id': '1234567890126',
                    'thread_name': 'QA用スレッド',
                    'histories': [
                        {
                            'id': "1234567890123",
                            'organization_id': "1410000000000",
                            'deployment_id': "1234567890123",
                            'thread_id': "1234567890126",
                            'thread_name': "QA用スレッド",
                            'input_text': "ABEJAについて教えて",
                            'output_text': "ABEJAは、スペイン語で「ミツバチ」の意味であり、植物の受粉を手伝い、世界の食料生産を支える存在として社名になっています。",
                            'input_token_count': 10,
                            'output_token_count': 10,
                            'tags': [
                                {
                                    'id': "1234567890127",
                                    'name': "OK",
                                    'description': "",
                                    'color': "green",
                                },
                                {
                                    'id': "1345667887931",
                                    'name': "NG",
                                    'description': "",
                                    'color': "red",
                                },
                                ...
                            ],
                            'metadata': [
                                {
                                    'id': "1234567890156",
                                    'key': "metadata1",
                                    'value': "dummy1",
                                },
                                {
                                    'id': "1345667871931",
                                    'key': "metadata2",
                                    'value': "dummy2",
                                },
                                ...
                            ],
                            'created_at' : "2023-12-04T16:01:52+09:00",
                            'updated_at' : "2023-12-04T16:01:52+09:00",
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

        # verify deployment type
        path = '/opsbee-llm/organizations/{}/deployments/{}'.format(
            organization_id,
            deployment_id,
        )
        resp_deployment = self._connection.api_request(method='GET', path=path)
        try:
            deployment_type = resp_deployment["type"]
        except Exception as e:
            raise BadRequest(
                error="Failed to get deployment type",
                error_description=f"Failed to get deployment type | {e}",
                status_code=400
            )

        if deployment_type != "qa":
            raise BadRequest(
                error="deployment type is not supported",
                error_description=f"The specified deployment '{deployment_id}' type is '{deployment_type}', but it not supported! Only 'qa' is supported.",
                status_code=400
            )

        # get qa histories
        if search_query:
            path = '/opsbee-llm/organizations/{}/deployments/{}/qa_histories?search_query={}&offset={}&limit={}'.format(
                organization_id,
                deployment_id,
                search_query,
                offset,
                limit,
            )
        else:
            path = '/opsbee-llm/organizations/{}/deployments/{}/qa_histories?offset={}&limit={}'.format(
                organization_id,
                deployment_id,
                offset,
                limit,
            )

        return self._connection.api_request(method='GET', path=path, params=params)

    def get_qa_history(
        self,
        organization_id: str,
        deployment_id: str,
        history_id: str,
    ) -> dict:
        """get qa histories

        API reference: GET /opsbee-llm/organizations/<organization_id>/deployments/<deployment_id>/qa_histories/<history_id>

        Request Syntax:
            .. code-block:: python

                organization_id = "1410000000000"
                deployment_id = "1234567890123"
                history_id = "1234567890125"
                response = api_client.get_qa_histories(
                    organization_id, deployment_id, history_id)

        Params:
            - **organization_id** (str): organization identifier
            - **deployment_id** (str): deployment identifier for OpsBee LLM
            - **history_id** (str): history identifier

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    'id': "1234567890123",
                    'organization_id': "1410000000000",
                    'deployment_id': "1234567890123",
                    'thread_id': "1234567890126",
                    'thread_name': "QA用スレッド",
                    'input_text': "ABEJAについて教えて",
                    'output_text': "ABEJAは、スペイン語で「ミツバチ」の意味であり、植物の受粉を手伝い、世界の食料生産を支える存在として社名になっています。",
                    'input_token_count': 10,
                    'output_token_count': 10,
                    'tags': [
                        {
                            'id': "1234567890127",
                            'name': "OK",
                            'description': "",
                            'color': "green",
                        },
                        {
                            'id': "1345667887931",
                            'name': "NG",
                            'description': "",
                            'color': "red",
                        },
                        ...
                    ],
                    'metadata': [
                        {
                            'id': "1234567890156",
                            'key': "metadata1",
                            'value': "dummy1",
                        },
                        {
                            'id': "1345667871931",
                            'key': "metadata2",
                            'value': "dummy2",
                        },
                        ...
                    ],
                    'created_at' : "2023-12-04T16:01:52+09:00",
                    'updated_at' : "2023-12-04T16:01:52+09:00",
                }

        Raises:
            - BadRequest
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        # verify deployment type
        path = '/opsbee-llm/organizations/{}/deployments/{}'.format(
            organization_id,
            deployment_id,
        )
        resp_deployment = self._connection.api_request(method='GET', path=path)
        try:
            deployment_type = resp_deployment["type"]
        except Exception as e:
            raise BadRequest(
                error="Failed to get deployment type",
                error_description=f"Failed to get deployment type | {e}",
                status_code=400
            )

        if deployment_type != "qa":
            raise BadRequest(
                error="deployment type is not supported",
                error_description=f"The specified deployment '{deployment_id}' type is '{deployment_type}', but it not supported! Only 'qa' is supported.",
                status_code=400
            )

        # get qa histories
        path = '/opsbee-llm/organizations/{}/deployments/{}/qa_histories/{}'.format(
            organization_id,
            deployment_id,
            history_id,
        )
        return self._connection.api_request(method='GET', path=path)

    def create_qa_history(
        self,
        organization_id: str,
        deployment_id: str,
        input_text: str,
        output_text: str,
        input_token_count: Optional[int] = 0,
        output_token_count: Optional[int] = 0,
        tag_ids: Optional[list] = None,
        metadata: Optional[List[Dict]] = None,
    ) -> dict:
        """create a qa history

        API reference: POST /opsbee-llm/organizations/<organization_id>/deployments/<deployment_id>/qa_histories

        Request Syntax:
            .. code-block:: python

                organization_id = "1410000000000"
                deployment_id = "1234567890123"
                input_text = "ABEJAについて教えて"
                output_text = "ABEJAは、スペイン語で「ミツバチ」の意味であり、植物の受粉を手伝い、世界の食料生産を支える存在として社名になっています。"
                tag_ids = ['1111111111111', '2222222222222']
                metadata = [{'metadata1': 'value1'}, {'metadata2': 'value2'}]
                response = api_client.create_qa_history(
                    organization_id, deployment_id, input_text, output_text, tag_ids, metadata)

        Params:
            - **organization_id** (str): organization identifier
            - **deployment_id** (str): deployment identifier for OpsBee LLM
            - **input_text** (str): input text to LLM
            - **output_text** (str): output text from LLM
            - **input_token_count** (str): token count of input text
            - **output_token_count** (str): token count of output text
            - **tag_ids** (list): **[optional]** list of tag identifiers
            - **metadata** (list[dict]): **[optional]** list of {key: value} metadata
                (key size limited under 65535 bytes. value size limited under 65535 bytes. number of keys limited under 20)

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    'id': "1234567890123",
                    'organization_id': "1410000000000",
                    'deployment_id': "1234567890123",
                    'thread_id': "1234567890126",
                    'thread_name': "QA用スレッド",
                    'input_text': "ABEJAについて教えて",
                    'output_text': "ABEJAは、スペイン語で「ミツバチ」の意味であり、植物の受粉を手伝い、世界の食料生産を支える存在として社名になっています。",
                    'input_token_count': 10,
                    'output_token_count': 10,
                    'tags': [
                        {
                            'id': "1234567890123",
                            'name': "OK",
                            'description': "",
                            'color': "green",
                        },
                        {
                            'id': "1345667887931",
                            'name': "NG",
                            'description': "",
                            'color': "red",
                        },
                        ...
                    ],
                    'metadata': [
                        {
                            'id': "1234567890123",
                            'key': "metadata1",
                            'value': "dummy1",
                        },
                        {
                            'id': "1345667871931",
                            'key': "metadata2",
                            'value': "dummy2",
                        },
                        ...
                    ],
                    'created_at' : "2023-12-04T16:01:52+09:00",
                    'updated_at' : "2023-12-04T16:01:52+09:00",
                }

        Raises:
            - BadRequest
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        if not input_text and not output_text:
            error_message = '"input_text" or "output_text" is necessary'
            raise BadRequest(
                error=error_message,
                error_description=error_message,
                status_code=400
            )

        # verify deployment type
        path = '/opsbee-llm/organizations/{}/deployments/{}'.format(
            organization_id,
            deployment_id,
        )
        resp_deployment = self._connection.api_request(method='GET', path=path)
        try:
            deployment_type = resp_deployment["type"]
        except Exception as e:
            raise BadRequest(
                error="Failed to get deployment type",
                error_description=f"Failed to get deployment type | {e}",
                status_code=400
            )

        if deployment_type != "qa":
            raise BadRequest(
                error="deployment type is not supported",
                error_description=f"The specified deployment '{deployment_id}' type is '{deployment_type}', but it not supported! Only 'qa' is supported.",
                status_code=400
            )

        # create history
        path = '/opsbee-llm/organizations/{}/deployments/{}/qa_histories'.format(
            organization_id,
            deployment_id,
        )

        payload = {
            'input_text': input_text,
            'output_text': output_text,
            'input_token_count': input_token_count,
            'output_token_count': output_token_count,
        }
        if tag_ids is None:
            payload['tag_ids'] = []
        else:
            payload['tag_ids'] = tag_ids

        if metadata is None:
            payload['metadata'] = []
        else:
            payload['metadata'] = metadata

        return self._connection.api_request(method='POST', path=path, json=payload)

    def update_qa_history(
        self,
        organization_id: str,
        deployment_id: str,
        history_id: str,
        input_text: Optional[str] = None,
        output_text: Optional[str] = None,
        input_token_count: Optional[int] = None,
        output_token_count: Optional[int] = None,
        tag_ids: Optional[list] = None,
    ) -> dict:
        """update a qa history

        API reference: PATCH /opsbee-llm/organizations/<organization_id>/deployments/<deployment_id>/qa_histories/<history_id>

        Request Syntax:
            .. code-block:: python

                organization_id = "1410000000000"
                deployment_id = "1234567890123"
                history_id = "1234567890125"
                input_text = "ABEJAについて教えて"
                output_text = "ABEJAは、スペイン語で「ミツバチ」の意味であり、植物の受粉を手伝い、世界の食料生産を支える存在として社名になっています。"
                response = api_client.update_qa_history(
                    organization_id, deployment_id, history_id, input_text, output_text)

        Params:
            - **organization_id** (str): organization identifier
            - **deployment_id** (str): deployment identifier for OpsBee LLM
            - **history_id** (str): history identifier
            - **input_text** (str): **[optional]** input text to LLM. if None is specified, the input_text does not updated.
            - **output_text** (str): **[optional]** output text from LLM. if None is specified, the output_text does not updated.
            - **input_token_count** (str): **[optional]** token count of input text. if None is specified, the input_token_count does not updated.
            - **output_token_count** (str): **[optional]** token count of output text. if None is specified, the output_token_count does not updated.
            - **tag_ids** (list): **[optional]** list of tag identifiers. if None is specified, the tag_ids does not updated.

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    'id': "1234567890123",
                    'organization_id': "1410000000000",
                    'deployment_id': "1234567890123",
                    'thread_id': "1234567890126",
                    'thread_name': "QA用スレッド",
                    'input_text': "ABEJAについて教えて",
                    'output_text': "ABEJAは、スペイン語で「ミツバチ」の意味であり、植物の受粉を手伝い、世界の食料生産を支える存在として社名になっています。",
                    'input_token_count': 10,
                    'output_token_count': 10,
                    'tags': [
                        {
                            'id': "1234567890123",
                            'name': "OK",
                            'description': "",
                            'color': "green",
                        },
                        {
                            'id': "1345667887931",
                            'name': "NG",
                            'description': "",
                            'color': "red",
                        },
                        ...
                    ],
                    'metadata': [
                        {
                            'id': "1234567890123",
                            'key': "metadata1",
                            'value': "dummy1",
                        },
                        {
                            'id': "1345667871931",
                            'key': "metadata2",
                            'value': "dummy2",
                        },
                        ...
                    ],
                    'created_at' : "2023-12-04T16:01:52+09:00",
                    'updated_at' : "2023-12-04T16:01:52+09:00",
                }

        Raises:
            - BadRequest
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        # verify deployment type
        path = '/opsbee-llm/organizations/{}/deployments/{}'.format(
            organization_id,
            deployment_id,
        )
        resp_deployment = self._connection.api_request(method='GET', path=path)
        try:
            deployment_type = resp_deployment["type"]
        except Exception as e:
            raise BadRequest(
                error="Failed to get deployment type",
                error_description=f"Failed to get deployment type | {e}",
                status_code=400
            )

        if deployment_type != "qa":
            raise BadRequest(
                error="deployment type is not supported",
                error_description=f"The specified deployment '{deployment_id}' type is '{deployment_type}', but it not supported! Only 'qa' is supported.",
                status_code=400
            )

        # get qa history
        path = '/opsbee-llm/organizations/{}/deployments/{}/qa_histories/{}'.format(
            organization_id,
            deployment_id,
            history_id,
        )
        resp_history = self._connection.api_request(method='GET', path=path)

        # update history
        path = '/opsbee-llm/organizations/{}/deployments/{}/qa_histories/{}'.format(
            organization_id,
            deployment_id,
            history_id,
        )

        if not input_text:
            input_text = resp_history["input_text"]
        if not output_text:
            output_text = resp_history["output_text"]
        if not input_token_count:
            input_token_count = resp_history["input_token_count"]
        if not output_token_count:
            output_token_count = resp_history["output_token_count"]
        if not tag_ids:
            tag_ids = []
            for tag in resp_history["tags"]:
                tag_ids.append(tag["id"])

        payload = {
            'input_text': input_text,
            'output_text': output_text,
            'input_token_count': input_token_count,
            'output_token_count': output_token_count,
        }
        if tag_ids is None:
            payload['tag_ids'] = []
        else:
            payload['tag_ids'] = tag_ids

        return self._connection.api_request(method='PATCH', path=path, json=payload)

    def delete_qa_history(
        self,
        organization_id: str,
        deployment_id: str,
        history_id: str,
    ) -> dict:
        """delete a qa history

        API reference: DELETE /opsbee-llm/organizations/<organization_id>/deployments/<deployment_id>/qa_histories/<history_id>

        Request Syntax:
            .. code-block:: python

                organization_id = "1410000000000"
                deployment_id = "1234567890123"
                history_id = "1234567890125"
                response = api_client.delete_qa_history(
                    organization_id, deployment_id, history_id)

        Params:
            - **organization_id** (str): organization identifier
            - **deployment_id** (str): deployment identifier for OpsBee LLM
            - **history_id** (str): history identifier

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    'id': "1234567890123",
                    'organization_id': "1410000000000",
                    'deployment_id': "1234567890123",
                    'thread_id': "1234567890126",
                    'thread_name': "QA用スレッド",
                    'input_text': "ABEJAについて教えて",
                    'output_text': "ABEJAは、スペイン語で「ミツバチ」の意味であり、植物の受粉を手伝い、世界の食料生産を支える存在として社名になっています。",
                    'input_token_count': 10,
                    'output_token_count': 10,
                    'tags': [
                        {
                            'id': "1234567890123",
                            'name': "OK",
                            'description': "",
                            'color': "green",
                        },
                        {
                            'id': "1345667887931",
                            'name': "NG",
                            'description': "",
                            'color': "red",
                        },
                        ...
                    ],
                    'metadata': [
                        {
                            'id': "1234567890123",
                            'key': "metadata1",
                            'value': "dummy1",
                        },
                        {
                            'id': "1345667871931",
                            'key': "metadata2",
                            'value': "dummy2",
                        },
                        ...
                    ],
                    'created_at' : "2023-12-04T16:01:52+09:00",
                    'updated_at' : "2023-12-04T16:01:52+09:00",
                }

        Raises:
            - BadRequest
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        # verify deployment type
        path = '/opsbee-llm/organizations/{}/deployments/{}'.format(
            organization_id,
            deployment_id,
        )
        resp_deployment = self._connection.api_request(method='GET', path=path)
        try:
            deployment_type = resp_deployment["type"]
        except Exception as e:
            raise BadRequest(
                error="Failed to get deployment type",
                error_description=f"Failed to get deployment type | {e}",
                status_code=400
            )

        if deployment_type != "qa":
            raise BadRequest(
                error="deployment type is not supported",
                error_description=f"The specified deployment '{deployment_id}' type is '{deployment_type}', but it not supported! Only 'qa' is supported.",
                status_code=400
            )

        # delete history
        path = '/opsbee-llm/organizations/{}/deployments/{}/qa_histories/{}'.format(
            organization_id,
            deployment_id,
            history_id,
        )
        return self._connection.api_request(method='DELETE', path=path)

    def get_chat_histories(
        self,
        organization_id: str,
        deployment_id: str,
        search_query: Optional[str] = None,
        offset: Optional[int] = 0,
        limit: Optional[int] = 1000,
    ) -> dict:
        """get chat histories

        API reference: GET /opsbee-llm/organizations/<organization_id>/deployments/<deployment_id>/histories

        Request Syntax:
            .. code-block:: python

                organization_id = "1410000000000"
                deployment_id = "1234567890123"
                offset = 0
                limit = 1000
                response = api_client.get_chat_histories(
                    organization_id, deployment_id, offset, limit)

        Params:
            - **organization_id** (str): organization identifier
            - **deployment_id** (str): deployment identifier for OpsBee LLM
            - **search_query** (str): **[optional]** search query
                - available search keys is below:
                    - `history_id:`
                    - `input_text:`
                    - `output_text:`
                    - `input_token_count:`
                    - `output_token_count:`
                    - `tag_id:`
                    - `tag_name:`
                    - `metadata_id:`
                    - `metadata_key:`
                    - `metadata_value:`
                    - `created_at:`
                    - `updated_at:`
                - AND and OR operators are available for each keys.
                - `*` operators are available for `input_text:`, `output_text:` keys.
                - `<=`, `<`, `>=`, `>` operators are available for `input_token_count:`, `output_token_count:`, `created_at`, `updated_at` keys.
                example:
                    search_query='input_text:"ABEJA*" AND input_token_count:>=10 AND metadata_key:metadata1 AND metadata_key:metadata2'
            - **offset** (int): **[optional]** offset of histories ( which starts from 0 )
            - **limit** (int): **[optional]** max number of histories to be returned

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    'organization_id': '1410000000000'
                    'deployment_id': '1234567890123',
                    'thread_id': '1234567890126',
                    'thread_name': 'thread name',
                    'histories': [
                        {
                            'id': "1234567890123",
                            'organization_id': "1410000000000",
                            'deployment_id': "1234567890123",
                            'thread_id': "1234567890126",
                            'thread_name': "thread name",
                            'input_text': "ABEJAについて教えて",
                            'output_text': "ABEJAは、スペイン語で「ミツバチ」の意味であり、植物の受粉を手伝い、世界の食料生産を支える存在として社名になっています。",
                            'input_token_count': 10,
                            'output_token_count': 10,
                            'tags': [
                                {
                                    'id': "1234567890127",
                                    'name': "OK",
                                    'description': "",
                                    'color': "green",
                                },
                                {
                                    'id': "1345667887931",
                                    'name': "NG",
                                    'description': "",
                                    'color': "red",
                                },
                                ...
                            ],
                            'metadata': [
                                {
                                    'id': "1234567890156",
                                    'key': "metadata1",
                                    'value': "dummy1",
                                },
                                {
                                    'id': "1345667871931",
                                    'key': "metadata2",
                                    'value': "dummy2",
                                },
                                ...
                            ],
                            'created_at' : "2023-12-04T16:01:52+09:00",
                            'updated_at' : "2023-12-04T16:01:52+09:00",
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

        # verify deployment type
        path = '/opsbee-llm/organizations/{}/deployments/{}'.format(
            organization_id,
            deployment_id,
        )
        resp_deployment = self._connection.api_request(method='GET', path=path)
        try:
            deployment_type = resp_deployment["type"]
        except Exception as e:
            raise BadRequest(
                error="Failed to get deployment type",
                error_description=f"Failed to get deployment type | {e}",
                status_code=400
            )

        if deployment_type != "chat":
            raise BadRequest(
                error="deployment type is not supported",
                error_description=f"The specified deployment '{deployment_id}' type is '{deployment_type}', but it not supported! Only 'chat' is supported.",
                status_code=400
            )

        # get chat histories
        if search_query:
            path = '/opsbee-llm/organizations/{}/deployments/{}/histories?search_query={}&offset={}&limit={}'.format(
                organization_id,
                deployment_id,
                search_query,
                offset,
                limit,
            )
        else:
            path = '/opsbee-llm/organizations/{}/deployments/{}/histories?offset={}&limit={}'.format(
                organization_id,
                deployment_id,
                offset,
                limit,
            )
        return self._connection.api_request(method='GET', path=path, params=params)

    def get_chat_history(
        self,
        organization_id: str,
        deployment_id: str,
        thread_id: str,
        history_id: str,
    ) -> dict:
        """get chat history

        API reference: GET /opsbee-llm/organizations/<organization_id>/deployments/<deployment_id>/threads/<thread_id>/histories/<history_id>

        Request Syntax:
            .. code-block:: python

                organization_id = "1410000000000"
                deployment_id = "1234567890123"
                thread_id = "1234567890125"
                history_id = "1234567890129"
                response = api_client.get_chat_history(
                    organization_id, deployment_id, thread_id, history_id)

        Params:
            - **organization_id** (str): organization identifier
            - **deployment_id** (str): deployment identifier for OpsBee LLM
            - **thread_id** (str): thread identifier
            - **history_id** (str): history identifier

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    'id': "1234567890123",
                    'organization_id': "1410000000000",
                    'deployment_id': "1234567890123",
                    'thread_id': "1234567890126",
                    'thread_name': "thread name",
                    'input_text': "ABEJAについて教えて",
                    'output_text': "ABEJAは、スペイン語で「ミツバチ」の意味であり、植物の受粉を手伝い、世界の食料生産を支える存在として社名になっています。",
                    'input_token_count': 10,
                    'output_token_count': 10,
                    'tags': [
                        {
                            'id': "1234567890127",
                            'name': "OK",
                            'description': "",
                            'color': "green",
                        },
                        {
                            'id': "1345667887931",
                            'name': "NG",
                            'description': "",
                            'color': "red",
                        },
                        ...
                    ],
                    'metadata': [
                        {
                            'id': "1234567890156",
                            'key': "metadata1",
                            'value': "dummy1",
                        },
                        {
                            'id': "1345667871931",
                            'key': "metadata2",
                            'value': "dummy2",
                        },
                        ...
                    ],
                    'created_at' : "2023-12-04T16:01:52+09:00",
                    'updated_at' : "2023-12-04T16:01:52+09:00",
                }

        Raises:
            - BadRequest
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        # verify deployment type
        path = '/opsbee-llm/organizations/{}/deployments/{}'.format(
            organization_id,
            deployment_id,
        )
        resp_deployment = self._connection.api_request(method='GET', path=path)
        try:
            deployment_type = resp_deployment["type"]
        except Exception as e:
            raise BadRequest(
                error="Failed to get deployment type",
                error_description=f"Failed to get deployment type | {e}",
                status_code=400
            )

        if deployment_type != "chat":
            raise BadRequest(
                error="deployment type is not supported",
                error_description=f"The specified deployment '{deployment_id}' type is '{deployment_type}', but it not supported! Only 'chat' is supported.",
                status_code=400
            )

        # get chat history
        path = '/opsbee-llm/organizations/{}/deployments/{}/threads/{}/histories/{}'.format(
            organization_id,
            deployment_id,
            thread_id,
            history_id,
        )
        return self._connection.api_request(method='GET', path=path)

    def create_chat_history(
        self,
        organization_id: str,
        deployment_id: str,
        thread_id: str,
        input_text: str,
        output_text: str,
        input_token_count: Optional[int] = 0,
        output_token_count: Optional[int] = 0,
        tag_ids: Optional[list] = None,
        metadata: Optional[List[Dict]] = None,
    ) -> dict:
        """create a chat history

        API reference: POST /opsbee-llm/organizations/<organization_id>/deployments/<deployment_id>/threads/<thread_id>/histories

        Request Syntax:
            .. code-block:: python

                organization_id = "1410000000000"
                deployment_id = "1234567890123"
                thread_id = "1234567890123"
                input_text = "ABEJAについて教えて"
                output_text = "ABEJAは、スペイン語で「ミツバチ」の意味であり、植物の受粉を手伝い、世界の食料生産を支える存在として社名になっています。"
                tag_ids = ['1111111111111', '2222222222222']
                metadata = [{'metadata1': 'value1'}, {'metadata2': 'value2'}]
                response = api_client.create_chat_history(
                    organization_id, deployment_id, thread_id, input_text, output_text, tag_ids, metadata)

        Params:
            - **organization_id** (str): organization identifier
            - **deployment_id** (str): deployment identifier for OpsBee LLM
            - **thread_id** (str): thread identifier
            - **input_text** (str): input text to LLM
            - **output_text** (str): output text from LLM
            - **input_token_count** (str): token count of input text
            - **output_token_count** (str): token count of output text
            - **tag_ids** (list): list of tag identifiers
            - **metadata** (list[dict]): list of {key: value} metadata
                (key size limited under 65535 bytes. value size limited under 65535 bytes. number of keys limited under 20)

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    'id': "1234567890123",
                    'organization_id': "1410000000000",
                    'deployment_id': "1234567890123",
                    'thread_id': "1234567890126",
                    'thread_name': "スレッドA",
                    'input_text': "ABEJAについて教えて",
                    'output_text': "ABEJAは、スペイン語で「ミツバチ」の意味であり、植物の受粉を手伝い、世界の食料生産を支える存在として社名になっています。",
                    'input_token_count': 10,
                    'output_token_count': 10,
                    'tags': [
                        {
                            'id': "1234567890123",
                            'name': "OK",
                            'description': "",
                            'color': "green",
                        },
                        {
                            'id': "1345667887931",
                            'name': "NG",
                            'description': "",
                            'color': "red",
                        },
                        ...
                    ],
                    'metadata': [
                        {
                            'id': "1234567890123",
                            'key': "metadata1",
                            'value': "dummy1",
                        },
                        {
                            'id': "1345667871931",
                            'key': "metadata2",
                            'value': "dummy2",
                        },
                        ...
                    ],
                    'created_at' : "2023-12-04T16:01:52+09:00",
                    'updated_at' : "2023-12-04T16:01:52+09:00",
                }

        Raises:
            - BadRequest
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        if not input_text and not output_text:
            error_message = '"input_text" or "output_text" is necessary'
            raise BadRequest(
                error=error_message,
                error_description=error_message,
                status_code=400
            )

        # verify deployment type
        path = '/opsbee-llm/organizations/{}/deployments/{}'.format(
            organization_id,
            deployment_id,
        )
        resp_deployment = self._connection.api_request(method='GET', path=path)
        try:
            deployment_type = resp_deployment["type"]
        except Exception as e:
            raise BadRequest(
                error="Failed to get deployment type",
                error_description=f"Failed to get deployment type | {e}",
                status_code=400
            )

        if deployment_type != "chat":
            raise BadRequest(
                error="deployment type is not supported",
                error_description=f"The specified deployment '{deployment_id}' type is '{deployment_type}', but it not supported! Only 'chat' is supported.",
                status_code=400
            )

        # create history
        path = '/opsbee-llm/organizations/{}/deployments/{}/threads/{}/histories'.format(
            organization_id,
            deployment_id,
            thread_id,
        )

        payload = {
            'input_text': input_text,
            'output_text': output_text,
            'input_token_count': input_token_count,
            'output_token_count': output_token_count,
        }
        if tag_ids is None:
            payload['tag_ids'] = []
        else:
            payload['tag_ids'] = tag_ids

        if metadata is None:
            payload['metadata'] = []
        else:
            payload['metadata'] = metadata

        return self._connection.api_request(method='POST', path=path, json=payload)

    def update_chat_history(
        self,
        organization_id: str,
        deployment_id: str,
        thread_id: str,
        history_id: str,
        input_text: Optional[str] = None,
        output_text: Optional[str] = None,
        input_token_count: Optional[int] = None,
        output_token_count: Optional[int] = None,
        tag_ids: Optional[list] = None,
    ) -> dict:
        """update a chat history

        API reference: PATCH /opsbee-llm/organizations/<organization_id>/deployments/<deployment_id>/threads/<thread_id>/histories/<history_id>

        Request Syntax:
            .. code-block:: python

                organization_id = "1410000000000"
                deployment_id = "1234567890123"
                thread_id = "1234567890124"
                history_id = "1234567890125"
                input_text = "ABEJAについて教えて"
                output_text = "ABEJAは、スペイン語で「ミツバチ」の意味であり、植物の受粉を手伝い、世界の食料生産を支える存在として社名になっています。"
                response = api_client.update_qa_history(
                    organization_id, deployment_id, thread_id, history_id, input_text, output_text)

        Params:
            - **organization_id** (str): organization identifier
            - **deployment_id** (str): deployment identifier for OpsBee LLM
            - **thread_id** (str): thread identifier
            - **history_id** (str): history identifier
            - **input_text** (str): **[optional]** input text to LLM. if None is specified, the input_text does not updated.
            - **output_text** (str): **[optional]** output text from LLM. if None is specified, the output_text does not updated.
            - **input_token_count** (str): **[optional]** token count of input text. if None is specified, the input_token_count does not updated.
            - **output_token_count** (str): **[optional]** token count of output text. if None is specified, the output_token_count does not updated.
            - **tag_ids** (list): **[optional]** list of tag identifiers. if None is specified, the tag_ids does not updated.

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    'id': "1234567890123",
                    'organization_id': "1410000000000",
                    'deployment_id': "1234567890123",
                    'thread_id': "1234567890126",
                    'thread_name': "チャット用スレッド",
                    'input_text': "ABEJAについて教えて",
                    'output_text': "ABEJAは、スペイン語で「ミツバチ」の意味であり、植物の受粉を手伝い、世界の食料生産を支える存在として社名になっています。",
                    'input_token_count': 10,
                    'output_token_count': 10,
                    'tags': [
                        {
                            'id': "1234567890123",
                            'name': "OK",
                            'description': "",
                            'color': "green",
                        },
                        {
                            'id': "1345667887931",
                            'name': "NG",
                            'description': "",
                            'color': "red",
                        },
                        ...
                    ],
                    'metadata': [
                        {
                            'id': "1234567890123",
                            'key': "metadata1",
                            'value': "dummy1",
                        },
                        {
                            'id': "1345667871931",
                            'key': "metadata2",
                            'value': "dummy2",
                        },
                        ...
                    ],
                    'created_at' : "2023-12-04T16:01:52+09:00",
                    'updated_at' : "2023-12-04T16:01:52+09:00",
                }

        Raises:
            - BadRequest
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        # verify deployment type
        path = '/opsbee-llm/organizations/{}/deployments/{}'.format(
            organization_id,
            deployment_id,
        )
        resp_deployment = self._connection.api_request(method='GET', path=path)
        try:
            deployment_type = resp_deployment["type"]
        except Exception as e:
            raise BadRequest(
                error="Failed to get deployment type",
                error_description=f"Failed to get deployment type | {e}",
                status_code=400
            )

        if deployment_type != "chat":
            raise BadRequest(
                error="deployment type is not supported",
                error_description=f"The specified deployment '{deployment_id}' type is '{deployment_type}', but it not supported! Only 'chat' is supported.",
                status_code=400
            )

        # get chat history
        path = '/opsbee-llm/organizations/{}/deployments/{}/threads/{}/histories/{}'.format(
            organization_id,
            deployment_id,
            thread_id,
            history_id,
        )
        resp_history = self._connection.api_request(method='GET', path=path)

        # update history
        path = '/opsbee-llm/organizations/{}/deployments/{}/threads/{}/histories/{}'.format(
            organization_id,
            deployment_id,
            thread_id,
            history_id,
        )

        if not input_text:
            input_text = resp_history["input_text"]
        if not output_text:
            output_text = resp_history["output_text"]
        if not input_token_count:
            input_token_count = resp_history["input_token_count"]
        if not output_token_count:
            output_token_count = resp_history["output_token_count"]
        if not tag_ids:
            tag_ids = []
            for tag in resp_history["tags"]:
                tag_ids.append(tag["id"])

        payload = {
            'input_text': input_text,
            'output_text': output_text,
            'input_token_count': input_token_count,
            'output_token_count': output_token_count,
        }
        if tag_ids is None:
            payload['tag_ids'] = []
        else:
            payload['tag_ids'] = tag_ids

        return self._connection.api_request(method='PATCH', path=path, json=payload)

    def delete_chat_history(
        self,
        organization_id: str,
        deployment_id: str,
        thread_id: str,
        history_id: str,
    ) -> dict:
        """delete a chat history

        API reference: DELETE /opsbee-llm/organizations/<organization_id>/deployments/<deployment_id>/threads/<thread_id>/histories/<history_id>

        Request Syntax:
            .. code-block:: python

                organization_id = "1410000000000"
                deployment_id = "1234567890123"
                thread_id = "1234567890124"
                history_id = "1234567890125"
                response = api_client.delete_chat_history(
                    organization_id, deployment_id, thread_id, history_id)

        Params:
            - **organization_id** (str): organization identifier
            - **deployment_id** (str): deployment identifier for OpsBee LLM
            - **thread_id** (str): thread identifier
            - **history_id** (str): history identifier

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    'id': "1234567890125",
                    'organization_id': "1410000000000",
                    'deployment_id': "1234567890123",
                    'thread_id': "1234567890124",
                    'thread_name': "チャット用スレッド",
                    'input_text': "ABEJAについて教えて",
                    'output_text': "ABEJAは、スペイン語で「ミツバチ」の意味であり、植物の受粉を手伝い、世界の食料生産を支える存在として社名になっています。",
                    'input_token_count': 10,
                    'output_token_count': 10,
                    'tags': [
                        {
                            'id': "1234567890123",
                            'name': "OK",
                            'description': "",
                            'color': "green",
                        },
                        {
                            'id': "1345667887931",
                            'name': "NG",
                            'description': "",
                            'color': "red",
                        },
                        ...
                    ],
                    'metadata': [
                        {
                            'id': "1234567890123",
                            'key': "metadata1",
                            'value': "dummy1",
                        },
                        {
                            'id': "1345667871931",
                            'key': "metadata2",
                            'value': "dummy2",
                        },
                        ...
                    ],
                    'created_at' : "2023-12-04T16:01:52+09:00",
                    'updated_at' : "2023-12-04T16:01:52+09:00",
                }

        Raises:
            - BadRequest
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        # verify deployment type
        path = '/opsbee-llm/organizations/{}/deployments/{}'.format(
            organization_id,
            deployment_id,
        )
        resp_deployment = self._connection.api_request(method='GET', path=path)
        try:
            deployment_type = resp_deployment["type"]
        except Exception as e:
            raise BadRequest(
                error="Failed to get deployment type",
                error_description=f"Failed to get deployment type | {e}",
                status_code=400
            )

        if deployment_type != "chat":
            raise BadRequest(
                error="deployment type is not supported",
                error_description=f"The specified deployment '{deployment_id}' type is '{deployment_type}', but it not supported! Only 'chat' is supported.",
                status_code=400
            )

        # delete history
        path = '/opsbee-llm/organizations/{}/deployments/{}/threads/{}/histories/{}'.format(
            organization_id,
            deployment_id,
            thread_id,
            history_id,
        )
        return self._connection.api_request(method='DELETE', path=path)

    def get_tags(
        self,
        organization_id: str,
        offset: Optional[int] = 0,
        limit: Optional[int] = 1000,
    ) -> dict:
        """get history tags

        API reference: GET /opsbee-llm/organizations/<organization_id>/tags

        Request Syntax:
            .. code-block:: python

                organization_id = "1410000000000"
                offset = 0
                limit = 1000
                response = api_client.get_tags(
                    organization_id, offset, limit)

        Params:
            - **organization_id** (str): organization identifier
            - **offset** (int): **[optional]** offset of tags ( which starts from 0 )
            - **limit** (int): **[optional]** max number of tags to be returned

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    'organization_id': '1410000000000'
                    'tags': [
                        {
                            'id': "1234567890125",
                            'name': "OK",
                            'description': "",
                            'color': "green",
                            'created_at' : "2023-12-04T16:01:52+09:00",
                            'updated_at' : "2023-12-04T16:01:52+09:00",
                        },
                        {
                            'id': "1345667887931",
                            'name': "NG",
                            'description': "",
                            'color': "red",
                            'created_at' : "2023-12-04T16:01:52+09:00",
                            'updated_at' : "2023-12-04T16:01:52+09:00",
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

        path = '/opsbee-llm/organizations/{}/tags?offset={}&limit={}'.format(
            organization_id,
            offset,
            limit,
        )
        return self._connection.api_request(method='GET', path=path, params=params)

    def get_tag(
        self,
        organization_id: str,
        tag_id: str,
    ) -> dict:
        """get tags

        API reference: GET /opsbee-llm/organizations/<organization_id>/tags/<tag_id>

        Request Syntax:
            .. code-block:: python

                organization_id = "1410000000000"
                tag_id = "1234567890125"
                response = api_client.get_tag(
                    organization_id, tag_id)

        Params:
            - **organization_id** (str): organization identifier
            - **tag_id** (str): tag identifier

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    'id': "1234567890125",
                    'name': "OK",
                    'description': "",
                    'color': "green",
                    'created_at' : "2023-12-04T16:01:52+09:00",
                    'updated_at' : "2023-12-04T16:01:52+09:00",
                },

        Raises:
            - BadRequest
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        path = '/opsbee-llm/organizations/{}/tags/{}'.format(
            organization_id,
            tag_id,
        )
        return self._connection.api_request(method='GET', path=path)

    def create_tag(
        self,
        organization_id: str,
        name: str,
        description: Optional[str] = None,
        color: Optional[str] = "grey",
    ) -> dict:
        """create a tag

        API reference: POST /opsbee-llm/organizations/<organization_id>/tags

        Request Syntax:
            .. code-block:: python

                organization_id = "1410000000000"
                name = "OK"
                description = "有益な出力文が出力されるときのタグです"
                color = "green"
                response = api_client.create_tag(
                    organization_id, name, description, color)

        Params:
            - **organization_id** (str): organization identifier
            - **name** (str): tag name
            - **description** (str): **[optional]** tag description
            - **color** (str): **[optional]** tag color
                available colors are "red", "orange", "yellow", "olive", "green", "teal", "blue", "violet", "purple", "pink", "brown", "grey", "black".
                default is "grey".

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    'id': "1234567890123",
                    'organization_id': "1410000000000",
                    'name': "OK",
                    'description': "有益な出力文が出力されるときのタグです",
                    'color': "green",
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
        if not description:
            description = ""

        available_colors = [
            "red", "orange", "yellow", "olive", "green", "teal", "blue", "violet", "purple", "pink", "brown", "grey", "black"
        ]
        if not color:
            color = "grey"
        if color not in available_colors:
            raise BadRequest(
                error='color is not supported',
                error_description=f'color "{color}" is not supported. available colors are {available_colors}',
                status_code=400
            )

        path = '/opsbee-llm/organizations/{}/tags'.format(
            organization_id,
        )

        payload = {
            'name': name,
            'description': description,
            'color': color,
        }
        return self._connection.api_request(method='POST', path=path, json=payload)

    def update_tag(
        self,
        organization_id: str,
        tag_id: str,
        name: str,
        description: Optional[str] = None,
        color: Optional[str] = "grey",
    ) -> dict:
        """update a tag

        API reference: PATCH /opsbee-llm/organizations/<organization_id>/tags/<tag_id>

        Request Syntax:
            .. code-block:: python

                organization_id = "1410000000000"
                tag_id = "1234567890123"
                name = "OK"
                description = "有益な出力文が出力されるときのタグです"
                color = "green"
                response = api_client.update_tag(
                    organization_id, tag_id, name, description, color)

        Params:
            - **organization_id** (str): organization identifier
            - **tag_id** (str): tag identifier
            - **name** (str): tag name
            - **description** (str): **[optional]** tag description.
            - **color** (str): **[optional]** tag color
                available colors are "red", "orange", "yellow", "olive", "green", "teal", "blue", "violet", "purple", "pink", "brown", "grey", "black".
                default is "grey".

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    'id': "1234567890123",
                    'organization_id': "1410000000000",
                    'name': "OK",
                    'description': "有益な出力文が出力されるときのタグです",
                    'color': "green",
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
        if not description:
            description = ""

        available_colors = [
            "red", "orange", "yellow", "olive", "green", "teal", "blue", "violet", "purple", "pink", "brown", "grey", "black"
        ]
        if not color:
            color = "grey"
        if color not in available_colors:
            raise BadRequest(
                error='color is not supported',
                error_description=f'color "{color}" is not supported. available colors are {available_colors}',
                status_code=400
            )

        path = '/opsbee-llm/organizations/{}/tags/{}'.format(
            organization_id,
            tag_id,
        )

        payload = {
            'name': name,
            'description': description,
            'color': color,
        }
        return self._connection.api_request(method='PATCH', path=path, json=payload)

    def delete_tag(
        self,
        organization_id: str,
        tag_id: str,
    ) -> dict:
        """delete a tag

        API reference: DELETE /opsbee-llm/organizations/<organization_id>/tags/<tag_id>

        Request Syntax:
            .. code-block:: python

                organization_id = "1410000000000"
                tag_id = "9968625354849"
                response = api_client.delete_tags(
                    organization_id, deployment_id, tag_id)

        Params:
            - **organization_id** (str): organization identifier
            - **tag_id** (str): tag identifier

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    'message': 'tag 9968625354849 was deleted.
                }

        Raises:
            - BadRequest
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        path = '/opsbee-llm/organizations/{}/tags/{}'.format(
            organization_id,
            tag_id,
        )
        return self._connection.api_request(method='DELETE', path=path)

    def create_qa_history_metadata(
        self,
        organization_id: str,
        deployment_id: str,
        history_id: str,
        key: str,
        value: str,
    ) -> dict:
        """create a chat history metadata

        API reference: POST /opsbee-llm/organizations/<organization_id>/deployments/<deployment_id>/qa_histories/<history_id>/metadata

        Request Syntax:
            .. code-block:: python

                organization_id = "1410000000000"
                deployment_id = "1234567890123"
                history_id = "1234567890125"
                key = "metadata1"
                value = "dummy1"
                response = api_client.create_qa_history_metadata(
                    organization_id, deployment_id, history_id, key, value)

        Params:
            - **organization_id** (str): organization identifier
            - **deployment_id** (str): deployment identifier for OpsBee LLM
            - **history_id** (str): history identifier
            - **key** (str): key name of key-value metadata (limited to 65535 bytes and limited to number of keys is under 20)
            - **value** (str): value of key-value metadata (limited to 65535 bytes)

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    'id': "1234567890130",
                    'organization_id': "1410000000000",
                    'deployment_id': "1234567890123",
                    'history_id': "1234567890125",
                    'key': "metadata1",
                    'value': "dummy1",
                    'created_at' : "2023-12-04T16:01:52+09:00",
                    'updated_at' : "2023-12-04T16:01:52+09:00",
                }

        Raises:
            - BadRequest
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        if not key:
            error_message = '"key" is necessary'
            raise BadRequest(
                error=error_message,
                error_description=error_message,
                status_code=400
            )
        if not value:
            error_message = '"value" is necessary'
            raise BadRequest(
                error=error_message,
                error_description=error_message,
                status_code=400
            )

        # verify deployment type
        path = '/opsbee-llm/organizations/{}/deployments/{}'.format(
            organization_id,
            deployment_id,
        )
        resp_deployment = self._connection.api_request(method='GET', path=path)
        try:
            deployment_type = resp_deployment["type"]
        except Exception as e:
            raise BadRequest(
                error="Failed to get deployment type",
                error_description=f"Failed to get deployment type | {e}",
                status_code=400
            )

        if deployment_type != "qa":
            raise BadRequest(
                error="deployment type is not supported",
                error_description=f"The specified deployment '{deployment_id}' type is '{deployment_type}', but it not supported! Only 'qa' is supported.",
                status_code=400
            )

        # create metadata
        path = '/opsbee-llm/organizations/{}/deployments/{}/qa_histories/{}/metadata'.format(
            organization_id,
            deployment_id,
            history_id,
        )

        payload = {
            'key': key,
            'value': value,
        }
        return self._connection.api_request(method='POST', path=path, json=payload)

    def update_qa_history_metadata(
        self,
        organization_id: str,
        deployment_id: str,
        history_id: str,
        metadata_id: str,
        key: str,
        value: str,
    ) -> dict:
        """update a qa history metadata

        API reference: PATCH /opsbee-llm/organizations/<organization_id>/deployments/<deployment_id>/qa_histories/<history_id>/metadata/<metadata_id>

        Request Syntax:
            .. code-block:: python

                organization_id = "1410000000000"
                deployment_id = "1234567890123"
                history_id = "1234567890125"
                metadata_id = "1234567890130"
                key = "metadata1"
                value = "dummy1"
                response = api_client.update_qa_history_metadata(
                    organization_id, deployment_id, thread_id, history_id, metadata_id, key, value)

        Params:
            - **organization_id** (str): organization identifier
            - **deployment_id** (str): deployment identifier for OpsBee LLM
            - **history_id** (str): history identifier
            - **metadata_id** (str): metadata identifier
            - **key** (str): key name of key-value metadata (limited to 65535 bytes and limited to number of keys is under 20)
            - **value** (str): value of key-value metadata (limited to 65535 bytes)

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    'id': "1234567890130",
                    'organization_id': "1410000000000",
                    'deployment_id': "1234567890123",
                    'history_id': "1234567890125",
                    'key': "metadata1",
                    'value': "dummy1",
                    'created_at' : "2023-12-04T16:01:52+09:00",
                    'updated_at' : "2023-12-04T16:01:52+09:00",
                }

        Raises:
            - BadRequest
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        if not key:
            error_message = '"key" is necessary'
            raise BadRequest(
                error=error_message,
                error_description=error_message,
                status_code=400
            )
        if not value:
            error_message = '"value" is necessary'
            raise BadRequest(
                error=error_message,
                error_description=error_message,
                status_code=400
            )

        # verify deployment type
        path = '/opsbee-llm/organizations/{}/deployments/{}'.format(
            organization_id,
            deployment_id,
        )
        resp_deployment = self._connection.api_request(method='GET', path=path)
        try:
            deployment_type = resp_deployment["type"]
        except Exception as e:
            raise BadRequest(
                error="Failed to get deployment type",
                error_description=f"Failed to get deployment type | {e}",
                status_code=400
            )

        if deployment_type != "qa":
            raise BadRequest(
                error="deployment type is not supported",
                error_description=f"The specified deployment '{deployment_id}' type is '{deployment_type}', but it not supported! Only 'qa' is supported.",
                status_code=400
            )

        # update metadata
        path = '/opsbee-llm/organizations/{}/deployments/{}/qa_histories/{}/metadata/{}'.format(
            organization_id,
            deployment_id,
            history_id,
            metadata_id,
        )

        payload = {
            'key': key,
            'value': value,
        }
        return self._connection.api_request(method='PATCH', path=path, json=payload)

    def delete_qa_history_metadata(
        self,
        organization_id: str,
        deployment_id: str,
        history_id: str,
        metadata_id: str,
    ) -> dict:
        """delete a qa history metadata

        API reference: DELETE /opsbee-llm/organizations/<organization_id>/deployments/<deployment_id>/qa_histories/<history_id>/metadata/<metadata_id>

        Request Syntax:
            .. code-block:: python

                organization_id = "1410000000000"
                deployment_id = "1234567890123"
                history_id = "1234567890125"
                metadata_id = "1234567890130"
                response = api_client.delete_qa_history_metadata(
                    organization_id, deployment_id, history_id, metadata_id)

        Params:
            - **organization_id** (str): organization identifier
            - **deployment_id** (str): deployment identifier for OpsBee LLM
            - **history_id** (str): history identifier
            - **metadata_id** (str): metadata identifier

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    'message': 'metadata 1234567890130 was deleted.'
                }

        Raises:
            - BadRequest
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        # verify deployment type
        path = '/opsbee-llm/organizations/{}/deployments/{}'.format(
            organization_id,
            deployment_id,
        )
        resp_deployment = self._connection.api_request(method='GET', path=path)
        try:
            deployment_type = resp_deployment["type"]
        except Exception as e:
            raise BadRequest(
                error="Failed to get deployment type",
                error_description=f"Failed to get deployment type | {e}",
                status_code=400
            )

        if deployment_type != "qa":
            raise BadRequest(
                error="deployment type is not supported",
                error_description=f"The specified deployment '{deployment_id}' type is '{deployment_type}', but it not supported! Only 'qa' is supported.",
                status_code=400
            )

        # delete metadata
        path = '/opsbee-llm/organizations/{}/deployments/{}/qa_histories/{}/metadata/{}'.format(
            organization_id,
            deployment_id,
            history_id,
            metadata_id,
        )
        return self._connection.api_request(method='DELETE', path=path)

    def create_chat_history_metadata(
        self,
        organization_id: str,
        deployment_id: str,
        thread_id: str,
        history_id: str,
        key: str,
        value: str,
    ) -> dict:
        """create a chat history metadata

        API reference: POST /opsbee-llm/organizations/<organization_id>/deployments/<deployment_id>/threads/<thread_id>/histories/<history_id>/metadata

        Request Syntax:
            .. code-block:: python

                organization_id = "1410000000000"
                deployment_id = "1234567890123"
                thread_id = "1234567890124"
                history_id = "1234567890125"
                key = "metadata1"
                value = "dummy1"
                response = api_client.create_chat_history_metadata(
                    organization_id, deployment_id, thread_id, history_id, key, value)

        Params:
            - **organization_id** (str): organization identifier
            - **deployment_id** (str): deployment identifier for OpsBee LLM
            - **thread_id** (str): thread identifier
            - **history_id** (str): history identifier
            - **key** (str): key name of key-value metadata (limited to 65535 bytes and limited to number of keys is under 20)
            - **value** (str): value of key-value metadata (limited to 65535 bytes)

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    'id': "1234567890130",
                    'organization_id': "1410000000000",
                    'deployment_id': "1234567890123",
                    'history_id': "1234567890125",
                    'key': "metadata1",
                    'value': "dummy1",
                    'created_at' : "2023-12-04T16:01:52+09:00",
                    'updated_at' : "2023-12-04T16:01:52+09:00",
                }

        Raises:
            - BadRequest
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        if not key:
            error_message = '"key" is necessary'
            raise BadRequest(
                error=error_message,
                error_description=error_message,
                status_code=400
            )
        if not value:
            error_message = '"value" is necessary'
            raise BadRequest(
                error=error_message,
                error_description=error_message,
                status_code=400
            )

        # verify deployment type
        path = '/opsbee-llm/organizations/{}/deployments/{}'.format(
            organization_id,
            deployment_id,
        )
        resp_deployment = self._connection.api_request(method='GET', path=path)
        try:
            deployment_type = resp_deployment["type"]
        except Exception as e:
            raise BadRequest(
                error="Failed to get deployment type",
                error_description=f"Failed to get deployment type | {e}",
                status_code=400
            )

        if deployment_type != "chat":
            raise BadRequest(
                error="deployment type is not supported",
                error_description=f"The specified deployment '{deployment_id}' type is '{deployment_type}', but it not supported! Only 'chat' is supported.",
                status_code=400
            )

        # create metadata
        path = '/opsbee-llm/organizations/{}/deployments/{}/threads/{}/histories/{}/metadata'.format(
            organization_id,
            deployment_id,
            thread_id,
            history_id,
        )

        payload = {
            'key': key,
            'value': value,
        }
        return self._connection.api_request(method='POST', path=path, json=payload)

    def update_chat_history_metadata(
        self,
        organization_id: str,
        deployment_id: str,
        thread_id: str,
        history_id: str,
        metadata_id: str,
        key: str,
        value: str,
    ) -> dict:
        """update a chat history metadata

        API reference: PATCH /opsbee-llm/organizations/<organization_id>/deployments/<deployment_id>/threads/<thread_id>
            /histories/<history_id>/metadata/<metadata_id>

        Request Syntax:
            .. code-block:: python

                organization_id = "1410000000000"
                deployment_id = "1234567890123"
                thread_id = "1234567890124"
                history_id = "1234567890125"
                metadata_id = "1234567890130"
                key = "metadata1"
                value = "dummy1"
                response = api_client.update_chat_history_metadata(
                    organization_id, deployment_id, thread_id, history_id, metadata_id, key, value)

        Params:
            - **organization_id** (str): organization identifier
            - **deployment_id** (str): deployment identifier for OpsBee LLM
            - **thread_id** (str): thread identifier
            - **history_id** (str): history identifier
            - **metadata_id** (str): metadata identifier
            - **key** (str): key name of key-value metadata (limited to 65535 bytes and limited to number of keys is under 20)
            - **value** (str): value of key-value metadata (limited to 65535 bytes)

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    'id': "1234567890130",
                    'organization_id': "1410000000000",
                    'deployment_id': "1234567890123",
                    'history_id': "1234567890125",
                    'key': "metadata1",
                    'value': "dummy1",
                    'created_at' : "2023-12-04T16:01:52+09:00",
                    'updated_at' : "2023-12-04T16:01:52+09:00",
                }

        Raises:
            - BadRequest
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        if not key:
            error_message = '"key" is necessary'
            raise BadRequest(
                error=error_message,
                error_description=error_message,
                status_code=400
            )
        if not value:
            error_message = '"value" is necessary'
            raise BadRequest(
                error=error_message,
                error_description=error_message,
                status_code=400
            )

        # verify deployment type
        path = '/opsbee-llm/organizations/{}/deployments/{}'.format(
            organization_id,
            deployment_id,
        )
        resp_deployment = self._connection.api_request(method='GET', path=path)
        try:
            deployment_type = resp_deployment["type"]
        except Exception as e:
            raise BadRequest(
                error="Failed to get deployment type",
                error_description=f"Failed to get deployment type | {e}",
                status_code=400
            )

        if deployment_type != "chat":
            raise BadRequest(
                error="deployment type is not supported",
                error_description=f"The specified deployment '{deployment_id}' type is '{deployment_type}', but it not supported! Only 'chat' is supported.",
                status_code=400
            )

        # update metadata
        path = '/opsbee-llm/organizations/{}/deployments/{}/threads/{}/histories/{}/metadata/{}'.format(
            organization_id,
            deployment_id,
            thread_id,
            history_id,
            metadata_id,
        )

        payload = {
            'key': key,
            'value': value,
        }
        return self._connection.api_request(method='PATCH', path=path, json=payload)

    def delete_chat_history_metadata(
        self,
        organization_id: str,
        deployment_id: str,
        thread_id: str,
        history_id: str,
        metadata_id: str,
    ) -> dict:
        """delete a chat history metadata

        API reference: DELETE /opsbee-llm/organizations/<organization_id>/deployments/<deployment_id>/threads/<thread_id>
            /histories/<history_id>/metadata/<metadata_id>

        Request Syntax:
            .. code-block:: python

                organization_id = "1410000000000"
                deployment_id = "1234567890123"
                thread_id = "1234567890124"
                history_id = "1234567890125"
                metadata_id = "1234567890130"
                response = api_client.delete_chat_history_metadata(
                    organization_id, deployment_id, thread_id, history_id, metadata_id)

        Params:
            - **organization_id** (str): organization identifier
            - **deployment_id** (str): deployment identifier for OpsBee LLM
            - **thread_id** (str): thread identifier
            - **history_id** (str): history identifier
            - **metadata_id** (str): metadata identifier

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    'message': 'metadata 1234567890130 was deleted.'
                }

        Raises:
            - BadRequest
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        # verify deployment type
        path = '/opsbee-llm/organizations/{}/deployments/{}'.format(
            organization_id,
            deployment_id,
        )
        resp_deployment = self._connection.api_request(method='GET', path=path)
        try:
            deployment_type = resp_deployment["type"]
        except Exception as e:
            raise BadRequest(
                error="Failed to get deployment type",
                error_description=f"Failed to get deployment type | {e}",
                status_code=400
            )

        if deployment_type != "chat":
            raise BadRequest(
                error="deployment type is not supported",
                error_description=f"The specified deployment '{deployment_id}' type is '{deployment_type}', but it not supported! Only 'chat' is supported.",
                status_code=400
            )

        # delete metadata
        path = '/opsbee-llm/organizations/{}/deployments/{}/threads/{}/histories/{}/metadata/{}'.format(
            organization_id,
            deployment_id,
            thread_id,
            history_id,
            metadata_id,
        )
        return self._connection.api_request(method='DELETE', path=path)
