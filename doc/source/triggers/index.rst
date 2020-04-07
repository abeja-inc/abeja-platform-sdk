.. ABEJA Trigger Library documentation master file, created by
   sphinx-quickstart on Sat Feb 10 15:14:37 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

===============================
ABEJA Trigger SDK documentation
===============================
ABEJA Trigger library is SDK for python, which allows developers to create, get and delete triggers.

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

   from abeja.triggers import APIClient

   api_client = APIClient()
   trigger = api_client.get_trigger(organization_id, deployment_id, trigger_id)


API Mapping
-----------


+----------+------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------+
| method   | path                                                                                     |                                                                                  |
+==========+==========================================================================================+==================================================================================+
| post     | /organizations/<organization_id>/deployments/<deployment_id>/triggers                    | :meth:`APIClient.create_trigger() <abeja.triggers.APIClient.create_trigger>`     |
+----------+------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------+
| get      | /organizations/<organization_id>/deployments/<deployment_id>/triggers                    | :meth:`APIClient.get_triggers() <abeja.triggers.APIClient.get_triggers>`         |
+----------+------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------+
| get      | /organizations/<organization_id>/deployments/<deployment_id>/triggers/<trigger_id>       | :meth:`APIClient.get_trigger() <abeja.triggers.APIClient.get_trigger>`           |
+----------+------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------+
| delete   | /organizations/<organization_id>/deployments/<deployment_id>/triggers/<trigger_id>       | :meth:`APIClient.delete_trigger() <abeja.triggers.APIClient.delete_trigger>`     |
+----------+------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------+
| get      | /organizations/<organization_id>/deployments/<deployment_id>/triggers/<trigger_id>/runs  | :meth:`APIClient.get_trigger_runs() <abeja.triggers.APIClient.get_trigger_runs>` |
+----------+------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------+
