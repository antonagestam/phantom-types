from typing import Literal, Iterable, Final
from .base import Predicate, T


def true(_value: object) -> Literal[True]:
    return True


def false(_value: object) -> Literal[False]:
    return False


def neg(p: Predicate[T]) -> Predicate[T]:
    def check(value: T) -> bool:
        return not p(value)
    return check


def truthy(value: object) -> bool:
    return bool(value)


falsy: Final = neg(truthy)


def both(p: Predicate[T], q: Predicate[T]) -> Predicate[T]:
    def check(value: T) -> bool:
        return p(value) and q(value)
    return check


def all_of(predicates: Iterable[Predicate[T]]) -> Predicate[T]:
    def check(value: T) -> bool:
        return all(p(value) for p in predicates)
    return check


def any_of(predicates: Iterable[Predicate[T]]) -> Predicate[T]:
    def check(value: T) -> bool:
        return any(p(value) for p in predicates)
    return check
