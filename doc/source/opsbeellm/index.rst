.. ABEJA OpsBeeLLM Library documentation master file, created by
   sphinx-quickstart on Sat Feb 10 15:14:37 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

==================================
ABEJA OpsBeeLLM SDK documentation
==================================
ABEJA OpsBeeLLM library is SDK for python, which allows developers to create, get and delete OpsBeeLLM resources.

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

   from abeja.opsbeellm.history import APIClient as OpsBeeLLMHisotryAPIClient

   credential = {"user_id": "user-1111111111111", "personal_access_token": "dummy"}

   try:
      resp_history = OpsBeeLLMHistoryAPIClient(credential=credential).create_qa_history(
            organization_id="1111111111111",               # [Required] オーガニゼーションIDを指定してください
            deployment_id="2222222222222",                 # [Required] 作成したデプロイメントのIDを指定してください
            input_text="ABEJAについて教えて",                 # [Required] LLM への入力文を入力してください
            output_text="ABEJAは、スペイン語で「ミツバチ」の意味であり、植物の受粉を手伝い、世界の食料生産を支える存在として社名になっています。",  # [Required] LLM からの応答文を入力してください
            input_token_count=None,                        # [Optional] 必要に応じて、LLM への入力文のトークン数を指定してください。
            output_token_count=None,                       # [Optional] 必要に応じて、LLM からの出力文のトークン数を指定してください。
            tag_ids=[                                      # [Optional] 必要に応じて、入出力履歴に付与するためのタグのIDを List 型で設定してください。タグはあとからでも追加できます。
               '3333333333333',
               '4444444444444',
            ],
            metadata=[                                     # [Optional] 必要に応じて、入出力ペア履歴に関連付けさせたい key-value 形式のメタデータを List[dict] 型で設定してください。メタデータはあとからでも設定できます
               {"関連部署": "ABEJA全体"},
               {"model_name": "gpt-3.5-turbo-0613"},
               {"temperature": "0.0"},
            ],
         )
      print("resp_history: ", resp_history)
   except Exception as e:
      print(f'Faild to create qa history | {e}')


API Mapping (OpsBeeLLM Deployment)
-----------

.. csv-table::
   :header: method, path, description
   :widths: 5, 256, 256

   post, /opsbee-llm/organizations/<organization_id>/deployments, :meth:`APIClient.create_deployment() <abeja.opsbeellm.deployment.APIClient.create_deployment>`
   get, /opsbee-llm/organizations/<organization_id>/deployments, :meth:`APIClient.get_deployments() <abeja.opsbeellm.deployment.APIClient.get_deployments>`
   get, /opsbee-llm/organizations/<organization_id>/deployments/<deployment_id>, :meth:`APIClient.get_deployment() <abeja.opsbeellm.deployment.APIClient.get_deployment>`
   delete, /opsbee-llm/organizations/<organization_id>/deployments/<deployment_id>, :meth:`APIClient.delete_deployment() <abeja.opsbeellm.deployment.APIClient.delete_deployment>`
   patch, /opsbee-llm/organizations/<organization_id>/deployments/<deployment_id>, :meth:`APIClient.update_deployment() <abeja.opsbeellm.deployment.APIClient.update_deployment>`


API Mapping (OpsBeeLLM Thread)
-----------

.. csv-table::
   :header: method, path, description
   :widths: 5, 256, 256

   post, /opsbee-llm/organizations/<organization_id>/deployments/<deployment_id>/threads, :meth:`APIClient.create_thread() <abeja.opsbeellm.history.APIClient.create_thread>`
   get, /opsbee-llm/organizations/<organization_id>/deployments/<deployment_id>/threads, :meth:`APIClient.get_threads() <abeja.opsbeellm.history.APIClient.get_threads>`
   get, /opsbee-llm/organizations/<organization_id>/deployments/<deployment_id>/threads/<thread_id>, :meth:`APIClient.get_thread() <abeja.opsbeellm.history.APIClient.get_thread>`
   delete, /opsbee-llm/organizations/<organization_id>/deployments/<deployment_id>/threads/<thread_id>, :meth:`APIClient.delete_thread() <abeja.opsbeellm.history.APIClient.delete_thread>`
   patch, /opsbee-llm/organizations/<organization_id>/deployments/<deployment_id>/threads/<thread_id>, :meth:`APIClient.update_thread() <abeja.opsbeellm.history.APIClient.update_thread>`


