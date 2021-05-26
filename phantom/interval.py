"""
Types for describing narrower sets of numbers than builtin numeric types like ``int``
and ``float``. Use the provided base classes to build custom intervals. For example, to
represent number in the open range ``(0, 100)`` for a volume control you would define a
type like this::

    class VolumeLevel(int, Open, low=0, high=100):
        ...

There is also a set of concrete ready-to-use interval types provided, that use predicate
functions from :py:mod:`phantom.predicates.interval`.

::

    def take_portion(portion: Portion, whole: Natural) -> float:
        return portion * whole
"""

from __future__ import annotations

from typing import Any
from typing import Protocol
from typing import TypeVar
from typing import Union

from . import Phantom
from . import Predicate
from .predicates import interval
from .utils import resolve_class_attr

N = TypeVar("N", bound=float)


class IntervalCheck(Protocol):
    def __call__(self, a: N, b: N, /) -> Predicate[N]:
        ...


# See issue as to why the numeric tower isn't used for kind here.
# https://github.com/python/mypy/issues/3186
class Interval(Phantom[float], bound=Union[int, float], abstract=True):
    """
    Base class for all interval types, providing the following class arguments:

    * ``check: IntervalCheck``
    * ``low: float`` (defaults to negative infinity)
    * ``high: float`` (defaults to positive infinity)

    Concrete subclasses must specify their runtime type bound as their first base.
    """

    __check__: IntervalCheck

    def __init_subclass__(
        cls,
        check: IntervalCheck | None = None,
        low: float = float("-inf"),
        high: float = float("inf"),
        **kwargs: Any,
    ) -> None:
        resolve_class_attr(cls, "__check__", check)
        if getattr(cls, "__check__", None) is None:
            raise TypeError(f"{cls.__qualname__} must define an interval check")
        super().__init_subclass__(predicate=cls.__check__(low, high), **kwargs)


class Open(Interval, check=interval.open, abstract=True):
    """Uses :py:func:`phantom.predicate.interval.open` as ``check``."""


class Closed(Interval, check=interval.closed, abstract=True):
    """Uses :py:func:`phantom.predicate.interval.closed` as ``check``."""


class OpenClosed(Interval, check=interval.open_closed, abstract=True):
    """Uses :py:func:`phantom.predicate.interval.open_closed` as ``check``."""


class ClosedOpen(Interval, check=interval.closed_open, abstract=True):
    """Uses :py:func:`phantom.predicate.interval.closed_open` as ``check``."""


class Natural(int, Open, low=0):
    """Represents integer values in the inclusive range ``(0, ∞)``."""

    @classmethod
    def __modify_schema__(cls, field_schema: dict) -> None:
        field_schema.update(
            description="An integer value in the inclusive range (0, ∞).",
        )


class NegativeInt(int, Open, high=0):
    """Represents integer values in the inclusive range ``(-∞, 0)``."""


class Portion(float, Open, low=0, high=1):
    """Represents float values in the inclusive range ``(0, 1)``."""
