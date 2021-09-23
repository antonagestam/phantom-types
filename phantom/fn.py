from __future__ import annotations

import functools
from functools import partial
from typing import Any
from typing import Callable
from typing import TypeVar


def _name(fn: Callable) -> str:
    if isinstance(fn, partial):
        fn = fn.func
    try:
        return fn.__qualname__
    except AttributeError:
        return str(fn)


AA = TypeVar("AA")
AR = TypeVar("AR")
BA = TypeVar("BA")


def compose2(a: Callable[[AA], AR], b: Callable[[BA], AA]) -> Callable[[BA], AR]:
    """
    Returns a function composed from the two given functions ``a`` and ``b`` such that
    calling ``compose2(a, b)(x)`` is equivalent to calling ``a(b(x))``.

    >>> compose2("".join, reversed)("!olleH")
    'Hello!'
    """
    a_name = _name(a)
    b_name = _name(b)

    def c(arg: BA) -> AR:
        f"Function composed as {a_name}({b_name}(_))."
        return a(b(arg))

    c.__name__ = f"{a_name}∘{b_name}"
    return c


A = TypeVar("A")


def excepts(
    exception: tuple[type[Exception], ...] | type[Exception],
    negate: bool = False,
) -> Callable[[Callable[[A], Any]], Callable[[A], bool]]:
    """
    Turn a unary function that raises an exception into a boolean predicate.

    >>> def validate_positive(number: int) -> None:
    ...     if number < 0: raise ValueError
    >>> is_positive = excepts(ValueError)(validate_positive)
    >>> is_positive(0), is_positive(-1)
    (True, False)
    """

    def decorator(fn: Callable[[A], Any]) -> Callable[[A], bool]:
        @functools.wraps(fn)
        def wrapper(arg: A) -> bool:
            try:
                fn(arg)
            except exception:
                return negate
            return not negate

        return wrapper

    return decorator
