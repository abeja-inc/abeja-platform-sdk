from typing import Optional, NamedTuple
from enum import Enum


class CPUType(Enum):
    """CPU/GPU
    """
    CPU = 'cpu'
    GPU = 'gpu'


class CPUCategory(Enum):
    """CPU/GPU category

    CPU/GPU can be divided into several categories depending on
    their performance in ABEJA Platform.
    """
    A = 'a'
    B = 'b'
    C = 'c'
    D = 'd'


__InstanceType = NamedTuple('InstanceType', [
    ('cpu_type', CPUType),
    ('cpu_category', Optional[CPUCategory]),
    ('cpu', float),
])


class InstanceType(__InstanceType):
    """InstanceType defines container's CPU/GPU and memory.

    An instance type is generally formatted as ``{CPUType}-{cpu}`` or
    ``{CPUType}:{CPUCategory}-{cpu}`` (e.g. ``cpu-0.25``, ``gpu:b-2``)
    """

    @staticmethod
    def parse(value: str) -> 'InstanceType':
        items = value.split('-', maxsplit=1)
        if len(items) != 2:
            raise ValueError('invalid format: {}'.format(value))

        cpu = float(items[1])
        items = items[0].split(':', maxsplit=1)
        if len(items) == 1:
            cpu_type = CPUType(items[0])
            cpu_category = None
        elif len(items) == 2:
            cpu_type = CPUType(items[0])
            cpu_category = CPUCategory(items[1])
        else:
            raise ValueError('invalid format: {}'.format(value))

        return InstanceType(cpu_type=cpu_type, cpu_category=cpu_category, cpu=cpu)

    def is_gpu(self):
        return self.cpu_type == CPUType.GPU

    def is_cpu(self):
        return self.cpu_type == CPUType.CPU

    def __str__(self):
        if self.cpu_category:
            return '{}:{}-{}'.format(self.cpu_type.value, self.cpu_category.value, self.cpu)
        else:
            return '{}-{}'.format(self.cpu_type.value, self.cpu)
