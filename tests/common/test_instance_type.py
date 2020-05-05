import pytest
from abeja.common.instance_type import InstanceType, CPUType, CPUCategory

POSSIBLE_INSTANCE_TYPES = [
    ('cpu-0.25', InstanceType(CPUType.CPU, None, 0.25)),
    ('cpu-1', InstanceType(CPUType.CPU, None, 1)),
    ('cpu-2', InstanceType(CPUType.CPU, None, 2)),
    ('cpu-4', InstanceType(CPUType.CPU, None, 4)),
    ('cpu-8', InstanceType(CPUType.CPU, None, 8)),
    ('cpu-16', InstanceType(CPUType.CPU, None, 16)),
    ('gpu-1', InstanceType(CPUType.GPU, None, 1)),
    ('gpu:a-1', InstanceType(CPUType.GPU, CPUCategory.A, 1)),
    ('gpu:b-1', InstanceType(CPUType.GPU, CPUCategory.B, 1)),
    ('gpu:b-2', InstanceType(CPUType.GPU, CPUCategory.B, 2)),
    ('gpu:b-4', InstanceType(CPUType.GPU, CPUCategory.B, 4)),
]


@pytest.mark.parametrize('value,expected', POSSIBLE_INSTANCE_TYPES)
def test_parse(value, expected) -> None:
    instance_type = InstanceType.parse(value)
    assert instance_type == expected
    assert str(instance_type) == value


@pytest.mark.parametrize('expected,instance_type', POSSIBLE_INSTANCE_TYPES)
def test_str(expected, instance_type) -> None:
    assert str(instance_type) == expected
