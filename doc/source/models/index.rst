.. ABEJA Dataset Library documentation master file, created by
   sphinx-quickstart on Sat Feb 10 15:14:37 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. warning::
   We're planning to deprecate ``abeja.models`` package in the future version.
   Instead, the :doc:`abeja.training </training/index>` package contains far more detailed new high-level
   APIs. Furthermore, these classes provide more consistent and cleaner interface for developers.

=============================
ABEJA Model SDK documentation
=============================
ABEJA model library is SDK for python, which allows developers to create, get and delete models.

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

   from abeja.models import APIClient

   api_client = APIClient()
   model = api_client.get_model(organization_id, model_id)
   model_versions = api_client.list_model_versions(organization_id, model_id)


API Mapping
-----------

.. csv-table::
   :header: method, path, description
   :widths: 5, 256, 256

    get, /organizations/<organization_id>/training/definitions/<job_definition_name>/models, :meth:`APIClient.get_training_models() <abeja.models.APIClient.get_training_models>`
    post, /organizations/<organization_id>/training/definitions/<job_definition_name>/models, :meth:`APIClient.create_training_model() <abeja.models.APIClient.create_training_model>`
    get, /organizations/<organization_id>/training/definitions/<job_definition_name>/models/<model_id>, :meth:`APIClient.get_training_model() <abeja.models.APIClient.get_training_model>`
    patch, /organizations/<organization_id>/training/definitions/<job_definition_name>/models/<model_id>, :meth:`APIClient.patch_training_model() <abeja.models.APIClient.patch_training_model>`
    get, /organizations/<organization_id>/training/definitions/<job_definition_name>/models/<model_id>/download, :meth:`APIClient.download_training_model() <abeja.models.APIClient.download_training_model>`
    post, /organizations/<organization_id>/training/definitions/<job_definition_name>/models/<model_id>/archive, :meth:`APIClient.archive_training_model() <abeja.models.APIClient.archive_training_model>`
    post, /organizations/<organization_id>/training/definitions/<job_definition_name>/models/<model_id>/unarchive, :meth:`APIClient.unarchive_training_model() <abeja.models.APIClient.unarchive_training_model>`
