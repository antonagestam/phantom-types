# Workaround for something that looks like this bug
# https://github.com/pytest-dev/pytest/issues/4386
from __future__ import annotations

import functools
from itertools import product
from typing import Any
from typing import Callable
from typing import Optional
from typing import Tuple
from typing import Type
from typing import TypeVar
from typing import Union
from typing import get_args
from typing import get_origin


class UnresolvedClassAttribute(NotImplementedError):
    ...


def resolve_class_attr(
    cls: type, name: str, argument: Optional[object], required: bool = True
) -> None:
    argument = getattr(cls, name, None) if argument is None else argument
    if argument is not None:
        setattr(cls, name, argument)
    elif required and not getattr(cls, "__abstract__", False):
        raise UnresolvedClassAttribute(
            f"Concrete phantom type {cls.__qualname__} must define class attribute "
            f"{name}."
        )


A = TypeVar("A")


def excepts(
    exception: Union[Tuple[Type[Exception], ...], Type[Exception]],
    negate: bool = False,
) -> Callable[[Callable[[A], Any]], Callable[[A], bool]]:
    """Turn a unary function that raises an exception into a boolean predicate."""

    def decorator(fn: Callable[[A], Any]) -> Callable[[A], bool]:
        @functools.wraps(fn)
        def wrapper(arg: A, /) -> bool:
            try:
                fn(arg)
            except exception:
                return negate
            return not negate

        return wrapper

    return decorator


BoundType = Union[type, Tuple[type, ...]]


def _is_union(type_: BoundType) -> bool:
    return get_origin(type_) is Union


def _is_intersection(type_: BoundType) -> bool:
    return isinstance(type_, tuple)


def is_subtype(a: BoundType, b: BoundType) -> bool:  # noqa: C901
    """
    Return True if ``a`` is a subtype of ``b``. Supports single-level typing.Unions
    and intersections represented as tuples respectively without nesting.

    The cases that this function deals with can be divided into the following cases,
    where T is neither a union or intersection:

    1. Union, Union: Success if all types in a have a subclass in b.
    2. T, Union: Success if a is a subclass of one or more types in b.
    3. Union, T: Always fails (except when a single-type union, see 9).
    4. T, Intersection: Success if a is a subclass of all types in b.
    5. Intersection, T: Success if one type in a is a subclass of b.
    6. Intersection, Union: Success if one type in a is a subclass of one type in b.
    7. Union, Intersection: Always fails (except when a is a single-type union see 4).
    8. Intersection, Intersection: Success if all items in b have a subclass in a.
    9. T, T: Success if a is a subclass of b.
    """

    if _is_union(a) and _is_union(b):
        for a_part in get_args(a):
            for b_part in get_args(b):
                if issubclass(a_part, b_part):
                    break
            else:
                return False
        return True
    elif _is_intersection(a) and _is_union(b):
        assert isinstance(a, tuple)
        for a_part, b_part in product(a, get_args(b)):
            if issubclass(a_part, b_part):
                return True
        return False
    elif _is_intersection(a) and _is_intersection(b):
        assert isinstance(a, tuple)
        assert isinstance(b, tuple)
        for b_part in b:
            for a_part in a:
                if issubclass(a_part, b_part):
                    break
            else:
                return False
        return True
    elif _is_union(a):
        return False
    elif _is_union(b):
        assert isinstance(a, type)
        return any(issubclass(a, b_part) for b_part in get_args(b))
    elif _is_intersection(b):
        assert isinstance(a, type)
        assert isinstance(b, tuple)
        return all(issubclass(a, b_part) for b_part in b)
    elif _is_intersection(a):
        assert isinstance(a, tuple)
        return any(issubclass(a_part, b) for a_part in a)
    assert isinstance(a, type)
    return issubclass(a, b)
