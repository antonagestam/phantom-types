import abc
from typing import Type
from typing import TypeVar
from typing import Union


class Undefined:
    pass


V = TypeVar("V")
undefined = Undefined()
Undefined.__init__ = NotImplemented  # type: ignore[assignment]
Maybe = Union[Undefined, V]


def is_abstract(cls: Type) -> bool:
    return abc.ABC in cls.__mro__


def resolve_class_attr(cls: Type, name: str, argument: Maybe[object]) -> None:
    argument = (
        getattr(cls, name, undefined) if isinstance(argument, Undefined) else argument
    )
    if not isinstance(argument, Undefined):
        setattr(cls, name, argument)
