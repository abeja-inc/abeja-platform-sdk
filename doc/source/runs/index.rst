.. ABEJA Run Library documentation master file, created by
   sphinx-quickstart on Sat Feb 10 15:14:37 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

===============================
ABEJA Run SDK documentation
===============================
ABEJA Run library is SDK for python, which allows developers to create, get and delete runs.

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

   from abeja.runs import APIClient

   api_client = APIClient()
   run = api_client.get_run(organization_id, deployment_id, run_id)


API Mapping
-----------


+----------+---------------------------------------------------------------------------------------+------------------------------------------------------------------------------------+
| method   | path                                                                                  |                                                                                    |
+==========+=======================================================================================+====================================================================================+
| post     | /organizations/<organization_id>/deployments/<deployment_id>/runs                     | :meth:`APIClient.create_run() <abeja.runs.APIClient.create_run>`                   |
+----------+---------------------------------------------------------------------------------------+------------------------------------------------------------------------------------+
| get      | /organizations/<organization_id>/deployments/<deployment_id>/runs                     | :meth:`APIClient.get_runs() <abeja.runs.APIClient.get_runs>`                       |
+----------+---------------------------------------------------------------------------------------+------------------------------------------------------------------------------------+
| get      | /organizations/<organization_id>/deployments/<deployment_id>/runs/<run_id>            | :meth:`APIClient.get_run() <abeja.runs.APIClient.get_run>`                         |
+----------+---------------------------------------------------------------------------------------+------------------------------------------------------------------------------------+
| get      | /organizations/<organization_id>/deployments/<deployment_id>/runs/<run_id>/logs       | :meth:`APIClient.get_run_logs() <abeja.runs.APIClient.get_run_logs>`               |
+----------+---------------------------------------------------------------------------------------+------------------------------------------------------------------------------------+
| get      | /organizations/<organization_id>/deployments/<deployment_id>/runs/<run_id>/recentlogs | :meth:`APIClient.get_run_recent_logs() <abeja.runs.APIClient.get_run_recent_logs>` |
+----------+---------------------------------------------------------------------------------------+------------------------------------------------------------------------------------+
