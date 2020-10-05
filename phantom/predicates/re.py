from typing import Pattern

from phantom.base import Predicate


def is_match(pattern: Pattern[str]) -> Predicate[str]:
    def match(instance: str) -> bool:
        return pattern.match(instance) is not None

    return match


def is_full_match(pattern: Pattern[str]) -> Predicate[str]:
    def full_match(instance: str) -> bool:
        return pattern.fullmatch(instance) is not None

    return full_match
