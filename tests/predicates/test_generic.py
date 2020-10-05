from typing import Tuple
from typing import Type
from typing import Union

import pytest

from phantom.predicates import generic


class TestEqual:
    @pytest.mark.parametrize("a, b", [(1, 1.0), (False, 0), (True, 1)])
    def test_returns_true_for_equal_values(self, a: object, b: object) -> None:
        assert generic.equal(a)(b) is True
        assert generic.equal(b)(a) is True

    @pytest.mark.parametrize("a, b", [(2, 1), (1, 1.1), (True, False)])
    def test_returns_false_for_non_equal_values(self, a: object, b: object) -> None:
        assert generic.equal(a)(b) is False
        assert generic.equal(b)(a) is False


class TestIdentical:
    @pytest.mark.parametrize(
        "a, b", [(1, 1), ("a", "a"), (True, True), (False, False), ((), ())]
    )
    def test_returns_true_for_identical_values(self, a: object, b: object) -> None:
        assert generic.identical(a)(b) is True
        assert generic.identical(b)(a) is True

    @pytest.mark.parametrize("a, b", [([], []), (1, 1.0), (False, 0), (True, 1)])
    def test_returns_false_for_different_values(self, a: object, b: object) -> None:
        assert generic.identical(a)(b) is False
        assert generic.identical(b)(a) is False


class TestOfType:
    @pytest.mark.parametrize("instance,types", [(1, int), (1, (int, float))])
    def test_returns_true_for_instance_of_types(
        self, instance: object, types: Union[Type, Tuple[Type, ...]]
    ) -> None:
        assert generic.of_type(types)(instance) is True

    @pytest.mark.parametrize("instance,types", [(1, float), ("", (int, float))])
    def test_returns_false_for_instance_of_other_type(
        self, instance: object, types: Union[Type, Tuple[Type, ...]]
    ) -> None:
        assert generic.of_type(types)(instance) is False
