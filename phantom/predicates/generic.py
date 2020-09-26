from .base import Predicate, T
from typing import Any, Type, Tuple, Union


def equal(a: object) -> Predicate[T]:
    def check(b: T) -> bool:
        return a == b
    return check


def identical(a: object) -> Predicate[T]:
    def check(b: T) -> bool:
        return a is b
    return check


def of_type(t: Union[Type, Tuple[Type, ...]]) -> Predicate[T]:
    def check(a: T) -> bool:
        return isinstance(a, t)
    return check
