import pytest
from abeja.common.instance_type import (InstanceType, CPUType, CPUCategory,
                                        CPU_0_25,
                                        CPU_1,
                                        CPU_2,
                                        CPU_4,
                                        CPU_8,
                                        CPU_16,
                                        GPU_A1,
                                        GPU_B1,
                                        GPU_B4,
                                        GPU_B8)


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
                         (CPU_0_25, InstanceType.parse('cpu-0.25')),
                         (CPU_1, InstanceType.parse('cpu-1')),
                         (CPU_2, InstanceType.parse('cpu-2')),
                         (CPU_4, InstanceType.parse('cpu-4')),
                         (CPU_8, InstanceType.parse('cpu-8')),
                         (CPU_16, InstanceType.parse('cpu-16')),
                         (GPU_A1, InstanceType.parse('gpu:a-1')),
                         (GPU_B1, InstanceType.parse('gpu:b-1')),
                         (GPU_B4, InstanceType.parse('gpu:b-4')),
                         (GPU_B8, InstanceType.parse('gpu:b-8')),
                         ])
def test_constants(instance_type: InstanceType, expected: InstanceType) -> None:
    assert instance_type == expected


@pytest.mark.parametrize('instance_type,expected', [
    (CPU_0_25, True),
    (CPU_1, True),
    (CPU_2, True),
    (CPU_4, True),
    (CPU_8, True),
    (CPU_16, True),
    (GPU_A1, False),
    (GPU_B1, False),
    (GPU_B4, False),
    (GPU_B8, False),
])
def test_is_cpu(instance_type: InstanceType, expected: bool) -> None:
    assert instance_type.is_cpu() is expected


@pytest.mark.parametrize('instance_type,expected', [
    (CPU_0_25, False),
    (CPU_1, False),
    (CPU_2, False),
    (CPU_4, False),
    (CPU_8, False),
    (CPU_16, False),
    (GPU_A1, True),
    (GPU_B1, True),
    (GPU_B4, True),
    (GPU_B8, True),
])
def test_is_gpu(instance_type: InstanceType, expected: bool) -> None:
    assert instance_type.is_gpu() is expected
