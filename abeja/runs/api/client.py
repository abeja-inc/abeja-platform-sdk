from datetime import datetime
from typing import Dict, Optional

from abeja.common.api_client import BaseAPIClient


class APIClient(BaseAPIClient):
    """A low-level client for Run API

    .. code-block:: python

       from abeja.run import APIClient

       api_client = APIClient()
    """

    def create_run(self,
                   organization_id: str,
                   deployment_id: str,
                   version_id: str,
                   input_data: Optional[Dict[str,
                                             str]] = None,
                   output_template: Optional[Dict[str,
                                                  str]]=None,
                   distribution: Optional[int]=None,
                   retry_count: Optional[int]=None,
                   environment: Optional[Dict[str,
                                              str]]=None,
                   model_id: Optional[str] = None) -> dict:
        """submit a run

        API reference: POST /organizations/<organization_id>/deployments/<deployment_id>/runs

        Request Syntax:
            .. code-block:: python

                organization_id = "1234567890123"
                deployment_id = "1111111111111"
                version_id = "ver-1111111111111111"
                model_id = "3333333333333"
                input_data = {
                    "$datalake:1": "2222222222222/20180101T112233-44444444-5555-6666-7777-888888888888"
                }
                distribution = 0
                retry_count = 0
                environment = {
                    "EXAMPLE_ENV": "example"
                }
                response = api_client.create_run(
                    organization_id, deployment_id, version_id, input_data,
                    model_id=model_id, distribution=distribution, retry_count=retry_count, environment=environment)

        Params:
            - **organization_id** (str): The ID of the organization.
            - **deployment_id** (str): The ID of the deployment.
            - **version_id** (str): The ID of the version of a model.
            - **model_id** (str): training model identifier
            - **input_data** (dict): **[optional]** specifies input data in json format for INPUT.
              The format is like following ``{"<operator>:<protocol_version>": "<operator_payload>"}``.
              The value specified in INPUT is passed to the first argument of the handler of
              the user-defined code.
            - **output_data** (dict): **[optional]** specifies output data in json format for OUTPUT.
              The format is like following ``{"<operator>:<protocol_version>": "<operator_payload>"}``.
            - **distribution** (int): **[optional]** specifies the id whose remainder determine distributed
              queue, as default, round-robin is used.
            - **retry_count** (int): **[optional]** specifies the number of attempts from 0 to 9,
              defaults to 5.
            - **environment** (int): **[optional]** specifies the environment variables which can be
              referred from user code.

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    "deployment_id": "1111111111111",
                    "models": {
                        "alias": "3333333333333"
                    },
                    "model_version": "0.0.3",
                    "model_version_id": "ver-1111111111111111",
                    "input_data": {
                        "$datalake:1": "2222222222222/20180101T112233-44444444-5555-6666-7777-888888888888"
                    },
                    "output_template": null,
                    "retry_count": 7,
                    "run_id": "run-3333333333333333",
                    "status": "SUBMITTED",
                    "user_env_vars": {
                        "DEBUG": "debug"
                    },
                    "distribution": 0,
                    "created_at": "2018-01-01T00:00:00.000000Z",
                    "modified_at": "2018-01-01T00:00:00.000000Z"
                }

        Raises:
            - Unauthorized: Authentication failed
            - NotFound:
            - Forbidden:
            - InternalServerError:
        """
        params = {
            'version_id': version_id,
        }
        params['environment'] = environment or {}
        if input_data:
            params.update({
                'input_data': input_data
            })

        if model_id:
            params.update({
                'models': {
                    'alias': model_id
                }
            })
        if output_template:
            params['output_template'] = output_template
        if retry_count is not None:
            params['retry_count'] = retry_count
        if distribution is not None:
            params['distribution'] = distribution
        path = '/organizations/{}/deployments/{}/runs'.format(
            organization_id, deployment_id)
        return self._connection.api_request(
            method='POST', path=path, json=params)

    def get_run(
            self,
            organization_id: str,
            deployment_id: str,
            run_id: str) -> dict:
        """get a run

        API reference: GET /organizations/<organization_id>/deployments/<deployment_id>/runs/<run_id>

        Request Syntax:
            .. code-block:: python

                organization_id = "1234567890123"
                deployment_id = "1111111111111"
                run_id = "run-3333333333333333"
                response = api_client.get_run(organization_id, deployment_id, run_id)

        Params:
            - **organization_id** (str): The ID of the organization.
            - **deployment_id** (str): The ID of the deployment.
            - **run_id** (str): The ID of the run.

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    "deployment_id": "1111111111111",
                    "models": {
                        "alias": "3333333333333"
                    },
                    "model_version": "0.0.3",
                    "model_version_id": "ver-1111111111111111",
                    "input_data": {
                        "$datalake:1": "2222222222222/20180101T112233-44444444-5555-6666-7777-888888888888"
                    },
                    "output_template": null,
                    "retry_count": 7,
                    "run_id": "run-3333333333333333",
                    "status": "SUBMITTED",
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
            - **input_data** (str): input data in json format for INPUT.
            - **output_template** (str): output data in json format for OUTPUT.
            - **retry_count** (int): the number of attempts.
            - **run_id** (str): The ID of the run.
            - **status** (str): The status of the run, which is each one of ``SUBMITTED``, ``PENDING``,
              ``RUNNABLE``, ``STARTING``, ``RUNNING``, ``SUCCEEDED``, ``FAILED``.
            - **user_env_vars** (str): environment variables which are available in user code.
            - **created_at** (str): created date of the run.
            - **modified_at** (str): modified date of the run.

        Raises:
            - Unauthorized: Authentication failed
            - NotFound:
            - Forbidden:
            - InternalServerError:
        """
        path = '/organizations/{}/deployments/{}/runs/{}'.format(
            organization_id, deployment_id, run_id)
        return self._connection.api_request(method='GET', path=path)

    def get_runs(
            self,
            organization_id: str,
            deployment_id: str,
            next_page_token: Optional[str]=None,
            scan_forward: Optional[bool]=None) -> dict:
        """get runs

        API reference: GET /organizations/<organization_id>/deployments/<deployment_id>/runs/

        Request Syntax:
            .. code-block:: python

                organization_id = "1234567890123"
                deployment_id = "1111111111111"
                response = api_client.get_runs(organization_id, deployment_id)

        Params:
            - **organization_id** (str): The ID of the organization.
            - **deployment_id** (str): The ID of the deployment.
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
                            "deployment_id": "1111111111111",
                            "models": {
                                "alias": "3333333333333"
                            },
                            "model_version": "0.0.3",
                            "model_version_id": "ver-1111111111111111",
                            "input_data": {
                                "$datalake:1": "2222222222222/20180101T112233-44444444-5555-6666-7777-888888888888"
                            },
                            "output_template": null,
                            "retry_count": 7,
                            "run_id": "run-3333333333333333",
                            "status": "SUBMITTED",
                            "user_env_vars": {
                                "DEBUG": "debug"
                            },
                            "created_at": "2018-01-01T00:00:00.000000Z",
                            "modified_at": "2018-01-01T00:00:00.000000Z"
                        }
                    ],
                    "next_page_token": "..."
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
        path = '/organizations/{}/deployments/{}/runs'.format(
            organization_id, deployment_id)
        return self._connection.api_request(
            method='GET', path=path, params=params)

    def get_run_logs(
            self,
            organization_id: str,
            deployment_id: str,
            run_id: str,
            next_token: Optional[str]=None,
            start_time: Optional[datetime]=None,
            end_time: Optional[datetime]=None) -> dict:
        """get logs of the run

        API reference: GET /organizations/<organization_id>/deployments/<deployment_id>/runs/<run_id>/logs

        Request Syntax:
            .. code-block:: python

                organization_id = "1234567890123"
                deployment_id = "1111111111111"
                run_id = "run-3333333333333333"
                response = api_client.get_run_logs(organization_id, deployment_id, run_id)

        Params:
            - **organization_id** (str): The ID of the organization.
            - **deployment_id** (str): The ID of the deployment.
            - **run_id** (str): The ID of the run.
            - **next_token** (str): **[optional]** specifies the following logs
            - **start_time** (datetime): **[optional]** specifies the start utc datetime included in data series.
            - **end_time** (datetime): **[optional]** specifies the end utc datetime included in data series.

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    "events": [
                        {
                            "message": "...",
                            "timestamp": "2018-01-01T00:00:00.000000Z"
                        }
                    ],
                    "next_token": "..."
                }

            Response Structure:

            - **events** (list): list of messages emitted from the run. the messages are sorted in *ascending order*.
            - **next_token** (str): token for the next page of logs. *If no more logs, this key does not exist*.

        Raises:
            - Unauthorized: Authentication failed
            - NotFound:
            - Forbidden:
            - InternalServerError:
        """
        params = {}
        if next_token:
            params['next_token'] = next_token
        if start_time:
            params['start_time'] = start_time.strftime("%Y-%m-%dT%H:%M:%S")
        if end_time:
            params['end_time'] = end_time.strftime("%Y-%m-%dT%H:%M:%S")
        path = '/organizations/{}/deployments/{}/runs/{}/logs'.format(
            organization_id, deployment_id, run_id)
        return self._connection.api_request(
            method='GET', path=path, params=params)

    def get_run_recent_logs(
            self,
            organization_id: str,
            deployment_id: str,
            run_id: str,
            next_forward_token: Optional[str]=None,
            next_backward_token: Optional[str]=None,
            start_time: Optional[datetime]=None,
            end_time: Optional[datetime]=None) -> dict:
        """get recent logs of the run

        API reference: GET /organizations/<organization_id>/deployments/<deployment_id>/runs/<run_id>/recentlogs

        Request Syntax:
            .. code-block:: python

                organization_id = "1234567890123"
                deployment_id = "1111111111111"
                run_id = "run-3333333333333333"
                response = api_client.get_run_recent_logs(organization_id, deployment_id, run_id)

        Params:
            - **organization_id** (str): The ID of the organization.
            - **deployment_id** (str): The ID of the deployment.
            - **run_id** (str): The ID of the run.
            - **next_forward_token** (str): **[optional]** token for the next page of logs
            - **next_backward_token** (str): **[optional]** token for the next previous of logs
            - **start_time** (datetime): **[optional]** specifies the start utc datetime included in data series.
            - **end_time** (datetime): **[optional]** specifies the end utc datetime included in data series.

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: json

                {
                    "events": [
                        {
                            "message": "...",
                            "timestamp": "2018-01-01T00:00:00.000000Z"
                        }
                    ],
                    "next_backward_token": "...",
                    "next_forward_token": "..."
                }

            Response Structure:

            - **events** (list): list of messages emitted from the run. the messages are sorted in *descending order*.
            - **next_backward_token** (str): token for the previous page of logs. **If no more logs, this key exists and returns empty list**.
            - **next_forward_token** (str): token for the next page of logs. **If no more logs, this key exists and returns empty list**.

        Raises:
            - Unauthorized: Authentication failed
            - NotFound:
            - Forbidden:
            - InternalServerError:
        """
        params = {}
        if next_forward_token:
            params['next_forward_token'] = next_forward_token
        if next_backward_token:
            params['next_backward_token'] = next_backward_token
        if start_time:
            params['start_time'] = start_time.strftime("%Y-%m-%dT%H:%M:%S")
        if end_time:
            params['end_time'] = end_time.strftime("%Y-%m-%dT%H:%M:%S")
        path = '/organizations/{}/deployments/{}/runs/{}/recentlogs'.format(
            organization_id, deployment_id, run_id)
        return self._connection.api_request(
            method='GET', path=path, params=params)
