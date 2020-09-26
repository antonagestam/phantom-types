from typing import Union, Type, Final, TypeVar

Unset: Final = type("_Unset", (), {})
unset: Final = Unset()

V = TypeVar("V")


def default(value: Union[V, Unset], default: Type[V]) -> V:
    return default if isinstance(value, Unset) else value
