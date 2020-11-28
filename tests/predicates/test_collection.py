from typing import Container
from typing import Iterable
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


class TestContained:
    @pytest.mark.parametrize(
        "container, item",
        [
            ((1, 2), 1),
            ("abc", "b"),
        ],
    )
    def test_returns_true_for_item_in_container(
        self, container: Container, item: object
    ) -> None:
        assert collection.contained(container)(item) is True

    @pytest.mark.parametrize(
        "container, item",
        [
            ((2, 3), 1),
            ("abc", "d"),
        ],
    )
    def test_returns_false_for_item_not_in_container(
        self, container: Container, item: object
    ) -> None:
        assert collection.contained(container)(item) is False


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


class TestExists:
    @pytest.mark.parametrize(
        "predicate, iterable",
        [
            (generic.identical(...), ["a", "b", ...]),
            (numeric.greater(0), [-3, 0, 1, 0]),
            (generic.equal("a"), "cbad"),
        ],
    )
    def test_returns_true_for_iterable_containing_satisfying_item(
        self, predicate: Predicate[object], iterable: Iterable
    ) -> None:
        assert collection.exists(predicate)(iterable) is True

    @pytest.mark.parametrize(
        "predicate, iterable",
        [
            (generic.identical(...), ["a", "b", "c"]),
            (numeric.greater(1), [-3, 0, 1, 0]),
            (generic.equal("a"), "cbed"),
        ],
    )
    def test_returns_false_for_iterable_not_containing_satisfying_item(
        self, predicate: Predicate[object], iterable: Iterable
    ) -> None:
        assert collection.exists(predicate)(iterable) is False


class TestEvery:
    @pytest.mark.parametrize(
        "predicate, iterable",
        [
            (generic.identical(1), [1, 1, 1]),
            (generic.identical(1), []),
            (numeric.greater(0), [1, 2]),
            (generic.equal("a"), "aa"),
        ],
    )
    def test_returns_true_for_complete_iterable(
        self, predicate: Predicate[object], iterable: Iterable
    ) -> None:
        assert collection.every(predicate)(iterable) is True

    @pytest.mark.parametrize(
        "predicate, iterable",
        [
            (generic.identical(...), [..., "b", "c"]),
            (numeric.greater(1), [-3, 0, 1, 0, 2]),
            (generic.equal("a"), "abc"),
        ],
    )
    def test_returns_false_for_incomplete_iterable(
        self, predicate: Predicate[object], iterable: Iterable
    ) -> None:
        assert collection.every(predicate)(iterable) is False
