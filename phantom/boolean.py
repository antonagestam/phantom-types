from .base import PredicateType
from .predicates import bool


class Truthy(PredicateType[object], predicate=bool.truthy, bound=object):
    ...


class Falsy(PredicateType[object], predicate=bool.falsy, bound=object):
    ...
