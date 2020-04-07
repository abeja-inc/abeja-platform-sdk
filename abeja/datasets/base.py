# -*- coding: utf-8 -*-
class DatasetBase:
    def _set_values(self, values):
        for k, v in values.items():
            if not hasattr(self, k) or not getattr(self, k):
                setattr(self, k, v)
