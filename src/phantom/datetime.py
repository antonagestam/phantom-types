"""
Types for narrowing on the builtin datetime types.
"""
from __future__ import annotations

import datetime

from . import Phantom
from .bounds import parse_str
from .errors import MissingDependency
from .predicates.datetime import is_tz_aware
from .predicates.datetime import is_tz_naive
from .schema import Schema

try:
    from dateutil.parser import parse as parse_datetime_str
except ImportError as e:
    exception = e

    def parse_datetime_str(  # type: ignore[misc]
        *_: object,
        **__: object,
    ) -> datetime.datetime:
        raise MissingDependency(
            "python-dateutil needs to be installed to use this type for parsing. It "
            "can be installed with the phantom-types[dateutil] extra."
        ) from exception


def parse_datetime(value: object) -> datetime.datetime:
    if isinstance(value, datetime.datetime):
        return value
    return parse_datetime_str(parse_str(value))


class TZAware(datetime.datetime, Phantom, predicate=is_tz_aware):
    """
    A type for helping ensure that ``datetime`` objects are always timezone aware.

    >>> isinstance(datetime.datetime.now(), TZAware)
    False
    >>> isinstance(datetime.datetime.now(tz=datetime.timezone.utc), TZAware)
    True
    """

    # A property of being aware is (dt.tzinfo != None), so we can safely narrow this
    # attribute to not include None.
    tzinfo: datetime.tzinfo

    @classmethod
    def parse(cls, instance: object) -> TZAware:
        return super().parse(parse_datetime(instance))

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
    def parse(cls, instance: object) -> TZNaive:
        return super().parse(parse_datetime(instance))

    @classmethod
    def __schema__(cls) -> Schema:
        return {
            **super().__schema__(),  # type: ignore[misc]
            "description": "A date-time without timezone data.",
            "format": "date-time-naive",
        }
