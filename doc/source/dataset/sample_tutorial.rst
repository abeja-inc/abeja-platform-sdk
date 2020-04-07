
A Sample tutorial
==================
This tutorial will describe how to use this SDK for different use cases.


Register dataset and dataset items
----------------------------------

Steps 1: Upload data item to datalake
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Use  ABEJA_Console_, Datalake_API_, ABEJA_CLI_ to upload data to datalake.

.. _ABEJA_Console: https://console.abeja.io/datalake

.. _Datalake_API: https://developers.abeja.io/api/datalake-api/

.. _ABEJA_CLI: https://developers.abeja.io/cli/datalake-command/upload/


Step 2-1: Create Classification Dataset and Dataset Items
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    from abeja.datasets import Client

    ORGANIZATION_ID = '1102940376065'
    client = Client(organization_id=ORGANIZATION_ID)

    props = {
        "categories": [
            {
                "labels": [
                    {
                        "label_id": 1,
                        "label": "dog"
                    },
                    {
                        "label_id": 2,
                        "label": "cat"
                    },
                    {
                        "label_id": 3,
                        "label": "others"
                    }
                ],
                "category_id": 1,
                "name": "cats_dogs"
            }
        ]
    }
    dataset = client.datasets.create(name='test_dataset', type='classification', props=props)

    source_data = [
        {
            'data_type': 'image/jpeg',
            'data_uri': 'datalake://1200123803688/20170815T044617-f20dde80-1e3b-4496-bc06-1b63b026b872',
            'height': 500,
            'width': 200
        }
    ]

    attributes = {
        'classification': [
            {
                'category_id': 1,
                'label_id': 1
            }
        ]
    }
    dataset_item = dataset.dataset_items.create(
        source_data=source_data, attributes=attributes)


Step 2-2: Create Detection Dataset and Dataset Items
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    from abeja.datasets import Client

    ORGANIZATION_ID = '1102940376065'
    client = Client(organization_id=ORGANIZATION_ID)

    props = {
        "categories": [
            {
                "labels": [
                    {
                        "label_id": 1,
                        "label": "dog"
                    },
                    {
                        "label_id": 2,
                        "label": "cat"
                    },
                    {
                        "label_id": 3,
                        "label": "others"
                    }
                ],
                "category_id": 1,
                "name": "cats_dogs"
            }
        ]
    }

    dataset = client.datasets.create(name='test-dataset', type='detection', props=props)

    source_data = [
        {
            'data_type': 'image/jpeg',
            'data_uri': 'datalake://1200123803688/20170815T044617-f20dde80-1e3b-4496-bc06-1b63b026b872',
            'height': 500,
            'width': 200
        }
    ]

    attributes = {
        'detection': [
            {
                'category_id': 1,
                'label_id': 2,
                'rect': {
                    'xmin': 22,
                    'ymin': 145,
                    'xmax': 140,
                    'ymax': 220
                }
            }
        ]
    }
    dataset_item = dataset.dataset_items.create(source_data=source_data, attributes=attributes)


Use datasets
------------

Access datasets from training source and use dataset for training.

.. code-block:: python

    from abeja.datasets import Client

    client = Client()
    dataset = client.get_dataset(dataset_id)

    for item in dataset.dataset_items.list(prefetch=True):
        # Get data from the dataset source
        file_content = item.source_data[0].get_content()

        # Get attribute of that dataset
        label = item.attributes['classification'][0]['label_id']
