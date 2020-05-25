from typing import Optional

from abeja.common.api_client import BaseAPIClient


class APIClient(BaseAPIClient):
    """A low-level client for Security API

    .. code-block:: python

       from abeja.security import APIClient

       api_client = APIClient()
    """

    def create_ip_address(self, organization_id: str,
                          payload: Optional[dict] = None) -> dict:
        """create a ip address

        API reference: POST /organizations/<organization_id>/security/cidrs

        Request Syntax:
            .. code-block:: python

               organization_id = "1111111111111"

               payload = {
                   "description": "Example CIDR",
                   "cidr": "192.168.0.0/24"
               }
               response = api_client.create_ip_address(organization_id, payload=payload)

        Params:
            - **organization_id** (str): organization identifier
            - **payload** (dict): payload of ip address
                - **description** (str): description
                - **cidr** (str): cidr

        Return type:
            dict
        Returns:
            Response Syntax:
                .. code-block:: json

                   {
                       "id": "305",
                       "description": "Example CIDR",
                       "cidr": "192.168.0.0/24",
                       "created_at": "2017-04-27T07:49:30Z",
                       "updated_at": "2018-02-14T03:14:05Z"
                   }

        Raises:
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        path = '/organizations/{}/security/cidrs'.format(organization_id)
        return self._connection.api_request(
            method='POST', path=path, json=payload)

    def get_ip_address(self, organization_id: str, cidr_id: str) -> dict:
        """get a ip address

        API reference: GET /organizations/<organization_id>/security/cidrs/<cidr_id>

        Request Syntax:
            .. code-block:: python

               response = api_client.get_ip_address(organization_id='1111111111111', cidr_id='305')

        Params:
            - **organization_id** (str): organization_id
            - **cidr_id** (str): cidr identifier

        Return type:
            dict

        Returns:
            Response Syntax:
                .. code-block:: json

                   {
                       "id": "305",
                       "description": "Example CIDR",
                       "cidr": "192.168.0.0/24",
                       "created_at": "2017-04-27T07:49:30Z",
                       "updated_at": "2018-02-14T03:14:05Z"
                   }

        Raises:
          - NotFound: Ip address not found
          - Unauthorized: Authentication failed
          - InternalServerError
        """
        path = '/organizations/{}/security/cidrs/{}'.format(
            organization_id, cidr_id)
        return self._connection.api_request(method='GET', path=path)

    def get_ip_addresses(self, organization_id: str) -> dict:
        """Get ip address entries

        API reference: GET /organizations/<organization_id>/security/cidrs

        Request syntax:
            .. code-block:: python

               response = api_client.get_ip_addresses(organization_id='1111111111111')

        Params:
            - **organization_id** (str): organization_id

        Return type:
            dict

        Returns:
            Return syntax:
                .. code-block:: json

                   {
                       "organization_id": "1111111111111",
                       "organization_name": "organization-1178",
                       "created_at": "2019-02-19T03:01:49Z",
                       "updated_at": "2019-02-19T03:01:49Z",
                       "offset": 0,
                       "limit": 50,
                       "has_next": false,
                       "cidrs": [
                           "192.168.0.0/24"
                       ]
                   }

        Raises:
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        path = '/organizations/{}/security/cidrs'.format(organization_id)
        return self._connection.api_request(method='GET', path=path)

    def update_ip_address(self, organization_id: str, cidr_id: str,
                          payload: Optional[dict] = None) -> dict:
        """update a ip address

        API reference: PATCH /organizations/<organization_id>/security/cidrs/<cidr_id>

        Request Syntax:
            .. code-block:: python

                payload = {
                    "description": "Example CIDR",
                    "cidr": "192.168.0.0/24"
                }
                response = api_client.update_ip_address(organization_id='1111111111111', cidr_id='305',
                                                        payload=payload)

        Params:
            - **organization_id** (str): organization_id
            - **cidr_id** (str): cidr identifier
            - **payload** (dict): payload of ip address
                - **description** (str): description
                - **cidr** (str): cidr

        Return type:
            dict

        Returns:
            Response Syntax:
                .. code-block:: json

                   {
                       "id": "305",
                       "description": "Example CIDR",
                       "cidr": "192.168.0.0/24",
                       "created_at": "2017-04-27T07:49:30Z",
                       "updated_at": "2018-02-14T03:14:05Z"
                   }

        Raises:
          - NotFound: Ip address not found
          - Unauthorized: Authentication failed
          - InternalServerError
        """
        path = '/organizations/{}/security/cidrs/{}'.format(
            organization_id, cidr_id)
        return self._connection.api_request(
            method='PATCH', path=path, json=payload)

    def delete_ip_address(self, organization_id: str, cidr_id: str) -> dict:
        """delete a ip address

        API reference: DELETE /organizations/<organization_id>/security/cidrs/<cidr_id>

        Request syntax:
            .. code-block:: python

               response = api_client.delete_ip_address(
                   organization_id='1111111111111', cidr_id='305')

        Params:
            - **organization_id** (str): organization_id
            - **cidr_id** (str): cidr identifier

        Return type:
            dict

        Responses:
            Response syntax:
                .. code-block:: json

                   {
                       "id": "305",
                       "description": "Example CIDR",
                       "cidr": "192.168.0.0/24",
                       "created_at": "2017-04-27T07:49:30Z",
                       "updated_at": "2018-02-14T03:14:05Z"
                   }

        Raises:
          - NotFound: ip address not found
          - Unauthorized: Authentication failed
          - InternalServerError
        """
        path = '/organizations/{}/security/cidrs/{}'.format(
            organization_id, cidr_id)
        return self._connection.api_request(method='DELETE', path=path)

    def check_ip_address(self, organization_id: str,
                         payload: Optional[dict] = None) -> dict:
        """check a ip address

        API reference: POST /organizations/<organization_id>/security/cidrs/check

        Request Syntax:
            .. code-block:: python

               organization_id = "1111111111111"

               payload = {
                   "ip_address": "33.222.111.44"
               }
               response = api_client.check_ip_address(organization_id, payload=payload)

        Params:
            - **organization_id** (str): organization identifier
            - **payload** (dict): payload of ip address
                - **ip_address** (str): ip address

        Return type:
            dict
        Returns:
            Response Syntax:
                .. code-block:: json

                   {
                       "accessible": true,
                       "ip_address": "33.222.111.44"
                   }

        Raises:
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        path = '/organizations/{}/security/cidrs/check'.format(organization_id)
        return self._connection.api_request(
            method='POST', path=path, json=payload)
