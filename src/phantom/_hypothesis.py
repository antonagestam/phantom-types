from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Callable
from typing import TypeVar
from typing import Union

from typing_extensions import TypeAlias

if TYPE_CHECKING:
    from hypothesis.strategies import SearchStrategy
else:
    try:
        from hypothesis.strategies import SearchStrategy
    except ImportError:
        SearchStrategy = None

__all__ = ("HypothesisStrategy", "register_type_strategy", "SearchStrategy")

T = TypeVar("T")
HypothesisStrategy: TypeAlias = Union[
    SearchStrategy,
    Callable[[type[T]], Union[SearchStrategy[T], None]],
]
register_type_strategy: Callable[[type, HypothesisStrategy], None] | None


try:
    from hypothesis.strategies import register_type_strategy  # type: ignore[assignment]
except ImportError:
    register_type_strategy = None
