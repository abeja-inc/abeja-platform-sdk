from typing import Optional

from abeja.opsbeellm.common.api_client import OpsBeeLLMBaseAPIClient
from abeja.exceptions import BadRequest


class APIClient(OpsBeeLLMBaseAPIClient):
    """A Low-Level client for OpsBee LLM History API

    .. code-block:: python

       from abeja.opsbeellm.history import APIClient

       api_client = APIClient()
    """

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
                    'created_at' : 2023-12-13T04:42:34.913644Z,
                    'updated_at' : 2023-12-13T04:42:34.913644Z,
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

    def create_history(
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
        """create a LLM history

        Request Syntax:
            .. code-block:: python

                account_id = "1122334455660"
                organization_id = "1410000000000"
                deployment_id = "1234567890123"
                input_text = "ABEJAについて教えて"
                output_text = "ABEJAは、スペイン語で「ミツバチ」の意味であり、植物の受粉を手伝い、世界の食料生産を支える存在として社名になっています。"
                response = api_client.create_history(
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
                    'created_at' : 2023-12-13T04:42:34.913644Z,
                    'updated_at' : 2023-12-13T04:42:34.913644Z,
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
                error="Failed to get thread_id",
                error_description=f"Failed to get thread_id | {e}",
                status_code=400
            )

        if deployment_type != "qa":
            raise BadRequest(
                error="deployment type is not supported",
                error_description=f"The specified deployment '{deployment_id}' type is '{deployment_type}', but it not supported! Only 'qa' is supported.",
                status_code=400
            )

        # get thread_id
        path = '/accounts/{}/organizations/{}/deployments/{}/threads'.format(
            account_id,
            organization_id,
            deployment_id,
        )
        resp_threads = self._connection.api_request(method='GET', path=path)
        try:
            thread_id = resp_threads["threads"][0]["id"]
        except Exception as e:
            raise BadRequest(
                error="Failed to get thread_id",
                error_description=f"Failed to get thread_id | {e}",
                status_code=400
            )

        # create history
        path = '/accounts/{}/organizations/{}/deployments/{}/threads/{}/history'.format(
            account_id,
            organization_id,
            deployment_id,
            thread_id
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
        """create a chat LLM history

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
                    'created_at' : 2023-12-13T04:42:34.913644Z,
                    'updated_at' : 2023-12-13T04:42:34.913644Z,
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
                error="Failed to get thread_id",
                error_description=f"Failed to get thread_id | {e}",
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
