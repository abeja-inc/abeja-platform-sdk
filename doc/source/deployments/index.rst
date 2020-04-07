.. ABEJA Deployment Library documentation master file, created by
   sphinx-quickstart on Sat Feb 10 15:14:37 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

==================================
ABEJA Deployment SDK documentation
==================================
ABEJA Deployment library is SDK for python, which allows developers to create, get and delete deployments.

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

   from abeja.deployments import APIClient

   api_client = APIClient()
   deployment = api_client.get_deployment(organization_id, deployment_id)


API Mapping
-----------

.. csv-table::
   :header: method, path, description
   :widths: 5, 256, 256

    post, /organizations/<organization_id>/models/<model_id>/deployments, **DEPRECATED** :meth:`APIClient.create_deployment() <abeja.deployments.APIClient.create_deployment>`
    post, /organizations/<organization_id>/deployments, :meth:`APIClient.create_deployment() <abeja.deployments.APIClient.create_deployment>`
    get, /organizations/<organization_id>/deployments, :meth:`APIClient.get_deployments() <abeja.deployments.APIClient.get_deployments>`
    get, /organizations/<organization_id>/deployments/<deployment_id>, :meth:`APIClient.get_deployment() <abeja.deployments.APIClient.get_deployment>`
    delete, /organizations/<organization_id>/deployments/<deployment_id>, :meth:`APIClient.delete_deployment() <abeja.deployments.APIClient.delete_deployment>`
    get, /organizations/<organization_id>/deployments/<deployment_id>/versions, :meth:`APIClient.get_deployment_versions() <abeja.deployments.APIClient.get_deployment_versions>`
    post, /organizations/<organization_id>/deployments/<deployment_id>/versions, :meth:`APIClient.create_deployment_version() <abeja.deployments.APIClient.create_deployment_version>`
    get, /organizations/<organization_id>/deployments/<deployment_id>/versions/<version_id>, :meth:`APIClient.get_deployment_version() <abeja.deployments.APIClient.get_deployment_version>`
    delete, /organizations/<organization_id>/deployments/<deployment_id>/versions/<version_id>, :meth:`APIClient.delete_deployment_version() <abeja.deployments.APIClient.delete_deployment_version>`
    get, /organizations/<organization_id>/deployments/<deployment_id>/versions/<version_id>/download, :meth:`APIClient.download_deployment_version() <abeja.deployments.APIClient.download_deployment_version>`
