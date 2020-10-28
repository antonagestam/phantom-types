from typing import Container
from typing import Iterable
from typing import Sized

from phantom.base import Predicate


def contains(value: object) -> Predicate[Container]:
    def compare(container: Container) -> bool:
        return value in container

    return compare


# TODO: Cover, document
def of(container: Container) -> Predicate[object]:
    def compare(value: object) -> bool:
        return value in container

    return compare


def count(predicate: Predicate[int]) -> Predicate[Sized]:
    def compare(sized: Sized) -> bool:
        return predicate(len(sized))

    return compare


# TODO: Cover, document
def exists(predicate: Predicate[object]) -> Predicate[Iterable]:
    def compare(iterable: Iterable) -> bool:
        return any(predicate(item) for item in iterable)

    return compare
