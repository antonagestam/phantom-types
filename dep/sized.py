from typing import Any
from typing import Generic
from typing import Optional
from typing import Sequence
from typing import TypeVar

from .base import Dependent


T = TypeVar("T", bound=Sequence)


class SizedSequence(Sequence, Dependent[T], Generic[T]):
    __min__: int
    __max__: float

    def __init_subclass__(
        cls, *, min: Optional[int] = None, max: Optional[float] = None, **kwargs: Any
    ):
        super().__init_subclass__(**kwargs)
        # Resolve __min__ and __max__ in the order: class argument, inherited value,
        # default.
        cls.__min__ = getattr(cls, "__min__", 0) if min is None else min
        cls.__max__ = getattr(cls, "__max__", float("inf")) if max is None else max

    @classmethod
    def __instancecheck__(cls, instance: Any) -> bool:
        return (
            isinstance(instance, Sequence)
            and cls.__min__ <= len(instance) <= cls.__max__
        )

    def __class_getitem__(cls, item):
        return cls


class NonEmpty(SizedSequence[T], Generic[T], min=1):
    ...


class Empty(SizedSequence[T], Generic[T], min=0, max=0):
    ...
