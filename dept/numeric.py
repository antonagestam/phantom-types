from typing import Any
from typing import Type
from typing import TypeVar

from .base import Dependent


T = TypeVar("T", bound=float)


class OpenRange(Dependent[T]):
    __min__: float
    __max__: float
    __type__: Type[T]

    def __init_subclass__(
        cls,
        *,
        type: Type[T],
        min: float = float("-inf"),
        max: float = float("inf"),
        **kwargs: Any
    ):
        cls.__min__ = min
        cls.__max__ = max
        cls.__type__ = type
        super().__init_subclass__(**kwargs)

    @classmethod
    def __instancecheck__(cls, instance: Any) -> bool:
        return (
            isinstance(instance, cls.__type__)
            and cls.__min__ <= instance <= cls.__max__
        )


class Natural(int, OpenRange, type=int, min=0):
    ...


class NegativeInt(int, OpenRange, type=int, max=0):
    ...


class Portion(float, OpenRange, type=float, min=0, max=1):
    ...
