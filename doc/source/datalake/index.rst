.. ABEJA Datalake Library documentation master file, created by
   sphinx-quickstart on Sat Feb 10 15:14:37 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

======================================
ABEJA Datalake documentation
======================================
ABEJA Datalake library is SDK for python, which allows developers to create, get and delete datalake resources.

--------------
High level API
--------------
High level API is used following classes.


.. toctree::
   :glob:

   apis/client


Usage
-----


.. code-block:: python

   from abeja.datalake import Client

   client = Client()

-------------
Low level API
-------------
Low level APIs are directly access the API endpoint.


.. toctree::
   :glob:

   apis/api_client


Usage
-----


.. code-block:: python

   from abeja.datalake import APIClient

   api = APIClient()
   channel = api.get_channel(organization_id, channel_id)


API Mapping
------------

.. csv-table::
   :header: method, path, description
   :widths: 5, 256, 256

    post, /organizations/<organization_id>/channels, :meth:`APIClient.create_channel() <abeja.datalake.APIClient.create_channel>`
    get, /organizations/<organization_id>/channels, :meth:`APIClient.list_channels() <abeja.datalake.APIClient.list_channels>`
    get, /organizations/<organization_id>/channels/<channel_id>, :meth:`APIClient.get_channel() <abeja.datalake.APIClient.get_channel>`
    patch, /organizations/<organization_id>/channels/<channel_id>, :meth:`APIClient.patch_channel() <abeja.datalake.APIClient.patch_channel>`
    delete, /organizations/<organization_id>/channels/<channel_id>, :meth:`APIClient.delete_channel() <abeja.datalake.APIClient.delete_channel>`
    get, /organizations/<organization_id>/channels/<channel_id>/datasources, :meth:`APIClient.list_channel_datasources() <abeja.datalake.APIClient.list_channel_datasources>`
    put, /organizations/<organization_id>/channels/<channel_id>/datasources/<datasource_id>, :meth:`APIClient.put_channel_datasource() <abeja.datalake.APIClient.put_channel_datasource>`
    delete, /organizations/<organization_id>/channels/<channel_id>/datasources, :meth:`APIClient.delete_channel_datasource() <abeja.datalake.APIClient.delete_channel_datasource>`
    post, /channels/, :meth:`APIClient.get_channel_file_upload() <abeja.datalake.APIClient.get_channel_file_upload>`
    get, /channels/<channel_id>/, :meth:`APIClient.list_channel_files() <abeja.datalake.APIClient.list_channel_files>`
    get, /channels/<channel_id>/<file_id>, :meth:`APIClient.get_channel_file_download() <abeja.datalake.APIClient.get_channel_file_download>`
    delete, /channels/<channel_id>/<file_id>, :meth:`APIClient.delete_channel_file() <abeja.datalake.APIClient.delete_channel_file>`
    post, /organizations/<organization_id>/buckets, :meth:`APIClient.create_bucket() <abeja.datalake.APIClient.create_bucket>`
    get, /organizations/<organization_id>/buckets, :meth:`APIClient.list_buckets() <abeja.datalake.APIClient.list_buckets>`
    get, /organizations/<organization_id>/buckets/<bucket_id>, :meth:`APIClient.get_bucket() <abeja.datalake.APIClient.get_bucket>`
    patch, /organizations/<organization_id>/buckets/<bucket_id>, :meth:`APIClient.patch_bucket() <abeja.datalake.APIClient.patch_bucket>`
    post, /organizations/<organization_id>/buckets/<bucket_id>/archive, :meth:`APIClient.archive_bucket() <abeja.datalake.APIClient.archive_bucket>`
    post, /organizations/<organization_id>/buckets/<bucket_id>/unarchive, :meth:`APIClient.unarchive_bucket() <abeja.datalake.APIClient.unarchive_bucket>`
    post, /organizations/<organization_id>/buckets/<bucket_id>/files, :meth:`APIClient.upload_bucket_file() <abeja.datalake.APIClient.upload_bucket_file>`
    post, /organizations/<organization_id>/buckets/<bucket_id>/files, :meth:`APIClient.upload_bucket_files() <abeja.datalake.APIClient.upload_bucket_files>`
    get, /organizations/<organization_id>/buckets/<bucket_id>/files, :meth:`APIClient.list_bucket_files() <abeja.datalake.APIClient.list_bucket_files>`
    get, /organizations/<organization_id>/buckets/<bucket_id>/files/<file_id>, :meth:`APIClient.get_bucket_file() <abeja.datalake.APIClient.get_bucket_file>`

--------
Tutorial
--------


.. toctree::
   :glob:

   sample_tutorial
