from typing import Any
from typing import Pattern

from .base import Phantom
from .predicates import re


class Match(str, Phantom, abstract=True):
    def __init_subclass__(cls, pattern: Pattern[str], **kwargs: Any) -> None:
        super().__init_subclass__(predicate=re.is_match(pattern), **kwargs)


class FullMatch(str, Phantom, abstract=True):
    def __init_subclass__(cls, pattern: Pattern[str], **kwargs: Any) -> None:
        super().__init_subclass__(predicate=re.is_full_match(pattern), **kwargs)
