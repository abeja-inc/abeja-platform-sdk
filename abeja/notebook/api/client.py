from typing import Optional

from abeja.common.api_client import BaseAPIClient
from abeja.notebook.types import InstanceType, ImageType, NotebookType


class APIClient(BaseAPIClient):
    """A Low-Level client for Notebook API

    .. code-block:: python

       from abeja.notebook import APIClient

       api_client = APIClient()
    """

    def create_notebook(
            self,
            organization_id: str,
            job_definition_name: str,
            instance_type: Optional[str] = None,
            image: Optional[str] = None,
            notebook_type: Optional[str] = None) -> dict:
        """create a notebook.

        API reference: POST /organizations/{organization_id}/training/definitions/{job_definition_name}/notebooks

        Request Syntax:
            .. code-block:: python

                organization_id = "1410000000000"
                job_definition_name = "test_job_definition"
                instance_type = 'cpu-1'
                image = 'abeja-inc/all-cpu:19.10'
                notebook_type = 'lab'
                response = api_client.create_notebook(
                    organization_id, job_definition_name,
                    instance_type, image, notebook_type
                )
        Params:
            - **organization_id** (str): organization id
            - **job_definition_name** (str): training job definition name
            - **instance_type** (str): **[optional]** instance type (ex. cpu-1)
            - **image** (str): **[optional]** runtime environment (ex. abeja-inc/all-cpu:19.10)
            - **notebook_type** (str): **[optional]** notebook type (notebook or lab)

        Return type:
            dict

        Returns:
            Response Syntax:
                .. code-block:: python

                    {
                        "job_definition_id": "1234567890123",
                        "training_notebook_id": "1410000000000",
                        "name": "notebook-3",
                        "description": None,
                        "status": "Pending",
                        "status_message": None,
                        "instance_type": "cpu-1",
                        "image": "abeja-inc/all-cpu:18.10",
                        "creator": {
                            "updated_at": "2018-01-04T03:02:12Z",
                            "role": "admin",
                            "is_registered": True,
                            "id": "1122334455660",
                            "email": "test@abeja.asia",
                            "display_name": None,
                            "created_at": "2017-05-26T01:38:46Z"
                        },
                        "created_at": "2018-06-07T04:42:34.913644Z",
                        "modified_at": "2018-06-07T04:42:34.913726Z"
                    }
        Raises:
            - NotFound
            - BadRequest
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        params = {}
        if instance_type is not None and InstanceType.to_enum(instance_type):
            params['instance_type'] = instance_type
        if image is not None and ImageType.to_enum(image):
            params['image'] = image
        if notebook_type is not None and NotebookType.to_enum(notebook_type):
            params['notebook_type'] = notebook_type
        path = '/organizations/{}/training/definitions/{}/notebooks'.format(
            organization_id, job_definition_name)
        return self._connection.api_request(
            method='POST', path=path, json=params)

    def get_notebooks(
            self,
            organization_id: str,
            job_definition_name: str) -> dict:
        """get notebooks.

        API reference: GET /organizations/{organization_id}/training/definitions/{job_definition_name}/notebooks

        Request Syntax:
            .. code-block:: python

                organization_id = "1410000000000"
                job_definition_name = "test_job_definition"
                response = api_client.get_notebooks(
                    organization_id, job_definition_name
                )
        Params:
            - **organization_id** (str): organization id
            - **job_definition_name** (str): training job definition name

        Return type:
            dict

        Returns:
            Response Syntax:
                .. code-block:: python

                    {
                            "total": 1,
                            "offset": 0,
                            "limit": 10,
                            "entries": [
                                {
                                "job_definition_id": "1234567890123",
                                "training_notebook_id": "1410000000000",
                                "name": "notebook-3",
                                "description": None,
                                "status": "Pending",
                                "status_message": None,
                                "instance_type": "cpu-1",
                                "image": "abeja-inc/all-cpu:18.10",
                                "creator": {
                                    "updated_at": "2018-01-04T03:02:12Z",
                                    "role": "admin",
                                    "is_registered": True,
                                    "id": "1122334455660",
                                    "email": "test@abeja.asia",
                                    "display_name": None,
                                    "created_at": "2017-05-26T01:38:46Z"
                                },
                                "created_at": "2018-06-07T04:42:34.913644Z",
                                "modified_at": "2018-06-07T04:42:34.913726Z"
                                }
                            ]
                        }

        Raises:
            - NotFound
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        path = '/organizations/{}/training/definitions/{}/notebooks'.format(
            organization_id, job_definition_name)
        return self._connection.api_request(method='GET', path=path)

    def get_notebook(
            self,
            organization_id: str,
            job_definition_name: str,
            notebook_id: str=None) -> dict:
        """get a notebook.

        API reference: GET /organizations/{organization_id}/training/definitions/{job_definition_name}/notebooks/{notebook_id}

        Request Syntax:
            .. code-block:: python

                organization_id = "1410000000000"
                job_definition_name = "test_job_definition"
                notebook_id = "1230000000000"
                response = api_client.get_notebook(
                    organization_id, job_definition_name, notebook_id
                )
        Params:
            - **organization_id** (str): organization id
            - **job_definition_name** (str): training job definition name
            - **notebook_id** (str): notebook id

        Return type:
            dict

        Returns:
            Response Syntax:
                .. code-block:: python

                    {
                        "job_definition_id": "1234567890123",
                        "training_notebook_id": "1410000000000",
                        "name": "notebook-3",
                        "description": None,
                        "status": "Pending",
                        "status_message": None,
                        "instance_type": "cpu-1",
                        "image": "abeja-inc/all-cpu:18.10",
                        "creator": {
                            "updated_at": "2018-01-04T03:02:12Z",
                            "role": "admin",
                            "is_registered": True,
                            "id": "1122334455660",
                            "email": "test@abeja.asia",
                            "display_name": None,
                            "created_at": "2017-05-26T01:38:46Z"
                        },
                        "created_at": "2018-06-07T04:42:34.913644Z",
                        "modified_at": "2018-06-07T04:42:34.913726Z"
                    }

        Raises:
            - NotFound
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        path = '/organizations/{}/training/definitions/{}/notebooks/{}'.format(
            organization_id, job_definition_name, notebook_id)
        return self._connection.api_request(method='GET', path=path)

    def update_notebook(
            self,
            organization_id: str,
            job_definition_name: str,
            notebook_id: str,
            instance_type: Optional[str] = None,
            image: Optional[str] = None,
            notebook_type: Optional[str] = None) -> dict:
        """update a notebook.

        API reference: PUT /organizations/{organization_id}/training/definitions/{job_definition_name}/notebooks/{notebook_id}

        Request Syntax:
            .. code-block:: python

                organization_id = "1410000000000"
                job_definition_name = "test_job_definition"
                notebook_id = "1230000000000"
                instance_type = 'cpu-1'
                image = 'abeja-inc/all-cpu:19.10'
                response = api_client.update_notebook(
                    organization_id, job_definition_name, notebook_id,
                    instance_type=instance_type, image=image
                )
        Params:
            - **organization_id** (str): organization id
            - **job_definition_name** (str): training job definition name
            - **notebook_id** (str): notebook id
            - **instance_type** (str): **[optional]** instance type (ex. cpu-1)
            - **image** (str): **[optional]** runtime environment (ex. abeja-inc/all-cpu:19.10)
            - **notebook_type** (str): **[optional]** notebook type (notebook or lab)

        Return type:
            dict

        Returns:
            Response Syntax:
                .. code-block:: python

                    {
                        "job_definition_id": "1234567890123",
                        "training_notebook_id": 0,
                        "name": "notebook-3",
                        "description": None,
                        "status": "Pending",
                        "status_message": None,
                        "instance_type": "cpu-1",
                        "image": "abeja-inc/all-cpu:18.10",
                        "creator": {
                            "updated_at": "2018-01-04T03:02:12Z",
                            "role": "admin",
                            "is_registered": True,
                            "id": "1122334455660",
                            "email": "test@abeja.asia",
                            "display_name": None,
                            "created_at": "2017-05-26T01:38:46Z"
                        },
                        "created_at": "2018-06-07T04:42:34.913644Z",
                        "modified_at": "2018-06-07T04:42:34.913726Z"
                    }

        Raises:
            - NotFound
            - BadRequest
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        params = {}
        if instance_type is not None and InstanceType.to_enum(instance_type):
            params['instance_type'] = instance_type
        if image is not None and ImageType.to_enum(image):
            params['image'] = image
        if notebook_type is not None and NotebookType.to_enum(notebook_type):
            params['notebook_type'] = notebook_type
        path = '/organizations/{}/training/definitions/{}/notebooks/{}'.format(
            organization_id, job_definition_name, notebook_id)
        return self._connection.api_request(
            method='PUT', path=path, json=params)

    def delete_notebook(
            self,
            organization_id: str,
            job_definition_name: str,
            notebook_id: str) -> dict:
        """delete a notebook.

        API reference: DELETE /organizations/{organization_id}/training/definitions/{job_definition_name}/notebooks/{notebook_id}

        Request Syntax:
            .. code-block:: python

                organization_id = "1410000000000"
                job_definition_name = "test_job_definition"
                notebook_id = "1230000000000"
                response = api_client.delete_notebook(
                    organization_id, job_definition_name, notebook_id
                )
        Params:
            - **organization_id** (str): organization id
            - **job_definition_name** (str): training job definition name
            - **notebook_id** (str): notebook id

        Return type:
            dict

        Returns:
            Response Syntax:
                .. code-block:: python

                    {
                        "value": {
                            "message": "1111111111111 deleted"
                        }
                    }
        Raises:
            - NotFound
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        path = '/organizations/{}/training/definitions/{}/notebooks/{}'.format(
            organization_id, job_definition_name, notebook_id)
        return self._connection.api_request(method='DELETE', path=path)

    def start_notebook(
            self,
            organization_id: str,
            job_definition_name: str,
            notebook_id: str,
            notebook_type: Optional[str] = None) -> dict:
        """start a notebook.

        API reference: POST /organizations/{organization_id}/training/definitions/{job_definition_name}/notebooks/{notebook_id}/start

        Request Syntax:
            .. code-block:: python

                organization_id = "1410000000000"
                job_definition_name = "test_job_definition"
                notebook_id = "1230000000000"
                response = api_client.start_notebook(
                    organization_id, job_definition_name, notebook_id
                )
        Params:
            - **organization_id** (str): organization id
            - **job_definition_name** (str): training job definition name
            - **notebook_id** (str): notebook id
            - **notebook_type** (str): **[optional]** notebook type (notebook or lab)

        Return type:
            dict

        Returns:
            Response Syntax:
                .. code-block:: python

                    {
                        "job_definition_id": "1234567890123",
                        "training_notebook_id": 0,
                        "name": "notebook-3",
                        "description": None,
                        "status": "Pending",
                        "status_message": None,
                        "instance_type": "cpu-1",
                        "image": "abeja-inc/all-cpu:18.10",
                        "creator": {
                            "updated_at": "2018-01-04T03:02:12Z",
                            "role": "admin",
                            "is_registered": True,
                            "id": "1122334455660",
                            "email": "test@abeja.asia",
                            "display_name": None,
                            "created_at": "2017-05-26T01:38:46Z"
                        },
                        "created_at": "2018-06-07T04:42:34.913644Z",
                        "modified_at": "2018-06-07T04:42:34.913726Z"
                    }

        Raises:
            - NotFound
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        params = {}
        if notebook_type is not None and NotebookType.to_enum(notebook_type):
            params['notebook_type'] = notebook_type
        path = '/organizations/{}/training/definitions/{}/notebooks/{}/start'.format(
            organization_id, job_definition_name, notebook_id)
        return self._connection.api_request(
            method='POST', path=path, json=params)

    def stop_notebook(
            self,
            organization_id: str,
            job_definition_name: str,
            notebook_id: str) -> dict:
        """stop a notebook.

        API reference: POST /organizations/{organization_id}/training/definitions/{job_definition_name}/notebooks/{notebook_id}/stop

        Request Syntax:
            .. code-block:: python

                organization_id = "1410000000000"
                job_definition_name = "test_job_definition"
                notebook_id = "1230000000000"
                response = api_client.stop_notebook(
                    organization_id, job_definition_name, notebook_id
                )
        Params:
            - **organization_id** (str): organization id
            - **job_definition_name** (str): training job definition name
            - **notebook_id** (str): notebook id

        Return type:
            dict

        Returns:
            Response Syntax:
                .. code-block:: python

                    {
                        "job_definition_id": "1234567890123",
                        "training_notebook_id": 0,
                        "name": "notebook-3",
                        "description": None,
                        "status": "Pending",
                        "status_message": None,
                        "instance_type": "cpu-1",
                        "image": "abeja-inc/all-cpu:18.10",
                        "creator": {
                            "updated_at": "2018-01-04T03:02:12Z",
                            "role": "admin",
                            "is_registered": True,
                            "id": "1122334455660",
                            "email": "test@abeja.asia",
                            "display_name": None,
                            "created_at": "2017-05-26T01:38:46Z"
                        },
                        "created_at": "2018-06-07T04:42:34.913644Z",
                        "modified_at": "2018-06-07T04:42:34.913726Z"
                    }

        Raises:
            - NotFound
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        path = '/organizations/{}/training/definitions/{}/notebooks/{}/stop'.format(
            organization_id, job_definition_name, notebook_id)
        return self._connection.api_request(method='POST', path=path, json={})

    def get_notebook_recent_logs(
        self,
        organization_id: str,
        job_definition_name: str,
        notebook_id: str,
        next_forward_token: Optional[str]=None,
        next_backward_token: Optional[str]=None,
    ) -> dict:
        """get recent logs of the notebook.

        API reference: GET /organizations/{organization_id}/training/definitions/{job_definition_name}/notebooks/{notebook_id}/recentlogs

        Request Syntax:
            .. code-block:: python

                organization_id = "1410000000000"
                job_definition_name = "test_job_definition"
                notebook_id = "1230000000000"
                response = api_client.get_notebook_recent_logs(
                    organization_id, job_definition_name, notebook_id
                )
        Params:
            - **organization_id** (str): organization id
            - **job_definition_name** (str): training job definition name
            - **notebook_id** (str): notebook id
            - **next_forward_token** (str): **[optional]** token for the next page of logs
            - **next_backward_token** (str): **[optional]** token for the next previous of logs

        Return type:
            dict

        Returns:
            Response Syntax:
                .. code-block:: python

                    {
                        "events": [
                            {
                            "message": "start executing model with abeja-runtime-python36 (version: 0.X.X)",
                            "timestamp": "2019-10-16T00:00:00.000Z"
                            }
                        ],
                        "next_backward_token": "...",
                        "next_forward_token": "..."
                    }

        Raises:
            - NotFound
            - Unauthorized: Authentication failed
            - InternalServerError
        """
        params = {}
        if next_forward_token:
            params['next_forward_token'] = next_forward_token
        if next_backward_token:
            params['next_backward_token'] = next_backward_token
        path = '/organizations/{}/training/definitions/{}/notebooks/{}/recentlogs'.format(
            organization_id, job_definition_name, notebook_id)
        return self._connection.api_request(
            method='GET', path=path, params=params)
