from __future__ import annotations

from typing import Any
from typing import Callable
from typing import Iterable
from typing import Sequence
from typing import TypeVar
from typing import cast

from typing_extensions import Final
from typing_extensions import TypeAlias
from typing_extensions import get_args

from ._utils.misc import is_union
from .errors import BoundError
from .predicates.boolean import all_of
from .predicates.generic import of_complex_type
from .predicates.generic import of_type

__all__ = ("get_bound_parser", "parse_str", "Parser")

T = TypeVar("T", covariant=True)
Parser: TypeAlias = Callable[[object], T]


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


def get_bound_parser(bound: type[T] | Any) -> Parser[T]:
    within_bound = (
        # Interpret sequence as intersection
        all_of(of_type(t) for t in bound)
        if isinstance(bound, Sequence)
        else of_complex_type(bound)
    )

    def parser(instance: object) -> T:
        if not within_bound(instance):
            raise BoundError(
                f"Value is not within bound of {display_bound(bound)!r}: {instance!r}"
            )
        return cast(T, instance)

    return parser


parse_str: Final[Callable[[object], str]] = get_bound_parser(str)
