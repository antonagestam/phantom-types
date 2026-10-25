from __future__ import annotations

from collections.abc import Callable
from collections.abc import Iterable
from collections.abc import Sequence
from typing import Any
from typing import Final
from typing import TypeAlias
from typing import TypeVar
from typing import cast
from typing import get_args

from ._utils.misc import is_union
from .errors import BoundError
from .predicates.boolean import all_of
from .predicates.generic import of_complex_type
from .predicates.generic import of_type

__all__ = ("Parser", "get_bound_parser", "parse_str")

T_co = TypeVar("T_co", covariant=True)
Parser: TypeAlias = Callable[[object], T_co]


def display_bound(bound: Any) -> str:
    if isinstance(bound, Iterable):
        return f"Intersection[{', '.join(display_bound(part) for part in bound)}]"
    if is_union(bound):
        return (
            f"typing.Union["
            f"{', '.join(display_bound(part) for part in get_args(bound))}"
            f"]"
        )
    return str(getattr(bound, "__name__", bound))


def get_bound_parser(bound: type[T_co] | Any) -> Parser[T_co]:
    within_bound = (
        # Interpret sequence as intersection
        all_of(of_type(t) for t in bound)
        if isinstance(bound, Sequence)
        else of_complex_type(bound)
    )

    def parser(instance: object) -> T_co:
        if not within_bound(instance):
            raise BoundError(
                f"Value is not within bound of {display_bound(bound)!r}: {instance!r}"
            )
        return cast(T_co, instance)

    return parser


parse_str: Final[Callable[[object], str]] = get_bound_parser(str)
