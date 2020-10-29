from typing import Tuple
from typing import Union

from .base import Predicate


def equal(a: object) -> Predicate[object]:
    def check(b: object) -> bool:
        return a == b

    return check


def identical(a: object) -> Predicate[object]:
    def check(b: object) -> bool:
        return a is b

    return check


def of_type(t: Union[type, Tuple[type, ...]]) -> Predicate[object]:
    def check(a: object) -> bool:
        return isinstance(a, t)

    return check
