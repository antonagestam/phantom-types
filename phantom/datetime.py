import datetime

from .base import Phantom
from .predicates.datetime import is_tz_aware
from .predicates.datetime import is_tz_naive


class TZAware(datetime.datetime, Phantom, predicate=is_tz_aware):
    ...


class TZNaive(datetime.datetime, Phantom, predicate=is_tz_naive):
    ...
