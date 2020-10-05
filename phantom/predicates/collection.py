from typing import Container
from typing import Sized
from typing import TypeVar

from phantom.base import Predicate

U = TypeVar("U")


def contains(value: U) -> Predicate[Container]:
    def compare(container: Container) -> bool:
        return value in container

    return compare


def count(predicate: Predicate[int]) -> Predicate[Sized]:
    def compare(sized: Sized) -> bool:
        return predicate(len(sized))

    return compare
