from typing import Union

import typeguard
from typeguard import CollectionCheckStrategy
from typeguard import ForwardRefPolicy

from . import Predicate
from ._utils import bind_name


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


def of_type(t: Union[type, tuple[type, ...]]) -> Predicate[object]:
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
            typeguard.check_type(
                value=a,
                expected_type=t,
                typecheck_fail_callback=None,
                forward_ref_policy=ForwardRefPolicy.ERROR,
                collection_check_strategy=CollectionCheckStrategy.ALL_ITEMS,
            )
        except typeguard.TypeCheckError:
            return False
        return True

    return check
