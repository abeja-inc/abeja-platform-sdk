.. ABEJA Endpoint Library documentation master file, created by
   sphinx-quickstart on Sat Feb 10 15:14:37 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

================================
ABEJA Endpoint SDK documentation
================================
ABEJA Endpoint library is SDK for python, which allows developers to create, get and delete endpoints.

-------------
Low level API
-------------
Low level API directly accesses the API endpoints.

.. toctree::
   :glob:

   apis/api_client


Usage
-----

.. code-block:: python

   from abeja.endpoints import APIClient

   api_client = APIClient()
   endpoint = api_client.get_endpoint(organization_id, endpoint)


API Mapping
-----------

+----------+--------------------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| method   | path                                                                                 |                                                                                 |
+==========+======================================================================================+=================================================================================+
| post     | /organizations/<organization_id>/deployments/<deployment_id>/endpoints               | :meth:`APIClient.create_endpoint() <abeja.endpoints.APIClient.create_endpoint>` |
+----------+--------------------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| get      | /organizations/<organization_id>/deployments/<deployment_id>/endpoints               | :meth:`APIClient.get_endpoints() <abeja.endpoints.APIClient.get_endpoints>`     |
+----------+--------------------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| get      | /organizations/<organization_id>/deployments/<deployment_id>/endpoints/<endpoint>    | :meth:`APIClient.get_endpoint() <abeja.endpoints.APIClient.get_endpoint>`       |
+----------+--------------------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| patch    | /organizations/<organization_id>/deployments/<deployment_id>/endpoints/<endpoint>    | :meth:`APIClient.update_endpoint() <abeja.endpoints.APIClient.update_endpoint>` |
+----------+--------------------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| delete   | /organizations/<organization_id>/deployments/<deployment_id>/endpoints/<endpoint>    | :meth:`APIClient.delete_endpoint() <abeja.endpoints.APIClient.delete_endpoint>` |
+----------+--------------------------------------------------------------------------------------+---------------------------------------------------------------------------------+