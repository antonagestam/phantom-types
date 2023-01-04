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


def _take_first(predicate, sequence, default=None):
    # NOTE: should I move this somewhere else?
    return next(filter(predicate, sequence), default)


def _description_from_docstring(cls) -> str:
    """Extract and reformat docstring from passed class or closest parent.

    Returns description text with fixed indentation, or
    an empty string in case the docstring is not present.
    """
    closest_docstring_parent = _take_first(lambda x: x.__doc__, cls.__mro__, cls)
    docstring = (closest_docstring_parent.__doc__ or "")
    if not docstring:
        return ""

    lines = docstring.strip().split("\n", maxsplit=1)
    if len(lines) == 1:
        return docstring

    return "\n".join((lines[0].strip(), textwrap.dedent(lines[1])))

def _fixup_description(cls, field_schema):
    docstring_cls = cls
    if cls.__use_docstring__:
        # use_docstring=True for given class
        field_schema["description"] = _description_from_docstring(docstring_cls)
    elif "description" not in field_schema:
        # use_docstring might have been set in a parent
        # -> must use it, if no description was provided in __schema__
        docstring_cls = _take_first(lambda x: x.__use_docstring__, cls.__mro__)
        if docstring_cls:
            field_schema["description"] = _description_from_docstring(docstring_cls)


class SchemaField:

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
        _fixup_description(cls, field_schema)


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
