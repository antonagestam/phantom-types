import datetime
from typing import Any

from .base import Phantom


def is_tz_aware(dt: datetime.datetime) -> bool:
    # https://docs.python.org/3/library/datetime.html#determining-if-an-object-is-aware-or-naive
    return dt.tzinfo is not None and dt.tzinfo.utcoffset(dt) is not None


class TZAware(datetime.datetime, Phantom):
    @classmethod
    def __instancecheck__(cls, instance: Any) -> bool:
        return isinstance(instance, datetime.datetime) and is_tz_aware(instance)


class TZNaive(datetime.datetime, Phantom):
    @classmethod
    def __instancecheck__(cls, instance: Any) -> bool:
        return isinstance(instance, datetime.datetime) and not is_tz_aware(instance)
