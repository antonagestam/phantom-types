from typing import TypeVar, Protocol

T = TypeVar("T", bound=object, contravariant=True)


class Predicate(Protocol[T]):
    def __call__(self, arg: T, /) -> bool:
        ...
