from typing import Any
from typing import Type
from typing import TypeVar

from .base import Phantom


T = TypeVar("T", bound=float)


class OpenRange(Phantom):
    __min__: float
    __max__: float
    __type__: Type[float]

    def __init_subclass__(
        cls, *, min: float = float("-inf"), max: float = float("inf")
    ):
        super().__init_subclass__()
        cls.__min__ = min
        cls.__max__ = max
        if not issubclass(cls.__bases__[0], (int, float)):
            raise TypeError(
                "The first base of subclasses of OpenRange must be a subclass "
                "of either int or float."
            )
        cls.__type__ = cls.__bases__[0]

    @classmethod
    def __instancecheck__(cls, instance: Any) -> bool:
        return (
            isinstance(instance, cls.__type__)
            and cls.__min__ <= instance <= cls.__max__
        )


class Natural(int, OpenRange, min=0):
    ...


class NegativeInt(int, OpenRange, max=0):
    ...


class Portion(float, OpenRange, min=0, max=1):
    ...
