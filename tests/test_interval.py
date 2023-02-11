from __future__ import annotations

from decimal import Decimal
from functools import total_ordering

import pytest

from phantom.interval import Inclusive
from phantom.interval import Interval
from phantom.interval import Natural
from phantom.interval import NegativeInt
from phantom.interval import Portion
from phantom.interval import _get_scalar_float_bounds
from phantom.interval import _get_scalar_int_bounds
from phantom.interval import _NonScalarBounds
from phantom.predicates import interval

from .types import FloatInc
from .types import FloatIncExc
from .types import IntExc
from .types import IntExcInc


class TestInterval:
    def test_subclassing_without_check_raises(self):
        with pytest.raises(TypeError, match="I must define an interval check$"):

            class I(Interval, abstract=False):  # noqa: E742
                ...

    def test_parse_coerces_str(self):
        class Great(int, Inclusive, low=10):
            ...

        assert Great.parse("10") == 10

    def test_allows_decimal_bound(self):
        class I(  # noqa: E742
            Decimal,
            Interval,
            check=interval.exclusive,
            low=Decimal("1.15"),
            high=Decimal("2.36"),
        ):
            ...

        assert not isinstance(2, I)
        assert not isinstance(1.98, I)
        assert isinstance(Decimal("1.98"), I)


parametrize_negative_ints = pytest.mark.parametrize("i", (-10, -1, -0, +0))
parametrize_positive_ints = pytest.mark.parametrize("i", (10, 1, +0, -0))


class TestNegativeInt:
    @parametrize_negative_ints
    def test_negative_int_is_instance(self, i):
        assert isinstance(i, NegativeInt)

    def test_positive_int_is_not_instance(self):
        assert not isinstance(1, NegativeInt)
        assert not isinstance(10, NegativeInt)

    def test_instantiation_raises_for_positive_int(self):
        with pytest.raises(TypeError):
            NegativeInt.parse(1)
        with pytest.raises(TypeError):
            NegativeInt.parse(10)

    @parametrize_negative_ints
    def test_instantiation_returns_instance(self, i):
        assert i is NegativeInt.parse(i)


class TestNatural:
    @parametrize_positive_ints
    def test_positive_int_is_instance(self, i):
        assert isinstance(i, Natural)

    def test_negative_int_is_not_instance(self):
        assert not isinstance(-1, Natural)
        assert not isinstance(-10, Natural)

    def test_instantiation_raises_for_positive_int(self):
        with pytest.raises(TypeError):
            Natural.parse(-1)
        with pytest.raises(TypeError):
            Natural.parse(-10)
        with pytest.raises(TypeError):
            Natural(-1)

    @parametrize_positive_ints
    def test_instantiation_returns_instance(self, i):
        assert i is Natural.parse(i)
        assert i is Natural(i)


parametrize_portion_values = pytest.mark.parametrize(
    "i", (0.0, 1.0, -0.0, +1.0, 0.8652559794322651)
)
# TODO: Use math.nextafter on Python 3.9 to test as close to limit as possible
parametrize_non_portion_values = pytest.mark.parametrize("i", (-1, -0.1, 1.1, 2))


class TestPortion:
    @parametrize_portion_values
    def test_value_inside_range_is_instance(self, i):
        assert isinstance(i, Portion)

    @parametrize_non_portion_values
    def test_value_outside_range_is_instance(self, i):
        assert not isinstance(i, Portion)

    @parametrize_portion_values
    def test_instantiation_returns_instance(self, i):
        assert i is Portion.parse(i)
        assert i is Portion(i)

    @parametrize_non_portion_values
    def test_instantiation_raises_for_non_portion_values(self, i):
        with pytest.raises(TypeError):
            Portion.parse(i)
        with pytest.raises(TypeError):
            Portion(i)


class TestGetScalarIntBounds:
    @pytest.mark.parametrize(
        ("type_", "exclude_min", "exclude_max", "expected_low", "expected_high"),
        (
            (FloatInc, False, False, 0, 100),
            (IntExc, True, True, 1, 99),
            (IntExcInc, True, False, 1, 100),
            (FloatIncExc, False, True, 0, 99),
            (Natural, False, False, 0, None),
            (NegativeInt, False, False, None, 0),
        ),
    )
    def test_returns_correct_bounds(
        self,
        type_: type[Interval],
        exclude_min: bool,
        exclude_max: bool,
        expected_low: int | None,
        expected_high: int | None,
    ):
        (low, high) = _get_scalar_int_bounds(type_, exclude_min, exclude_max)
        assert low == expected_low
        assert high == expected_high

    def test_raises_non_scalar_bounds_for_non_int_lower_bound(self):
        @total_ordering
        class Inf:
            def __eq__(self, other):
                return False

            def __lt__(self, other):
                return False

        class Int(int, Inclusive, low=Inf(), high=100):
            ...

        with pytest.raises(_NonScalarBounds):
            _get_scalar_int_bounds(Int)

    def test_raises_non_scalar_bounds_for_non_int_upper_bound(self):
        @total_ordering
        class Inf:
            def __eq__(self, other):
                return False

            def __lt__(self, other):
                return False

        class Int(int, Inclusive, low=0, high=Inf()):
            ...

        with pytest.raises(_NonScalarBounds):
            _get_scalar_int_bounds(Int)


class TestGetScalarFloatBounds:
    @pytest.mark.parametrize(
        ("type_", "expected_low", "expected_high"),
        (
            (FloatInc, 0, 100),
            (Natural, 0, None),
            (NegativeInt, None, 0),
            (Portion, 0, 1),
        ),
    )
    def test_returns_correct_bounds(
        self,
        type_: type[Interval],
        expected_low: int,
        expected_high: int,
    ):
        (low, high) = _get_scalar_float_bounds(type_)
        assert low == expected_low
        assert high == expected_high

    def test_raises_non_scalar_bounds_for_non_int_lower_bound(self):
        @total_ordering
        class Inf:
            def __eq__(self, other):
                return False

            def __lt__(self, other):
                return False

        class Int(float, Inclusive, low=Inf(), high=100):
            ...

        with pytest.raises(_NonScalarBounds):
            _get_scalar_float_bounds(Int)

    def test_raises_non_scalar_bounds_for_non_int_upper_bound(self):
        @total_ordering
        class Inf:
            def __eq__(self, other):
                return False

            def __lt__(self, other):
                return False

        class Int(float, Inclusive, low=0, high=Inf()):
            ...

        with pytest.raises(_NonScalarBounds):
            _get_scalar_float_bounds(Int)
