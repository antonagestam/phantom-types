from typing import Any
from typing import Final
from typing import Generic
from typing import Iterable
from typing import MutableMapping
from typing import MutableSequence
from typing import MutableSet
from typing import Optional
from typing import Protocol
from typing import runtime_checkable
from typing import Sized
from typing import Type
from typing import TypeVar

from .base import Dependent


@runtime_checkable
class SizedIterable(Sized, Iterable, Protocol):
    ...


Mutable: Final = (MutableSequence, MutableSet, MutableMapping)
T = TypeVar("T", bound=SizedIterable)


class DependentSized(Iterable, Sized, Dependent[T], Generic[T]):
    __min__: int
    __max__: float

    def __init_subclass__(
        cls, *, min: Optional[int] = None, max: Optional[float] = None, **kwargs: Any
    ):
        super().__init_subclass__(**kwargs)
        # Resolve __min__ and __max__ in the order: class argument, inherited
        # value, default.
        cls.__min__ = getattr(cls, "__min__", 0) if min is None else min
        cls.__max__ = getattr(cls, "__max__", float("inf")) if max is None else max

    @classmethod
    def __instancecheck__(cls, instance: Any) -> bool:
        return (
            isinstance(instance, SizedIterable)
            and not isinstance(instance, Mutable)
            and cls.__min__ <= len(instance) <= cls.__max__
        )

    def __class_getitem__(cls: Type[T], item: Type[SizedIterable]) -> Type[T]:
        return cls


class NonEmpty(DependentSized[T], Generic[T], min=1):
    ...


class Empty(DependentSized[T], Generic[T], min=0, max=0):
    ...
