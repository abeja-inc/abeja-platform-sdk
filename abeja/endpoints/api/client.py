from abeja.common.api_client import BaseAPIClient


class APIClient(BaseAPIClient):
    """A low-level client for Endpoint API

    .. code-block:: python

       from abeja.endpoints import APIClient

       api_client = APIClient()
    """

    def create_endpoint(
            self, organization_id: str, deployment_id: str, service_id: str,
            custom_alias: str='default') -> dict:
        """create a endpoint

        API reference: POST /organizations/{organization_id}/deployments/{deployment_id}/endpoints

        Request Syntax:
            .. code-block:: python

               organization_id = "1111111111111"
               deployment_id = "2222222222222"
               service_id = "ser-abc3333333333333"
               custom_alias = "default"

               response = api_client.create_endpoint(organization_id, deployment_id, service_id, custom_alias)

        Params:
            - **organization_id** (str): organization identifier
            - **deployment_id** (str): deployment identifier
            - **service_id** (str): service identifier for alias
            - **custom_alias** (str): custom alias name

        Return type:
            dict
        Returns:
            Response Syntax:
                .. code-block:: json

                   {
                       "endpoint_id": "pnt-abc1111111111111",
                       "custom_alias": "default",
                       "service_id": "ser-abc2222222222222"
                   }

        Raises:
            - BadRequest: the resource already exists or parameters is insufficient or invalid.
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        payload = {
            'service_id': service_id,
            'custom_alias': custom_alias,
        }
        path = '/organizations/{}/deployments/{}/endpoints'.format(
            organization_id, deployment_id)
        return self._connection.api_request(
            method='POST', path=path, json=payload)

    def get_endpoint(
            self,
            organization_id: str,
            deployment_id: str,
            endpoint: str) -> dict:
        """get a endpoint

        API reference: GET /organizations/<organization_id>/deployments/<deployment_id>/endpoints/<endpoint>

        Request Syntax:
            .. code-block:: python

               response = api_client.get_endpoint(organization_id='1111111111111', deployment_id='1111111111111',
                                                  endpoint='pnt-abc1111111111111')

        Params:
            - **organization_id** (str): organization_id
            - **deployment_id** (str): deployment identifier
            - **endpoint** (str): endpoint identifier or custom alias

        Return type:
            dict

        Returns:
            Response Syntax:
                .. code-block:: json

                   {
                       "endpoint_id": "pnt-d28322af41a14e16",
                       "custom_alias": "default",
                        "service_id": "ser-57e40a4c681a4a09"
                   }

        Raises:
          - NotFound: endpoint not found
          - Unauthorized: Authentication failed
          - InternalServerError
        """

        path = '/organizations/{}/deployments/{}/endpoints/{}'.format(
            organization_id, deployment_id, endpoint)
        return self._connection.api_request(method='GET', path=path)

    def get_endpoints(self, organization_id: str, deployment_id: str) -> dict:
        """Get endpoints entries

        API reference: GET /organizations/<organization_id>/deployments/<deployment_id>/endpoints

        Request syntax:
            .. code-block:: python

               response = api_client.get_endpoints(organization_id='1111111111111', deployment_id='1111111111111')

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
                               "endpoint_id": "pnt-abc1111111111111",
                               "custom_alias": "default",
                               "service_id": "ser-abc1111111111111"
                           }
                       ]
                   }

        Raises:
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        path = '/organizations/{}/deployments/{}/endpoints'.format(
            organization_id, deployment_id)
        return self._connection.api_request(method='GET', path=path)

    def update_endpoint(
            self,
            organization_id: str,
            deployment_id: str,
            endpoint: str,
            service_id: str) -> dict:
        """update a endpoint

        API reference: PATCH /organizations/<organization_id>/deployments/<deployment_id>/endpoints/<endpoint>

        Request syntax:
            .. code-block:: python

               response = api_client.update_endpoint(organization_id='1111111111111',
                                                     deployment_id='1111111111111',
                                                     endpoint='pnt-abc1111111111111',
                                                     service_id='ser-abc1111111111111')

        Params:
            - **organization_id** (str): organization_id
            - **deployment_id** (str): deployment identifier
            - **endpoint** (str): endpoint identifier or custom alias
            - **service_id** (str): service identifier

        Return type:
            dict

        Responses:
            Response syntax:
                .. code-block:: json

                   {
                       "message": "pnt-1111111111111111 updated"
                   }

        Raises:
          - NotFound: endpoint not found
          - Unauthorized: Authentication failed
          - InternalServerError
        """
        path = '/organizations/{}/deployments/{}/endpoints/{}'.format(
            organization_id, deployment_id, endpoint)
        payload = {
            'service_id': service_id
        }
        return self._connection.api_request(
            method='PATCH', path=path, json=payload)

    def delete_endpoint(
            self,
            organization_id: str,
            deployment_id: str,
            endpoint: str) -> dict:
        """delete a endpoint

        API reference: DELETE /organizations/<organization_id>/deployments/<deployment_id>/endpoints/<endpoint>

        Request syntax:
            .. code-block:: python

               response = api_client.delete_endpoint(organization_id='1111111111111',
                                                     deployment_id='1111111111111', endpoint='pnt-abc1111111111111')

        Params:
            - **organization_id** (str): organization_id
            - **deployment_id** (str): deployment identifier
            - **endpoint** (str): endpoint identifier or custom alias

        Return type:
            dict

        Responses:
            Response syntax:
                .. code-block:: json

                   {
                       "message": "pnt-abc1111111111111 deleted"
                   }

        Raises:
          - NotFound: endpoint not found
          - Unauthorized: Authentication failed
          - InternalServerError
        """
        path = '/organizations/{}/deployments/{}/endpoints/{}'.format(
            organization_id, deployment_id, endpoint)
        return self._connection.api_request(method='DELETE', path=path)
