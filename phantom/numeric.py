from __future__ import annotations

from typing import Optional
from typing import Protocol
from typing import TypeVar

from .base import Predicate
from .base import PredicateType
from .predicates import interval
from .utils import resolve_class_attr

N = TypeVar("N", bound=float)


class IntervalCheck(Protocol):
    def __call__(self, a: N, b: N, /) -> Predicate[N]:
        ...


class Interval(PredicateType[float]):
    __check__: IntervalCheck

    def __init_subclass__(
        cls,
        check: Optional[IntervalCheck] = None,
        low: float = float("-inf"),
        high: float = float("inf"),
        **kwargs: object,
    ) -> None:
        resolve_class_attr(cls, "__check__", check)
        if getattr(cls, "__check__", None) is None:
            raise TypeError(f"{cls.__qualname__} must define an interval check")
        # See issue as to why the numeric tower isn't used here.
        # https://github.com/python/mypy/issues/3186
        bound = b if issubclass(b := cls.__mro__[1], (int, float)) else None
        super().__init_subclass__(
            predicate=cls.__check__(low, high), bound=bound, **kwargs
        )


class Open(Interval, check=interval.open):
    ...


class Closed(Interval, check=interval.closed):
    ...


class OpenClosed(Interval, check=interval.open_closed):
    ...


class ClosedOpen(Interval, check=interval.closed_open):
    ...


class Natural(int, Open, low=0):
    ...


class NegativeInt(int, Open, high=0):
    ...


class Portion(float, Open, low=0, high=1):
    ...
