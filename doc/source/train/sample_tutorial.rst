
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
    filepaths = ["requirements.txt"]
    handler = "train:handler",
    image = "abeja-inc/all-cpu:19.04",
    environment = {},
    response = api_client.create_training_job_definition_version(
        organization_id,
        job_definition_name,
        filepaths,
        handler,
        image=image,
        environment=environment
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
