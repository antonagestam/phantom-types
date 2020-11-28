from .base import Phantom
from .predicates import boolean


class Truthy(Phantom[object], predicate=boolean.truthy, bound=object):
    ...


class Falsy(Phantom[object], predicate=boolean.falsy, bound=object):
    ...
