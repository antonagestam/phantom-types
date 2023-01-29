"""
This module provides a single type: :py:class:`SequenceNotStr`. This type is equivalent
to :py:class:`typing.Sequence` except it excludes values of type :py:class:`str` and
:py:class:`bytes` from the set of valid instances. This can be useful when you want to
eliminate the easy mistake of forgetting to wrap a string value in a containing
sequence.
"""
from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Callable
from typing import Generic
from typing import Sequence
from typing import TypeVar

from typing_extensions import get_args

from . import Phantom
from .predicates import boolean
from .predicates.generic import of_type

if TYPE_CHECKING:
    from hypothesis.strategies import SearchStrategy

__all__ = ("SequenceNotStr",)

T = TypeVar("T")


class SequenceNotStr(
    Sequence[T],
    Phantom,
    Generic[T],
    # Note: We don't eliminate mutable types here like in PhantomSized. This is because
    # the property of not being a str cannot change by mutation, so this specific
    # phantom type is safe to use with mutable types.
    predicate=boolean.negate(of_type((str, bytes))),
):
    @classmethod
    def __register_strategy__(cls) -> Callable[[type[T]], SearchStrategy[T]]:
        from hypothesis.strategies import from_type
        from hypothesis.strategies import tuples

        def create_strategy(type_: type[T]) -> SearchStrategy[T] | None:
            try:
                (inner_type,) = get_args(type_)
            except ValueError:
                return None
            return tuples(from_type(inner_type))

        return create_strategy
