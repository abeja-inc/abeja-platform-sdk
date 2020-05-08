ABEJA Training documentation (abeja.training)
=============================================
ABEJA training library is SDK for python, which allows developers to create, get and delete training related resources.

--------------
High level API
--------------
High-level API is used through following classes.

.. toctree::
   :glob:

   apis/client

Usage
-----

.. code-block:: python

   from abeja.training import Client, JobStatus

   client = Client()
   adapter = client.job_definitions()
   definition = adapter.get('flower-classification')

   for job in definition.jobs().list():
      if job.status == JobStatus.COMPLETE:
         print('Job {} was completed!', job.job_id)


-------------
Low level API
-------------
Low-Level API directly accesses the API endpoint.


.. toctree::
   :glob:

   apis/api_client


Usage
-----

.. code-block:: python

   from abeja.training import APIClient

   api = APIClient()
   job_definitions = api.get_training_job_definitions(organization_id)


API Mapping
-----------

+--------+---------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------+
| method |                                                     path                                                      |                                                                                                                              |
+========+===============================================================================================================+==============================================================================================================================+
| post   | /organizations/<organization_id>/training/definitions                                                         | :meth:`APIClient.create_training_job_definition() <abeja.training.APIClient.create_training_job_definition>`                 |
+--------+---------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------+
| get    | /organizations/<organization_id>/training/definitions                                                         | :meth:`APIClient.get_training_job_definitions() <abeja.training.APIClient.get_training_job_definitions>`                     |
+--------+---------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------+
| get    | /organizations/<organization_id>/training/definitions/<job_definition_name>                                   | :meth:`APIClient.get_training_job_definition() <abeja.training.APIClient.get_training_job_definition>`                       |
+--------+---------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------+
| post   | /organizations/<organization_id>/training/definitions/<job_definition_name>/archive                           | :meth:`APIClient.archive_training_job_definition() <abeja.training.APIClient.archive_training_job_definition>`               |
+--------+---------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------+
| post   | /organizations/<organization_id>/training/definitions/<job_definition_name>/unarchive                         | :meth:`APIClient.unarchive_training_job_definition() <abeja.training.APIClient.unarchive_training_job_definition>`           |
+--------+---------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------+
| delete | /organizations/<organization_id>/training/definitions/<job_definition_name>                                   | :meth:`APIClient.delete_training_job_definition() <abeja.training.APIClient.delete_training_job_definition>`                 |
+--------+---------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------+
| post   | /organizations/<organization_id>/training/definitions/<job_definition_name>/versions                          | :meth:`APIClient.create_training_job_definition_version() <abeja.training.APIClient.create_training_job_definition_version>` |
+--------+---------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------+
| get    | /organizations/<organization_id>/training/definitions/<job_definition_name>/versions                          | :meth:`APIClient.get_training_job_definition_versions() <abeja.training.APIClient.get_training_job_definition_versions>`     |
+--------+---------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------+
| get    | /organizations/<organization_id>/training/definitions/<job_definition_name>/versions/<version_id>             | :meth:`APIClient.get_training_job_definition_version() <abeja.training.APIClient.get_training_job_definition_version>`       |
+--------+---------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------+
| patch  | /organizations/<organization_id>/training/definitions/<job_definition_name>/versions/<version_id>             | :meth:`APIClient.patch_training_job_definition_version() <abeja.training.APIClient.patch_training_job_definition_version>`   |
+--------+---------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------+
| delete | /organizations/<organization_id>/training/definitions/<job_definition_name>/versions/<version_id>             | :meth:`APIClient.delete_training_job_definition_version() <abeja.training.APIClient.delete_training_job_definition_version>` |
+--------+---------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------+
| post   | /organizations/<organization_id>/training/definitions/<job_definition_name>/versions/<version_id>/jobs        | :meth:`APIClient.create_training_job() <abeja.training.APIClient.create_training_job>`                                       |
+--------+---------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------+
| get    | /organizations/<organization_id>/training/definitions/<job_definition_name>/jobs                              | :meth:`APIClient.get_training_jobs() <abeja.training.APIClient.get_training_jobs>`                                           |
+--------+---------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------+
| get    | /organizations/<organization_id>/training/definitions/<job_definition_name>/jobs/<training_job_id>            | :meth:`APIClient.get_training_job() <abeja.training.APIClient.get_training_job>`                                             |
+--------+---------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------+
| post   | /organizations/<organization_id>/training/definitions/<job_definition_name>/jobs/<training_job_id>/stop       | :meth:`APIClient.stop_training_job() <abeja.training.APIClient.stop_training_job>`                                           |
+--------+---------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------+
| get    | /organizations/<organization_id>/training/definitions/<job_definition_name>/jobs/<training_job_id>/result     | :meth:`APIClient.get_training_result() <abeja.training.APIClient.get_training_result>`                                       |
+--------+---------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------+
| delete | /organizations/<organization_id>/training/definitions/<job_definition_name>/jobs/<training_job_id>/statistics | :meth:`APIClient.update_statistics() <abeja.training.APIClient.update_statistics>`                                           |
+--------+---------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------+


--------
Tutorial
--------

.. toctree::
   :glob:

   sample_tutorial
