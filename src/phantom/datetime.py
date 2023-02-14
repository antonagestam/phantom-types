"""
Types for narrowing on the builtin datetime types.

These types can be used without installing any extra dependencies, however, to parse
strings, python-dateutil must be installed or a
:py:class:`phantom.errors.MissingDependency` error will be raised when calling parse.

You can install python-dateutil by using the ``[dateutil]`` or ``[all]`` extras.
"""
from __future__ import annotations

import datetime

from . import Phantom
from . import _hypothesis
from .bounds import parse_str
from .errors import MissingDependency
from .predicates.datetime import is_tz_aware
from .predicates.datetime import is_tz_naive
from .schema import Schema

try:
    import dateutil.parser

    parse_datetime_str = dateutil.parser.parse
    DateutilParseError = dateutil.parser.ParserError
except ImportError as e:
    exception = e

    def parse_datetime_str(
        *_: object,
        **__: object,
    ) -> datetime.datetime:
        raise MissingDependency(
            "python-dateutil needs to be installed to use this type for parsing. It "
            "can be installed with the phantom-types[dateutil] extra."
        ) from exception

    class DateutilParseError(Exception):  # type: ignore[no-redef]
        ...


__all__ = ("TZAware", "TZNaive")


def parse_datetime(value: object) -> datetime.datetime:
    if isinstance(value, datetime.datetime):
        return value
    str_value = parse_str(value)
    try:
        return parse_datetime_str(str_value)
    except DateutilParseError as exc:
        raise TypeError("Could not parse datetime from given string") from exc


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

    @classmethod
    def __register_strategy__(cls) -> _hypothesis.SearchStrategy:
        from hypothesis.strategies import datetimes
        from hypothesis.strategies import timezones

        return datetimes(timezones=timezones())


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

    @classmethod
    def __register_strategy__(cls) -> _hypothesis.SearchStrategy:
        from hypothesis.strategies import datetimes
        from hypothesis.strategies import none

        return datetimes(timezones=none())
