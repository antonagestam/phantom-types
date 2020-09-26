from __future__ import annotations
from typing import TypeVar, Final, Union, Type, Generic, Callable

from .base import PredicateType, Predicate
from .predicates import interval
from phantom.utils import default, Unset, unset

infinity: Final = float("inf")
negative_infinity: Final = float("-inf")

T = TypeVar("T", bound=float)


class Interval(PredicateType[T], Generic[T]):
    def __init_subclass__(
        cls,
        check: Callable[[float, float], Predicate[T]],
        low: float = negative_infinity,
        high: float = infinity,
        bound: Union[Unset, Type] = unset,
        **kwargs,
    ) -> None:
        super().__init_subclass__(
            predicate=check(low, high),
            bound=default(bound, float),
            **kwargs,
        )


class Open(PredicateType[T], check=interval.open):
    ...


class Closed(PredicateType[T], check=interval.closed):
    ...


class OpenClosed(PredicateType[T], check=interval.open_closed):
    ...


class ClosedOpen(PredicateType[T], check=interval.closed_open):
    ...


class Natural(Open, low=0, bound=int):
    ...


class NegativeInt(Open, high=0, bound=int):
    ...


class Portion(Open, low=0, high=1):
    ...
