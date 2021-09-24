from .base import Predicate
from .boolean import negate
from .generic import equal
from .utils import bind_name


def less(n: float) -> Predicate[float]:
    """
    Create a new predicate that succeeds when its argument is strictly less than ``n``.
    """

    @bind_name(less, n)
    def check(value: float) -> bool:
        return value < n

    return check


def le(n: float) -> Predicate[float]:
    """
    Create a new predicate that succeeds when its argument is less than or equal to
    ``n``.
    """

    @bind_name(le, n)
    def check(value: float) -> bool:
        return value <= n

    return check


def greater(n: float) -> Predicate[float]:
    """
    Create a new predicate that succeeds when its argument is strictly greater than
    ``n``.
    """

    @bind_name(greater, n)
    def check(value: float) -> bool:
        return value > n

    return check


def ge(n: float) -> Predicate[float]:
    """
    Create a new predicate that succeeds when its argument is greater than or equal to
    ``n``.
    """

    @bind_name(ge, n)
    def check(value: float) -> bool:
        return value >= n

    return check


def positive(n: float) -> bool:
    """Return :py:const:`True` when ``n`` is strictly greater than zero."""
    return greater(0)(n)


def non_positive(n: float) -> bool:
    """Return :py:const:`True` when ``n``  is less than or equal to zero."""
    return le(0)(n)


def negative(n: float) -> bool:
    """Return :py:const:`True` when ``n`` is strictly less than zero."""
    return less(0)(n)


def non_negative(n: float) -> bool:
    """Return :py:const:`True` when ``n`` is greater than or equal to zero."""
    return ge(0)(n)


def modulo(n: float, p: Predicate[float]) -> Predicate[float]:
    """
    Create a new predicate that succeeds when its argument modulo ``n`` satisfies the
    given predicate ``p``.
    """

    @bind_name(modulo, n, p)
    def check(value: float) -> bool:
        return p(value % n)

    return check


def even(n: int) -> bool:
    """Return :py:const:`True`  when ``n`` is even."""
    return modulo(2, equal(0))(n)


def odd(n: int) -> bool:
    """Return :py:const:`True`  when ``n`` is odd."""
    return negate(even)(n)
