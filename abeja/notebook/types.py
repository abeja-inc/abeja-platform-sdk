from enum import Enum

from abeja.exceptions import BadRequest


class InstanceType(Enum):
    CPU_1 = 'cpu-1'
    CPU_2 = 'cpu-2'
    CPU_4 = 'cpu-4'
    CPU_8 = 'cpu-8'
    CPU_16 = 'cpu-16'
    GPU_1 = 'gpu-1'

    @classmethod
    def to_enum(cls, status: str):
        for elm in InstanceType:
            if elm.value == status:
                return elm
        error_message = "'{}' is not supported as InstanceType".format(status)
        raise BadRequest(
            error=error_message,
            error_description=error_message,
            status_code=400)


class ImageType(Enum):
    IMAGE_CPU_1810 = 'abeja-inc/all-cpu:18.10'
    IMAGE_CPU_1904 = 'abeja-inc/all-cpu:19.04'
    IMAGE_CPU_1910 = 'abeja-inc/all-cpu:19.10'
    IMAGE_GPU_1810 = 'abeja-inc/all-gpu:18.10'
    IMAGE_GPU_1904 = 'abeja-inc/all-gpu:19.04'
    IMAGE_GPU_1910 = 'abeja-inc/all-gpu:19.10'

    @classmethod
    def to_enum(cls, status: str):
        for elm in ImageType:
            if elm.value == status:
                return elm
        error_message = "'{}' is not supported as image".format(status)
        raise BadRequest(
            error=error_message,
            error_description=error_message,
            status_code=400)


class NotebookType(Enum):
    NOTEBOOK = 'notebook'
    LAB = 'lab'

    @classmethod
    def to_enum(cls, status: str):
        for elm in NotebookType:
            if elm.value == status:
                return elm
        error_message = "'{}' is not supported as NotebookTyle".format(status)
        raise BadRequest(
            error=error_message,
            error_description=error_message,
            status_code=400)
