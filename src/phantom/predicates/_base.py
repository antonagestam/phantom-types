from typing import Callable
from typing import TypeVar

from typing_extensions import TypeAlias

T_contra = TypeVar("T_contra", bound=object, contravariant=True)

Predicate: TypeAlias = Callable[[T_contra], bool]
