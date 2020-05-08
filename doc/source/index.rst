.. ABEJA SDK Library documentation master file, created by
   sphinx-quickstart on Sat Feb 10 15:14:37 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

========================
ABEJA SDK documentation!
========================
ABEJA SDK is Libirary for python, which allow developers to create, get and delete ABEJA Platform resources.

Contents:

.. toctree::
   :maxdepth: 2

   dataset/index
   training/index
   train/index
   notebooks/index
   datalake/index
   models/index
   deployments/index
   security/index
   services/index
   endpoints/index
   runs/index
   triggers/index
   registry/index

==============
Authentication
==============

There are two ways to set credential information for ABEJA Platform SDK usage.

.. _authentication_environment_variables:

Environment Variables
=====================

ABEJA Platform SDK reads env vars with keys below and use these as credential information.

+--------------------------------------+--------------------------------------------------------------------+
| Variable Name                        | Description                                                        |
+======================================+====================================================================+
| ABEJA_ORGANIZATION_ID                | Organization Identifier                                            |
+--------------------------------------+--------------------------------------------------------------------+
| ABEJA_PLATFORM_USER_ID               | User Identifier (which starts with `user-` )                       |
+--------------------------------------+--------------------------------------------------------------------+
| ABEJA_PLATFORM_PERSONAL_ACCESS_TOKEN | User's Personal Access Token                                       |
+--------------------------------------+--------------------------------------------------------------------+


.. _authentication_client_parameter:

Client Parameter
================

ABEJA Platform SDK Client accepts credential information when instantiating.
It is required to passing parameters in different way between high level interface and low level interface.

High Level Interface
--------------------

.. code-block:: python

   from abeja.datalake import Client

   organization_id = '1234567890123'
   credential = {
       'user_id': 'user-1234567890123',
       'personal_access_token': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
   }
   client = Client(organization_id=organization_id, credential=credential)
   channel = client.get_channel(channel_id='9999999999999')

You can set connection_timeout and max_retry_count to Client.

.. code-block:: python

   from abeja.datalake import Client

   organization_id = '1234567890123'
   credential = {
       'user_id': 'user-1234567890123',
       'personal_access_token': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
   }
   client = Client(organization_id=organization_id, credential=credential, timeout=60, max_retry_count=10)



Low Level Interface
-------------------

.. code-block:: python

   from abeja.datalake import APIClient

   organization_id = '1234567890123'
   credential = {
       'user_id': 'user-1234567890123',
       'personal_access_token': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
   }
   client = APIClient(credential=credential)
   channel = client.get_channel(organization_id=organization_id, channel_id='9999999999999')

You can set connection_timeout and max_retry_count to APIClient.

.. code-block:: python

   from abeja.datalake import APIClient

   organization_id = '1234567890123'
   credential = {
       'user_id': 'user-1234567890123',
       'personal_access_token': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
   }
   client = APIClient(credential=credential, timeout=60, max_retry_count=10)


Environment Variables
=====================

ABEJA Platform SDK reads env vars with keys below and use as http request parameters.

+--------------------------------------+-------------------------------------------------------------------------------+
| Variable Name                        | Description                                                                   |
+======================================+===============================================================================+
| ABEJA_SDK_CONNECTION_TIMEOUT         | Connection timeout of http request to API. Specify in seconds. Default is 30. |
+--------------------------------------+-------------------------------------------------------------------------------+
| ABEJA_SDK_MAX_RETRY_COUNT            | Max retry count of http request to API. Default is 5.                         |
+--------------------------------------+-------------------------------------------------------------------------------+

Priority
========

There are multiple ways to pass the credentials that are checked in the following order/priority.

1. `credential` passed in client object initialization.
2. `PLATFORM_AUTH_TOKEN` in environment variables.
3. `ABEJA_PLATFORM_USER_ID` and `ABEJA_PLATFORM_PERSONAL_ACCESS_TOKEN` in environment variables.

Priority of connetion_timeout and max_retry_count is as below.

1. `connetion_timeout` / `max_retry_count` passed as argument to Client and APIClient
2. Environment variables.
3. Default values.

==================
Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
