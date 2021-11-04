"""
Types for narrowing on the builtin datetime types.
"""

import datetime

from .base import Phantom
from .predicates.datetime import is_tz_aware
from .predicates.datetime import is_tz_naive
from .schema import Schema


class TZAware(datetime.datetime, Phantom, predicate=is_tz_aware):
    """
    A type for helping ensure that ``datetime`` objects are always timezone aware.

    >>> isinstance(datetime.datetime.now(), TZAware)
    False
    >>> isinstance(datetime.datetime.now(tz=datetime.timezone.utc), TZAware)
    True
    """

    @classmethod
    def __schema__(cls) -> Schema:
        return {
            **super().__schema__(),  # type: ignore[misc]
            "description": "A date-time with timezone data.",
        }


class TZNaive(datetime.datetime, Phantom, predicate=is_tz_naive):
    """
    >>> isinstance(datetime.datetime.now(), TZNaive)
    True
    >>> isinstance(datetime.datetime.now(tz=datetime.timezone.utc), TZNaive)
    False
    """

    @classmethod
    def __schema__(cls) -> Schema:
        return {
            **super().__schema__(),  # type: ignore[misc]
            "description": "A date-time without timezone data.",
            "format": "date-time-naive",
        }
