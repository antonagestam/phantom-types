from __future__ import annotations

from functools import partial
from operator import add
from operator import mul
from typing import Callable
from typing import TypeVar

import pytest

from phantom.fn import compose2


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
