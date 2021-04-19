"""
Types for representing strings that match a pattern.

::

    class Greeting(Match, pattern=re.compile(r"^(Hi|Hello)")):
        ...

    assert isinstance("Hello Jane!", Greeting)
"""
from typing import Any
from typing import Pattern

from .base import Phantom
from .predicates import re


class Match(str, Phantom, abstract=True):
    """
    Takes ``pattern: Pattern[str]`` as class argument. Uses the
    :py:func:`phantom.predicate.re.is_match` predicate.
    """

    def __init_subclass__(cls, pattern: Pattern[str], **kwargs: Any) -> None:
        super().__init_subclass__(predicate=re.is_match(pattern), **kwargs)


class FullMatch(str, Phantom, abstract=True):
    """
    Takes ``pattern: Pattern[str]`` as class argument. Uses the
    :py:func:`phantom.predicate.re.is_full_match` predicate.
    """

    def __init_subclass__(cls, pattern: Pattern[str], **kwargs: Any) -> None:
        super().__init_subclass__(predicate=re.is_full_match(pattern), **kwargs)
