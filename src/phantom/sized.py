"""
Types describing collections with size boundaries. These types should only be used with
immutable collections. There is a naive check that eliminates some of the most common
mutable collections in the instance check. However, a guaranteed check is probably
impossible to implement, so some amount of developer discipline is required.

Sized types are created by subclassing ``PhantomSized`` and providing a predicate that
will be called with the size of the tested collection. For instance, ``NonEmpty`` is
implemented using ``len=numeric.greater(0)``.

This made-up type would describe sized collections with between 5 and 10 ints:

.. code-block:: python

    class SpecificSize(PhantomSized[int], len=interval.open(5, 10)):
        ...
"""
from typing import Any
from typing import Generic
from typing import Iterable
from typing import MutableMapping
from typing import MutableSequence
from typing import MutableSet
from typing import Sized
from typing import TypeVar

# We attempt to import _ProtocolMeta from typing_extensions to support Python 3.7 but
# fall back the typing module to support Python 3.8+. This is the closest I could find
# to documentation of _ProtocolMeta.
# https://github.com/python/cpython/commit/74d7f76e2c953fbfdb7ce01b7319d91d471cc5ef
try:
    from typing_extensions import _ProtocolMeta  # type: ignore[attr-defined]
except ImportError:
    from typing import _ProtocolMeta  # type: ignore[attr-defined]

from typing_extensions import Final
from typing_extensions import Protocol
from typing_extensions import runtime_checkable

from . import Phantom
from . import PhantomMeta
from . import Predicate
from .predicates import boolean
from .predicates import collection
from .predicates import generic
from .predicates import numeric

__all__ = (
    "SizedIterable",
    "PhantomSized",
    "NonEmpty",
    "Empty",
)

from .schema import Schema

mutable: Final = (MutableSequence, MutableSet, MutableMapping)
T = TypeVar("T", bound=object, covariant=True)


@runtime_checkable
class SizedIterable(Sized, Iterable[T], Protocol[T]):
    """Intersection of :py:class:`typing.Sized` and :py:class:`typing.Iterable`."""


# This raises a mypy error because disallow_subclassing_any is enabled and _ProtocolMeta
# isn't publicly typed.
class SizedIterablePhantomMeta(PhantomMeta, _ProtocolMeta):  # type: ignore[misc]
    ...


class PhantomSized(
    Phantom[Sized],
    SizedIterable[T],
    Generic[T],
    metaclass=SizedIterablePhantomMeta,
    bound=SizedIterable,
    abstract=True,
):
    """Takes class argument ``len: Predicate[float]``."""

    def __init_subclass__(cls, len: Predicate[float], **kwargs: Any) -> None:
        super().__init_subclass__(
            predicate=boolean.both(
                boolean.negate(generic.of_type(mutable)),
                collection.count(len),
            ),
            **kwargs,
        )

    @classmethod
    def __schema__(cls) -> Schema:
        return {
            **super().__schema__(),  # type: ignore[misc]
            "type": "array",
        }


class NonEmpty(PhantomSized[T], Generic[T], len=numeric.greater(0)):
    """A sized collection with at least one item."""

    @classmethod
    def __schema__(cls) -> Schema:
        return {
            **super().__schema__(),  # type: ignore[misc]
            "description": "A non-empty array.",
            "minItems": 1,
        }


class Empty(PhantomSized[T], Generic[T], len=generic.equal(0)):
    """A sized collection with exactly zero items."""

    @classmethod
    def __schema__(cls) -> Schema:
        return {
            **super().__schema__(),  # type: ignore[misc]
            "description": "An empty array.",
            "maxItems": 0,
        }
