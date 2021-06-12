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
from .schema import Schema
from .utils import resolve_class_attr


class Match(str, Phantom, abstract=True):
    """
    Takes ``pattern: Pattern[str]`` as class argument. Uses the
    :py:func:`phantom.predicate.re.is_match` predicate.
    """

    __pattern__: Pattern[str]

    def __init_subclass__(cls, pattern: Pattern[str], **kwargs: Any) -> None:
        resolve_class_attr(cls, "__pattern__", pattern)
        super().__init_subclass__(predicate=re.is_match(cls.__pattern__), **kwargs)

    @classmethod
    def __schema__(cls) -> Schema:
        return {
            **super().__schema__(),  # type: ignore[misc]
            "description": (
                "A string starting with a match of the format regular expression."
            ),
            "format": str(cls.__pattern__),
        }


class FullMatch(str, Phantom, abstract=True):
    """
    Takes ``pattern: Pattern[str]`` as class argument. Uses the
    :py:func:`phantom.predicate.re.is_full_match` predicate.
    """

    __pattern__: Pattern[str]

    def __init_subclass__(cls, pattern: Pattern[str], **kwargs: Any) -> None:
        resolve_class_attr(cls, "__pattern__", pattern)
        super().__init_subclass__(predicate=re.is_full_match(cls.__pattern__), **kwargs)

    @classmethod
    def __schema__(cls) -> Schema:
        return {
            **super().__schema__(),  # type: ignore[misc]
            "description": "A string that matches the format regular expression.",
            "format": str(cls.__pattern__),
        }
