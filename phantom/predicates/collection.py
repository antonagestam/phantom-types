from typing import Container
from typing import Iterable
from typing import Sized

from phantom.base import Predicate


def contains(value: object) -> Predicate[Container]:
    """Return a predicate that is successful given a container with `value` in it."""

    def compare(container: Container) -> bool:
        return value in container

    return compare


def contained(container: Container) -> Predicate[object]:
    """Return a predicate that is successful given a value contained by `container`."""

    def compare(value: object) -> bool:
        return value in container

    return compare


def count(predicate: Predicate[int]) -> Predicate[Sized]:
    """
    Return a predicate that is successful given an object with a size satisfying
    `predicate`.
    """

    def compare(sized: Sized) -> bool:
        return predicate(len(sized))

    return compare


def exists(predicate: Predicate[object]) -> Predicate[Iterable]:
    """
    Return a predicate that is successful given an iterable where one or more items
    satisfy `predicate`.
    """

    def compare(iterable: Iterable) -> bool:
        return any(predicate(item) for item in iterable)

    return compare


def every(predicate: Predicate[object]) -> Predicate[Iterable]:
    """
    Return a predicate that is successful given an iterable where all items satisfy
    `predicate`.
    """

    def compare(iterable: Iterable) -> bool:
        return all(predicate(item) for item in iterable)

    return compare
