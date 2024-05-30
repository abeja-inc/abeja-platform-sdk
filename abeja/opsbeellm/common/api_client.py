from typing import Optional

from abeja.opsbeellm.common.connection import OpsBeeLLMConnection


class OpsBeeLLMBaseAPIClient:
    """A low-level client for ABEJA Platform OpsBeeLLM API"""

    def __init__(
            self,
            credential: Optional[dict] = None,
            timeout: Optional[int] = None,
            max_retry_count: Optional[int] = None):
        self._connection = OpsBeeLLMConnection(credential, timeout, max_retry_count)
