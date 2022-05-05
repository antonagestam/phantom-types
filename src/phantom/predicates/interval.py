"""
Functions that create new predicates that succeed when their argument is strictly or non
strictly between the upper and lower bounds. There are corresponding phantom types that
use these predicates in :py:mod:`phantom.interval`.
"""

from typing import TypeVar

from phantom._utils.types import SupportsLeGe
from phantom._utils.types import SupportsLeGt
from phantom._utils.types import SupportsLtGe
from phantom._utils.types import SupportsLtGt

from ._base import Predicate
from ._utils import bind_name

T = TypeVar("T")


def open(low: T, high: T) -> Predicate[SupportsLeGe[T]]:
    """
    Create a predicate that succeeds when its argument is in the range ``(low, high)``.
    """

    @bind_name(open, low, high)
    def check(value: SupportsLeGe[T]) -> bool:
        return low <= value <= high

    return check


def open_closed(low: T, high: T) -> Predicate[SupportsLtGe[T]]:
    """
    Create a predicate that succeeds when its argument is in the range ``(low, high]``.
    """

    @bind_name(open_closed, low, high)
    def check(value: SupportsLtGe[T]) -> bool:
        return low <= value < high

    return check


def closed_open(low: T, high: T) -> Predicate[SupportsLeGt[T]]:
    """
    Create a predicate that succeeds when its argument is in the range ``[low, high)``.
    """

    @bind_name(closed_open, low, high)
    def check(value: SupportsLeGt[T]) -> bool:
        return low < value <= high

    return check


def closed(low: T, high: T) -> Predicate[SupportsLtGt[T]]:
    """
    Create a predicate that succeeds when its argument is in the range ``[low, high]``.
    """

    @bind_name(closed, low, high)
    def check(value: SupportsLtGt[T]) -> bool:
        return low < value < high

    return check
