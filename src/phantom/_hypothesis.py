from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING
from typing import TypeAlias
from typing import TypeVar

if TYPE_CHECKING:
    from hypothesis.strategies import SearchStrategy
else:
    SearchStrategy = None


__all__ = ("HypothesisStrategy", "register_type_strategy", "SearchStrategy")

T = TypeVar("T")
HypothesisStrategy: TypeAlias = (
    "SearchStrategy | Callable[[type[T]], SearchStrategy[T] | None]"
)
register_type_strategy: Callable[[type, HypothesisStrategy], None] | None


try:
    from hypothesis.strategies import register_type_strategy  # type: ignore[assignment]
except ImportError:
    register_type_strategy = None
