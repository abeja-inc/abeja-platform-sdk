from typing import NamedTuple


__ExecEnv = NamedTuple('ExecEnv', [
    ('value', str),
])


class ExecEnv(__ExecEnv):
    """Set of unique names of execution which environments your machine learning
    model running or deployed on.

    - **CLOUD**: ABEJA Platform
    - **EDGE**: An edge device
    - **LOCAL**: train-local via ABEJA SDK/CLI
    - **NONE**: For pre-trained models
    """

    def __str__(self) -> str:
        return self.value


CLOUD = ExecEnv('cloud')
EDGE = ExecEnv('edge')
LOCAL = ExecEnv('local')
NONE = ExecEnv('none')
