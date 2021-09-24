"""
Types describing objects that coerce to either ``True`` or ``False`` respectively when
calling ``bool()`` on them.
"""

from .base import Phantom
from .predicates import boolean


class Truthy(Phantom[object], predicate=boolean.truthy, bound=object):
    """
    >>> isinstance("Huzzah!", Truthy)
    True
    >>> isinstance((), Truthy)
    False
    """


class Falsy(Phantom[object], predicate=boolean.falsy, bound=object):
    """
    >>> isinstance((), Falsy)
    True
    >>> isinstance("Hej!", Falsy)
    False
    """
