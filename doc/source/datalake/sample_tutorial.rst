
A Sample tutorial
==================
This tutorial will describe how to use this SDK for different use cases.


Create a datalake channel and upload files to the channel.
--------------------------------------------------------------------

Steps 1: Create a Datalake channel
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    from abeja.datalake import Client as DatalakeClient
    from abeja.datalake.storage_type import StorageType

    organization_id = '1234567890123'
    user_id = 'user-xxxx'
    personal_access_token = 'xxxxx'
    credential = {
        'user_id': user_id,
        'personal_access_token': personal_access_token
    }

    datalake_client = DatalakeClient(organization_id=organization_id, credential=credential)

    name = 'test_channel'
    description = 'a channel for testing'
    channel = datalake_client.channels.create(name, description, StorageType.DATALAKE.value)


Steps 2: Upload file to the Datalake channel
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    from abeja.datalake import Client as DatalakeClient

    organization_id = '1234567890123'
    channel_id = '1230000000000'

    datalake_client = DatalakeClient(organization_id=organization_id)
    channel = datalake_client.get_channel(channel_id)

    file_path = 'test_image.jpeg'
    metadata = {'label': 'testing'}
    file = channel.upload_file(file_path, metadata=metadata)

Steps 3: Get files from the Datalake channel
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    from abeja.datalake import Client as DatalakeClient

    client = DatalakeClient()
    organization_id = '1234567890123'
    channel_id = '1230000000000'

    datalake_client = DatalakeClient(organization_id=organization_id)
    channel = datalake_client.get_channel(channel_id)

    for file in channel.list_files():
        print(file.file_id)

Use channel
------------

Access channel and upload files in a directory.

.. code-block:: python

    from abeja.datalake import Client as DatalakeClient

    client = DatalakeClient()
    channel = client.get_channel(channel_id)
    metadata = {'x-abeja-meta-label': 'cat'}
    files = channel.upload_dir('data/1', metadata=metadata, content_type='image/jpeg')
