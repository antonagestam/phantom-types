from typing import Protocol
from typing import TypeVar

T = TypeVar("T", bound=object, contravariant=True)


class Predicate(Protocol[T]):
    def __call__(self, arg: T, /) -> bool:
        ...
