import abc
from typing import Any
from typing import Type
from typing import TypeVar


class DependentMeta(abc.ABCMeta):
    """
    Metaclass that defers __instancecheck__ to derived classes and prevents
    actual instance creation.
    """

    def __instancecheck__(self, instance: Any) -> bool:
        if not issubclass(self, Dependent):
            return False
        return self.__instancecheck__(instance)

    def __subclasscheck__(self, subclass):
        if hasattr(self, "__subclasscheck__"):
            return self.__subclasscheck__(subclass)
        return False

    def __call__(cls, instance):
        return cls.from_instance(instance)  # type: ignore[attr-defined]


Derived = TypeVar("Derived")


class Dependent(metaclass=DependentMeta):
    @classmethod
    def from_instance(cls: Type[Derived], instance: Any) -> Derived:
        if not isinstance(instance, cls):
            raise TypeError(f"Can't create {cls.__qualname__} from {instance!r}")
        return instance

    @classmethod
    @abc.abstractmethod
    def __instancecheck__(cls, instance: Any) -> bool:
        ...
