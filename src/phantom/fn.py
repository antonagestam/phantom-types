from __future__ import annotations

import functools
from functools import partial
from typing import Any
from typing import Callable
from typing import Final
from typing import Generic
from typing import ParamSpec
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
        return a(b(arg))

    c.__name__ = f"{a_name}∘{b_name}"
    c.__doc__ = f"Function composed as {a_name}({b_name}(_))."
    return c


Y = TypeVar("Y")
Z = TypeVar("Z")
P = ParamSpec("P")


class Pipe(Generic[P, Y]):
    """
    >>> __through__ = Pipe()
    >>> a = lambda x: f"Hello, {x}"
    >>> b = lambda x: f"{x}, how are you?"
    >>> fn = (__through__ | b) | __through__ | a
    >>> fn("Anton")
    """

    def __init__(self, func: Callable[P, Y] | None = None) -> None:
        self.func: Final = func

    def __or__(self, other: Callable[[Y], Z]) -> Callable[P, Z] | Pipe[Y, Z]:
        if not callable(other):
            return NotImplemented
        if self.func is None:
            return Pipe(other)
        return compose2(self.func, other)


class composable(Generic[P, Y]):
    """
    Decorator to compose functions with the | operator.
    """

    def __init__(self, _func: Callable[P, Y]):
        self._func: Callable[P, Y] = _func

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> Y:
        return self._func(*args, **kwargs)

    def __or__(self, other: Callable[[Y], Z]) -> composable[P, Z]:
        def composed(*args: P.args, **kwargs: P.kwargs) -> Z:
            return other(self(*args, **kwargs))

        return composable(composed)


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
