from __future__ import annotations

from typing import Any
from typing import Generic
from typing import Type
from typing import TypeVar

from .base import BaseInstanceCheck


T = TypeVar("T", bound=Any)


# TODO: Add new types to numeric tower
#   https://docs.python.org/3/library/numbers.html#adding-more-numeric-abcs
class OpenRange(Generic[T], metaclass=BaseInstanceCheck):
    __min__: float
    __max__: float
    __runtime_type__: Type[T]

    def __init_subclass__(
        cls,
        *,
        runtime_type: Type[T],
        min: float = float("-inf"),
        max: float = float("inf"),
        **kwargs: Any,
    ):
        cls.__runtime_type__ = runtime_type
        cls.__min__ = min
        cls.__max__ = max
        super().__init_subclass__(**kwargs)  # type: ignore[call-arg]

    @classmethod
    def __instancecheck__(cls, instance: Any) -> bool:
        return (
            isinstance(instance, cls.__runtime_type__)
            and cls.__min__ <= instance <= cls.__max__
        )

    C = TypeVar("C", bound="OpenRange")

    @classmethod
    def from_instance(cls: Type[C], instance: T) -> C:
        if not isinstance(instance, cls):
            raise ValueError(f"Can't create {cls.__qualname__} from {instance}")
        return instance


class NegativeInt(int, OpenRange, max=0, runtime_type=int):
    ...


class PositiveInt(int, OpenRange, min=0, runtime_type=int):
    ...


class Portion(float, OpenRange, min=0, max=1, runtime_type=float):
    ...
