from typing import Optional
from typing import Sequence
from typing import TypedDict


class Schema(TypedDict, total=False):
    description: Optional[str]
    examples: Optional[Sequence[object]]
    minimum: Optional[float]
    maximum: Optional[float]
    exclusiveMinimum: Optional[float]
    exclusiveMaximum: Optional[float]


class SchemaField:
    @classmethod
    def __modify_schema__(cls, field_schema: dict) -> None:
        field_schema.update(
            {key: value for key, value in cls.__schema__().items() if value is not None}
        )

    @classmethod
    def __schema__(cls) -> Schema:
        return {}
