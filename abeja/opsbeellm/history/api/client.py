from typing import Optional

from abeja.opsbeellm.common.api_client import OpsBeeLLMBaseAPIClient
from abeja.exceptions import BadRequest


class APIClient(OpsBeeLLMBaseAPIClient):
    """A Low-Level client for OpsBee LLM History API

    .. code-block:: python

       from abeja.opsbeellm.history import APIClient

       api_client = APIClient()
    """

    def get_threads(
        self,
        account_id: str,
        organization_id: str,
        deployment_id: str,
        offset: Optional[int] = 0,
        limit: Optional[int] = 1000,
    ) -> dict:
        """get threads

        API reference: GET /accounts/<account_id>/organizations/<organization_id>/deployments/<deployment_id>/threads

        Request Syntax:
            .. code-block:: python

                account_id = "1122334455660"
                organization_id = "1410000000000"
                deployment_id = "1234567890123"
                offset = 0
                limit = 1000
                response = api_client.get_threads(
                    account_id, organization_id, deployment_id, offset, limit)

        Params:
            - **account_id** (str): account identifier
            - **organization_id** (str): organization identifier
            - **deployment_id** (str): deployment identifier for OpsBee LLM
            - **offset** (int): **[optional]** offset of threads ( which starts from 0 )
            - **limit** (int): **[optional]** max number of threads to be returned

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: python
                {
                    'account_id': '1122334455660',
                    'organization_id': '1410000000000'
                    'deployment_id': '1234567890123',
                    'threads': [
                        {
                            'id': "1234567890124",
                            'account_id': "1122334455660",
                            'organization_id': "1410000000000",
                            'deployment_id': "1234567890123",
                            'name': "threadA name",
                            'description': "threadA description",
                            'created_at' : 2023-12-13T04:42:34.913644Z,
                            'updated_at' : 2023-12-13T04:42:34.913644Z,
                        },
                        {
                            'id': "1234567890125",
                            'account_id': "1122334455660",
                            'organization_id': "1410000000000",
                            'deployment_id': "1234567890123",
                            'name': "threadB name",
                            'description': "threadB description",
                            'created_at' : "2023-12-13T04:42:34.913644Z",
                            'updated_at' : "2023-12-13T04:42:34.913644Z",
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

        path = '/accounts/{}/organizations/{}/deployments/{}/threads?offset={}&limit={}'.format(
            account_id,
            organization_id,
            deployment_id,
            offset,
            limit,
        )
        return self._connection.api_request(method='GET', path=path, params=params)

    def get_thread(
        self,
        account_id: str,
        organization_id: str,
        deployment_id: str,
        thread_id: str,
    ) -> dict:
        """get thread

        API reference: GET /accounts/<account_id>/organizations/<organization_id>/deployments/<deployment_id>/threads/<thread_id>

        Request Syntax:
            .. code-block:: python

                account_id = "1122334455660"
                organization_id = "1410000000000"
                deployment_id = "1234567890123"
                thread_id = "1234567890125"
                response = api_client.get_thread(
                    account_id, organization_id, deployment_id, thread_id)

        Params:
            - **account_id** (str): account identifier
            - **organization_id** (str): organization identifier
            - **deployment_id** (str): deployment identifier for OpsBee LLM
            - **thread_id** (str): thread identifier

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: python
                {
                    'id': "1234567890125",
                    'account_id': "1122334455660",
                    'organization_id': "1410000000000",
                    'deployment_id': "1234567890123",
                    'name': "threadA name",
                    'description': "threadA description",
                    'created_at' : 2023-12-13T04:42:34.913644Z,
                    'updated_at' : 2023-12-13T04:42:34.913644Z,
                }

        Raises:
            - BadRequest
            - Unauthorized: Authentication failed
            - InternalServerError
        """

        path = '/accounts/{}/organizations/{}/deployments/{}/threads/{}'.format(
            account_id,
            organization_id,
            deployment_id,
            thread_id,
        )
        return self._connection.api_request(method='GET', path=path)

    def create_thread(
        self,
        account_id: str,
        organization_id: str,
        deployment_id: str,
        name: str,
        description: Optional[str] = None,
    ) -> dict:
        """create a thread

        API reference: POST /accounts/<account_id>/organizations/<organization_id>/deployments/<deployment_id>/threads/

        Request Syntax:
            .. code-block:: python

                account_id = "1122334455660"
                organization_id = "1410000000000"
                deployment_id = "1234567890123"
                name = "thread name"
                description = "thread description"
                response = api_client.create_thread(
                    account_id, organization_id, deployment_id, name, description)

        Params:
            - **account_id** (str): account identifier
            - **organization_id** (str): organization identifier
            - **deployment_id** (str): deployment identifier for OpsBee LLM
            - **name** (str): thread name
            - **description** (str): **[optional]** thread description

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: python
                {
                    'id': "1234567890123",
                    'account_id': "1122334455660",
                    'organization_id': "1410000000000",
                    'deployment_id': "1234567890123",
                    'name': "thread name",
                    'description': "thread description",
                    'created_at' : "2023-12-13T04:42:34.913644Z",
                    'updated_at' : "2023-12-13T04:42:34.913644Z",
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

        path = '/accounts/{}/organizations/{}/deployments/{}/threads'.format(
            account_id,
            organization_id,
            deployment_id,
        )

        payload = {
            'name': name,
        }
        if description is not None:
            payload['description'] = description

        return self._connection.api_request(method='POST', path=path, json=payload)

    def update_thread(
        self,
        account_id: str,
        organization_id: str,
        deployment_id: str,
        thread_id: str,
        name: str,
        description: Optional[str] = None,
    ) -> dict:
        """update a thread

        API reference: PATCH /accounts/<account_id>/organizations/<organization_id>/deployments/<deployment_id>/threads/<thread_id>

        Request Syntax:
            .. code-block:: python

                account_id = "1122334455660"
                organization_id = "1410000000000"
                deployment_id = "1234567890123"
                thread_id = "1234567890125"
                name = "thread name"
                description = "thread description"
                response = api_client.update_thread(
                    account_id, organization_id, deployment_id, thread_id, name, description)

        Params:
            - **account_id** (str): account identifier
            - **organization_id** (str): organization identifier
            - **deployment_id** (str): deployment identifier for OpsBee LLM
            - **thread_id** (str): thread identifier
            - **name** (str): thread name
            - **description** (str): **[optional]** thread description

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: python
                {
                    'id': "1234567890125",
                    'account_id': "1122334455660",
                    'organization_id': "1410000000000",
                    'deployment_id': "1234567890123",
                    'name': "thread name",
                    'description': "thread description",
                    'created_at' : "2023-12-13T04:42:34.913644Z",
                    'updated_at' : "2023-12-15T04:42:34.913644Z",
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

        path = '/accounts/{}/organizations/{}/deployments/{}/threads/{}'.format(
            account_id,
            organization_id,
            deployment_id,
            thread_id
        )

        payload = {
            'name': name,
        }
        if description is not None:
            payload['description'] = description

        return self._connection.api_request(method='PATCH', path=path, json=payload)

    def delete_thread(
        self,
        account_id: str,
        organization_id: str,
        deployment_id: str,
        thread_id: str,
    ) -> dict:
        """delete a thread

        API reference: DELETE /accounts/<account_id>/organizations/<organization_id>/deployments/<deployment_id>/threads/<thread_id>

        Request Syntax:
            .. code-block:: python

                account_id = "1122334455660"
                organization_id = "1410000000000"
                deployment_id = "9968625354849"
                thread_id = "1234567890125"
                response = api_client.delete_thread(
                    account_id, organization_id, deployment_id, thread_id)

        Params:
            - **account_id** (str): account identifier
            - **organization_id** (str): organization identifier
            - **deployment_id** (str): deployment identifier
            - **thread_id** (str): thread identifier

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: python
                {
                    'message': f'thread 9968625354849 was deleted.
                }

        Raises:
            - BadRequest
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        path = '/accounts/{}/organizations/{}/deployments/{}/threads/{}'.format(
            account_id,
            organization_id,
            deployment_id,
            thread_id
        )
        return self._connection.api_request(method='DELETE', path=path)

    def get_qa_histories(
        self,
        account_id: str,
        organization_id: str,
        deployment_id: str,
        offset: Optional[int] = 0,
        limit: Optional[int] = 1000,
    ) -> dict:
        """get qa histories

        API reference: GET /accounts/<account_id>/organizations/<organization_id>/deployments/<deployment_id>/qa_history

        Request Syntax:
            .. code-block:: python

                account_id = "1122334455660"
                organization_id = "1410000000000"
                deployment_id = "1234567890123"
                offset = 0
                limit = 1000
                response = api_client.get_qa_histories(
                    account_id, organization_id, deployment_id, offset, limit)

        Params:
            - **account_id** (str): account identifier
            - **organization_id** (str): organization identifier
            - **deployment_id** (str): deployment identifier for OpsBee LLM
            - **offset** (int): **[optional]** offset of threads ( which starts from 0 )
            - **limit** (int): **[optional]** max number of threads to be returned

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: python
                {
                    'account_id': '1122334455660',
                    'organization_id': '1410000000000'
                    'deployment_id': '1234567890123',
                    'thread_id': '1234567890126',
                    'thread_name': 'QA用スレッド',
                    'histories': [
                        {
                            'id': "1234567890123",
                            'account_id': "1122334455660",
                            'organization_id': "1410000000000",
                            'deployment_id': "1234567890123",
                            'thread_id': "1234567890126",
                            'thread_name': "QA用スレッド",
                            'input_text': "今日の天気は？",
                            'output_text': "今日は晴れです",
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
                            'created_at' : "2023-12-13T04:42:34.913644Z",
                            'updated_at' : "2023-12-13T04:42:34.913644Z",
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

        # verify deployment type
        path = '/accounts/{}/organizations/{}/deployments/{}'.format(
            account_id,
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
        path = '/accounts/{}/organizations/{}/deployments/{}/qa_history?offset={}&limit={}'.format(
            account_id,
            organization_id,
            deployment_id,
            offset,
            limit,
        )
        return self._connection.api_request(method='GET', path=path, params=params)

    def get_qa_history(
        self,
        account_id: str,
        organization_id: str,
        deployment_id: str,
        history_id: str,
    ) -> dict:
        """get qa histories

        API reference: GET /accounts/<account_id>/organizations/<organization_id>/deployments/<deployment_id>/qa_history/<history_id>

        Request Syntax:
            .. code-block:: python

                account_id = "1122334455660"
                organization_id = "1410000000000"
                deployment_id = "1234567890123"
                history_id = "1234567890125"
                response = api_client.get_qa_histories(
                    account_id, organization_id, deployment_id, history_id)

        Params:
            - **account_id** (str): account identifier
            - **organization_id** (str): organization identifier
            - **deployment_id** (str): deployment identifier for OpsBee LLM
            - **history_id** (str): history identifier

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: python
                {
                    'id': "1234567890123",
                    'account_id': "1122334455660",
                    'organization_id': "1410000000000",
                    'deployment_id': "1234567890123",
                    'thread_id': "1234567890126",
                    'thread_name': "QA用スレッド",
                    'input_text': "今日の天気は？",
                    'output_text': "今日は晴れです",
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
                    'created_at' : "2023-12-13T04:42:34.913644Z",
                    'updated_at' : "2023-12-13T04:42:34.913644Z",
                }

        Raises:
            - BadRequest
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        # verify deployment type
        path = '/accounts/{}/organizations/{}/deployments/{}'.format(
            account_id,
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
        path = '/accounts/{}/organizations/{}/deployments/{}/qa_history/{}'.format(
            account_id,
            organization_id,
            deployment_id,
            history_id,
        )
        return self._connection.api_request(method='GET', path=path)

    def create_qa_history(
        self,
        account_id: str,
        organization_id: str,
        deployment_id: str,
        input_text: str,
        output_text: str,
        input_token_count: Optional[int] = 0,
        output_token_count: Optional[int] = 0,
        tag_ids: Optional[list] = None,
        metadata: Optional[dict] = None,
    ) -> dict:
        """create a qa history

        API reference: POST /accounts/<account_id>/organizations/<organization_id>/deployments/<deployment_id>/qa_history

        Request Syntax:
            .. code-block:: python

                account_id = "1122334455660"
                organization_id = "1410000000000"
                deployment_id = "1234567890123"
                input_text = "ABEJAについて教えて"
                output_text = "ABEJAは、スペイン語で「ミツバチ」の意味であり、植物の受粉を手伝い、世界の食料生産を支える存在として社名になっています。"
                response = api_client.create_qa_history(
                    account_id, organization_id, deployment_id, input_text, output_text)

        Params:
            - **account_id** (str): account identifier
            - **organization_id** (str): organization identifier
            - **deployment_id** (str): deployment identifier for OpsBee LLM
            - **input_text** (str): input text to LLM
            - **output_text** (str): output text from LLM
            - **input_token_count** (str): token count of input text
            - **output_token_count** (str): token count of output text
            - **tag_ids** (list): **[optional]** list of tag identifiers
            - **metadata** (list[dict]): **[optional]** list of {key: value} metadata

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: python
                {
                    'id': "1234567890123",
                    'account_id': "1122334455660",
                    'organization_id': "1410000000000",
                    'deployment_id': "1234567890123",
                    'thread_id': "1234567890126",
                    'thread_name': "QA用スレッド",
                    'input_text': "今日の天気は？",
                    'output_text': "今日は晴れです",
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
                    'created_at' : "2023-12-13T04:42:34.913644Z",
                    'updated_at' : "2023-12-13T04:42:34.913644Z",
                }

        Raises:
            - BadRequest
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        if not input_text:
            error_message = '"input_text" is necessary'
            raise BadRequest(
                error=error_message,
                error_description=error_message,
                status_code=400
            )
        if not output_text:
            error_message = '"output_text" is necessary'
            raise BadRequest(
                error=error_message,
                error_description=error_message,
                status_code=400
            )

        # verify deployment type
        path = '/accounts/{}/organizations/{}/deployments/{}'.format(
            account_id,
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
        path = '/accounts/{}/organizations/{}/deployments/{}/qa_history'.format(
            account_id,
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
        account_id: str,
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

        API reference: PATCH /accounts/<account_id>/organizations/<organization_id>/deployments/<deployment_id>/qa_history/<history_id>

        Request Syntax:
            .. code-block:: python

                account_id = "1122334455660"
                organization_id = "1410000000000"
                deployment_id = "1234567890123"
                history_id = "1234567890125"
                input_text = "ABEJAについて教えて"
                output_text = "ABEJAは、スペイン語で「ミツバチ」の意味であり、植物の受粉を手伝い、世界の食料生産を支える存在として社名になっています。"
                response = api_client.update_qa_history(
                    account_id, organization_id, deployment_id, history_id, input_text, output_text)

        Params:
            - **account_id** (str): account identifier
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

            .. code-block:: python
                {
                    'id': "1234567890123",
                    'account_id': "1122334455660",
                    'organization_id': "1410000000000",
                    'deployment_id': "1234567890123",
                    'thread_id': "1234567890126",
                    'thread_name': "QA用スレッド",
                    'input_text': "今日の天気は？",
                    'output_text': "今日は晴れです",
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
                    'created_at' : "2023-12-13T04:42:34.913644Z",
                    'updated_at' : "2023-12-13T04:42:34.913644Z",
                }

        Raises:
            - BadRequest
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        # verify deployment type
        path = '/accounts/{}/organizations/{}/deployments/{}'.format(
            account_id,
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
        path = '/accounts/{}/organizations/{}/deployments/{}/qa_history/{}'.format(
            account_id,
            organization_id,
            deployment_id,
            history_id,
        )
        resp_history = self._connection.api_request(method='GET', path=path)

        # update history
        path = '/accounts/{}/organizations/{}/deployments/{}/qa_history/{}'.format(
            account_id,
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
        account_id: str,
        organization_id: str,
        deployment_id: str,
        history_id: str,
    ) -> dict:
        """delete a qa history

        API reference: DELETE /accounts/<account_id>/organizations/<organization_id>/deployments/<deployment_id>/qa_history/<history_id>

        Request Syntax:
            .. code-block:: python

                account_id = "1122334455660"
                organization_id = "1410000000000"
                deployment_id = "1234567890123"
                history_id = "1234567890125"
                response = api_client.delete_qa_history(
                    account_id, organization_id, deployment_id, history_id)

        Params:
            - **account_id** (str): account identifier
            - **organization_id** (str): organization identifier
            - **deployment_id** (str): deployment identifier for OpsBee LLM
            - **history_id** (str): history identifier

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: python
                {
                    'id': "1234567890123",
                    'account_id': "1122334455660",
                    'organization_id': "1410000000000",
                    'deployment_id': "1234567890123",
                    'thread_id': "1234567890126",
                    'thread_name': "QA用スレッド",
                    'input_text': "今日の天気は？",
                    'output_text': "今日は晴れです",
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
                    'created_at' : "2023-12-13T04:42:34.913644Z",
                    'updated_at' : "2023-12-13T04:42:34.913644Z",
                }

        Raises:
            - BadRequest
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        # verify deployment type
        path = '/accounts/{}/organizations/{}/deployments/{}'.format(
            account_id,
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
        path = '/accounts/{}/organizations/{}/deployments/{}/qa_history/{}'.format(
            account_id,
            organization_id,
            deployment_id,
            history_id,
        )
        return self._connection.api_request(method='DELETE', path=path)

    def get_chat_histories(
        self,
        account_id: str,
        organization_id: str,
        deployment_id: str,
        offset: Optional[int] = 0,
        limit: Optional[int] = 1000,
    ) -> dict:
        """get chat histories

        API reference: GET /accounts/<account_id>/organizations/<organization_id>/deployments/<deployment_id>/history

        Request Syntax:
            .. code-block:: python

                account_id = "1122334455660"
                organization_id = "1410000000000"
                deployment_id = "1234567890123"
                offset = 0
                limit = 1000
                response = api_client.get_chat_histories(
                    account_id, organization_id, deployment_id, offset, limit)

        Params:
            - **account_id** (str): account identifier
            - **organization_id** (str): organization identifier
            - **deployment_id** (str): deployment identifier for OpsBee LLM
            - **offset** (int): **[optional]** offset of threads ( which starts from 0 )
            - **limit** (int): **[optional]** max number of threads to be returned

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: python
                {
                    'account_id': '1122334455660',
                    'organization_id': '1410000000000'
                    'deployment_id': '1234567890123',
                    'thread_id': '1234567890126',
                    'thread_name': 'thread name',
                    'histories': [
                        {
                            'id': "1234567890123",
                            'account_id': "1122334455660",
                            'organization_id': "1410000000000",
                            'deployment_id': "1234567890123",
                            'thread_id': "1234567890126",
                            'thread_name': "thread name",
                            'input_text': "今日の天気は？",
                            'output_text': "今日は晴れです",
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
                            'created_at' : "2023-12-13T04:42:34.913644Z",
                            'updated_at' : "2023-12-13T04:42:34.913644Z",
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

        # verify deployment type
        path = '/accounts/{}/organizations/{}/deployments/{}'.format(
            account_id,
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
                error_description=f"The specified deployment '{deployment_id}' type is '{deployment_type}', but it not supported! Only 'qa' is supported.",
                status_code=400
            )

        # get chat histories
        path = '/accounts/{}/organizations/{}/deployments/{}/history?offset={}&limit={}'.format(
            account_id,
            organization_id,
            deployment_id,
            offset,
            limit,
        )
        return self._connection.api_request(method='GET', path=path, params=params)

    def get_chat_history(
        self,
        account_id: str,
        organization_id: str,
        deployment_id: str,
        thread_id: str,
        history_id: str,
    ) -> dict:
        """get chat history

        API reference: GET /accounts/<account_id>/organizations/<organization_id>/deployments/<deployment_id>/threads/<thread_id>/history/<history_id>

        Request Syntax:
            .. code-block:: python

                account_id = "1122334455660"
                organization_id = "1410000000000"
                deployment_id = "1234567890123"
                thread_id = "1234567890125"
                history_id = "1234567890129"
                response = api_client.get_chat_history(
                    account_id, organization_id, deployment_id, thread_id, history_id)

        Params:
            - **account_id** (str): account identifier
            - **organization_id** (str): organization identifier
            - **deployment_id** (str): deployment identifier for OpsBee LLM
            - **thread_id** (str): thread identifier
            - **history_id** (str): history identifier

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: python
                {
                    'id': "1234567890123",
                    'account_id': "1122334455660",
                    'organization_id': "1410000000000",
                    'deployment_id': "1234567890123",
                    'thread_id': "1234567890126",
                    'thread_name': "thread name",
                    'input_text': "今日の天気は？",
                    'output_text': "今日は晴れです",
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
                    'created_at' : "2023-12-13T04:42:34.913644Z",
                    'updated_at' : "2023-12-13T04:42:34.913644Z",
                }

        Raises:
            - BadRequest
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        # verify deployment type
        path = '/accounts/{}/organizations/{}/deployments/{}'.format(
            account_id,
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
                error_description=f"The specified deployment '{deployment_id}' type is '{deployment_type}', but it not supported! Only 'qa' is supported.",
                status_code=400
            )

        # get chat history
        path = '/accounts/{}/organizations/{}/deployments/{}/threads/{}/history/{}'.format(
            account_id,
            organization_id,
            deployment_id,
            thread_id,
            history_id,
        )
        return self._connection.api_request(method='GET', path=path)

    def create_chat_history(
        self,
        account_id: str,
        organization_id: str,
        deployment_id: str,
        thread_id: str,
        input_text: str,
        output_text: str,
        input_token_count: Optional[int] = 0,
        output_token_count: Optional[int] = 0,
        tag_ids: Optional[list] = None,
        metadata: Optional[dict] = None,
    ) -> dict:
        """create a chat history

        API reference: POST /accounts/<account_id>/organizations/<organization_id>/deployments/<deployment_id>/threads/<thread_id>/history

        Request Syntax:
            .. code-block:: python

                account_id = "1122334455660"
                organization_id = "1410000000000"
                deployment_id = "1234567890123"
                thread_id = "1234567890123"
                input_text = "ABEJAについて教えて"
                output_text = "ABEJAは、スペイン語で「ミツバチ」の意味であり、植物の受粉を手伝い、世界の食料生産を支える存在として社名になっています。"
                response = api_client.create_chat_history(
                    account_id, organization_id, deployment_id, thread_id, input_text, output_text)

        Params:
            - **account_id** (str): account identifier
            - **organization_id** (str): organization identifier
            - **deployment_id** (str): deployment identifier for OpsBee LLM
            - **thread_id** (str): thread identifier
            - **input_text** (str): input text to LLM
            - **output_text** (str): output text from LLM
            - **input_token_count** (str): token count of input text
            - **output_token_count** (str): token count of output text
            - **tag_ids** (list): list of tag identifiers
            - **metadata** (list[dict]): list of {key: value} metadata

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: python
                {
                    'id': "1234567890123",
                    'account_id': "1122334455660",
                    'organization_id': "1410000000000",
                    'deployment_id': "1234567890123",
                    'thread_id': "1234567890126",
                    'thread_name': "スレッドA",
                    'input_text': "今日の天気は？",
                    'output_text': "今日は晴れです",
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
                    'created_at' : "2023-12-13T04:42:34.913644Z",
                    'updated_at' : "2023-12-13T04:42:34.913644Z",
                }

        Raises:
            - BadRequest
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        if not input_text:
            error_message = '"input_text" is necessary'
            raise BadRequest(
                error=error_message,
                error_description=error_message,
                status_code=400
            )
        if not output_text:
            error_message = '"output_text" is necessary'
            raise BadRequest(
                error=error_message,
                error_description=error_message,
                status_code=400
            )

        # verify deployment type
        path = '/accounts/{}/organizations/{}/deployments/{}'.format(
            account_id,
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
                error_description=f"The specified deployment '{deployment_id}' type is '{deployment_type}', but it not supported! Only 'qa' is supported.",
                status_code=400
            )

        # create history
        path = '/accounts/{}/organizations/{}/deployments/{}/threads/{}/history'.format(
            account_id,
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
        account_id: str,
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

        API reference: PATCH /accounts/<account_id>/organizations/<organization_id>/deployments/<deployment_id>/threads/<thread_id>/history/<history_id>

        Request Syntax:
            .. code-block:: python

                account_id = "1122334455660"
                organization_id = "1410000000000"
                deployment_id = "1234567890123"
                thread_id = "1234567890124"
                history_id = "1234567890125"
                input_text = "ABEJAについて教えて"
                output_text = "ABEJAは、スペイン語で「ミツバチ」の意味であり、植物の受粉を手伝い、世界の食料生産を支える存在として社名になっています。"
                response = api_client.update_qa_history(
                    account_id, organization_id, deployment_id, thread_id, history_id, input_text, output_text)

        Params:
            - **account_id** (str): account identifier
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

            .. code-block:: python
                {
                    'id': "1234567890123",
                    'account_id': "1122334455660",
                    'organization_id': "1410000000000",
                    'deployment_id': "1234567890123",
                    'thread_id': "1234567890126",
                    'thread_name': "チャット用スレッド",
                    'input_text': "今日の天気は？",
                    'output_text': "今日は晴れです",
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
                    'created_at' : "2023-12-13T04:42:34.913644Z",
                    'updated_at' : "2023-12-13T04:42:34.913644Z",
                }

        Raises:
            - BadRequest
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        # verify deployment type
        path = '/accounts/{}/organizations/{}/deployments/{}'.format(
            account_id,
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
        path = '/accounts/{}/organizations/{}/deployments/{}/threads/{}/history/{}'.format(
            account_id,
            organization_id,
            deployment_id,
            thread_id,
            history_id,
        )
        resp_history = self._connection.api_request(method='GET', path=path)

        # update history
        path = '/accounts/{}/organizations/{}/deployments/{}/threads/{}/history/{}'.format(
            account_id,
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
        account_id: str,
        organization_id: str,
        deployment_id: str,
        thread_id: str,
        history_id: str,
    ) -> dict:
        """delete a chat history

        API reference: DELETE /accounts/<account_id>/organizations/<organization_id>/deployments/<deployment_id>/threads/<thread_id>/history/<history_id>

        Request Syntax:
            .. code-block:: python

                account_id = "1122334455660"
                organization_id = "1410000000000"
                deployment_id = "1234567890123"
                thread_id = "1234567890124"
                history_id = "1234567890125"
                response = api_client.delete_chat_history(
                    account_id, organization_id, deployment_id, thread_id, history_id)

        Params:
            - **account_id** (str): account identifier
            - **organization_id** (str): organization identifier
            - **deployment_id** (str): deployment identifier for OpsBee LLM
            - **thread_id** (str): thread identifier
            - **history_id** (str): history identifier

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: python
                {
                    'id': "1234567890125",
                    'account_id': "1122334455660",
                    'organization_id': "1410000000000",
                    'deployment_id': "1234567890123",
                    'thread_id': "1234567890124",
                    'thread_name': "チャット用スレッド",
                    'input_text': "今日の天気は？",
                    'output_text': "今日は晴れです",
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
                    'created_at' : "2023-12-13T04:42:34.913644Z",
                    'updated_at' : "2023-12-13T04:42:34.913644Z",
                }

        Raises:
            - BadRequest
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        # verify deployment type
        path = '/accounts/{}/organizations/{}/deployments/{}'.format(
            account_id,
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
        path = '/accounts/{}/organizations/{}/deployments/{}/threads/{}/history/{}'.format(
            account_id,
            organization_id,
            deployment_id,
            thread_id,
            history_id,
        )
        return self._connection.api_request(method='DELETE', path=path)
