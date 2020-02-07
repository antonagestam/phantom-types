"""
The general idea is to be able to not throw away the gathered information when
parsing input. If we require input to have a certain shape in one place, and do
work to make sure it adheres, we want to able to reuse that information later.
"""
from __future__ import annotations

from typing import Any
from typing import Collection
from typing import Generic
from typing import Sized
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


class NegativeInt(OpenRange, max=0, runtime_type=int):
    ...


class PositiveInt(OpenRange, min=0, runtime_type=int):
    ...


assert not isinstance(1, NegativeInt)
assert isinstance(-1, NegativeInt)

j = NegativeInt.from_instance(-1)
assert isinstance(j, NegativeInt)
assert isinstance(j, int)


class CustomRange(OpenRange, min=-1, max=1, runtime_type=int):
    ...


assert not isinstance(-2, CustomRange)
assert isinstance(-1, CustomRange)
assert isinstance(1, CustomRange)
assert not isinstance(1.0, CustomRange)
assert not isinstance(2, CustomRange)


S = TypeVar("S", bound=Any)


# TODO: Should have __len__() -> OpenRange(min=self.__min__, max=self.__max__, type=int)
class FixedSize(Generic[S], metaclass=BaseInstanceCheck):
    __min__: float
    __max__: float
    __runtime_type__: Type[S]

    def __init_subclass__(
        cls,
        *,
        runtime_type: Type[S],
        min: float = 0,
        max: float = float("inf"),
        **kwargs: Any,
    ):
        cls.__runtime_type__ = runtime_type
        cls.__min__ = min
        cls.__max__ = max
        super().__init_subclass__(**kwargs)  # type: ignore[call-arg]

    @classmethod
    def __instancecheck__(cls, instance: Any) -> bool:
        if not isinstance(instance, Sized):
            return False
        return (
            isinstance(instance, cls.__runtime_type__)
            and cls.__min__ <= len(instance) <= cls.__max__
        )

    C = TypeVar("C", bound="FixedSize")

    @classmethod
    def from_instance(cls: Type[C], instance: S) -> C:
        if not isinstance(instance, cls):
            raise ValueError(f"Can't create {cls.__qualname__} from {instance}")
        return instance


class NonEmpty(FixedSize, min=1, runtime_type=Collection):
    ...


class Empty(FixedSize, min=0, max=0, runtime_type=Collection):
    ...


assert not isinstance([], NonEmpty)
assert isinstance([1], NonEmpty)

assert not isinstance((), NonEmpty)
assert isinstance((1,), NonEmpty)

assert not isinstance(set(), NonEmpty)
assert isinstance({1}, NonEmpty)

assert not isinstance({}, NonEmpty)
assert isinstance({"a": "b"}, NonEmpty)
