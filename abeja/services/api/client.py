from datetime import datetime
from typing import Dict, Optional

from abeja.common.api_client import BaseAPIClient


class APIClient(BaseAPIClient):
    """A low-level client for Service API

    .. code-block:: python

       from abeja.services import APIClient

       api_client = APIClient()
    """

    def create_service(self,
                       organization_id: str,
                       deployment_id: str,
                       version_id: str,
                       instance_number: int=1,
                       min_instance_number: Optional[int]=None,
                       max_instance_number: Optional[int]=None,
                       enable_autoscale: Optional[bool]=None,
                       instance_type: str='cpu-0.25',
                       environment: Optional[Dict[str,
                                                  str]]=None,
                       model_id: Optional[str] = None) -> dict:
        """create a service

        API reference: POST /organizations/{organization_id}/deployments/{deployment_id}/services

        Request Syntax:
            .. code-block:: python

               organization_id = "1111111111111"
               deployment_id = "9999999999999"
               version_id = "ver-abc3333333333333"
               model_id = "3333333333333"
               environment = {
                   "EXAMPLE_ENV": "abc"
               }

               response = api_client.create_service(
                   organization_id, deployment_id, version_id,
                   model_id=model_id, environment=environment)

        Params:
            - **organization_id** (str): organization identifier
            - **deployment_id** (str): deployment identifier
            - **version_id** (str): version identifier of paired model
            - **model_id** (str): training model identifier
            - **environment** (dict): env variable of running environment
            - **instance_type** (str): instance type of running environment
            - **instance_number** (str): number of instance
            - **min_instance_number** (str): number of minimum instance
            - **max_instance_number** (str): number of maximum instance
            - **enable_autoscale** (str): enable auto scaling

        Return type:
            dict
        Returns:
            Response Syntax:
                .. code-block:: json

                   {
                       "service_id": "ser-abc1111111111111",
                       "deployment_id": "9999999999999",
                       "models": {
                           "alias": "3333333333333"
                       },
                       "model_version": "0.0.1",
                       "model_version_id": "ver-abc1111111111111",
                       "status": "IN_PROGRESS",
                       "instance_number": 1,
                       "min_instance_number": 1,
                       "max_instance_number": 2,
                       "enable_autoscale": true,
                       "instance_type": "cpu-0.25",
                       "metrics_url": "https://p.datadoghq.com/sb/aaaaaaaaa-bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
                       "user_env_vars": {
                           "EXAMPLE_ENV": "abc"
                       },
                       "created_at": "2018-06-05T13:07:49.602076Z",
                       "modified_at": "2018-06-05T13:07:50.771671Z",
                   }

        Raises:
            - BadRequest: the resource already exists or parameters is insufficient or invalid.
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        payload = {
            'instance_type': instance_type,
            'instance_number': instance_number,
            'version_id': version_id
        }
        if model_id is not None:
            payload.update({
                'models': {
                    'alias': model_id
                }
            })
        if environment is not None:
            payload.update({
                'environment': environment
            })
        if min_instance_number is not None:
            payload.update({
                'min_instance_number': min_instance_number
            })
        if max_instance_number is not None:
            payload.update({
                'max_instance_number': max_instance_number
            })
        if enable_autoscale is not None:
            payload.update({
                'enable_autoscale': enable_autoscale
            })
        path = '/organizations/{}/deployments/{}/services'.format(
            organization_id, deployment_id)
        return self._connection.api_request(
            method='POST', path=path, json=payload)

    def get_service(
            self,
            organization_id: str,
            deployment_id: str,
            service_id: str) -> dict:
        """get a service

        API reference: GET /organizations/<organization_id>/deployments/<deployment_id>/services/<service_id>

        Request Syntax:
            .. code-block:: python

               response = api_client.get_service(organization_id='1111111111111', deployment_id='9999999999999',
                                                 service_id='ser-abc1111111111111')

        Params:
            - **organization_id** (str): organization_id
            - **deployment_id** (str): deployment identifier
            - **service_id** (str): service identifier

        Return type:
            dict

        Returns:
            Response Syntax:
                .. code-block:: json

                   {
                       "service_id": "ser-abc1111111111111",
                       "deployment_id": "9999999999999",
                       "models": {
                           "alias": "3333333333333"
                       },
                       "model_version": "0.0.1",
                       "model_version_id": "ver-abc1111111111111",
                       "status": "READY",
                       "instance_number": 1,
                       "instance_type": "cpu-0.25",
                       "metrics_url": "https://p.datadoghq.com/sb/aaaaaaaaa-bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
                       "user_env_vars": {
                           "EXAMPLE_ENV": "abc"
                       },
                       "created_at": "2018-06-05T12:34:33.485329Z",
                       "modified_at": "2018-06-05T12:34:34.568985Z"
                   }

        Raises:
          - NotFound: service not found
          - Unauthorized: Authentication failed
          - InternalServerError
        """
        path = '/organizations/{}/deployments/{}/services/{}'.format(
            organization_id, deployment_id, service_id)
        return self._connection.api_request(method='GET', path=path)

    def get_services(self, organization_id: str, deployment_id: str) -> dict:
        """Get services entries

        API reference: GET /organizations/<organization_id>/deployments/<deployment_id>/services

        Request syntax:
            .. code-block:: python

               response = api_client.list_services(organization_id='1111111111111', deployment_id='9999999999999')

        Params:
            - **organization_id** (str): organization_id
            - **deployment_id** (str): deployment identifier

        Return type:
            dict

        Returns:
            Return syntax:
                .. code-block:: json

                   {
                       "entries": [
                           {
                               "service_id": "ser-abc1111111111111",
                               "deployment_id": "9999999999999",
                               "models": {
                                   "alias": "3333333333333"
                               },
                               "model_version": "0.0.1",
                               "model_version_id": "ver-abc1111111111111",
                               "status": "READY",
                               "instance_number": 1,
                               "instance_type": "cpu-0.25",
                               "metrics_url": "https://p.datadoghq.com/sb/aaaaaaaaa-bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
                               "user_env_vars": {
                                   "EXAMPLE_ENV": "abc"
                               },
                               "created_at": "2018-06-05T12:34:33.485329Z",
                               "modified_at": "2018-06-05T12:34:34.568985Z"
                           }
                       ]
                   }


        Raises:
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        path = '/organizations/{}/deployments/{}/services'.format(
            organization_id, deployment_id)
        return self._connection.api_request(method='GET', path=path)

    def update_service(
            self,
            organization_id: str,
            deployment_id: str,
            service_id: str,
            payload: Optional[dict] = None) -> dict:
        """update a service

        API reference: PATCH /organizations/<organization_id>/deployments/<deployment_id>/services/<service_id>

        Request Syntax:
            .. code-block:: python

                payload = {
                    "instance_number": 4,
                    "min_instance_number": 2,
                    "max_instance_number": 6,
                    "enable_autoscale": 'true'
                }
                response = api_client.update_service(organization_id='1111111111111', deployment_id='9999999999999',
                                                 service_id='ser-abc1111111111111', payload=payload)

        Params:
            - **organization_id** (str): organization_id
            - **deployment_id** (str): deployment identifier
            - **service_id** (str): service identifier
            - **payload** (dict): payload of service **[optional]**

        Return type:
            dict

        Returns:
            Response Syntax:
                .. code-block:: json

                   {
                       "deployment_id": "1408443944117",
                       "instance_number": 1,
                       "instance_type": "cpu-1",
                       "metrics_url": "https://p.datadoghq.com/sb/xxxxxxxxx-yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy",
                       "models": {
                           "alias": "3333333333333"
                       },
                       "model_version": "1.0.0",
                       "model_version_id": "ver-1cfab7455c8e43a7",
                       "service_id": "ser-abc1111111111111",
                       "status": "IN_PROGRESS",
                       "record_channel_id": "5678901234567",
                       "user_env_vars": {
                           "EXAMPLE_ENV2": "exmaple2"
                       },
                       "merged_env_vars": {
                           "EXAMPLE_ENV": "deployment_example",
                           "EXAMPLE_ENV2": "exmaple2"
                       },
                       "service_process_type": "multi",
                       "modified_at": "2018-01-01T00:00:00.102289Z",
                       "created_at": "2018-01-01T00:00:00.102289Z"
                   }

        Raises:
          - NotFound: service not found
          - Unauthorized: Authentication failed
          - InternalServerError
        """
        path = '/organizations/{}/deployments/{}/services/{}'.format(
            organization_id, deployment_id, service_id)
        return self._connection.api_request(
            method='PATCH', path=path, json=payload)

    def delete_service(
            self,
            organization_id: str,
            deployment_id: str,
            service_id: str) -> dict:
        """delete a service

        API reference: DELETE /organizations/<organization_id>/deployments/<deployment_id>/services/<service_id>

        Request syntax:
            .. code-block:: python

               response = api_client.delete_service(organization_id='1111111111111',
                                                    deployment_id='9999999999999', service_id='ser-abc1111111111111')

        Params:
            - **organization_id** (str): organization_id
            - **deployment_id** (str): deployment identifier
            - **service_id** (str): service identifier

        Return type:
            dict

        Responses:
            Response syntax:
                .. code-block:: json

                   {
                       "message": "ser-abc1111111111111 deleted"
                   }

        Raises:
          - NotFound: service not found
          - Unauthorized: Authentication failed
          - InternalServerError
        """
        path = '/organizations/{}/deployments/{}/services/{}'.format(
            organization_id, deployment_id, service_id)
        return self._connection.api_request(method='DELETE', path=path)

    def stop_service(
            self,
            organization_id: str,
            deployment_id: str,
            service_id: str) -> dict:
        """stop a service

        API reference: POST /organizations/<organization_id>/deployments/<deployment_id>/services/<service_id>/stop

        Request syntax:
            .. code-block:: python

               response = api_client.stop_service(organization_id='1111111111111',
                                                　deployment_id='9999999999999', service_id='ser-abc1111111111111')

        Params:
            - **organization_id** (str): organization_id
            - **deployment_id** (str): deployment identifier
            - **service_id** (str): service identifier

        Return type:
            dict

        Responses:
            Response syntax:
                .. code-block:: json

                   {
                       "message": "ser-abc1111111111111 stopped"
                   }

        Raises:
          - BadRequest: service is not running
          - NotFound: service not found
          - Unauthorized: Authentication failed
          - InternalServerError
        """
        path = '/organizations/{}/deployments/{}/services/{}/stop'.format(
            organization_id, deployment_id, service_id)
        return self._connection.api_request(method='POST', path=path)

    def start_service(
            self,
            organization_id: str,
            deployment_id: str,
            service_id: str) -> dict:
        """start a service

        API reference: POST /organizations/<organization_id>/deployments/<deployment_id>/services/<service_id>/start

        Request syntax:
            .. code-block:: python

               response = api_client.stop_service(organization_id='1111111111111',
                                                　deployment_id='9999999999999', service_id='ser-abc1111111111111')

        Params:
            - **organization_id** (str): organization_id
            - **deployment_id** (str): deployment identifier
            - **service_id** (str): service identifier

        Return type:
            dict

        Responses:
            Response syntax:
                .. code-block:: json

                   {
                       "message": "ser-abc1111111111111 started"
                   }

        Raises:
          - BadRequest: service is already running
          - NotFound: service not found
          - Unauthorized: Authentication failed
          - InternalServerError
        """
        path = '/organizations/{}/deployments/{}/services/{}/start'.format(
            organization_id, deployment_id, service_id)
        return self._connection.api_request(method='POST', path=path)

    def get_service_recent_logs(
            self,
            organization_id: str,
            deployment_id: str,
            service_id: str,
            next_forward_token: Optional[str]=None,
            next_backward_token: Optional[str]=None,
            start_time: Optional[datetime]=None,
            end_time: Optional[datetime]=None) -> dict:
        """get recent logs of the service

        API reference: GET /organizations/<organization_id>/deployments/<deployment_id>/services/<service_id>/recentlogs

        Request Syntax:
            .. code-block:: python

                organization_id = "1234567890123"
                deployment_id = "1111111111111"
                service_id = "ser-3333333333333333"
                response = api_client.get_service_recent_logs(organization_id, deployment_id, service_id)

        Params:
            - **organization_id** (str): organization_id
            - **deployment_id** (str): deployment identifier
            - **service_id** (str): service identifier
            - **next_forward_token** (str): **[optional]** token for the next page of logs
            - **next_backward_token** (str): **[optional]** token for the next previous of logs
            - **start_time** (datetime): **[optional]** specifies the start utc datetime included in data series
            - **end_time** (datetime): **[optional]** specifies the end utc datetime included in data series

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

            - **events** (list): list of messages emitted from the service. the messages are sorted in *descending order*.
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
        path = '/organizations/{}/deployments/{}/services/{}/recentlogs'.format(
            organization_id, deployment_id, service_id)
        return self._connection.api_request(
            method='GET', path=path, params=params)
