from typing import Iterable
from typing import TypeVar

from typing_extensions import Literal

from . import Predicate
from ._utils import bind_name

T_contra = TypeVar("T_contra", bound=object, contravariant=True)


def true(_value: object) -> Literal[True]:
    """Always return :py:const:`True`."""
    return True


def false(_value: object) -> Literal[False]:
    """Always return :py:const:`False`."""
    return False


def negate(predicate: Predicate[T_contra]) -> Predicate[T_contra]:
    """Negate a given predicate."""

    @bind_name(negate, predicate)
    def check(value: T_contra) -> bool:
        return not predicate(value)

    return check


def truthy(value: object) -> bool:
    """Return :py:const:`True` for truthy objects."""
    return bool(value)


def falsy(value: object) -> bool:
    """Return :py:const:`True` for falsy objects."""
    return negate(truthy)(value)


def both(p: Predicate[T_contra], q: Predicate[T_contra]) -> Predicate[T_contra]:
    """
    Create a new predicate that succeeds when both of the given predicates succeed.
    """

    @bind_name(both, p, q)
    def check(value: T_contra) -> bool:
        return p(value) and q(value)

    return check


def either(p: Predicate[T_contra], q: Predicate[T_contra]) -> Predicate[T_contra]:
    """
    Create a new predicate that succeeds when at least one of the given predicates
    succeed.
    """

    @bind_name(either, p, q)
    def check(value: T_contra) -> bool:
        return p(value) or q(value)

    return check


def xor(p: Predicate[T_contra], q: Predicate[T_contra]) -> Predicate[T_contra]:
    """
    Create a new predicate that succeeds when one of the given predicates succeed, but
    not both.
    """

    @bind_name(xor, p, q)
    def check(value: T_contra) -> bool:
        return p(value) ^ q(value)

    return check


def all_of(predicates: Iterable[Predicate[T_contra]]) -> Predicate[T_contra]:
    """Create a new predicate that succeeds when all of the given predicates succeed."""
    predicates = tuple(predicates)

    @bind_name(all_of, *predicates)
    def check(value: T_contra) -> bool:
        return all(p(value) for p in predicates)

    return check


def any_of(predicates: Iterable[Predicate[T_contra]]) -> Predicate[T_contra]:
    """
    Create a new predicate that succeeds when at least one of the given predicates
    succeed.
    """
    predicates = tuple(predicates)

    @bind_name(any_of, *predicates)
    def check(value: T_contra) -> bool:
        return any(p(value) for p in predicates)

    return check


def one_of(predicates: Iterable[Predicate[T_contra]]) -> Predicate[T_contra]:
    """
    Create a new predicate that succeeds when exactly one of the given predicates
    succeed.
    """
    predicates = tuple(predicates)

    @bind_name(one_of, *predicates)
    def check(value: T_contra) -> bool:
        return 1 == sum(p(value) for p in predicates)

    return check
