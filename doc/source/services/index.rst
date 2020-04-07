.. ABEJA Service Library documentation master file, created by
   sphinx-quickstart on Sat Feb 10 15:14:37 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

===============================
ABEJA Service SDK documentation
===============================
ABEJA Service library is SDK for python, which allows developers to create, get and delete services.

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

   from abeja.services import APIClient

   api_client = APIClient()
   service = api_client.get_service(organization_id, deployment_id, service_id)


API Mapping
-----------


+----------+------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------+
| method   | path                                                                                     |                                                                                  |
+==========+==========================================================================================+==================================================================================+
| post     | /organizations/<organization_id>/deployments/<deployment_id>/services                    | :meth:`APIClient.create_service() <abeja.services.APIClient.create_service>`     |
+----------+------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------+
| get      | /organizations/<organization_id>/deployments/<deployment_id>/services                    | :meth:`APIClient.get_services() <abeja.services.APIClient.get_services>`         |
+----------+------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------+
| get      | /organizations/<organization_id>/deployments/<deployment_id>/services/<service_id>       | :meth:`APIClient.get_service() <abeja.services.APIClient.get_service>`           |
+----------+------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------+
| patch    | /organizations/<organization_id>/deployments/<deployment_id>/services/<service_id>       | :meth:`APIClient.update_service() <abeja.services.APIClient.update_service>`     |
+----------+------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------+
| delete   | /organizations/<organization_id>/deployments/<deployment_id>/services/<service_id>       | :meth:`APIClient.delete_service() <abeja.services.APIClient.delete_service>`     |
+----------+------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------+
| POST     | /organizations/<organization_id>/deployments/<deployment_id>/services/<service_id>/stop  | :meth:`APIClient.stop_service() <abeja.services.APIClient.stop_service>`         |
+----------+------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------+
| POST     | /organizations/<organization_id>/deployments/<deployment_id>/services/<service_id>/start | :meth:`APIClient.start_service() <abeja.services.APIClient.start_service>`       |
+----------+------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------+