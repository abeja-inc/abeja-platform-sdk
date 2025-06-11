.. ABEJA Secret Version Library documentation master file, created by
   sphinx-quickstart on Sat May 01 12:00:00 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

===================================
ABEJA Secret Version SDK documentation
===================================
ABEJA Secret Version library is SDK for python, which allows developers to create, get, update and delete secret versions in Secret Manager.

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

   from abeja.secret_version.api import APIClient

   credential = {"user_id": "user-1111111111111", "personal_access_token": "dummy"}

   try:
      # Get secret versions
      organization_id = "1410000000000"
      secret_id = "3053595942757"
      offset = 0
      limit = 50
      response = APIClient(credential=credential).get_secret_versions(
         organization_id=organization_id,               # [Required] 組織IDを指定してください
         secret_id=secret_id,                          # [Required] シークレットIDを指定してください
         offset=offset,                                # [Optional] バージョンのオフセット（0から開始）
         limit=limit                                   # [Optional] 返却するバージョンの最大数（1から100の間）
      )
      print("Secret Versions:", response)
      
      # Get a specific secret version
      version_id = "1234567890123"
      response = APIClient(credential=credential).get_secret_version(
         organization_id=organization_id,               # [Required] 組織IDを指定してください
         secret_id=secret_id,                          # [Required] シークレットIDを指定してください
         version_id=version_id                         # [Required] バージョンIDを指定してください
      )
      print("Secret Version:", response)
      
      # Create a new secret version
      value = "AKIAIOSFODNN7EXAMPLE"
      response = APIClient(credential=credential).create_secret_version(
         organization_id=organization_id,               # [Required] 組織IDを指定してください
         secret_id=secret_id,                          # [Required] シークレットIDを指定してください
         value=value                                   # [Required] シークレット値を指定してください
      )
      print("Created Secret Version:", response)
      
      # Update a secret version status
      status = "inactive"  # 'active' or 'inactive'
      response = APIClient(credential=credential).update_secret_version(
         organization_id=organization_id,               # [Required] 組織IDを指定してください
         secret_id=secret_id,                          # [Required] シークレットIDを指定してください
         version_id=version_id,                        # [Required] バージョンIDを指定してください
         status=status                                 # [Required] 新しいステータス値 ('active'または'inactive')
      )
      print("Updated Secret Version:", response)
      
      # Delete a secret version
      response = APIClient(credential=credential).delete_secret_version(
         organization_id=organization_id,               # [Required] 組織IDを指定してください
         secret_id=secret_id,                          # [Required] シークレットIDを指定してください
         version_id=version_id                         # [Required] 削除するバージョンIDを指定してください
      )
      print("Delete Result:", response)
   except Exception as e:
      print(f'Failed to operate on secret version | {e}')


API Mapping
-----------

.. csv-table::
   :header: method, path, description
   :widths: 5, 256, 256

   GET, /secret-manager/organizations/<organization_id>/secrets/<secret_id>/versions, :meth:`APIClient.get_secret_versions() <abeja.secret_version.api.client.APIClient.get_secret_versions>`
   GET, /secret-manager/organizations/<organization_id>/secrets/<secret_id>/versions/<version_id>, :meth:`APIClient.get_secret_version() <abeja.secret_version.api.client.APIClient.get_secret_version>`
   POST, /secret-manager/organizations/<organization_id>/secrets/<secret_id>/versions, :meth:`APIClient.create_secret_version() <abeja.secret_version.api.client.APIClient.create_secret_version>`
   PATCH, /secret-manager/organizations/<organization_id>/secrets/<secret_id>/versions/<version_id>, :meth:`APIClient.update_secret_version() <abeja.secret_version.api.client.APIClient.update_secret_version>`
   DELETE, /secret-manager/organizations/<organization_id>/secrets/<secret_id>/versions/<version_id>, :meth:`APIClient.delete_secret_version() <abeja.secret_version.api.client.APIClient.delete_secret_version>`