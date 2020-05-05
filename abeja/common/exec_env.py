from enum import Enum


class ExecEnv(Enum):
    """Set of unique names of execution environments your machine learning
    model running or deployed on.

    - **CLOUD**: ABEJA Platform
    - **EDGE**: An edge device
    - **LOCAL**: train-local via ABEJA SDK/CLI
    - **NONE**: For pre-trained models
    - **UNKNOWN**: Unrecognized value
    """
    CLOUD = 'cloud'
    EDGE = 'edge'
    LOCAL = 'local'
    NONE = 'none'
    UNKNOWN = 'unknown'

    @staticmethod
    def from_value(value: str) -> 'ExecEnv':
        """Get a member by ``value`` if exists, otherwise return ``UNKNOWN``."""
        try:
            return ExecEnv(value)
        except ValueError:
            return ExecEnv.UNKNOWN
