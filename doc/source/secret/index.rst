.. ABEJA Secret Library documentation master file, created by
   sphinx-quickstart on Sat May 01 12:00:00 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

==============================
ABEJA Secret SDK documentation
==============================
ABEJA Secret library is SDK for python, which allows developers to create, get, update and delete secrets in Secret Manager.

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

   from abeja.secret.api import APIClient

   credential = {"user_id": "user-1111111111111", "personal_access_token": "dummy"}

   try:
      # Get a list of secrets
      organization_id = "1410000000000"
      offset = 0
      limit = 50
      response = APIClient(credential=credential).get_secrets(
         organization_id=organization_id,               # [Required] 組織IDを指定してください
         offset=offset,                                # [Optional] シークレットのオフセット（0から開始）
         limit=limit                                   # [Optional] 返却するシークレットの最大数（1から100の間）
      )
      print("Secrets:", response)
      
      # Get a specific secret
      secret_id = "3053595942757"
      response = APIClient(credential=credential).get_secret(
         organization_id=organization_id,               # [Required] 組織IDを指定してください
         secret_id=secret_id                           # [Required] シークレットIDを指定してください
      )
      print("Secret:", response)
      
      # Create a new secret
      name = "AWS_ACCESS_KEY"
      value = "AKIAIOSFODNN7EXAMPLE"
      description = "AWS access key"
      expired_at = "2024-12-15T16:50:33+09:00"
      response = APIClient(credential=credential).create_secret(
         organization_id=organization_id,               # [Required] 組織IDを指定してください
         name=name,                                    # [Required] シークレット名を指定してください
         value=value,                                  # [Required] シークレット値を指定してください
         description=description,                      # [Optional] シークレットの説明
         expired_at=expired_at                        # [Optional] 有効期限（ISO 8601形式）
      )
      print("Created Secret:", response)
      
      # Update a secret
      response = APIClient(credential=credential).update_secret(
         organization_id=organization_id,               # [Required] 組織IDを指定してください
         secret_id=secret_id,                          # [Required] シークレットIDを指定してください
         description="Updated AWS access key",         # [Optional] 更新するシークレットの説明
         expired_at="2025-12-15T16:50:33+09:00"       # [Optional] 更新する有効期限（ISO 8601形式）
      )
      print("Updated Secret:", response)
      
      # Delete a secret
      response = APIClient(credential=credential).delete_secret(
         organization_id=organization_id,               # [Required] 組織IDを指定してください
         secret_id=secret_id                           # [Required] シークレットIDを指定してください
      )
      print("Delete Result:", response)
   except Exception as e:
      print(f'Failed to operate on secret | {e}')


API Mapping
-----------

.. csv-table::
   :header: method, path, description
   :widths: 5, 256, 256

   GET, /secret-manager/organizations/<organization_id>/secrets, :meth:`APIClient.get_secrets() <abeja.secret.api.client.APIClient.get_secrets>`
   GET, /secret-manager/organizations/<organization_id>/secrets/<secret_id>, :meth:`APIClient.get_secret() <abeja.secret.api.client.APIClient.get_secret>`
   POST, /secret-manager/organizations/<organization_id>/secrets, :meth:`APIClient.create_secret() <abeja.secret.api.client.APIClient.create_secret>`
   PATCH, /secret-manager/organizations/<organization_id>/secrets/<secret_id>, :meth:`APIClient.update_secret() <abeja.secret.api.client.APIClient.update_secret>`
   DELETE, /secret-manager/organizations/<organization_id>/secrets/<secret_id>, :meth:`APIClient.delete_secret() <abeja.secret.api.client.APIClient.delete_secret>`