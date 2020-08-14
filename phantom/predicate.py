from typing import Callable
from typing import cast
from typing import ClassVar
from typing import Dict
from typing import Generic
from typing import get_type_hints
from typing import Type
from typing import TypeVar

from . import predicates
from .base import Phantom


T = TypeVar("T", bound=object, covariant=True)
Predicate = Callable[[T], bool]


def _get_predicate_bound(fn: Predicate[T]) -> Type[T]:
    hints: Dict[str, type] = get_type_hints(fn)
    del hints["return"]

    types = iter(hints.values())
    type_ = cast(Type[T], next(types))

    try:
        next(types)
    except StopIteration:
        return type_
    else:
        raise TypeError(f"{fn.__qualname__} is not a predicate")


class PredicateType(Phantom, Generic[T]):
    __predicate__: ClassVar[Predicate[T]]
    __bound__: ClassVar[Type[T]]

    def __init_subclass__(cls, *, predicate: Predicate[T]) -> None:
        super().__init_subclass__()
        cls.__predicate__ = predicate
        cls.__bound__ = _get_predicate_bound(predicate)
        _get_predicate_bound(predicate)

    @classmethod
    def __instancecheck__(cls, instance: object) -> bool:
        return isinstance(instance, cls.__bound__) and cls.__predicate__(instance)


class Truthy(PredicateType, predicate=predicates.is_truthy):
    ...


class Falsy(PredicateType, predicate=predicates.is_falsy):
    ...
