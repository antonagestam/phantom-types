from __future__ import annotations

import abc
from typing import Any
from typing import Callable
from typing import ClassVar
from typing import Generic
from typing import Iterable
from typing import Optional
from typing import Tuple
from typing import Type
from typing import TypeVar
from typing import Union

from .utils import resolve_class_attr


class PhantomMeta(abc.ABCMeta):
    """
    Metaclass that defers __instancecheck__ to derived classes and prevents actual
    instance creation.
    """

    def __instancecheck__(self, instance: object) -> bool:
        if not issubclass(self, PhantomBase):
            return False
        return self.__instancecheck__(instance)

    # With the current level of metaclass support in mypy it's unlikely that we'll be
    # able to make this context typed, hence the ignores.
    def __call__(cls, instance):  # type: ignore[no-untyped-def]
        return cls.parse(instance)  # type: ignore[attr-defined,misc]


class NotWithinBound(TypeError):
    ...


def parse_bound(bound: Type[T], instance: object) -> T:
    if not isinstance(instance, bound):
        raise NotWithinBound(
            f"Can't parse {bound.__qualname__} from {type(instance).__name__} value: "
            f"{instance!r}"
        )
    return instance


Derived = TypeVar("Derived")


class PhantomBase(metaclass=PhantomMeta):
    @classmethod
    def parse(cls: Type[Derived], instance: object) -> Derived:
        return parse_bound(cls, instance)

    @classmethod
    @abc.abstractmethod
    def __instancecheck__(cls, instance: object) -> bool:
        ...


T = TypeVar("T", covariant=True, bound=object)
TypeSpec = Union[Type[T], Tuple[Type[T], ...]]
Predicate = Callable[[T], bool]


# TODO: Consider introducing class argument abstract: bool, to be able to add stricter
#  checks for allowing the deferral of definitions of class arguments/attributes. Using
#  abc.ABC is probably too much of a hassle due to metaclass conflicts.
class Phantom(PhantomBase, Generic[T]):
    """
    Behaviour for __bound__ should be that is always overridable with a class argument
    of bound=..., but will default to any bases given before Phantom. The thesis is that
    this will provide an API that is _ for most cases and enough flexibility for more
    complex cases.

    Implicit bound:
    >>> class A(float, Phantom):
    ...     ...
    >>> A.__bound__
    (<class 'float'>,)

    Explicit bound:
    >>> class A(Phantom, bound=int):
    ...     ...
    >>> A.__bound__
    (<class 'int'>,)

    Speficy kind in base type:
    >>> class A(Phantom, kind=(int, float)):
    ...     ...
    >>> class B(A, bound=str):
    ...     ... #doctest: +ELLIPSIS
    Traceback (most recent call last):
      ...
    TypeError: One of the bounds of <class 'phantom.base.B'> (<class 'str'>) isn't a \
subtype of its kind ((<class 'int'>, <class 'float'>))
    """

    __predicate__: ClassVar[Predicate[T]]
    __bound__: ClassVar[TypeSpec[T]]
    __kind__: ClassVar[TypeSpec[Any]]

    def __init_subclass__(
        cls,
        predicate: Optional[Predicate[T]] = None,
        bound: Optional[Type[T]] = None,
        kind: Optional[TypeSpec] = None,
        **kwargs: Any,
    ) -> None:
        super().__init_subclass__(**kwargs)  # type: ignore[call-arg]
        resolve_class_attr(cls, "__predicate__", predicate)
        resolve_class_attr(cls, "__kind__", kind)
        cls._resolve_bound(bound)

    @classmethod
    def _interpret_implicit_bound(cls) -> Iterable[type]:
        for type_ in cls.__mro__:
            if type_ is cls:
                continue
            if issubclass(type_, Phantom):
                break
            yield type_
        else:
            raise RuntimeError(f"{cls} is not a subclass of Phantom")

    @classmethod
    def _resolve_bound(cls, class_arg: Optional[TypeSpec[T]]) -> None:
        bound: TypeSpec
        if class_arg is not None:
            bound = class_arg if isinstance(class_arg, tuple) else (class_arg,)
        elif implicit := tuple(cls._interpret_implicit_bound()):
            bound = implicit
        elif (inherited := getattr(cls, "__bound__", None)) is not None:
            bound = inherited
        else:
            return
        if (kind := getattr(cls, "__kind__", None)) is not None:
            for part in bound if isinstance(bound, Iterable) else (bound,):
                if not issubclass(part, kind):
                    raise TypeError(
                        f"One of the bounds of {cls} ({part}) isn't a subtype of its "
                        f"kind ({kind})"
                    )
        cls.__bound__ = bound

    @classmethod
    def __instancecheck__(cls, instance: object) -> bool:
        return isinstance(instance, cls.__bound__) and cls.__predicate__(instance)
