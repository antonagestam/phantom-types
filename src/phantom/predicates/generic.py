from typing import Tuple
from typing import Union

import typeguard

from .base import Predicate
from .utils import bind_name


def equal(a: object) -> Predicate[object]:
    """Create a new predicate that succeeds when its argument is equal to ``a``."""

    @bind_name(equal, a)
    def check(b: object) -> bool:
        return a == b

    return check


def identical(a: object) -> Predicate[object]:
    """Create a new predicate that succeeds when its argument is identical to ``a``."""

    @bind_name(identical, a)
    def check(b: object) -> bool:
        return a is b

    return check


def of_type(t: Union[type, Tuple[type, ...]]) -> Predicate[object]:
    """
    Create a new predicate that succeeds when its argument is an instance of ``t``.
    """

    @bind_name(of_type, t)
    def check(a: object) -> bool:
        return isinstance(a, t)

    return check


def of_complex_type(t: type) -> Predicate[object]:
    @bind_name(of_complex_type, t)
    def check(a: object) -> bool:
        try:
            typeguard.check_type("a", a, t, globals={}, locals={})
        except TypeError:
            return False
        return True

    return check
