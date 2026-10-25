from collections.abc import Sequence
from typing import Literal

from typing_extensions import TypedDict


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
    def __schema__(cls) -> Schema:
        """
        Hook for providing schema metadata. Override in subclasses to customize a types
        schema representation. The returned keys extend and override the JSON schema
        that pydantic generates for what the type decodes into. Keys with a value of
        ``None`` are left out.

        Example:

        .. code-block:: python

            class Name(str, Phantom, predicate=...):
                @classmethod
                def __schema__(cls):
                    return {**super().__schema__(), "description": "A name type"}
        """
        return {"title": cls.__name__}
