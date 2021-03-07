from __future__ import annotations

from functools import partial
from operator import add
from operator import mul
from typing import Callable
from typing import Sequence
from typing import TypeVar

import pytest

from phantom import Predicate
from phantom.fn import compose2
from phantom.predicates.boolean import both
from phantom.predicates.collection import count
from phantom.predicates.collection import every
from phantom.predicates.generic import equal


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
