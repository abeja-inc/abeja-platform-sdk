from enum import Enum
from typing import Union


class Metric:
    def __init__(self, key: str, value: float) -> None:
        if not isinstance(key, str):
            raise TypeError(
                'metric key must be str type, got {}'.format(
                    type(key)))
        self.key = key
        if not (
            isinstance(
                value, (int, float)) and not isinstance(
                value, bool)):
            raise TypeError(
                'metric value must be int or float type, got {}'.format(
                    type(value)))
        self.value = float(value)

    def is_scalar(self) -> bool:
        return self.key in ['main/loss', 'main/acc', 'test/loss', 'test/acc']

    class SpecialValues(Enum):
        INFINITY = "Infinity"
        MINUS_INFINITY = "-Infinity"

    def __format_value(self) -> Union[float, str]:
        if self.value == float('inf'):
            return Metric.SpecialValues.INFINITY.value
        elif self.value == float('-inf'):
            return Metric.SpecialValues.MINUS_INFINITY.value
        return self.value

    def to_dict(self):
        key = self.key.replace('/', '_')
        value = self.__format_value()
        return {
            key: value,
        }
