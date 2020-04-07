.. ABEJA Dataset Library documentation master file, created by
   sphinx-quickstart on Sat Feb 10 15:14:37 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

===========================
ABEJA Dataset documentation
===========================
ABEJA dataset library is (SDK) for python, which allow developers to create, get and delete dataset and dataset items.


--------------
High level API
--------------
High level APIs are used trough following classes.

.. toctree::
   :glob:

   apis/client


Usage
-----


.. code-block:: python

   from abeja.datasets import Client

   client = Client(organization_id)
   dataset = client.get_dataset(dataset_id)
   for item in dataset.dataset_items.list():
      pass


API Mapping
-----------

+-------------+-------------------------------------------------------------------+-------------------------------------------------------------------------------------------+
| method      | path                                                              |                                                                                           |
+=============+===================================================================+===========================================================================================+
| post        | /organizations/<organization_id>/datasets                         | :meth:`Datasets.create() <abeja.datasets.dataset.Datasets.create>`                        |
+-------------+-------------------------------------------------------------------+-------------------------------------------------------------------------------------------+
| get         | /organizations/<organization_id>/datasets                         | :meth:`Datasets.list() <abeja.datasets.dataset.Datasets.list>`                            |
+-------------+-------------------------------------------------------------------+-------------------------------------------------------------------------------------------+
| get         | /organizations/<organization_id>/datasets/<id>                    | :meth:`Datasets.get() <abeja.datasets.dataset.Datasets.get>`                              |
+-------------+-------------------------------------------------------------------+-------------------------------------------------------------------------------------------+
| delete      | /organizations/<organization_id>/datasets/<id>                    | :meth:`Datasets.delete() <abeja.datasets.dataset.Datasets.delete>`                        |
+-------------+-------------------------------------------------------------------+-------------------------------------------------------------------------------------------+
| post        | /organizations/<organization_id>/datasets/<dataset_id>/items      | :meth:`DatasetItems.create() <abeja.datasets.dataset_item.DatasetItems.create>`           |
+-------------+-------------------------------------------------------------------+-------------------------------------------------------------------------------------------+
| get         | /organizations/<organization_id>/datasets/<dataset_id>/items      | :meth:`DatasetItems.list() <abeja.datasets.dataset_item.DatasetItems.list>`               |
+-------------+-------------------------------------------------------------------+-------------------------------------------------------------------------------------------+
| get         | /organizations/<organization_id>/datasets/<dataset_id>/items/<id> | :meth:`DatasetItems.get() <abeja.datasets.dataset_item.DatasetItems.get>`                 |
+-------------+-------------------------------------------------------------------+-------------------------------------------------------------------------------------------+
| update      | /organizations/<organization_id>/datasets/<dataset_id>/items/<id> | :meth:`DatasetItems.update() <abeja.datasets.dataset_item.DatasetItems.update>`           |
+-------------+-------------------------------------------------------------------+-------------------------------------------------------------------------------------------+
| bulk_update | /organizations/<organization_id>/datasets/<dataset_id>/items      | :meth:`DatasetItems.bulk_update() <abeja.datasets.dataset_item.DatasetItems.bulk_update>` |
+-------------+-------------------------------------------------------------------+-------------------------------------------------------------------------------------------+
| delete      | /organizations/<organization_id>/datasets/<dataset_id>/items/<id> | :meth:`DatasetItems.delete() <abeja.datasets.dataset_item.DatasetItems.delete>`           |
+-------------+-------------------------------------------------------------------+-------------------------------------------------------------------------------------------+


-------------
Low level API
-------------
Low lavel apis are directly access the api endpoint.

.. toctree::
   :glob:

   apis/api_client


Usage
-----


.. code-block:: python

   from abeja.datasets import APIClient

   api = APIClient()
   dataset = api.get_dataset(organization_id, dataset_id)
   dataset_items = api.list_dataset_items(organization_id, dataset_id)


API Mapping
-----------


+-------------+-------------------------------------------------------------------+--------------------------------------------------------------------------------------------------+
| method      | path                                                              |                                                                                                  |
+=============+===================================================================+==================================================================================================+
| post        | /organizations/<organization_id>/datasets                         | :meth:`APIClient.create_dataset() <abeja.datasets.APIClient.create_dataset>`                     |
+-------------+-------------------------------------------------------------------+--------------------------------------------------------------------------------------------------+
| get         | /organizations/<organization_id>/datasets                         | :meth:`APIClient.list_datasets() <abeja.datasets.APIClient.list_datasets>`                       |
+-------------+-------------------------------------------------------------------+--------------------------------------------------------------------------------------------------+
| get         | /organizations/<organization_id>/datasets/<id>                    | :meth:`APIClient.get_dataset() <abeja.datasets.APIClient.get_dataset>`                           |
+-------------+-------------------------------------------------------------------+--------------------------------------------------------------------------------------------------+
| delete      | /organizations/<organization_id>/datasets/<id>                    | :meth:`APIClient.delete_dataset() <abeja.datasets.APIClient.delete_dataset>`                     |
+-------------+-------------------------------------------------------------------+--------------------------------------------------------------------------------------------------+
| post        | /organizations/<organization_id>/datasets/<dataset_id>/items      | :meth:`APIClient.create_dataset_item() <abeja.datasets.APIClient.create_dataset_item>`           |
+-------------+-------------------------------------------------------------------+--------------------------------------------------------------------------------------------------+
| get         | /organizations/<organization_id>/datasets/<dataset_id>/items      | :meth:`APIClient.list_dataset_items() <abeja.datasets.APIClient.list_dataset_items>`             |
+-------------+-------------------------------------------------------------------+--------------------------------------------------------------------------------------------------+
| get         | /organizations/<organization_id>/datasets/<dataset_id>/items/<id> | :meth:`APIClient.get_dataset_item() <abeja.datasets.APIClient.get_dataset_item>`                 |
+-------------+-------------------------------------------------------------------+--------------------------------------------------------------------------------------------------+
| update      | /organizations/<organization_id>/datasets/<dataset_id>/items/<id> | :meth:`APIClient.update_dataset_item() <abeja.datasets.APIClient.update_dataset_item>`           |
+-------------+-------------------------------------------------------------------+--------------------------------------------------------------------------------------------------+
| bulk_update | /organizations/<organization_id>/datasets/<dataset_id>/items      | :meth:`APIClient.bulk_update_dataset_item() <abeja.datasets.APIClient.bulk_update_dataset_item>` |
+-------------+-------------------------------------------------------------------+--------------------------------------------------------------------------------------------------+
| delete      | /organizations/<organization_id>/datasets/<dataset_id>/items/<id> | :meth:`APIClient.delete_dataset_item() <abeja.datasets.APIClient.delete_dataset_item>`           |
+-------------+-------------------------------------------------------------------+--------------------------------------------------------------------------------------------------+


--------
Tutorial
--------


.. toctree::
   :glob:

   sample_tutorial
