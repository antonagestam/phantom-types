from __future__ import annotations

from typing import Callable
from typing import Generic
from typing import Type
from typing import TypeVar

from phantom.utils import Maybe
from phantom.utils import default
from phantom.utils import undefined

from .base import Predicate
from .base import PredicateType
from .predicates import interval

T = TypeVar("T", bound=float)


class Interval(PredicateType[T], Generic[T]):
    def __init_subclass__(
        cls,
        check: Callable[[float, float], Predicate[T]],
        low: float = float("-inf"),
        high: float = float("inf"),
        bound: Maybe[Type] = undefined,
        **kwargs: object,
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
