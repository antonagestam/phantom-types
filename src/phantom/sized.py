"""
Types describing collections with size boundaries. These types should only be used with
immutable collections. There is a naive check that eliminates some of the most common
mutable collections in the instance check. However, a guaranteed check is probably
impossible to implement, so some amount of developer discipline is required.

Sized types are created by subclassing :py:class:`PhantomBound` and providing a minimum,
maximum, or both as the ``min`` and ``max`` class arguments. For instance,
:py:class:`NonEmpty` is implemented using ``min=1``.

This made-up type would describe sized collections with between 5 and 10 ints:

.. code-block:: python

    class SpecificSize(PhantomBound[int], min=5, max=10):
        ...


This example creates a type that accepts strings with 255 or less characters:

.. code-block:: python

    class SizedStr(str, PhantomBound[str], max=255):
        ...

"""
from __future__ import annotations

from typing import Any
from typing import Generic
from typing import Iterable
from typing import Sized
from typing import TypeVar

from typing_extensions import Protocol
from typing_extensions import runtime_checkable

from . import Phantom
from . import PhantomMeta
from . import Predicate
from ._utils.misc import is_not_known_mutable_instance
from .predicates import boolean
from .predicates import collection
from .predicates import interval
from .predicates import numeric
from .schema import Schema

# We attempt to import _ProtocolMeta from typing_extensions to support Python 3.7 but
# fall back the typing module to support Python 3.8+. This is the closest I could find
# to documentation of _ProtocolMeta.
# https://github.com/python/cpython/commit/74d7f76e2c953fbfdb7ce01b7319d91d471cc5ef
try:
    from typing_extensions import _ProtocolMeta  # type: ignore[attr-defined]
except ImportError:
    from typing import _ProtocolMeta

__all__ = (
    "SizedIterable",
    "PhantomSized",
    "PhantomBound",
    "NonEmpty",
    "NonEmptyStr",
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
    """
    Takes class argument ``len: Predicate[int]``.

    Discouraged in favor of :py:class:`PhantomBound`, which better supports automatic
    schema generation.
    """

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


class UnresolvedBounds(Exception):
    ...


class LSPViolation(Exception):
    ...


class PhantomBound(
    Phantom[Sized],
    SizedIterable[T],
    Generic[T],
    metaclass=SizedIterablePhantomMeta,
    bound=SizedIterable,
    abstract=True,
):
    """Takes class arguments ``min: int``, ``max: int``."""

    __min__: int | None
    __max__: int | None

    def __init_subclass__(  # noqa
        cls,
        min: int | None = None,
        max: int | None = None,
        abstract: bool = False,
        **kwargs: Any,
    ) -> None:
        inherited_min = getattr(cls, "__min__", None)
        inherited_max = getattr(cls, "__max__", None)
        cls.__min__ = inherited_min if min is None else min
        cls.__max__ = inherited_max if max is None else max

        # Note: There's possibly value in generalizing this, to be able to declaratively
        #       describe the relationship between an attribute and its inherited value.
        if (
            cls.__min__ is not None
            and inherited_min is not None
            and cls.__min__ < inherited_min
        ):
            raise LSPViolation(
                f"Cannot set a smaller min than inherited ({cls.__min__} < "
                f"{inherited_min})."
            )

        if (
            cls.__max__ is not None
            and inherited_max is not None
            and cls.__max__ > inherited_max
        ):
            raise LSPViolation(
                f"Cannot set a larger max than inherited ({cls.__max__} > "
                f"{inherited_max})."
            )

        if cls.__min__ is not None and cls.__max__ is not None:
            size = interval.inclusive(cls.__min__, cls.__max__)
        elif cls.__min__ is not None:
            size = numeric.ge(cls.__min__)
        elif cls.__max__ is not None:
            size = numeric.le(cls.__max__)
        elif abstract:
            super().__init_subclass__(abstract=abstract, **kwargs)
            return
        else:
            raise UnresolvedBounds(
                f"Concrete type {cls.__qualname__} must provide either min or max, or "
                f"both."
            )

        super().__init_subclass__(
            predicate=boolean.both(
                is_not_known_mutable_instance,
                collection.count(size),
            ),
            abstract=abstract,
            **kwargs,
        )

    @classmethod
    def __schema__(cls) -> Schema:
        return (
            {
                **super().__schema__(),  # type: ignore[misc]
                "type": "string",
                "minLength": cls.__min__,
                "maxLength": cls.__max__,
            }
            if str in cls.__mro__
            else {
                **super().__schema__(),  # type: ignore[misc]
                "type": "array",
                "minItems": cls.__min__,
                "maxItems": cls.__max__,
            }
        )


class NonEmpty(PhantomBound[T], Generic[T], min=1):
    """A sized collection with at least one item."""

    @classmethod
    def __schema__(cls) -> Schema:
        return {
            **super().__schema__(),  # type: ignore[misc]
            "description": "A non-empty array.",
        }


class NonEmptyStr(str, NonEmpty[str]):
    """A sized str with at least one character."""

    @classmethod
    def __schema__(cls) -> Schema:
        return {
            **super().__schema__(),  # type: ignore[misc]
            "description": "A non-empty string.",
        }


class Empty(PhantomBound[T], Generic[T], max=0):
    """A sized collection with exactly zero items."""

    @classmethod
    def __schema__(cls) -> Schema:
        return {
            **super().__schema__(),  # type: ignore[misc]
            "description": "An empty array.",
        }
