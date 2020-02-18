from typing import Any
from typing import Optional
from typing import Sized
from typing import TypeVar

from .base import Dependent


S = TypeVar("S", bound=Sized)


class SizeDependent(Dependent[S]):
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
            isinstance(instance, Sized) and cls.__min__ <= len(instance) <= cls.__max__
        )


class NonEmpty(SizeDependent, min=1):
    ...


class Empty(SizeDependent, min=0, max=0):
    ...
