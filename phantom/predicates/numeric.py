from typing import Final

from .base import Predicate
from .bool import neg
from .generic import equal


def less(n: float) -> Predicate[float]:
    def check(value: float) -> bool:
        return value < n
    return check


def le(n: float) -> Predicate[float]:
    def check(value: float) -> bool:
        return value <= n
    return check


def greater(n: float) -> Predicate[float]:
    def check(value: float) -> bool:
        return value > n
    return check


def ge(n: float) -> Predicate[float]:
    def check(value: float) -> bool:
        return value >= n
    return check


positive: Final = greater(0)
non_positive: Final = le(0)
negative: Final = less(0)
non_negative: Final = ge(0)


def modulo(n: float, p: Predicate[float]) -> Predicate[float]:
    def check(value: float) -> bool:
        return p(value % n)
    return check


even: Final = modulo(2, equal(0))
odd: Final = neg(even)
