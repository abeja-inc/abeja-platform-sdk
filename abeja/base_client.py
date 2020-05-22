# -*- coding: utf-8 -*-
import os


class BaseClient:
    """base class of ABEJA SDK clients"""

    def __init__(self, organization_id=None, credential=None):
        self.organization_id = organization_id or os.environ.get(
            'ABEJA_ORGANIZATION_ID')
