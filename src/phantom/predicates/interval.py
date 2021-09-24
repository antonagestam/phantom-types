"""
Functions that create new predicates that succeed when their argument is strictly or non
strictly between the upper and lower bounds. There are corresponding phantom types that
use these predicates in :py:mod:`phantom.interval`.
"""
from .base import Predicate
from .utils import bind_name


def open(low: float, high: float) -> Predicate[float]:
    """
    Create a predicate that succeeds when its argument is in the range ``(low, high)``.
    """

    @bind_name(open, low, high)
    def check(value: float) -> bool:
        return low <= value <= high

    return check


def open_closed(low: float, high: float) -> Predicate[float]:
    """
    Create a predicate that succeeds when its argument is in the range ``(low, high]``.
    """

    @bind_name(open_closed, low, high)
    def check(value: float) -> bool:
        return low <= value < high

    return check


def closed_open(low: float, high: float) -> Predicate[float]:
    """
    Create a predicate that succeeds when its argument is in the range ``[low, high)``.
    """

    @bind_name(closed_open, low, high)
    def check(value: float) -> bool:
        return low < value <= high

    return check


def closed(low: float, high: float) -> Predicate[float]:
    """
    Create a predicate that succeeds when its argument is in the range ``[low, high]``.
    """

    @bind_name(closed, low, high)
    def check(value: float) -> bool:
        return low < value < high

    return check
