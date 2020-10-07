from __future__ import annotations

import abc
from typing import Callable
from typing import ClassVar
from typing import Generic
from typing import Optional
from typing import Type
from typing import TypeVar

from .utils import resolve_class_attr


class PhantomMeta(abc.ABCMeta):
    """
    Metaclass that defers __instancecheck__ to derived classes and prevents actual
    instance creation.
    """

    def __instancecheck__(self, instance: object) -> bool:
        if not issubclass(self, Phantom):
            return False
        return self.__instancecheck__(instance)

    # With the current level of metaclass support in mypy it's unlikely that we'll be
    # able to make this context typed, hence the ignores.
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


T = TypeVar("T", covariant=True, bound=object)
Predicate = Callable[[T], bool]


class PredicateType(Phantom, Generic[T]):
    __predicate__: ClassVar[Predicate[T]]
    __bound__: ClassVar[Type[T]]

    def __init_subclass__(
        cls,
        predicate: Optional[Predicate[T]] = None,
        bound: Optional[Type[T]] = None,
        **kwargs: object,
    ) -> None:
        super().__init_subclass__(**kwargs)  # type: ignore[call-arg]
        resolve_class_attr(cls, "__predicate__", predicate)
        resolve_class_attr(cls, "__bound__", bound)

    @classmethod
    def __instancecheck__(cls, instance: object) -> bool:
        return isinstance(instance, cls.__bound__) and cls.__predicate__(instance)
