from typing import Optional
from typing import Tuple
from typing import Union

from .base import Predicate


def ends_with(
    suffix: Union[str, Tuple[str, ...]],
    start: Optional[int] = None,
    end: Optional[int] = None,
) -> Predicate[str]:
    def check(value: str) -> bool:
        return value.endswith(suffix, start, end)

    return check


def starts_with(
    prefix: Union[str, Tuple[str, ...]],
    start: Optional[int] = None,
    end: Optional[int] = None,
) -> Predicate[str]:
    def check(value: str) -> bool:
        return value.startswith(prefix, start, end)

    return check
