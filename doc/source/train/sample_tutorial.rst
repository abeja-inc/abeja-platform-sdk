
A Sample tutorial
==================
This tutorial describes how to use this SDK for different use cases.


Register Training Job Definition, Training Job Definition Version and Training Job.
-----------------------------------------------------------------------------------

.. code-block:: python

    from abeja.train import APIClient

    client = APIClient()

    # create Training Job Definition
    job_definition_name = 'test_job_definition'
    response = api_client.create_training_job_definition(
        organization_id,
        job_definition_name
    )

    # create Training Job Definition Version
    params = {
        "handler": "train:handler",
        "datasets": {
            "mnist": "1111111111111"
        },
        "image": "abeja-inc/all-cpu:19.04",
        "source_code_base64": "...",
        "user_parameters": {},
        "instance_type": "gpu-1"
    }
    response = api_client.create_training_job_definition_version(
        organization_id,
        job_definition_name,
        params
    )

    # create Training Job
    version_id = 1
    user_parameters = {}
    instance_type = "gpu-1"
    response = api_client.create_training_job(
        organization_id,
        job_definition_name,
        version_id,
        user_parameters,
        instance_type
    )
