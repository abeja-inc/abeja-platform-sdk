from typing import Optional

from abeja.opsbeellm.common.api_client import OpsBeeLLMBaseAPIClient
from abeja.exceptions import BadRequest


class APIClient(OpsBeeLLMBaseAPIClient):
    """A Low-Level client for OpsBee LLM API

    .. code-block:: python

       from abeja.opsbeellm import APIClient

       api_client = APIClient()
    """

    def create_history(
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
        """create a LLM history

        API reference: POST /accounts/<account_id>/organizations/<organization_id>/deployments/<deployment_id>/threads/<thread_id>/history

        Request Syntax:
            .. code-block:: python

                account_id = "1122334455660"
                organization_id = "1410000000000"
                deployment_id = "1234567890123"
                thread_id = "1234567890123"
                response = api_client.create_history(
                    account_id, organization_id, deployment_id, thread_id)

        Params:
            - **account_id** (str): ACCOUND_ID
            - **organization_id** (str): ORGANIZATION_ID
            - **deployment_id** (str): DEPLOYMENT_ID for OpsBee LLM
            - **thread_id** (str): THREAD_ID

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