API Mapping (OpsBeeLLM History)
-----------

.. csv-table::
   :header: method, path, description
   :widths: 5, 256, 256

   post, /opsbee-llm/organizations/<organization_id>/deployments/<deployment_id>/qa_histories, :meth:`APIClient.create_qa_history() <abeja.opsbeellm.history.APIClient.create_qa_history>`
   get, /opsbee-llm/organizations/<organization_id>/deployments/<deployment_id>/qa_histories, :meth:`APIClient.get_qa_histories() <abeja.opsbeellm.history.APIClient.get_qa_histories>`
   get, /opsbee-llm/organizations/<organization_id>/deployments/<deployment_id>/qa_histories/<history_id>, :meth:`APIClient.get_qa_history() <abeja.opsbeellm.history.APIClient.get_qa_history>`
   delete, /opsbee-llm/organizations/<organization_id>/deployments/<deployment_id>/qa_histories/<history_id>, :meth:`APIClient.delete_qa_history() <abeja.opsbeellm.history.APIClient.delete_qa_history>`
   patch, /opsbee-llm/organizations/<organization_id>/deployments/<deployment_id>/qa_histories/<history_id>, :meth:`APIClient.update_qa_history() <abeja.opsbeellm.history.APIClient.update_qa_history>`

   post, /opsbee-llm/organizations/<organization_id>/deployments/<deployment_id>/threads/<thread_id>/histories, :meth:`APIClient.create_chat_history() <abeja.opsbeellm.history.APIClient.create_chat_history>`
   get, /opsbee-llm/organizations/<organization_id>/deployments/<deployment_id>/threads/<thread_id>/histories, :meth:`APIClient.get_chat_histories() <abeja.opsbeellm.history.APIClient.get_chat_histories>`
   get, /opsbee-llm/organizations/<organization_id>/deployments/<deployment_id>/threads/<thread_id>/histories/<history_id>, :meth:`APIClient.get_chat_history() <abeja.opsbeellm.history.APIClient.get_chat_history>`
   delete, /opsbee-llm/organizations/<organization_id>/deployments/<deployment_id>/threads/<thread_id>/histories/<history_id>, :meth:`APIClient.delete_chat_history() <abeja.opsbeellm.history.APIClient.delete_chat_history>`
   patch, /opsbee-llm/organizations/<organization_id>/deployments/<deployment_id>/threads/<thread_id>/histories/<history_id>, :meth:`APIClient.update_chat_history() <abeja.opsbeellm.history.APIClient.update_chat_history>`


API Mapping (OpsBeeLLM History Metadata)
-----------

.. csv-table::
   :header: method, path, description
   :widths: 5, 256, 256

   post, /opsbee-llm/organizations/<organization_id>/deployments/<deployment_id>/qa_histories/<history_id>/metadata, :meth:`APIClient.create_qa_history_metadata() <abeja.opsbeellm.history.APIClient.create_qa_history_metadata>`
   delete, /opsbee-llm/organizations/<organization_id>/deployments/<deployment_id>/qa_histories/<history_id>/metadata, :meth:`APIClient.delete_qa_history_metadata() <abeja.opsbeellm.history.APIClient.delete_qa_history_metadata>`
   patch, /opsbee-llm/organizations/<organization_id>/deployments/<deployment_id>/qa_histories/<history_id>/metadata, :meth:`APIClient.update_qa_history_metadata() <abeja.opsbeellm.history.APIClient.update_qa_history_metadata>`

   post, /opsbee-llm/organizations/<organization_id>/deployments/<deployment_id>/threads/<thread_id>/histories/<history_id>/metadata, :meth:`APIClient.create_chat_history_metadata() <abeja.opsbeellm.history.APIClient.create_chat_history_metadata>`
   delete, /opsbee-llm/organizations/<organization_id>/deployments/<deployment_id>/threads/<thread_id>/histories/<history_id>/metadata, :meth:`APIClient.delete_chat_history_metadata() <abeja.opsbeellm.history.APIClient.delete_chat_history_metadata>`
   patch, /opsbee-llm/organizations/<organization_id>/deployments/<deployment_id>/threads/<thread_id>/histories/<history_id>/metadata, :meth:`APIClient.update_chat_history_metadata() <abeja.opsbeellm.history.APIClient.update_chat_history_metadata>`


