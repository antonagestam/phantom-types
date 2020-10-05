from typing import Container
from typing import Sized

from phantom.base import Predicate


def contains(value: object) -> Predicate[Container]:
    def compare(container: Container) -> bool:
        return value in container

    return compare


def count(predicate: Predicate[int]) -> Predicate[Sized]:
    def compare(sized: Sized) -> bool:
        return predicate(len(sized))

    return compare
