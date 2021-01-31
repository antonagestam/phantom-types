import math
from typing import Union

from .base import Predicate
from .boolean import negate
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


positive = greater(0)
non_positive = le(0)
negative = less(0)
non_negative = ge(0)


def modulo(n: float, p: Predicate[float]) -> Predicate[float]:
    def check(value: float) -> bool:
        return p(value % n)

    return check


def divisible(n: int) -> Predicate[int]:
    return modulo(n, equal(0))


even: Predicate[int] = divisible(2)
odd: Predicate[int] = negate(even)


is_nan: Predicate[Union[int, float]] = math.isnan
