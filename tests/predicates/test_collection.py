from typing import Container
from typing import Sized

import pytest

from phantom.base import Predicate
from phantom.predicates import collection
from phantom.predicates import generic
from phantom.predicates import numeric


class TestContains:
    @pytest.mark.parametrize(
        "item, container",
        [
            (1, (1, 2)),
            ("b", "abc"),
        ],
    )
    def test_returns_true_for_container_with_item(
        self, item: object, container: Container
    ) -> None:
        assert collection.contains(item)(container) is True

    @pytest.mark.parametrize(
        "item, container",
        [
            (1, (2, 3)),
            ("d", "abc"),
        ],
    )
    def test_returns_false_for_container_without_item(
        self, item: object, container: Container
    ) -> None:
        assert collection.contains(item)(container) is False


class TestCount:
    @pytest.mark.parametrize(
        "predicate, sized",
        [
            (generic.equal(1), [0]),
            (numeric.le(3), ("a", "b")),
            (numeric.ge(3), "abc"),
        ],
    )
    def test_returns_true_for_size_matching_predicate(
        self, predicate: Predicate, sized: Sized
    ) -> None:
        assert collection.count(predicate)(sized) is True

    @pytest.mark.parametrize(
        "predicate, sized",
        [
            (generic.equal(1), [0, 0]),
            (numeric.le(3), ("a", "b", 1, 2)),
            (numeric.ge(3), "ab"),
        ],
    )
    def test_returns_false_for_size_failing_predicate(
        self, predicate: Predicate, sized: Sized
    ) -> None:
        assert collection.count(predicate)(sized) is False
