from collections.abc import Callable
from typing import TypeAlias
from typing import TypeVar

T_contra = TypeVar("T_contra", bound=object, contravariant=True)

Predicate: TypeAlias = Callable[[T_contra], bool]
