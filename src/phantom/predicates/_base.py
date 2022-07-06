from typing import Callable
from typing import TypeVar

T_contra = TypeVar("T_contra", bound=object, contravariant=True)

Predicate = Callable[[T_contra], bool]
