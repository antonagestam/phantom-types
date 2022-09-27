from typing import Optional
from typing import Sequence

from typing_extensions import ClassVar
from typing_extensions import Literal
from typing_extensions import TypedDict
from typing_extensions import final

import textwrap


class Schema(TypedDict, total=False):
    title: str
    description: str
    type: Literal["array", "string", "float", "number"]  # noqa: A003
    format: str  # noqa: A003
    examples: Sequence[object]
    minimum: Optional[float]
    maximum: Optional[float]
    exclusiveMinimum: Optional[float]
    exclusiveMaximum: Optional[float]
    minItems: Optional[int]
    maxItems: Optional[int]
    minLength: Optional[int]
    maxLength: Optional[int]


def desc_from_docstring(cls) -> str:
    # ds = (next(filter(lambda x: x.__doc__, cls.__mro__), cls).__doc__ or "").strip()
    ds = (cls.__doc__ or "").strip()

    if not ds:
        return ""
    lines = ds.split("\n", maxsplit=1)
    if len(lines) == 1:
        return ds
    rest = textwrap.dedent(lines[1])
    if fst := lines[0].strip():
        return f"{fst}\n{rest}"
    else:
        return rest


class SchemaField:
    __use_docstring__: ClassVar[str]

    @classmethod
    @final
    def __modify_schema__(cls, field_schema: dict) -> None:
        """
        This final method is called by pydantic and collects overrides from
        :func:`Phantom.__schema__() <phantom.Phantom.__schema__>`. Override
        :func:`__schema__() <phantom.Phantom.__schema__>` to provide custom schema
        representations for phantom types.
        """
        field_schema.update(
            {key: value for key, value in cls.__schema__().items() if value is not None}
        )
        if cls.__use_docstring__:
            if ds := desc_from_docstring(cls):
                field_schema["description"] = ds

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
