from enum import Enum
from abeja.exceptions import BadRequest


# WARNING. This enum will be deprecated in the future version.
# It is now only used in parameter validation.
class InstanceTypeValidator(Enum):
    CPU_1 = 'cpu-1'
    CPU_2 = 'cpu-2'
    CPU_4 = 'cpu-4'
    CPU_8 = 'cpu-8'
    CPU_16 = 'cpu-16'
    GPU_A1 = 'gpu:a-1'
    GPU_B1 = 'gpu:b-1'
    GPU_B4 = 'gpu:b-4'
    GPU_B8 = 'gpu:b-8'

    @classmethod
    def validate(cls, status: str):
        for elm in InstanceType:
            if elm.value == status:
                return elm
        error_message = "'{}' is not supported as InstanceType".format(status)
        raise BadRequest(
            error=error_message,
            error_description=error_message,
            status_code=400)

    @classmethod
    def to_enum(cls, status: str):
        cls.validate(status)


# For backward compatibility
InstanceType = InstanceTypeValidator
