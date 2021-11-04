from typing import Optional
from typing import Sequence

from typing_extensions import Literal
from typing_extensions import TypedDict
from typing_extensions import final


class Schema(TypedDict, total=False):
    title: str
    description: str
    type: Literal["array", "string", "float", "number"]
    format: str
    examples: Sequence[object]
    minimum: Optional[float]
    maximum: Optional[float]
    exclusiveMinimum: Optional[float]
    exclusiveMaximum: Optional[float]
    minItems: Optional[int]
    maxItems: Optional[int]


class SchemaField:
    @classmethod
    @final
    def __modify_schema__(cls, field_schema: dict) -> None:
        """
        This final method is called by pydantic and collects overrides from
        :func:`Phantom.__schema__() <phantom.Phantom.__schema__>`.
        Override :func:`__schema__() <phantom.Phantom.__schema__>` to provide custom
        schema representations for phantom types.
        """
        field_schema.update(
            {key: value for key, value in cls.__schema__().items() if value is not None}
        )

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
