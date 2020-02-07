from __future__ import annotations

from typing import Any
from typing import Protocol
from typing import runtime_checkable


@runtime_checkable
class ImplementsInstanceCheck(Protocol):
    @classmethod
    def __instancecheck__(cls, instance: Any) -> bool:
        ...


class BaseInstanceCheck(type):
    """Metaclass that defers __instancecheck__ to its derived class."""

    def __instancecheck__(self, instance: Any) -> bool:
        if not issubclass(self, ImplementsInstanceCheck):
            return False
        return self.__instancecheck__(instance)
