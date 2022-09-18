"""
Types describing collections with size boundaries. These types should only be used with
immutable collections. There is a naive check that eliminates some of the most common
mutable collections in the instance check. However, a guaranteed check is probably
impossible to implement, so some amount of developer discipline is required.

Sized types are created by subclassing :py:class:`PhantomSized` and providing a
predicate that will be called with the size of the tested collection. For instance,
:py:class:`NonEmpty` is implemented using ``len=numeric.greater(0)``.

This made-up type would describe sized collections with between 5 and 10 ints:

.. code-block:: python

    class SpecificSize(PhantomSized[int], len=interval.open(5, 10)):
        ...
"""
from typing import Any
from typing import Generic
from typing import Iterable
from typing import Optional
from typing import Sized
from typing import TypeVar

# We attempt to import _ProtocolMeta from typing_extensions to support Python 3.7 but
# fall back the typing module to support Python 3.8+. This is the closest I could find
# to documentation of _ProtocolMeta.
# https://github.com/python/cpython/commit/74d7f76e2c953fbfdb7ce01b7319d91d471cc5ef
try:
    from typing_extensions import _ProtocolMeta  # type: ignore[attr-defined]
except ImportError:
    from typing import _ProtocolMeta

from typing_extensions import Protocol
from typing_extensions import runtime_checkable

from . import Phantom
from . import PhantomMeta
from . import Predicate
from ._utils.misc import is_not_known_mutable_instance
from .predicates import boolean
from .predicates import collection
from .predicates import generic
from .predicates import interval
from .predicates import numeric
from .schema import Schema

__all__ = (
    "SizedIterable",
    "PhantomSized",
    "NonEmpty",
    "Empty",
)


T = TypeVar("T", bound=object, covariant=True)


@runtime_checkable
class SizedIterable(Sized, Iterable[T], Protocol[T]):
    """Intersection of :py:class:`typing.Sized` and :py:class:`typing.Iterable`."""


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
    """Takes class argument ``len: Predicate[int]``."""

    def __init_subclass__(cls, len: Predicate[int], **kwargs: Any) -> None:
        super().__init_subclass__(
            predicate=boolean.both(
                is_not_known_mutable_instance,
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


class PhantomBounded(PhantomSized[T], Generic[T], abstract=True):
    __min__: Optional[int]
    __max__: Optional[int]

    def __init_subclass__(
        cls,
        min: Optional[int] = None,
        max: Optional[int] = None,
        **kwargs: Any,
    ) -> None:
        cls.__min__ = min
        cls.__max__ = max
        if min and max:
            predicate = collection.count(interval.open(min, max))
        elif min:
            predicate = collection.count(numeric.ge(min))
        elif max:
            predicate = collection.count(numeric.le(max))
        else:
            assert False
        super().__init_subclass__(len=predicate, **kwargs)

    @classmethod
    def __schema__(cls) -> Schema:
        return {
            **super().__schema__(),  # type: ignore[misc]
            "type": "array",
            "minItems": cls.__min__,
            "maxItems": cls.__max__,
        }


class Foo(PhantomBounded, min=5, max=10):
    ...


# TODO: Must accept kwarg in schema.SchemaField.__modify_schema__, and all __schema__
#       methods must be updated to accept this argument as well. It makes sense to
#       document/"dictate" that __schema__ implementations accept **kwarg: Any, to
#       future proof that contract.
assert Foo[str].__schema__()["items"] == "str"


class NonEmpty(PhantomBounded[T], Generic[T], min=1):
    """A sized collection with at least one item."""

    @classmethod
    def __schema__(cls) -> Schema:
        return {
            **super().__schema__(),  # type: ignore[misc]
            "description": "A non-empty array.",
            "minItems": 1,
        }


class Empty(PhantomBounded[T], Generic[T], max=0):
    """A sized collection with exactly zero items."""

    @classmethod
    def __schema__(cls) -> Schema:
        return {
            **super().__schema__(),  # type: ignore[misc]
            "description": "An empty array.",
            "maxItems": 0,
        }
