from typing import Tuple

import pytest

from phantom.predicates import interval

from .utils import assert_predicate_name_equals

Boundaries = Tuple[float, float]
parametrize_inside = pytest.mark.parametrize(
    "value, boundaries",
    [
        (1.0001, (1, 2)),
        (1.9999, (1, 2)),
        (1.00001, (1.0, 2)),
        (1.99999, (1, 2.0)),
    ],
)
parametrize_on_edge = pytest.mark.parametrize(
    "value, boundaries",
    [
        (1, (1, 2)),
        (2, (1, 2)),
        (1.0, (1.0, 2)),
        (2.0, (1, 2.0)),
    ],
)
parametrize_outside = pytest.mark.parametrize(
    "value, boundaries",
    [
        (0, (1, 2)),
        (3, (1, 2)),
        (0.99999, (1.0, 2)),
        (2.00001, (1, 2.0)),
        (20, (1, 3)),
    ],
)


class TestExclusive:
    def test_returns_true_for_middle_value(self) -> None:
        assert interval.exclusive(1, 3)(2) is True

    @parametrize_inside
    def test_returns_true_for_inside_value(
        self, value: float, boundaries: Boundaries
    ) -> None:
        assert interval.exclusive(*boundaries)(value) is True

    @parametrize_on_edge
    def test_returns_false_for_edge_value(
        self, value: float, boundaries: Boundaries
    ) -> None:
        assert interval.exclusive(*boundaries)(value) is False

    @parametrize_outside
    def test_returns_false_for_outside_value(
        self, value: float, boundaries: Boundaries
    ) -> None:
        assert interval.exclusive(*boundaries)(value) is False

    def test_repr_contains_bound_parameter(self):
        assert_predicate_name_equals(interval.exclusive(0, 1), "exclusive(0, 1)")


class TestInclusive:
    def test_returns_true_for_middle_value(self) -> None:
        assert interval.inclusive(1, 3)(2) is True

    @parametrize_inside
    def test_returns_true_for_inside_value(
        self, value: float, boundaries: Boundaries
    ) -> None:
        assert interval.inclusive(*boundaries)(value) is True

    @parametrize_on_edge
    def test_returns_true_for_edge_value(
        self, value: float, boundaries: Boundaries
    ) -> None:
        assert interval.inclusive(*boundaries)(value) is True

    @parametrize_outside
    def test_returns_false_for_outside_value(
        self, value: float, boundaries: Boundaries
    ) -> None:
        assert interval.inclusive(*boundaries)(value) is False

    def test_repr_contains_bound_parameter(self):
        assert_predicate_name_equals(interval.inclusive(0, 1), "inclusive(0, 1)")


class TestInclusiveExclusive:
    def test_returns_true_for_middle_value(self) -> None:
        assert interval.inclusive_exclusive(1, 3)(2) is True

    def test_lower_bound(self) -> None:
        intv = interval.inclusive_exclusive(5, 10)
        assert intv(5) is True
        assert intv(4.9999) is False

    def test_upper_bound(self) -> None:
        intv = interval.inclusive_exclusive(5, 10)
        assert intv(10) is False
        assert intv(9.9999) is True

    def test_repr_contains_bound_parameter(self):
        assert_predicate_name_equals(
            interval.inclusive_exclusive(0, 1), "inclusive_exclusive(0, 1)"
        )


class TestExclusiveInclusive:
    def test_returns_true_for_middle_value(self) -> None:
        assert interval.exclusive_inclusive(1, 3)(2) is True

    def test_lower_bound(self) -> None:
        intv = interval.exclusive_inclusive(5, 10)
        assert intv(5.0001) is True
        assert intv(5) is False

    def test_upper_bound(self) -> None:
        intv = interval.exclusive_inclusive(5, 10)
        assert intv(10) is True
        assert intv(10.00001) is False

    def test_repr_contains_bound_parameter(self):
        assert_predicate_name_equals(
            interval.exclusive_inclusive(0, 1), "exclusive_inclusive(0, 1)"
        )
