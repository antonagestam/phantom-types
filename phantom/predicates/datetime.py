import datetime

from .bool import neg


def is_tz_aware(dt: datetime.datetime) -> bool:
    # https://docs.python.org/3/library/datetime.html#determining-if-an-object-is-aware-or-naive
    return dt.tzinfo is not None and dt.tzinfo.utcoffset(dt) is not None


is_tz_naive = neg(is_tz_aware)
