from .base import Phantom
from .predicates import bool


class Truthy(Phantom[object], predicate=bool.truthy, bound=object):
    ...


class Falsy(Phantom[object], predicate=bool.falsy, bound=object):
    ...
