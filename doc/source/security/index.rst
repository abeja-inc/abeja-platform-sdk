.. ABEJA Security Library documentation master file, created by
   sphinx-quickstart on Sat Feb 10 15:14:37 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

================================
ABEJA Security SDK documentation
================================
ABEJA Security library is SDK for python, which allows developers to create, get and delete IP address used for access control.

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

   from abeja.security import APIClient

   api_client = APIClient()
   response = api_client.get_ip_address(organization_id, cidr_id)


API Mapping
-----------


+----------+-----------------------------------------------------------+------------------------------------------------------------------------------------+
| method   | path                                                      |                                                                                    |
+==========+===========================================================+====================================================================================+
| post     | /organizations/<organization_id>/security/cidrs           | :meth:`APIClient.create_ip_address() <abeja.security.APIClient.create_ip_address>` |
+----------+-----------------------------------------------------------+------------------------------------------------------------------------------------+
| get      | /organizations/<organization_id>/security/cidrs           | :meth:`APIClient.get_ip_addresses() <abeja.security.APIClient.get_ip_addresses>`   |
+----------+-----------------------------------------------------------+------------------------------------------------------------------------------------+
| get      | /organizations/<organization_id>/security/cidrs/<cidr_id> | :meth:`APIClient.get_ip_address() <abeja.security.APIClient.get_ip_address>`       |
+----------+-----------------------------------------------------------+------------------------------------------------------------------------------------+
| patch    | /organizations/<organization_id>/security/cidrs/<cidr_id> | :meth:`APIClient.update_ip_address() <abeja.security.APIClient.update_ip_address>` |
+----------+-----------------------------------------------------------+------------------------------------------------------------------------------------+
| delete   | /organizations/<organization_id>/security/cidrs/<cidr_id> | :meth:`APIClient.delete_ip_address() <abeja.security.APIClient.delete_ip_address>` |
+----------+-----------------------------------------------------------+------------------------------------------------------------------------------------+
| post     | /organizations/<organization_id>/security/cidrs/check     | :meth:`APIClient.check_ip_address() <abeja.security.APIClient.check_ip_address>`   |
+----------+-----------------------------------------------------------+------------------------------------------------------------------------------------+
