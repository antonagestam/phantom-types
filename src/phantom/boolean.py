"""
Types describing objects that coerce to either ``True`` or ``False`` respectively when
calling ``bool()`` on them.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from . import Phantom
from .predicates import boolean

if TYPE_CHECKING:
    from hypothesis.strategies import SearchStrategy


class Truthy(Phantom[object], predicate=boolean.truthy, bound=object):
    """
    >>> isinstance("Huzzah!", Truthy)
    True
    >>> isinstance((), Truthy)
    False
    """

    @classmethod
    def __register_strategy__(cls) -> SearchStrategy:
        from hypothesis.strategies import integers
        from hypothesis.strategies import just
        from hypothesis.strategies import lists
        from hypothesis.strategies import text

        return (
            just(True)
            | integers(min_value=1)
            | integers(max_value=-1)
            | lists(elements=integers(), min_size=1)
            | text(min_size=1)
        )


class Falsy(Phantom[object], predicate=boolean.falsy, bound=object):
    """
    >>> isinstance((), Falsy)
    True
    >>> isinstance("Hej!", Falsy)
    False
    """

    @classmethod
    def __register_strategy__(cls) -> SearchStrategy:
        from hypothesis.strategies import just

        return just(False) | just(0) | just(()) | just("") | just(b"")
