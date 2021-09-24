import datetime

from .boolean import negate


def is_tz_aware(dt: datetime.datetime) -> bool:
    """Return :py:const:`True` if ``dt`` is timezone aware."""
    # https://docs.python.org/3/library/datetime.html#determining-if-an-object-is-aware-or-naive
    return dt.tzinfo is not None and dt.tzinfo.utcoffset(dt) is not None


def is_tz_naive(dt: datetime.datetime) -> bool:
    """Return :py:const:`True` if ``dt`` is timezone naive."""
    return negate(is_tz_aware)(dt)
