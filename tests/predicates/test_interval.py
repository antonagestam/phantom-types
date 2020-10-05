from typing import Tuple

import pytest

from phantom.predicates import interval

Boundaries = Tuple[float, float]
parametrize_open_edge = pytest.mark.parametrize(
    "value, boundaries",
    [
        (1, (1, 2)),
        (2, (1, 2)),
        (1.0, (1.0, 2)),
        (2.0, (1, 2.0)),
    ],
)
parametrize_closed_edge = pytest.mark.parametrize(
    "value, boundaries",
    [
        (1.0001, (1, 2)),
        (1.9999, (1, 2)),
        (1.00001, (1.0, 2)),
        (1.99999, (1, 2.0)),
    ],
)
parametrize_closed_outside = pytest.mark.parametrize(
    "value, boundaries",
    [
        (0, (1, 2)),
        (3, (1, 2)),
        (0.99999, (1.0, 2)),
        (2.00001, (1, 2.0)),
        (20, (1, 3)),
    ],
)


class TestOpen:
    def test_returns_true_for_middle_value(self) -> None:
        assert interval.open(1, 3)(2) is True

    @parametrize_open_edge
    def test_returns_true_for_inclusive_edge_value(
        self, value: float, boundaries: Boundaries
    ) -> None:
        assert interval.open(*boundaries)(value) is True

    @parametrize_closed_outside
    def test_returns_false_for_exclusive_outside_value(
        self, value: float, boundaries: Boundaries
    ) -> None:
        assert interval.open(*boundaries)(value) is False


class TestClosed:
    def test_returns_true_for_middle_value(self) -> None:
        assert interval.closed(1, 3)(2) is True

    @parametrize_open_edge
    def test_returns_false_for_inclusive_edge_value(
        self, value: float, boundaries: Boundaries
    ) -> None:
        assert interval.closed(*boundaries)(value) is False

    @parametrize_closed_outside
    def test_returns_false_for_exclusive_outside_value(
        self, value: float, boundaries: Boundaries
    ) -> None:
        assert interval.closed(*boundaries)(value) is False

    @parametrize_closed_edge
    def test_returns_true_for_exclusive_edge_value(
        self, value: float, boundaries: Boundaries
    ) -> None:
        assert interval.closed(*boundaries)(value) is True


class TestOpenClosed:
    def test_returns_true_for_middle_value(self) -> None:
        assert interval.open_closed(1, 3)(2) is True

    def test_lower_bound(self) -> None:
        intv = interval.open_closed(5, 10)
        assert intv(5) is True
        assert intv(4.9999) is False

    def test_upper_bound(self) -> None:
        intv = interval.open_closed(5, 10)
        assert intv(10) is False
        assert intv(9.9999) is True


class TestClosedOpen:
    def test_returns_true_for_middle_value(self) -> None:
        assert interval.closed_open(1, 3)(2) is True

    def test_lower_bound(self) -> None:
        intv = interval.closed_open(5, 10)
        assert intv(5.0001) is True
        assert intv(5) is False

    def test_upper_bound(self) -> None:
        intv = interval.closed_open(5, 10)
        assert intv(10) is True
        assert intv(10.00001) is False
