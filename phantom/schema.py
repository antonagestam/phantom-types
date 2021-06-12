from typing import Literal
from typing import Optional
from typing import Sequence
from typing import TypedDict


class Schema(TypedDict, total=False):
    title: str
    description: str
    type: Literal["array", "string", "float", "number"]
    examples: Sequence[object]
    minimum: Optional[float]
    maximum: Optional[float]
    exclusiveMinimum: Optional[float]
    exclusiveMaximum: Optional[float]
    minItems: Optional[int]
    maxItems: Optional[int]


class SchemaField:
    @classmethod
    def __modify_schema__(cls, field_schema: dict) -> None:
        field_schema.update(
            {key: value for key, value in cls.__schema__().items() if value is not None}
        )

    @classmethod
    def __schema__(cls) -> Schema:
        return {"title": cls.__name__}
