.. ABEJA Service Library documentation master file, created by
   sphinx-quickstart on Sat Feb 10 15:14:37 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

=================================
ABEJA Notebook SDK documentation
=================================
ABEJA Notebook library is SDK for python, which allows developers to create, get and delete notebooks.

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

   from abeja.notebook import APIClient

   api_client = APIClient()
   notebook = api_client.get_notebooks(organization_id, job_definition_name)


API Mapping
-----------


+----------+----------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------+
| method   | path                                                                                                           |                                                                                                  |
+==========+================================================================================================================+==================================================================================================+
| post     | /organizations/<organization_id>/training/definitions/<job_definition_name>/notebooks                          | :meth:`APIClient.create_notebook() <abeja.notebook.APIClient.create_notebook>`                   |
+----------+----------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------+
| get      | /organizations/<organization_id>/training/definitions/<job_definition_name>/notebooks                          | :meth:`APIClient.get_notebooks() <abeja.notebook.APIClient.get_notebooks>`                       |
+----------+----------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------+
| get      | /organizations/<organization_id>/training/definitions/<job_definition_name>/notebooks/<notebook_id>            | :meth:`APIClient.get_notebook() <abeja.notebook.APIClient.get_notebook>`                         |
+----------+----------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------+
| patch    | /organizations/<organization_id>/training/definitions/<job_definition_name>/notebooks/<notebook_id>            | :meth:`APIClient.update_notebook() <abeja.notebook.APIClient.update_notebook>`                   |
+----------+----------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------+
| delete   | /organizations/<organization_id>/training/definitions/<job_definition_name>/notebooks/<notebook_id>            | :meth:`APIClient.delete_notebook() <abeja.notebook.APIClient.delete_notebook>`                   |
+----------+----------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------+
| POST     | /organizations/<organization_id>/training/definitions/<job_definition_name>/notebooks/<notebook_id>/stop       | :meth:`APIClient.stop_notebook() <abeja.notebook.APIClient.stop_notebook>`                       |
+----------+----------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------+
| POST     | /organizations/<organization_id>/training/definitions/<job_definition_name>/notebooks/<notebook_id>/start      | :meth:`APIClient.start_notebook() <abeja.notebook.APIClient.start_notebook>`                     |
+----------+----------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------+
| POST     | /organizations/<organization_id>/training/definitions/<job_definition_name>/notebooks/<notebook_id>/recentlogs | :meth:`APIClient.get_notebook_recent_logs() <abeja.notebook.APIClient.get_notebook_recent_logs>` |
+----------+----------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------+