API Mapping (OpsBeeLLM Tags)
-----------

.. csv-table::
   :header: method, path, description
   :widths: 5, 256, 256

   post, /opsbee-llm/organizations/<organization_id>/tags, :meth:`APIClient.create_tag() <abeja.opsbeellm.history.APIClient.create_tag>`
   get, /opsbee-llm/organizations/<organization_id>/tags, :meth:`APIClient.get_tags() <abeja.opsbeellm.history.APIClient.get_tags>`
   get, /opsbee-llm/organizations/<organization_id>/tags/<tag_id>, :meth:`APIClient.get_tag() <abeja.opsbeellm.history.APIClient.get_tag>`
   delete, /opsbee-llm/organizations/<organization_id>/tags/<tag_id>, :meth:`APIClient.delete_tag() <abeja.opsbeellm.history.APIClient.delete_tag>`
   patch, /opsbee-llm/organizations/<organization_id>/tags/<tag_id>, :meth:`APIClient.update_tag() <abeja.opsbeellm.history.APIClient.update_tag>`


API Mapping (OpsBeeLLM Dataset)
-----------

.. csv-table::
   :header: method, path, description
   :widths: 5, 256, 256

   post, /opsbee-llm/organizations/<organization_id>/datasets, :meth:`APIClient.create_dataset() <abeja.opsbeellm.dataset.APIClient.create_dataset>`
   get, /opsbee-llm/organizations/<organization_id>/datasets, :meth:`APIClient.get_datasets() <abeja.opsbeellm.dataset.APIClient.get_datasets>`
   get, /opsbee-llm/organizations/<organization_id>/datasets/<dataset_id>, :meth:`APIClient.get_dataset() <abeja.opsbeellm.dataset.APIClient.get_dataset>`
   delete, /opsbee-llm/organizations/<organization_id>/datasets/<dataset_id>, :meth:`APIClient.delete_dataset() <abeja.opsbeellm.dataset.APIClient.delete_dataset>`
   patch, /opsbee-llm/organizations/<organization_id>/datasets/<dataset_id>, :meth:`APIClient.update_dataset() <abeja.opsbeellm.dataset.APIClient.update_dataset>`

   post, /opsbee-llm/organizations/<organization_id>/datasets/<dataset_id>/items, :meth:`APIClient.create_dataset_item() <abeja.opsbeellm.dataset.APIClient.create_dataset_item>`
   get, /opsbee-llm/organizations/<organization_id>/datasets/<dataset_id>/items, :meth:`APIClient.get_dataset_items() <abeja.opsbeellm.dataset.APIClient.get_dataset_items>`
   get, /opsbee-llm/organizations/<organization_id>/datasets/<dataset_id>/items/<item_id>, :meth:`APIClient.get_dataset_item() <abeja.opsbeellm.dataset.APIClient.get_dataset_item>`
   delete, /opsbee-llm/organizations/<organization_id>/datasets/<dataset_id>/items/<item_id>, :meth:`APIClient.delete_dataset_item() <abeja.opsbeellm.dataset.APIClient.delete_dataset_item>`
   patch, /opsbee-llm/organizations/<organization_id>/datasets/<dataset_id>/items/<item_id>, :meth:`APIClient.update_dataset_item() <abeja.opsbeellm.dataset.APIClient.update_dataset_item>`
