from typing import Callable
from typing import TypeVar

AA = TypeVar("AA")
AR = TypeVar("AR")
BA = TypeVar("BA")


def compose2(a: Callable[[AA], AR], b: Callable[[BA], AA]) -> Callable[[BA], AR]:
    """
    >>> compose2(print, lambda a: a.upper())("hello")
    HELLO
    >>> compose2(str.title, " ".join)(["capitalized", "sentence"])
    'Capitalized Sentence'
    >>> print(compose2(str.title, ", ".join).__name__)
    str.title|str.join
    >>> print(compose2(str.title, ", ".join).__doc__)
    Function composed as str.title(str.join(_))
    """

    def c(arg: BA) -> AR:
        return a(b(arg))

    c.__name__ = f"{a.__qualname__}|{b.__qualname__}"
    c.__doc__ = f"Function composed as {a.__qualname__}({b.__qualname__}(_))."
    return c
