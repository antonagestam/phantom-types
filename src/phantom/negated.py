"""
This module provides a single type: :py:class:`SequenceNotStr`. This type is equivalent
to :py:class:`typing.Sequence` except it excludes values of type :py:class:`str` and
:py:class:`bytes` from the set of valid instances. This can be useful when you want to
eliminate the easy mistake of forgetting to wrap a string value in a containing
sequence.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING
from typing import Any
from typing import Generic
from typing import TypeVar
from typing import get_args

from ._utils.compat import require_pydantic

if TYPE_CHECKING:
    try:
        from pydantic import GetCoreSchemaHandler
        from pydantic_core import CoreSchema
        from pydantic_core.core_schema import ValidatorFunctionWrapHandler
    except ImportError:
        pass

from . import Phantom
from . import _hypothesis
from .predicates import boolean
from .predicates.generic import of_type

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
    def __register_strategy__(cls) -> _hypothesis.HypothesisStrategy:
        from hypothesis.strategies import from_type
        from hypothesis.strategies import tuples

        def create_strategy(
            type_: type[T],
        ) -> _hypothesis.SearchStrategy[tuple[T, ...]] | None:
            (inner_type,) = get_args(type_)
            return tuples(from_type(inner_type))

        return create_strategy

    @classmethod
    def _validate(
        cls,
        value: Any,
        handler: ValidatorFunctionWrapHandler,
    ) -> Any:
        """Pydantic V2 wrap validator."""
        validated = handler(value)
        if isinstance(validated, list):
            validated = tuple(validated)
        return cls.parse(validated)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: type[Any], handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        """Pydantic V2 hook for core schema generation."""
        require_pydantic()

        from pydantic_core.core_schema import list_schema
        from pydantic_core.core_schema import no_info_wrap_validator_function

        args = get_args(source)
        if args:
            item_schema = handler.generate_schema(args[0])
            bound_schema = list_schema(items_schema=item_schema)
        else:
            bound_schema = list_schema()

        return no_info_wrap_validator_function(cls._validate, bound_schema)
