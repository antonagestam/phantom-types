import abc
from typing import Type
from typing import TypeVar
from typing import Union


class Undefined:
    pass


V = TypeVar("V")
undefined = Undefined()
Maybe = Union[Undefined, V]


def default(value: Union[V, Undefined], default: V) -> V:
    return default if isinstance(value, Undefined) else value


def is_abstract(cls: Type) -> bool:
    return abc.ABC in cls.__mro__
