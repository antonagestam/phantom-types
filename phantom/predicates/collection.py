from typing import Container
from typing import Iterable
from typing import Sized
from typing import TypeVar

from phantom.base import Predicate


def contains(value: object) -> Predicate[Container]:
    """Create a new predicate that succeeds when its argument contains ``value``."""

    def compare(container: Container, /) -> bool:
        return value in container

    return compare


def contained(container: Container) -> Predicate[object]:
    """
    Create a new predicate that succeeds when its argument is contained by
    ``container``.
    """

    def compare(value: object, /) -> bool:
        return value in container

    return compare


def count(predicate: Predicate[int]) -> Predicate[Sized]:
    """
    Create a predicate that succeeds when the size of its argument satisfies the given
    ``predicate``.
    """

    def compare(sized: Sized, /) -> bool:
        return predicate(len(sized))

    return compare


_O = TypeVar("_O", bound=object)


def exists(predicate: Predicate[_O]) -> Predicate[Iterable]:
    """
    Create a predicate that succeeds when one or more items in its argument satisfies
    ``predicate``.
    """

    def compare(iterable: Iterable, /) -> bool:
        return any(predicate(item) for item in iterable)

    return compare


def every(predicate: Predicate[_O]) -> Predicate[Iterable]:
    """
    Create a predicate that succeeds when all items in its argument satisfy
    ``predicate``.
    """

    def compare(iterable: Iterable, /) -> bool:
        return all(predicate(item) for item in iterable)

    return compare
