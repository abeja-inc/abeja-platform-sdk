.. ABEJA Registry Library documentation master file, created by
   sphinx-quickstart on Sat Oct 15 18:00:00 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

================================
ABEJA Registry SDK documentation
================================
ABEJA Registry library is SDK for python, which allows developers to create, get and delete docker repositories.

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

   from abeja.registry import APIClient

   api_client = APIClient()
   res = api_client.get_repository(organization_id, repository_id)


API Mapping
-----------


+----------+-----------------------------------------------------------------------------+----------------------------------------------------------------------------------------+
| method   | path                                                                        |                                                                                        |
+==========+=============================================================================+========================================================================================+
| post     | /organizations/<organization_id>/registry/repositories                      | :meth:`APIClient.create_repository() <abeja.registry.APIClient.create_repository>`     |
+----------+-----------------------------------------------------------------------------+----------------------------------------------------------------------------------------+
| get      | /organizations/<organization_id>/registry/repositories                      | :meth:`APIClient.get_repositories() <abeja.registry.APIClient.get_repositories>`       |
+----------+-----------------------------------------------------------------------------+----------------------------------------------------------------------------------------+
| get      | /organizations/<organization_id>/registry/repositories/<repository_id>      | :meth:`APIClient.get_repository() <abeja.registry.APIClient.get_repository>`           |
+----------+-----------------------------------------------------------------------------+----------------------------------------------------------------------------------------+
| delete   | /organizations/<organization_id>/registry/repositories/<repository_id>      | :meth:`APIClient.delete_repository() <abeja.registry.APIClient.delete_repository>`     |
+----------+-----------------------------------------------------------------------------+----------------------------------------------------------------------------------------+
| get      | /organizations/<organization_id>/registry/repositories/<repository_id>/tags | :meth:`APIClient.get_repository_tags() <abeja.registry.APIClient.get_repository_tags>` |
+----------+-----------------------------------------------------------------------------+----------------------------------------------------------------------------------------+
