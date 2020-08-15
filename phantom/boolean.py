from . import predicates
from .base import PredicateType


class Truthy(PredicateType[object], predicate=predicates.is_truthy, bound=object):
    ...


class Falsy(PredicateType[object], predicate=predicates.is_falsy, bound=object):
    ...
