from typing import ClassVar
from typing import Generic
from typing import Iterable
from typing import MutableMapping
from typing import MutableSequence
from typing import MutableSet
from typing import Optional
from typing import Sized
from typing import Type
from typing import TypeVar

# We attempt to import _ProtocolMeta from typing_extensions to support Python 3.7 but
# fall back the typing module to support Python 3.8+. This is the closest I could find
# to documentation of _ProtocolMeta.
# https://github.com/python/cpython/commit/74d7f76e2c953fbfdb7ce01b7319d91d471cc5ef
try:
    from typing_extensions import _ProtocolMeta  # type: ignore[attr-defined]
except ImportError:
    from typing import _ProtocolMeta  # type: ignore[attr-defined]

from typing_extensions import Final
from typing_extensions import Protocol
from typing_extensions import runtime_checkable

from .base import Phantom
from .base import PhantomMeta


__all__ = (
    "PhantomSized",
    "NonEmpty",
    "Empty",
)


mutable: Final = (MutableSequence, MutableSet, MutableMapping)
T = TypeVar("T", bound=object, covariant=True)


@runtime_checkable
class SizedIterable(Sized, Iterable[T], Protocol[T]):
    ...


class SizedIterablePhantomMeta(PhantomMeta, _ProtocolMeta):
    ...


class PhantomSized(
    SizedIterable[T], Phantom, Generic[T], metaclass=SizedIterablePhantomMeta
):
    __min__: ClassVar[int] = 0
    __max__: ClassVar[float] = float("inf")

    def __init_subclass__(
        cls, *, min: Optional[int] = None, max: Optional[float] = None
    ):
        super().__init_subclass__()
        if min is not None:
            cls.__min__ = min
        if max is not None:
            cls.__max__ = max

    @classmethod
    def __instancecheck__(cls, instance: object) -> bool:
        return (
            isinstance(instance, SizedIterable)
            and not isinstance(instance, mutable)
            and cls.__min__ <= len(instance) <= cls.__max__
        )

    def __class_getitem__(cls: Type[T], item: Type[SizedIterable]) -> Type[T]:
        return cls


class NonEmpty(PhantomSized[T], Generic[T], min=1):
    ...


class Empty(PhantomSized[T], Generic[T], min=0, max=0):
    ...
