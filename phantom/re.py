from typing import ClassVar
from typing import Pattern

from .base import Phantom


class Match(str, Phantom):
    __pattern__: ClassVar[Pattern[str]]

    def __init_subclass__(cls, pattern: Pattern[str], **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)  # type: ignore[call-arg]
        cls.__pattern__ = pattern

    @classmethod
    def __instancecheck__(cls, instance: object) -> bool:
        return isinstance(instance, str) and cls.__pattern__.match(instance) is not None
