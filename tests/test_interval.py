import pytest

from phantom.interval import Interval
from phantom.interval import Natural
from phantom.interval import NegativeInt
from phantom.interval import Portion


class TestInterval:
    def test_subclassing_without_check_raises(self):
        with pytest.raises(TypeError, match="I must define an interval check$"):

            class I(Interval, abstract=False):  # noqa: E742
                ...


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
