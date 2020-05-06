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
def test_parse(value: str, expected: InstanceType) -> None:
    instance_type = InstanceType.parse(value)
    assert instance_type == expected
    assert str(instance_type) == value


@pytest.mark.parametrize('expected,instance_type', POSSIBLE_INSTANCE_TYPES)
def test_str(expected: InstanceType, instance_type: str) -> None:
    assert str(instance_type) == expected


@pytest.mark.parametrize('instance_type,expected', [
                         (InstanceType.CPU_0_25, InstanceType.parse('cpu-0.25')),
                         (InstanceType.CPU_1, InstanceType.parse('cpu-1')),
                         (InstanceType.CPU_2, InstanceType.parse('cpu-2')),
                         (InstanceType.CPU_4, InstanceType.parse('cpu-4')),
                         (InstanceType.CPU_8, InstanceType.parse('cpu-8')),
                         (InstanceType.CPU_16, InstanceType.parse('cpu-16')),
                         (InstanceType.GPU_A1, InstanceType.parse('gpu:a-1')),
                         (InstanceType.GPU_B1, InstanceType.parse('gpu:b-1')),
                         (InstanceType.GPU_B4, InstanceType.parse('gpu:b-4')),
                         (InstanceType.GPU_B8, InstanceType.parse('gpu:b-8')),
                         ])
def test_constants(instance_type: InstanceType, expected: InstanceType) -> None:
    assert instance_type == expected


@pytest.mark.parametrize('instance_type,expected', [
    (InstanceType.CPU_0_25, True),
    (InstanceType.CPU_1, True),
    (InstanceType.CPU_2, True),
    (InstanceType.CPU_4, True),
    (InstanceType.CPU_8, True),
    (InstanceType.CPU_16, True),
    (InstanceType.GPU_A1, False),
    (InstanceType.GPU_B1, False),
    (InstanceType.GPU_B4, False),
    (InstanceType.GPU_B8, False),
])
def test_is_cpu(instance_type: InstanceType, expected: bool) -> None:
    assert instance_type.is_cpu() is expected


@pytest.mark.parametrize('instance_type,expected', [
    (InstanceType.CPU_0_25, False),
    (InstanceType.CPU_1, False),
    (InstanceType.CPU_2, False),
    (InstanceType.CPU_4, False),
    (InstanceType.CPU_8, False),
    (InstanceType.CPU_16, False),
    (InstanceType.GPU_A1, True),
    (InstanceType.GPU_B1, True),
    (InstanceType.GPU_B4, True),
    (InstanceType.GPU_B8, True),
])
def test_is_gpu(instance_type: InstanceType, expected: bool) -> None:
    assert instance_type.is_gpu() is expected
