import pytest

from phantom.interval import Closed
from phantom.interval import ClosedOpen
from phantom.interval import Interval
from phantom.interval import Natural
from phantom.interval import NegativeInt
from phantom.interval import Open
from phantom.interval import OpenClosed
from phantom.interval import Portion


class TestInterval:
    def test_subclassing_without_check_raises(self):
        with pytest.raises(TypeError, match="I must define an interval check$"):

            class I(Interval, abstract=False):  # noqa: E742
                ...


class TestOpen:
    def test_implements_schema(self):
        class Op(int, Open, low=0, high=100):
            ...

        assert Op.__schema__() == {
            "minimum": 0,
            "maximum": 100,
            "description": "A value in the inclusive range (0, 100).",
        }


class TestClosed:
    def test_implements_schema(self):
        class C(float, Closed, low=-1, high=1):
            ...

        assert C.__schema__() == {
            "description": "A value in the exclusive range [-1, 1].",
            "exclusiveMinimum": -1,
            "exclusiveMaximum": 1,
        }


class TestOpenClosed:
    def test_implements_schema(self):
        class OC(float, OpenClosed, low=0, high=100):
            ...

        assert OC.__schema__() == {
            "description": "A value in the half-open range (0, 100].",
            "minimum": 0,
            "exclusiveMaximum": 100,
        }


class TestClosedOpen:
    def test_implements_schema(self):
        class CO(float, ClosedOpen, low=-100, high=0):
            ...

        assert CO.__schema__() == {
            "description": "A value in the half-open range [-100, 0).",
            "exclusiveMinimum": -100,
            "maximum": 0,
        }


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

    def test_implements_schema(self):
        assert NegativeInt.__schema__() == {
            "maximum": 0,
            "minimum": None,
            "description": "An integer value in the inclusive range (-∞, 0).",
        }


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

    def test_implements_schema(self):
        assert Natural.__schema__() == {
            "description": "An integer value in the inclusive range (0, ∞).",
            "minimum": 0,
            "maximum": None,
        }


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

    def test_implements_schema(self):
        assert Portion.__schema__() == {
            "description": "A float value in the inclusive range (0, 1).",
            "minimum": 0,
            "maximum": 1,
        }
