from typing import Callable
from typing import TypeVar

T = TypeVar("T", bound=object, contravariant=True)

Predicate = Callable[[T], bool]
