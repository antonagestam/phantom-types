import pytest

from phantom.predicates import numeric


class TestLess:
    def test_returns_true_for_values_below_limit(self) -> None:
        predicate = numeric.less(10)
        assert predicate(9) is True
        assert predicate(9.999) is True
        assert predicate(-5) is True

    def test_returns_false_for_values_above_limit(self) -> None:
        predicate = numeric.less(10)
        assert predicate(10) is False
        assert predicate(11) is False
        assert predicate(123) is False


class TestLE:
    def test_returns_true_for_values_below_limit(self) -> None:
        predicate = numeric.le(10)
        assert predicate(9) is True
        assert predicate(9.999) is True
        assert predicate(-5) is True
        assert predicate(10) is True

    def test_returns_false_for_values_above_limit(self) -> None:
        predicate = numeric.le(10)
        assert predicate(10.0001) is False
        assert predicate(11) is False
        assert predicate(123) is False


class TestGreater:
    def test_returns_true_for_values_above_limit(self) -> None:
        predicate = numeric.greater(120)
        assert predicate(121) is True
        assert predicate(120.0001) is True
        assert predicate(1200) is True

    def test_returns_false_for_values_below_limit(self) -> None:
        predicate = numeric.greater(120)
        assert predicate(120) is False
        assert predicate(119.9999) is False
        assert predicate(-120) is False


class TestGE:
    def test_returns_true_for_values_above_limit(self) -> None:
        predicate = numeric.ge(120)
        assert predicate(121) is True
        assert predicate(120.0001) is True
        assert predicate(1200) is True
        assert predicate(120) is True

    def test_returns_false_for_values_below_limit(self) -> None:
        predicate = numeric.ge(120)
        assert predicate(119.9999) is False
        assert predicate(-120) is False
        assert predicate(119) is False


class TestPositive:
    def test_limits(self) -> None:
        assert numeric.positive(0) is False
        assert numeric.positive(-1) is False
        assert numeric.positive(1) is True
        assert numeric.positive(0.0001) is True


class TestNonPositive:
    def test_limits(self) -> None:
        assert numeric.non_positive(0) is True
        assert numeric.non_positive(-1) is True
        assert numeric.non_positive(1) is False
        assert numeric.non_positive(0.0001) is False


class TestNegative:
    def test_limits(self) -> None:
        assert numeric.negative(0) is False
        assert numeric.negative(-1) is True
        assert numeric.negative(1) is False
        assert numeric.negative(-0.0001) is True


class TestNonNegative:
    def test_limits(self) -> None:
        assert numeric.non_negative(0) is True
        assert numeric.non_negative(-1) is False
        assert numeric.non_negative(1) is True
        assert numeric.non_negative(-0.0001) is False


parametrize_even = pytest.mark.parametrize("value", [-8296, 0, 2, 32, 9314])
parametrize_odd = pytest.mark.parametrize("value", [-13829, -1, 1, 31, 10023])


class TestEven:
    @parametrize_even
    def test_returns_true_for_even_value(self, value: int) -> None:
        assert numeric.even(value) is True

    @parametrize_odd
    def test_returns_false_for_odd_value(self, value: int) -> None:
        assert numeric.even(value) is False


class TestOdd:
    @parametrize_odd
    def test_returns_true_for_odd_value(self, value: int) -> None:
        assert numeric.odd(value) is True

    @parametrize_even
    def test_returns_false_for_even_value(self, value: int) -> None:
        assert numeric.odd(value) is False
