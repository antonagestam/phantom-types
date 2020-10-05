from typing import Optional
from typing import Type


def resolve_class_attr(cls: Type, name: str, argument: Optional[object]) -> None:
    argument = getattr(cls, name, None) if argument is None else argument
    if argument is not None:
        setattr(cls, name, argument)
