from functools import partial
from typing import Callable
from typing import TypeVar


def _name(fn: Callable) -> str:
    if isinstance(fn, partial):
        fn = fn.func
    return fn.__qualname__


AA = TypeVar("AA")
AR = TypeVar("AR")
BA = TypeVar("BA")


def compose2(a: Callable[[AA], AR], b: Callable[[BA], AA]) -> Callable[[BA], AR]:
    """
    Compose a new function that returns the result of applying a to the result of b.
    """
    a_name = _name(a)
    b_name = _name(b)

    def c(arg: BA) -> AR:
        f"Function composed as {a_name}({b_name}(_))."
        return a(b(arg))

    c.__name__ = f"{a_name}∘{b_name}"
    return c
