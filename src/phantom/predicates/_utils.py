from functools import partial
from typing import Callable
from typing import TypeVar


def _explode_partial(obj: partial) -> str:
    positional_args = ", ".join(map(repr, obj.args))
    keyword_args = ", ".join(
        f"{name}={value!r}" for name, value in obj.keywords.items()
    )
    args = ", ".join((positional_args, keyword_args))
    return f"{obj.func.__qualname__}({args})"


def _name_or_repr(obj: object) -> str:
    if isinstance(obj, partial):
        return _explode_partial(obj)
    try:
        return str(obj.__qualname__)  # type: ignore[attr-defined]
    except AttributeError:
        return repr(obj)


B = TypeVar("B", bound=Callable)


def bind_name(wrapped: Callable, *values: object) -> Callable[[B], B]:
    name = (
        f"{wrapped.__qualname__}({', '.join(_name_or_repr(value) for value in values)})"
    )

    def decorator(inner: B) -> B:
        inner.__qualname__ = inner.__name__ = name
        return inner

    return decorator
