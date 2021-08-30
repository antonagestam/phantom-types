from typing import Any
from typing import Tuple

__all__ = ("get_args",)

try:
    from typing import get_args  # type: ignore[attr-defined]
except ImportError:

    def get_args(tp: Any) -> Tuple[Any, ...]:
        return tp.__args__  # type: ignore[no-any-return]
