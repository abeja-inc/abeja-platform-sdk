.. ABEJA Training Library documentation master file, created by
   sphinx-quickstart on Sat Feb 10 15:14:37 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

============================
ABEJA Training documentation
============================
ABEJA training library is SDK for python, which allows developers to create, get and delete training related resources.

--------------
High level API
--------------
High-level API is used trough following classes.

.. toctree::
   :glob:

   apis/client

Usage
-----


.. code-block:: python

   from abeja.training import Client
   from abeja.training.statistics import Statistics as ABEJAStatistics

   client = Client()

   statistics = ABEJAStatistics(num_epochs=10, epoch=1)
   statistics.add_stage(name=ABEJAStatistics.STAGE_TRAIN, accuracy=90.0, loss=0.10)
   statistics.add_stage(name=ABEJAStatistics.STAGE_VALIDATION, accuracy=75.0, loss=0.07)

   client.update_statistics(statistics)


API Mapping
-----------


+--------+---------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------+
| method |                                                     path                                                      |                                                                                            |
+========+===============================================================================================================+============================================================================================+
| get    | /organizations/<organization_id>/training/definitions/<job_definition_name>/jobs/<training_job_id>/result     | :meth:`Client.download_training_result() <abeja.training.Client.download_training_result>` |
+--------+---------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------+
| post   | /organizations/<organization_id>/training/definitions/<job_definition_name>/jobs/<training_job_id>/statistics | :meth:`Client.update_statistics() <abeja.training.Client.update_statistics>`               |
+--------+---------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------+

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
| delete | /organizations/<organization_id>/training/definitions/<job_definition_name>                                   | :meth:`APIClient.delete_training_job_definition() <abeja.training.APIClient.delete_training_job_definition>`                 |
+--------+---------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------+
| post   | /organizations/<organization_id>/training/definitions/<job_definition_name>/versions                          | :meth:`APIClient.create_training_job_definition_version() <abeja.training.APIClient.create_training_job_definition_version>` |
+--------+---------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------+
| get    | /organizations/<organization_id>/training/definitions/<job_definition_name>/versions                          | :meth:`APIClient.get_training_job_definition_versions() <abeja.training.APIClient.get_training_job_definition_versions>`     |
+--------+---------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------+
| get    | /organizations/<organization_id>/training/definitions/<job_definition_name>/versions/<version_id>             | :meth:`APIClient.get_training_job_definition_version() <abeja.training.APIClient.get_training_job_definition_version>`       |
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
