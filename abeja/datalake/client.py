from typing import Dict, Optional

from abeja.base_client import BaseClient
from .channel import Channel
from .channel import Channels
from abeja.datalake import APIClient


class Client(BaseClient):
    """A high-level client for Datalake API

    .. code-block:: python

       from abeja.datalake import Client

       client = Client()
    """

    def __init__(
            self, organization_id: Optional[str] = None,
            credential: Optional[Dict[str, str]] = None,
            timeout: Optional[int] = None,
            max_retry_count: Optional[int] = None) -> None:
        super().__init__(organization_id, credential)
        self.api = APIClient(
            credential=credential,
            timeout=timeout,
            max_retry_count=max_retry_count)

    def get_channel(self, channel_id) -> Channel:
        """Get channel for specific channel_id

        Request syntax:
            .. code-block:: python

                channel = client.get_channel(channel_id='1111111111111')

        Params:
            - **channel_id** (str): channel id

        Return type:
            :class:`Channel <abeja.datalake.channel.Channel>` object
        """
        channels = Channels(self.api, self.organization_id)
        return channels.get(channel_id)

    @property
    def channels(self) -> Channels:
        """Get channel objects

        Request syntax:
            .. code-block:: python

                channels = client.channels

        Returns:
            :class:`Channels <abeja.datalake.channel.Channels>` object
        """
        return Channels(self.api, self.organization_id)
