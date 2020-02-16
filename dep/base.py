from __future__ import annotations

from abc import ABCMeta
from typing import Any
from typing import Generic
from typing import Protocol
from typing import runtime_checkable
from typing import Type
from typing import TypeVar


@runtime_checkable
class ImplementsInstanceCheck(Protocol):
    @classmethod
    def __instancecheck__(cls, instance: Any) -> bool:
        ...


class DependentTypeMeta(ABCMeta):
    """Metaclass that defers __instancecheck__ to derived classes."""

    def __instancecheck__(self, instance: Any) -> bool:
        if not issubclass(self, ImplementsInstanceCheck):
            return False
        return self.__instancecheck__(instance)


RuntimeType = TypeVar("RuntimeType", bound=Any)


class Dependent(Generic[RuntimeType], metaclass=DependentTypeMeta):
    Derived = TypeVar("Derived", bound="Dependent")

    @classmethod
    def from_instance(cls: Type[Derived], instance: RuntimeType) -> Derived:
        if not isinstance(instance, cls):
            raise ValueError(f"Can't create {cls.__qualname__} from {instance}")
        return instance

    def __init_subclass__(cls, **kwargs: Any) -> None:
        """
        We only override __init_subclass__  to suppress the mypy error in one place.
        """
        super().__init_subclass__(**kwargs)  # type: ignore[call-arg]
