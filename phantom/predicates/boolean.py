from typing import Iterable
from typing import Literal

from .base import Predicate
from .base import T


def true(_value: object) -> Literal[True]:
    return True


def false(_value: object) -> Literal[False]:
    return False


def negate(p: Predicate[T]) -> Predicate[T]:
    def check(value: T) -> bool:
        return not p(value)

    return check


def truthy(value: object) -> bool:
    return bool(value)


falsy = negate(truthy)


def both(p: Predicate[T], q: Predicate[T]) -> Predicate[T]:
    def check(value: T) -> bool:
        return p(value) and q(value)

    return check


def either(p: Predicate[T], q: Predicate[T]) -> Predicate[T]:
    def check(value: T) -> bool:
        return p(value) or q(value)

    return check


def xor(p: Predicate[T], q: Predicate[T]) -> Predicate[T]:
    def check(value: T) -> bool:
        return p(value) ^ q(value)

    return check


def all_of(predicates: Iterable[Predicate[T]]) -> Predicate[T]:
    predicates = tuple(predicates)

    def check(value: T) -> bool:
        return all(p(value) for p in predicates)

    return check


def any_of(predicates: Iterable[Predicate[T]]) -> Predicate[T]:
    predicates = tuple(predicates)

    def check(value: T) -> bool:
        return any(p(value) for p in predicates)

    return check


def one_of(predicates: Iterable[Predicate[T]]) -> Predicate[T]:
    predicates = tuple(predicates)

    def check(value: T) -> bool:
        return 1 == sum(p(value) for p in predicates)

    return check
