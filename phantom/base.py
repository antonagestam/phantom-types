import abc
from typing import Type
from typing import TypeVar


class PhantomMeta(abc.ABCMeta):
    """
    Metaclass that defers __instancecheck__ to derived classes and prevents
    actual instance creation.
    """

    def __instancecheck__(self, instance: object) -> bool:
        if not issubclass(self, Phantom):
            return False
        return self.__instancecheck__(instance)

    # With the current level of metaclass support in mypy it's unlikely that
    # we'll be able to make this context typed, hence the ignores.
    def __call__(cls, instance):  # type: ignore[no-untyped-def]
        return cls.from_instance(instance)  # type: ignore[attr-defined,misc]


Derived = TypeVar("Derived")


class Phantom(metaclass=PhantomMeta):
    @classmethod
    def from_instance(cls: Type[Derived], instance: object) -> Derived:
        if not isinstance(instance, cls):
            raise TypeError(
                f"Can't create phantom type {cls.__qualname__} from {instance!r}"
            )
        return instance

    @classmethod
    @abc.abstractmethod
    def __instancecheck__(cls, instance: object) -> bool:
        ...
