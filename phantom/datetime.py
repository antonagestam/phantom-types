"""
Types for narrowing on the builtin datetime types.
"""

import datetime

from .base import Phantom
from .predicates.datetime import is_tz_aware
from .predicates.datetime import is_tz_naive


class TZAware(datetime.datetime, Phantom, predicate=is_tz_aware):
    """
    A type for helping ensure that ``datetime`` objects are always timezone aware.

    >>> isinstance(datetime.datetime.now(), TZAware)
    False
    >>> isinstance(datetime.datetime.now(tz=datetime.timezone.utc), TZAware)
    True
    """


class TZNaive(datetime.datetime, Phantom, predicate=is_tz_naive):
    """
    >>> isinstance(datetime.datetime.now(), TZNaive)
    True
    >>> isinstance(datetime.datetime.now(tz=datetime.timezone.utc), TZNaive)
    False
    """
