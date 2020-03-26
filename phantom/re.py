from __future__ import annotations

from typing import Any
from typing import ClassVar
from typing import Pattern
from typing import TypeVar

from phantom.base import Phantom

P = TypeVar("P", bound=Pattern)


class Match(str, Phantom):
    __pattern__: ClassVar[Pattern]

    def __init_subclass__(cls, *, pattern: Pattern) -> None:
        super().__init_subclass__()
        cls.__pattern__ = pattern

    @classmethod
    def __instancecheck__(cls, instance: Any) -> bool:
        return isinstance(instance, str) and cls.__pattern__.match(instance) is not None
