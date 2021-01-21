from __future__ import annotations

from typing import Any
from typing import Optional
from typing import Protocol
from typing import TypeVar
from typing import Union

from .base import Phantom
from .base import Predicate
from .predicates import interval
from .utils import resolve_class_attr

N = TypeVar("N", bound=float)


class IntervalCheck(Protocol):
    def __call__(self, a: N, b: N, /) -> Predicate[N]:
        ...


# See issue as to why the numeric tower isn't used for kind here.
# https://github.com/python/mypy/issues/3186
class Interval(Phantom[float], bound=Union[int, float], abstract=True):
    __check__: IntervalCheck

    def __init_subclass__(
        cls,
        check: Optional[IntervalCheck] = None,
        low: float = float("-inf"),
        high: float = float("inf"),
        **kwargs: Any,
    ) -> None:
        resolve_class_attr(cls, "__check__", check)
        if getattr(cls, "__check__", None) is None:
            raise TypeError(f"{cls.__qualname__} must define an interval check")
        super().__init_subclass__(predicate=cls.__check__(low, high), **kwargs)


class Open(Interval, check=interval.open, abstract=True):
    ...


class Closed(Interval, check=interval.closed, abstract=True):
    ...


class OpenClosed(Interval, check=interval.open_closed, abstract=True):
    ...


class ClosedOpen(Interval, check=interval.closed_open, abstract=True):
    ...


class Natural(int, Open, low=0):
    ...


class NegativeInt(int, Open, high=0):
    ...


class Portion(float, Open, low=0, high=1):
    ...
