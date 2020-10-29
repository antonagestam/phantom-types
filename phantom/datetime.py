import datetime

from .base import Phantom
from .predicates.datetime import is_tz_aware
from .predicates.datetime import is_tz_naive


class TZAware(Phantom, bound=datetime.datetime, predicate=is_tz_aware):
    ...


class TZNaive(Phantom, bound=datetime.datetime, predicate=is_tz_naive):
    ...
