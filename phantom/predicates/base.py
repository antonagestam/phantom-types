from typing import Callable
from typing import TypeVar

from typing_extensions import Protocol

T = TypeVar("T", bound=object, contravariant=True)

Predicate = Callable[[T], bool]
