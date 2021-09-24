from __future__ import annotations

from functools import partial
from operator import add
from operator import attrgetter
from operator import itemgetter
from operator import mul
from typing import Callable
from typing import Sequence
from typing import TypeVar

import pytest

from phantom import Predicate
from phantom.fn import _name
from phantom.fn import compose2
from phantom.fn import excepts
from phantom.predicates.boolean import both
from phantom.predicates.collection import count
from phantom.predicates.collection import every
from phantom.predicates.generic import equal


class Test_name:
    class Nested:
        def method(self):
            ...

    @pytest.mark.parametrize(
        "function, expected",
        [
            (lambda: None, "Test_name.<lambda>"),
            (partial(int), "int"),
            (Nested.method, "Test_name.Nested.method"),
            (attrgetter("attrib"), "operator.attrgetter('attrib')"),
            (itemgetter("key"), "operator.itemgetter('key')"),
        ],
    )
    def test_can_get_name_of(self, function: Callable, expected: str) -> None:
        assert _name(function) == expected


def reversed_str(value: str) -> str:
    return "".join(reversed(value))


AA = TypeVar("AA")
AR = TypeVar("AR")
BA = TypeVar("BA")


class TestCompose2:
    @pytest.mark.parametrize(
        "a, b, argument, expected, name",
        [
            (str.title, reversed_str, "test", "Tset", "str.title∘reversed_str"),
            (reversed_str, str.title, "test", "tseT", "reversed_str∘str.title"),
            (partial(add, 7), partial(mul, 3), 5, 22, "add∘mul"),
            (partial(mul, 3), partial(add, 7), 5, 36, "mul∘add"),
        ],
    )
    def test_can_compose_two(
        self,
        a: Callable[[AA], AR],
        b: Callable[[BA], AA],
        argument: BA,
        expected: AR,
        name: str,
    ) -> None:
        composed = compose2(a, b)
        assert composed(argument) == expected
        assert composed.__name__ == name

    def test_can_compose_complex_predicate(self) -> None:
        as_parts: Callable[[str], list[str]] = partial(str.split, sep=".")
        is_valid_parts: Predicate[Sequence[str]] = both(
            count(equal(3)),
            every(str.isidentifier),
        )
        is_valid_name = compose2(is_valid_parts, as_parts)
        assert is_valid_name("three.part.name") is True
        assert is_valid_name("two.parts") is False
        assert is_valid_name("not identifier.not.valid") is False
        assert is_valid_name("") is False


class BaseError(Exception):
    ...


class Error(BaseError):
    ...


class ErrorA(Error):
    ...


class ErrorB(Error):
    ...


def dummy_function(val: type[Exception]) -> None:
    if val is not None:
        raise val


class TestExcepts:
    @pytest.mark.parametrize(
        "function, argument, return_value",
        [
            (excepts(Error)(dummy_function), ErrorA, False),
            (excepts((ErrorA, ErrorB))(dummy_function), ErrorA, False),
            (excepts((ErrorA, ErrorB))(dummy_function), None, True),
            (excepts((ErrorA, ErrorB), negate=True)(dummy_function), None, False),
            (excepts(Error, negate=True)(dummy_function), ErrorB, True),
        ],
    )
    def test_returns_bool(
        self,
        function: Callable,
        argument: object,
        return_value: bool,
    ) -> None:
        assert function(argument) is return_value

    def test_reraises(self) -> None:
        with pytest.raises(BaseError):
            excepts(Error)(dummy_function)(BaseError)
