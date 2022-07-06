from typing import TypeVar

from phantom._utils.types import SupportsGe
from phantom._utils.types import SupportsGt
from phantom._utils.types import SupportsLe
from phantom._utils.types import SupportsLt
from phantom._utils.types import SupportsMod

from ._base import Predicate
from ._utils import bind_name
from .boolean import negate
from .generic import equal

T = TypeVar("T")
U = TypeVar("U")


def less(n: T) -> Predicate[SupportsLt[T]]:
    """
    Create a new predicate that succeeds when its argument is strictly less than ``n``.
    """

    @bind_name(less, n)
    def check(value: SupportsLt[T]) -> bool:
        return value < n

    return check


def le(n: T) -> Predicate[SupportsLe[T]]:
    """
    Create a new predicate that succeeds when its argument is less than or equal to
    ``n``.
    """

    @bind_name(le, n)
    def check(value: SupportsLe[T]) -> bool:
        return value <= n

    return check


def greater(n: T) -> Predicate[SupportsGt[T]]:
    """
    Create a new predicate that succeeds when its argument is strictly greater than
    ``n``.
    """

    @bind_name(greater, n)
    def check(value: SupportsGt[T]) -> bool:
        return value > n

    return check


def ge(n: T) -> Predicate[SupportsGe[T]]:
    """
    Create a new predicate that succeeds when its argument is greater than or equal to
    ``n``.
    """

    @bind_name(ge, n)
    def check(value: SupportsGe[T]) -> bool:
        return value >= n

    return check


def positive(n: SupportsGt[int]) -> bool:
    """Return :py:const:`True` when ``n`` is strictly greater than zero."""
    return greater(0)(n)


def non_positive(n: SupportsLe[int]) -> bool:
    """Return :py:const:`True` when ``n``  is less than or equal to zero."""
    return le(0)(n)


def negative(n: SupportsLt[int]) -> bool:
    """Return :py:const:`True` when ``n`` is strictly less than zero."""
    return less(0)(n)


def non_negative(n: SupportsGe[int]) -> bool:
    """Return :py:const:`True` when ``n`` is greater than or equal to zero."""
    return ge(0)(n)


def modulo(n: T, p: Predicate[U]) -> Predicate[SupportsMod[T, U]]:
    """
    Create a new predicate that succeeds when its argument modulo ``n`` satisfies the
    given predicate ``p``.
    """

    @bind_name(modulo, n, p)
    def check(value: SupportsMod[T, U]) -> bool:
        return p(value % n)

    return check


def even(n: int) -> bool:
    """Return :py:const:`True`  when ``n`` is even."""
    return modulo(2, equal(0))(n)


def odd(n: int) -> bool:
    """Return :py:const:`True`  when ``n`` is odd."""
    return negate(even)(n)
