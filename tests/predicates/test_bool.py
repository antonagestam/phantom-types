from typing import Iterable

import pytest

from phantom.base import Predicate
from phantom.predicates import bool


class TestTrue:
    @pytest.mark.parametrize("value", [0, False, 1, "test", ()])
    def test_returns_true_for_any_given_value(self, value: object) -> None:
        assert bool.true(value) is True


class TestFalse:
    @pytest.mark.parametrize("value", [0, False, 1, "test", ()])
    def test_returns_false_for_any_given_value(self, value: object) -> None:
        assert bool.false(value) is False


parametrize_truthy = pytest.mark.parametrize("value", [1, "a", (0,), [""], True])
parametrize_falsy = pytest.mark.parametrize("value", [0, "", (), [], False])


class TestTruthy:
    @parametrize_truthy
    def test_returns_true_for_truthy_value(self, value: object) -> None:
        assert bool.truthy(value) is True

    @parametrize_falsy
    def test_returns_false_for_falsy_value(self, value: object) -> None:
        assert bool.truthy(value) is False


class TestFalsy:
    @parametrize_falsy
    def test_returns_true_for_falsy_value(self, value: object) -> None:
        assert bool.falsy(value) is True

    @parametrize_truthy
    def test_returns_false_for_truthy_value(self, value: object) -> None:
        assert bool.falsy(value) is False


class TestBoth:
    def test_returns_true_for_two_succeeding_predicates(self) -> None:
        assert bool.both(bool.true, bool.true)(0) is True

    def test_returns_false_for_failure_in_first_predicate(self) -> None:
        assert bool.both(bool.false, bool.true)(0) is False

    def test_returns_false_for_failure_in_second_predicate(self) -> None:
        assert bool.both(bool.true, bool.false)(0) is False


parametrize_all_true = pytest.mark.parametrize(
    "predicates",
    [(bool.true,), (bool.true, bool.true), (bool.true, bool.true, bool.true)],
)
parametrize_some_false = pytest.mark.parametrize(
    "predicates",
    [
        (bool.true, bool.false),
        (bool.false, bool.true),
        (bool.true, bool.false, bool.true),
    ],
)
parametrize_all_false = pytest.mark.parametrize(
    "predicates",
    [(bool.false,), (bool.false, bool.false), (bool.false, bool.false, bool.false)],
)


class TestAllOf:
    @parametrize_all_true
    def test_returns_true_for_succeeding_predicates(
        self, predicates: Iterable[Predicate]
    ) -> None:
        assert bool.all_of(predicates)(0) is True

    @parametrize_some_false
    def test_returns_false_for_some_failing_predicate(
        self, predicates: Iterable[Predicate]
    ) -> None:
        assert bool.all_of(predicates)(0) is False

    @parametrize_all_false
    def test_returns_false_for_only_failing_predicate(
        self, predicates: Iterable[Predicate]
    ) -> None:
        assert bool.all_of(predicates)(0) is False


class TestAnyOf:
    @parametrize_all_true
    def test_returns_true_for_succeeding_predicates(
        self, predicates: Iterable[Predicate]
    ) -> None:
        assert bool.any_of(predicates)(0) is True

    @parametrize_some_false
    def test_returns_true_for_some_failing_predicate(
        self, predicates: Iterable[Predicate]
    ) -> None:
        assert bool.any_of(predicates)(0) is True

    @parametrize_all_false
    def test_returns_false_for_only_failing_predicate(
        self, predicates: Iterable[Predicate]
    ) -> None:
        assert bool.any_of(predicates)(0) is False
