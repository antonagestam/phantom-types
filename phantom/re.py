from typing import Any
from typing import Pattern

from .base import PredicateType
from .predicates import re


class Match(PredicateType, bound=str):
    def __init_subclass__(cls, pattern: Pattern[str], **kwargs: Any) -> None:
        super().__init_subclass__(predicate=re.is_match(pattern), **kwargs)


class FullMatch(PredicateType, bound=str):
    def __init_subclass__(cls, pattern: Pattern[str], **kwargs: Any) -> None:
        super().__init_subclass__(predicate=re.is_full_match(pattern), **kwargs)
