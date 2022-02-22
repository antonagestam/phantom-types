from typing import Generic
from typing import Sequence
from typing import TypeVar

from .base import Phantom
from .predicates import boolean
from .predicates.generic import of_type
from .utils import is_not_mutable_instance

T = TypeVar("T")


class SequenceNotStr(
    Sequence[T],
    Phantom,
    Generic[T],
    predicate=boolean.both(
        is_not_mutable_instance,
        boolean.negate(of_type((str, bytes))),
    ),
):
    ...
