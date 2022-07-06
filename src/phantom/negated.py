"""
This module provides a single type: :py:class:`SequenceNotStr`. This type is equivalent
to :py:class:`typing.Sequence` except it excludes values of type :py:class:`str` and
:py:class:`bytes` from the set of valid instances. This can be useful when you want to
eliminate the easy mistake of forgetting to wrap a string value in a containing
sequence.
"""

from typing import Generic
from typing import Sequence
from typing import TypeVar

from . import Phantom
from .predicates import boolean
from .predicates.generic import of_type

__all__ = ("SequenceNotStr",)

T = TypeVar("T")


class SequenceNotStr(
    Sequence[T],
    # Explicitly pass object here as workaround for this issue:
    # https://github.com/python/cpython/issues/94607
    Phantom[object],
    Generic[T],
    # Note: We don't eliminate mutable types here like in PhantomSized. This is because
    # the property of not being a str cannot change by mutation, so this specific
    # phantom type is safe to use with mutable types.
    predicate=boolean.negate(of_type((str, bytes))),
):
    ...
