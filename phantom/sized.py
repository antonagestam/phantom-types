from typing import Any
from typing import Final
from typing import Generic
from typing import Iterable
from typing import MutableMapping
from typing import MutableSequence
from typing import MutableSet
from typing import Protocol
from typing import Sized
from typing import TypeVar
from typing import _ProtocolMeta  # type: ignore[attr-defined]
from typing import runtime_checkable

from .base import Phantom
from .base import PhantomMeta
from .base import Predicate
from .predicates import boolean
from .predicates import collection
from .predicates import generic
from .predicates import numeric

__all__ = (
    "PhantomSized",
    "NonEmpty",
    "Empty",
)


mutable: Final = (MutableSequence, MutableSet, MutableMapping)
T = TypeVar("T", bound=object, covariant=True)


@runtime_checkable
class SizedIterable(Sized, Iterable[T], Protocol[T]):
    ...


# This raises a mypy error because disallow_subclassing_any is enabled and _ProtocolMeta
# isn't publicly typed.
class SizedIterablePhantomMeta(PhantomMeta, _ProtocolMeta):  # type: ignore[misc]
    ...


class PhantomSized(
    SizedIterable[T],
    Phantom[Sized],
    Generic[T],
    metaclass=SizedIterablePhantomMeta,
    bound=SizedIterable,
    abstract=True,
):
    def __init_subclass__(cls, len: Predicate[float], **kwargs: Any) -> None:
        super().__init_subclass__(
            predicate=boolean.both(
                boolean.negate(generic.of_type(mutable)),
                collection.count(len),
            ),
            **kwargs,
        )


class NonEmpty(PhantomSized[T], Generic[T], len=numeric.greater(0)):
    ...


class Empty(PhantomSized[T], Generic[T], len=generic.equal(0)):
    ...
