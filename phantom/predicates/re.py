from typing import Pattern

from .base import Predicate


def is_match(pattern: Pattern[str]) -> Predicate[str]:
    """
    Create a new predicate that succeeds when the start of its argument matches the
    given ``pattern``.
    """

    def match(instance: str) -> bool:
        return pattern.match(instance) is not None

    return match


def is_full_match(pattern: Pattern[str]) -> Predicate[str]:
    """
    Create a new predicate that succeeds when its whole argument matches the given
    ``pattern``.
    """

    def full_match(instance: str) -> bool:
        return pattern.fullmatch(instance) is not None

    return full_match
