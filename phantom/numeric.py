from __future__ import annotations

import abc
from typing import Callable
from typing import Generic
from typing import Optional
from typing import Type
from typing import TypeVar

from .base import Predicate
from .base import PredicateType
from .predicates import interval

T = TypeVar("T", bound=float)

IntervalCheck = Callable[[float, float], Predicate[T]]


class Interval(PredicateType[T], Generic[T]):
    __check__: IntervalCheck[T]

    def __init_subclass__(
        cls,
        check: Optional[IntervalCheck[T]] = None,
        low: float = float("-inf"),
        high: float = float("inf"),
        bound: Type = float,
        **kwargs: object,
    ) -> None:
        check = getattr(cls, "__check__", None) if check is None else check
        if check is None:
            raise TypeError(f"{cls.__qualname__} must define an interval check")
        cls.__check__ = check
        super().__init_subclass__(
            predicate=cls.__check__(low, high), bound=bound, **kwargs
        )


class Open(Interval[T], check=interval.open):
    ...


class Closed(Interval[T], check=interval.closed):
    ...


class OpenClosed(Interval[T], check=interval.open_closed):
    ...


class ClosedOpen(Interval[T], check=interval.closed_open):
    ...


class Natural(Open, low=0, bound=int):
    ...


class NegativeInt(Open, high=0, bound=int):
    ...


class Portion(Open, low=0, high=1):
    ...
