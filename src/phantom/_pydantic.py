from __future__ import annotations

from collections.abc import Callable
from collections.abc import Iterable
from contextlib import suppress
from typing import TYPE_CHECKING
from typing import get_args

if TYPE_CHECKING:
    from pydantic import GetCoreSchemaHandler
    from pydantic import GetJsonSchemaHandler
    from pydantic.json_schema import JsonSchemaValue
    from pydantic_core.core_schema import AfterValidatorFunctionSchema
    from pydantic_core.core_schema import CoreSchema

    from ._utils.misc import BoundType
    from .schema import Schema


__all__ = ("get_core_schema", "get_decoding_schema", "get_json_schema")


def get_decoding_schema(
    phantom: type,
    bound: BoundType,
    source_type: object,
    handler: GetCoreSchemaHandler,
) -> CoreSchema:
    """
    Return the core schema that pydantic decodes input with, before the decoded value is
    passed to the parse() method of a phantom type. Parametrized iterable types decode
    into a tuple of their type argument, and other types into the first member of their
    bound that pydantic can describe. For other types, input is passed to parse() as is.
    """
    from pydantic import PydanticSchemaGenerationError
    from pydantic_core.core_schema import any_schema
    from pydantic_core.core_schema import tuple_schema

    if issubclass(phantom, Iterable):
        match get_args(source_type):
            case (item_type,):
                return tuple_schema(
                    [handler.generate_schema(item_type)],
                    variadic_item_index=0,
                )

    for member in bound if isinstance(bound, tuple) else (bound,):
        # pydantic raises for members it can't describe, such as the protocols that
        # sized and interval types are bound to.
        with suppress(PydanticSchemaGenerationError):
            schema = handler.generate_schema(member)
            # With arbitrary_types_allowed, pydantic gives unknown types an
            # is-instance schema, which has no JSON schema.
            if schema["type"] != "is-instance":
                return schema

    return any_schema()


def get_core_schema(
    parse: Callable[[object], object],
    decoding_schema: CoreSchema,
) -> AfterValidatorFunctionSchema:
    from pydantic_core import PydanticCustomError
    from pydantic_core.core_schema import no_info_after_validator_function

    def validate(value: object) -> object:
        try:
            return parse(value)
        except TypeError as exception:
            raise PydanticCustomError(
                "type_error",
                "{error}",
                {"error": str(exception)},
            ) from exception

    return no_info_after_validator_function(validate, decoding_schema)


def get_json_schema(
    schema: Schema,
    core_schema: AfterValidatorFunctionSchema,
    handler: GetJsonSchemaHandler,
) -> JsonSchemaValue:
    return {
        **handler(core_schema),
        **{key: value for key, value in schema.items() if value is not None},
    }
