"""
Types for representing strings that match a pattern.

.. code-block:: python

    class Greeting(Match, pattern=r"^(Hi|Hello)"):
        ...


    assert isinstance("Hello Jane!", Greeting)
"""
from __future__ import annotations

import re
from typing import Any
from typing import Pattern

from .base import Phantom
from .predicates.re import is_full_match
from .predicates.re import is_match
from .schema import Schema
from .utils import resolve_class_attr

__all__ = ("Match", "FullMatch")


def _compile(pattern: Pattern[str] | str) -> Pattern[str]:
    if not isinstance(pattern, Pattern):
        return re.compile(pattern)
    return pattern


class Match(str, Phantom, abstract=True):
    """
    Takes ``pattern: Pattern[str] | str`` as class argument as either a compiled
    :py:class:`Pattern` or a :py:class:`str` to be compiled. Uses the
    :py:func:`phantom.predicate.re.is_match` predicate.
    """

    __pattern__: Pattern[str]

    def __init_subclass__(cls, pattern: Pattern[str] | str, **kwargs: Any) -> None:
        resolve_class_attr(cls, "__pattern__", _compile(pattern))
        super().__init_subclass__(predicate=is_match(cls.__pattern__), **kwargs)

    @classmethod
    def __schema__(cls) -> Schema:
        return {
            **super().__schema__(),  # type: ignore[misc]
            "description": (
                "A string starting with a match of the format regular expression."
            ),
            "format": str(cls.__pattern__.pattern),
        }


class FullMatch(str, Phantom, abstract=True):
    """
    Takes ``pattern: Pattern[str] | str`` as class argument as either a compiled
    :py:class:`Pattern` or a :py:class:`str` to be compiled. Uses the
    :py:func:`phantom.predicate.re.is_full_match` predicate.
    """

    __pattern__: Pattern[str]

    def __init_subclass__(cls, pattern: Pattern[str] | str, **kwargs: Any) -> None:
        resolve_class_attr(cls, "__pattern__", _compile(pattern))
        super().__init_subclass__(predicate=is_full_match(cls.__pattern__), **kwargs)

    @classmethod
    def __schema__(cls) -> Schema:
        return {
            **super().__schema__(),  # type: ignore[misc]
            "description": "A string that matches the format regular expression.",
            "format": str(cls.__pattern__.pattern),
        }
