# Workaround for something that looks like this bug
# https://github.com/pytest-dev/pytest/issues/4386
from __future__ import annotations

import functools
from typing import Any
from typing import Callable
from typing import Optional
from typing import Tuple
from typing import Type
from typing import TypeVar
from typing import Union


class UnresolvedClassAttribute(NotImplementedError):
    ...


def resolve_class_attr(
    cls: Type, name: str, argument: Optional[object], required: bool = True
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
