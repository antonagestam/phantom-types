# Workaround for something that looks like this bug
# https://github.com/pytest-dev/pytest/issues/4386
from __future__ import annotations

import types
from dataclasses import is_dataclass
from itertools import product
from typing import MutableMapping
from typing import MutableSequence
from typing import MutableSet
from typing import NewType
from typing import Tuple
from typing import Union

from typing_extensions import Final
from typing_extensions import TypeGuard
from typing_extensions import get_args
from typing_extensions import get_origin


class UnresolvedClassAttribute(NotImplementedError):
    ...


def resolve_class_attr(
    cls: type,
    name: str,
    argument: object | None,
    required: bool = True,
) -> None:
    argument = getattr(cls, name, None) if argument is None else argument
    if argument is not None:
        setattr(cls, name, argument)
    elif required and not getattr(cls, "__abstract__", False):
        raise UnresolvedClassAttribute(
            f"Concrete phantom type {cls.__qualname__} must define class attribute "
            f"{name}."
        )


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


def fully_qualified_name(cls: type) -> str:
    return f"{cls.__module__}.{cls.__qualname__}"


mutable: Final = (MutableSequence, MutableSet, MutableMapping)
NotKnownMutable = NewType("NotKnownMutable", type)
"""
Internal type to mark types that are not known to be mutable. The term immutable is
avoided here because there is no way to guarantee that a checked type isn't actually
mutable, so we don't want to communicate in strong terms here.
"""


class MutableType(TypeError):
    ...


def is_not_mutable(type_: BoundType) -> TypeGuard[NotKnownMutable]:
    if any(is_subtype(type_, mutable_type) for mutable_type in mutable):
        raise MutableType(f"{type_!r} is a subclass of one of {mutable!r}")
    if (
        is_dataclass(type_)
        and not type_.__dataclass_params__.frozen  # type: ignore[union-attr]
    ):
        raise MutableType(f"{type_!r} is a an unfrozen dataclass type")
    return True


try:
    MaybeUnionType = types.UnionType  # type: ignore[attr-defined]
except AttributeError:
    MaybeUnionType = None


def is_union_type(value: object) -> TypeGuard[type]:
    return MaybeUnionType and isinstance(value, MaybeUnionType)


def is_union(value: object) -> TypeGuard[type]:
    return get_origin(value) == Union or is_union_type(value)
