.. ABEJA Training Library documentation master file, created by
   sphinx-quickstart on Sat Feb 10 15:14:37 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. warning::
   We're planning to deprecate ``abeja.train`` package in the future version.
   Instead, the :doc:`abeja.training </training/index>` package contains far more detailed new high-level
   APIs. Furthermore, these classes provide more consistent and cleaner interface for developers.

==========================================
ABEJA Training documentation (abeja.train)
==========================================
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

   from abeja.train import Client
   from abeja.train.statistics import Statistics as ABEJAStatistics

   client = Client()

   statistics = ABEJAStatistics(num_epochs=10, epoch=1)
   statistics.add_stage(name=ABEJAStatistics.STAGE_TRAIN, accuracy=90.0, loss=0.10)
   statistics.add_stage(name=ABEJAStatistics.STAGE_VALIDATION, accuracy=75.0, loss=0.07)

   client.update_statistics(statistics)


API Mapping
-----------


+----------+---------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------+
| method   | path                                                                                                          |                                                                                         |
+==========+===============================================================================================================+=========================================================================================+
| get      | /organizations/<organization_id>/training/definitions/<job_definition_name>/jobs/<training_job_id>/result     | :meth:`Client.download_training_result() <abeja.train.Client.download_training_result>` |
+----------+---------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------+
| post     | /organizations/<organization_id>/training/definitions/<job_definition_name>/jobs/<training_job_id>/statistics | :meth:`Client.update_statistics() <abeja.train.Client.update_statistics>`               |
+----------+---------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------+

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

   from abeja.train import APIClient

   api = APIClient()
   job_definitions = api.get_training_job_definitions(organization_id)


API Mapping
-----------

+----------+---------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------+
| method   | path                                                                                                          |                                                                                                                            |
+==========+===============================================================================================================+============================================================================================================================+
| post     | /organizations/<organization_id>/training/definitions                                                         | :meth:`APIClient.create_training_job_definition() <abeja.train.APIClient.create_training_job_definition>`                  |
+----------+---------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------+
| get      | /organizations/<organization_id>/training/definitions                                                         | :meth:`APIClient.get_training_job_definitions() <abeja.train.APIClient.get_training_job_definitions>`                      |
+----------+---------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------+
| get      | /organizations/<organization_id>/training/definitions/<job_definition_name>                                   | :meth:`APIClient.get_training_job_definition() <abeja.train.APIClient.get_training_job_definition>`                        |
+----------+---------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------+
| delete   | /organizations/<organization_id>/training/definitions/<job_definition_name>                                   | :meth:`APIClient.delete_training_job_definition() <abeja.train.APIClient.delete_training_job_definition>`                  |
+----------+---------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------+
| post     | /organizations/<organization_id>/training/definitions/<job_definition_name>/versions                          | :meth:`APIClient.create_training_job_definition_version() <abeja.train.APIClient.create_training_job_definition_version>`  |
+----------+---------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------+
| get      | /organizations/<organization_id>/training/definitions/<job_definition_name>/versions                          | :meth:`APIClient.get_training_job_definition_versions() <abeja.train.APIClient.get_training_job_definition_versions>`      |
+----------+---------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------+
| get      | /organizations/<organization_id>/training/definitions/<job_definition_name>/versions/<version_id>             | :meth:`APIClient.get_training_job_definition_version() <abeja.train.APIClient.get_training_job_definition_version>`        |
+----------+---------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------+
| delete   | /organizations/<organization_id>/training/definitions/<job_definition_name>/versions/<version_id>             | :meth:`APIClient.delete_training_job_definition_version() <abeja.train.APIClient.delete_training_job_definition_version>`  |
+----------+---------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------+
| post     | /organizations/<organization_id>/training/definitions/<job_definition_name>/versions/<version_id>/jobs        | :meth:`APIClient.create_training_job() <abeja.train.APIClient.create_training_job>`                                        |
+----------+---------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------+
| get      | /organizations/<organization_id>/training/definitions/<job_definition_name>/jobs                              | :meth:`APIClient.get_training_jobs() <abeja.train.APIClient.get_training_jobs>`                                            |
+----------+---------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------+
| get      | /organizations/<organization_id>/training/definitions/<job_definition_name>/jobs/<training_job_id>            | :meth:`APIClient.get_training_job() <abeja.train.APIClient.get_training_job>`                                              |
+----------+---------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------+
| post     | /organizations/<organization_id>/training/definitions/<job_definition_name>/jobs/<training_job_id>/stop       | :meth:`APIClient.stop_training_job() <abeja.train.APIClient.stop_training_job>`                                            |
+----------+---------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------+
| get      | /organizations/<organization_id>/training/definitions/<job_definition_name>/jobs/<training_job_id>/result     | :meth:`APIClient.get_training_result() <abeja.train.APIClient.get_training_result>`                                        |
+----------+---------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------+
| delete   | /organizations/<organization_id>/training/definitions/<job_definition_name>/jobs/<training_job_id>/statistics | :meth:`APIClient.update_statistics() <abeja.train.APIClient.update_statistics>`                                            |
+----------+---------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------+


--------
Tutorial
--------

.. toctree::
   :glob:

   sample_tutorial
