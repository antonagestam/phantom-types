from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING
from typing import Literal

if TYPE_CHECKING:
    try:
        from pydantic import GetJsonSchemaHandler
        from pydantic.json_schema import JsonSchemaValue
        from pydantic_core import CoreSchema
    except ImportError:
        pass

from typing_extensions import TypedDict
from typing_extensions import final


class Schema(TypedDict, total=False):
    title: str
    description: str
    type: Literal["array", "string", "float", "number"]
    format: str
    examples: Sequence[object]
    minimum: float | None
    maximum: float | None
    exclusiveMinimum: float | None
    exclusiveMaximum: float | None
    minItems: int | None
    maxItems: int | None
    minLength: int | None
    maxLength: int | None


class SchemaField:
    @classmethod
    @final
    def __get_pydantic_json_schema__(
        cls, schema: CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        """
        Pydantic V2 hook for JSON schema generation. Collects overrides from
        :func:`Phantom.__schema__() <phantom.Phantom.__schema__>`. Override
        :func:`__schema__() <phantom.Phantom.__schema__>` to provide custom schema
        representations for phantom types.
        """
        json_schema = handler(schema)
        json_schema = handler.resolve_ref_schema(json_schema)
        json_schema.update(
            {key: value for key, value in cls.__schema__().items() if value is not None}
        )
        return json_schema

    @classmethod
    def __schema__(cls) -> Schema:
        """
        Hook for providing schema metadata. Override in subclasses to customize a types
        schema representation. See pydantic's documentation on ``__modify_schema__()``
        for more information. This hook differs to pydantic's ``__modify_schema__()``
        and expects subclasses to instantiate new dicts instead of mutating a given one.

        Example:

        .. code-block:: python

            class Name(str, Phantom, predicate=...):
                @classmethod
                def __schema__(cls):
                    return {**super().__schema__(), "description": "A name type"}
        """
        return {"title": cls.__name__}
