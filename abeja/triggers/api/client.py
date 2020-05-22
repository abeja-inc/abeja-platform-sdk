from typing import Dict, Optional

from abeja.common.api_client import BaseAPIClient


class APIClient(BaseAPIClient):
    """A low-level client for Run API

    .. code-block:: python

       from abeja.run import APIClient

       api_client = APIClient()
    """

    def create_trigger(self,
                       organization_id: str,
                       deployment_id: str,
                       version_id: str,
                       input_service_name: str,
                       input_service_id: str,
                       output_service_name: Optional[str]=None,
                       output_service_id: Optional[str]=None,
                       distribution: Optional[int]=None,
                       retry_count: Optional[int]=None,
                       environment: Optional[Dict[str,
                                                  str]]=None,
                       model_id: Optional[str] = None):
        """create a trigger

        API reference: POST /organizations/<organization_id>/deployments/<deployment_id>/triggers

        Request Syntax:
            .. code-block:: python

                organization_id = "1234567890123"
                deployment_id = "1111111111111"
                version_id = "ver-1111111111111111"
                input_service_name = "datalake"
                input_service_id = "2222222222222"
                model_id = "3333333333333"
                distribution = 0
                retry_count = 0
                environment = {
                    "EXAMPLE_ENV": "exmaple"
                }
                response = api_client.create_trigger(
                    organization_id, deployment_id, version_id, input_service_name, input_service_id,
                    model_id=model_id, distribution=distribution, retry_count=retry_count, environment=environment)

        Params:
            - **organization_id** (str): The ID of the organization.
            - **deployment_id** (str): The ID of the deployment.
            - **version_id** (str): The ID of the version of a model.
            - **input_service_name** (str): specifies name of the input service, only ``datalake`` is available for now.
            - **input_service_id** (str): specifies id of the service. In case of ``datalake``, specify ``channel_id``.
            - **model_id** (str): training model identifier
            - **output_service_name** (str): **[optional]** specifies name of the output service.
            - **output_service_name** (str): **[optional]** specifies id of the service. If ``output_service_name`` is given, this field is required.
            - **distribution** (int): **[optional]** specifies the id whose remainder determine distributed queue, as default, round-robin is used.
            - **retry_count** (int): **[optional]** specifies the number of attempts from 0 to 9, defaults to 5.
            - **environment** (int): **[optional]** specifies the environment variables which can be referred from user code.

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    "deployment_id": "1111111111111",
                    "input_service_id": "2222222222222",
                    "input_service_name": "datalake",
                    "models": {
                        "alias": "3333333333333"
                    },
                    "model_version": "0.0.3",
                    "model_version_id": "ver-1111111111111111",
                    "organization_id": "1234567890123",
                    "output_service_id": null,
                    "output_service_name": null,
                    "retry_count": 7,
                    "distribution": 0,
                    "trigger_id": "tri-3333333333333333",
                    "user_env_vars": {
                        "DEBUG": "debug"
                    }
                }

        Raises:
            - Unauthorized: Authentication failed
            - NotFound:
            - Forbidden:
            - InternalServerError:
        """
        params = {
            'version_id': version_id,
            'input_service_name': input_service_name,
            'input_service_id': input_service_id,
            'environment': environment
        }
        if model_id:
            params.update({
                'models': {
                    'alias': model_id
                }
            })
        if output_service_name and output_service_id:
            params['output_service_name'] = output_service_name
            params['output_service_id'] = output_service_id
        if retry_count is not None:
            params['retry_count'] = retry_count
        if distribution is not None:
            params['distribution'] = distribution
        path = '/organizations/{}/deployments/{}/triggers'.format(
            organization_id, deployment_id)
        return self._connection.api_request(
            method='POST', path=path, json=params)

    def get_trigger(
            self,
            organization_id: str,
            deployment_id: str,
            trigger_id: str) -> dict:
        """get a trigger

        API reference: GET /organizations/<organization_id>/deployments/<deployment_id>/triggers/<trigger_id>

        Request Syntax:
            .. code-block:: python

                organization_id = "1234567890123"
                deployment_id = "1111111111111"
                trigger_id = "tri-3333333333333333"
                response = api_client.get_trigger(organization_id, deployment_id, trigger_id)

        Params:
            - **organization_id** (str): The ID of the organization.
            - **deployment_id** (str): The ID of the deployment.
            - **trigger_id** (str): The ID of the trigger.

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    "deployment_id": "1111111111111",
                    "input_service_id": "2222222222222",
                    "input_service_name": "datalake",
                    "models": {
                        "alias": "3333333333333"
                    },
                    "model_version": "0.0.3",
                    "model_version_id": "ver-1111111111111111",
                    "organization_id": "1234567890123",
                    "output_service_id": null,
                    "output_service_name": null,
                    "retry_count": 7,
                    "trigger_id": "tri-3333333333333333",
                    "user_env_vars": {
                        "DEBUG": "debug"
                    },
                    "created_at": "2018-01-01T00:00:00.000000Z",
                    "modified_at": "2018-01-01T00:00:00.000000Z"
                }

            Response Structure:

            - **deployment_id** (str): The ID of the deployment.
            - **models** (dict): combination of alias and model_id
            - **model_version** (str): The version of the model.
            - **model_version_id** (str): The ID of the version.
            - **input_service_name** (str): specifies name of the input service, only ``datalake`` is available for now.
            - **input_service_id** (str): specifies id of the service. In case of ``datalake``, specify ``channel_id``.
            - **output_service_name** (str): **[optional]** specifies name of the output service.
            - **output_service_name** (str): **[optional]** specifies id of the service. If ``output_service_name`` is given, this field is required.
            - **retry_count** (int): the number of attempts.
            - **run_id** (str): The ID of the run.
            - **user_env_vars** (str): environment variables which are available in user code.
            - **created_at** (str): created date of the run.
            - **modified_at** (str): modified date of the run.

        Raises:
            - Unauthorized: Authentication failed
            - NotFound:
            - Forbidden:
            - InternalServerError:
        """
        path = '/organizations/{}/deployments/{}/triggers/{}'.format(
            organization_id, deployment_id, trigger_id)
        return self._connection.api_request(method='GET', path=path)

    def get_triggers(self, organization_id: str, deployment_id: str) -> dict:
        """get triggers

        API reference: GET /organizations/<organization_id>/deployments/<deployment_id>/triggers/

        Request Syntax:
            .. code-block:: python

                organization_id = "1234567890123"
                deployment_id = "1111111111111"
                response = api_client.get_triggers(organization_id, deployment_id)

        Params:
            - **organization_id** (str): The ID of the organization.
            - **deployment_id** (str): The ID of the deployment.

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    "entries": [
                        {
                            "deployment_id": "1111111111111",
                            "input_service_id": "2222222222222",
                            "input_service_name": "datalake",
                            "models": {
                                "alias": "3333333333333"
                            },
                            "model_version": "0.0.3",
                            "model_version_id": "ver-1111111111111111",
                            "organization_id": "1234567890123",
                            "output_service_id": null,
                            "output_service_name": null,
                            "retry_count": 7,
                            "trigger_id": "tri-3333333333333333",
                            "user_env_vars": {
                                "DEBUG": "debug"
                            },
                            "created_at": "2018-01-01T00:00:00.000000Z",
                            "modified_at": "2018-01-01T00:00:00.000000Z"
                        }
                    ]
                }

        Raises:
            - Unauthorized: Authentication failed
            - NotFound:
            - Forbidden:
            - InternalServerError:
        """
        path = '/organizations/{}/deployments/{}/triggers'.format(
            organization_id, deployment_id)
        return self._connection.api_request(method='GET', path=path)

    def delete_trigger(
            self,
            organization_id: str,
            deployment_id: str,
            trigger_id: str) -> dict:
        """delete trigger

        API reference: DELETE /organizations/<organization_id>/deployments/<deployment_id>/triggers/<trigger_id>

        Request Syntax:
            .. code-block:: python

                organization_id = "1234567890123"
                deployment_id = "1111111111111"
                trigger_id = "tri-3333333333333333"
                response = api_client.delete_trigger(organization_id, deployment_id, trigger_id)

        Params:
            - **organization_id** (str): The ID of the organization.
            - **deployment_id** (str): The ID of the deployment.
            - **trigger_id** (str): The ID of the trigger.

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    "message": "tri-3333333333333333 deleted"
                }

        Raises:
            - Unauthorized: Authentication failed
            - NotFound:
            - Forbidden:
            - InternalServerError:
        """
        path = '/organizations/{}/deployments/{}/triggers/{}'.format(
            organization_id, deployment_id, trigger_id)
        return self._connection.api_request(method='DELETE', path=path)

    def get_trigger_runs(
            self,
            organization_id: str,
            deployment_id: str,
            trigger_id: str,
            next_page_token: Optional[str]=None,
            scan_forward: Optional[bool]=None) -> dict:
        """get runs of a trigger

        API reference: GET /organizations/<organization_id>/deployments/<deployment_id>/triggers/<trigger_id>/runs

        Request Syntax:
            .. code-block:: python

                organization_id = "1234567890123"
                deployment_id = "1111111111111"
                trigger_id = "tri-3333333333333333"
                response = api_client.get_trigger_runs(organization_id, deployment_id, trigger_id)

        Params:
            - **organization_id** (str): The ID of the organization.
            - **deployment_id** (str): The ID of the deployment.
            - **trigger_id** (str): The ID of the trigger.
            - **next_page_token** (str): **[optional]** Token for offset of entries.
            - **scan_forward** (str): **[optional]** By default ``False``, the sort order is descending. To reverse the order, set this to ``True``

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    "entries": [
                        {
                            "created_at": "2019-01-01T00:00:00.000000Z",
                            "deployment_id": "1111111111111",
                            "input_data": {
                                "$datalake:1": "2222222222222/20190101T000000-e8286a2a-100a-4a40-a7de-5c9a5794b76c"
                            },
                            "models": {
                                "alias": "3333333333333"
                            },
                            "model_version_id": "ver-1111111111111111",
                            "modified_at": "2019-01-01T00:00:00.000000Z",
                            "output_template": null,
                            "retry_count": 5,
                            "run_id": "run-3333333333333333",
                            "status": "SUCCEEDED",
                            "trigger_id": "tri-3333333333333333",
                            "user_env_vars": {}
                        }
                    ],
                    "next_page_token": "xxxxx"
                }

        Raises:
            - Unauthorized: Authentication failed
            - NotFound:
            - Forbidden:
            - InternalServerError:
        """
        params = {}
        if scan_forward is not None:
            params['scan_forward'] = scan_forward
        if next_page_token is not None:
            params['next_page_token'] = next_page_token
        path = '/organizations/{}/deployments/{}/triggers/{}/runs'.format(
            organization_id, deployment_id, trigger_id)
        return self._connection.api_request(
            method='GET', path=path, params=params)
