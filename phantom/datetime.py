import datetime

from .base import PredicateType
from .predicates.datetime import is_tz_aware
from .predicates.datetime import is_tz_naive


class TZAware(PredicateType, bound=datetime.datetime, predicate=is_tz_aware):
    ...


class TZNaive(PredicateType, bound=datetime.datetime, predicate=is_tz_naive):
    ...
