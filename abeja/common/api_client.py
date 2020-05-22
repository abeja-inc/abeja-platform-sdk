from typing import Optional

from abeja.common.connection import Connection


class BaseAPIClient:
    """A low-level client for ABEJA Platform API"""

    def __init__(
            self,
            credential: Optional[dict] = None,
            timeout: Optional[int] = None,
            max_retry_count: Optional[int] = None):
        self._connection = Connection(credential, timeout, max_retry_count)
