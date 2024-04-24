from enum import Enum


class OperationMode(Enum):
    ABEJA = 'abeja_platform'
    EDGE = 'edge'
    EDGE_V1 = 'edge_v1'

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_

    @classmethod
    def is_edge(cls, value):
        return value.startswith(OperationMode.EDGE.value + '_v')
