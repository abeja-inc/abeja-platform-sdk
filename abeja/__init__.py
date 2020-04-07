# flake8: noqa
from typing import Optional

from .version import VERSION
from .tracking import Tracking


def tracking(total_steps: Optional[int] = None):
    return Tracking(total_steps=total_steps)
