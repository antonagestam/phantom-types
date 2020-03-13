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

    def __call__(cls, instance):
        return cls.from_instance(instance)  # type: ignore[attr-defined]


Derived = TypeVar("Derived")


class Dependent(metaclass=DependentMeta):
    @classmethod
    def from_instance(cls: Type[Derived], instance: Any) -> Derived:
        if not isinstance(instance, cls):
            raise TypeError(f"Can't create {cls.__qualname__} from {instance!r}")
        return instance

    def __init_subclass__(cls) -> None:
        """
        We only override __init_subclass__ to suppress the mypy error in one
        place instead of in every subclass. See
        https://github.com/python/mypy/issues/4660
        """
        super().__init_subclass__()

    @classmethod
    @abc.abstractmethod
    def __instancecheck__(cls, instance: Any) -> bool:
        ...
