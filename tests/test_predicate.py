import pytest

from phantom.predicate import Falsy
from phantom.predicate import Truthy

parametrize_truthy = pytest.mark.parametrize("v", (object(), ("a",), 1, True))
parametrize_falsy = pytest.mark.parametrize("v", ((), 0, False))


class TestTruthy:
    @parametrize_truthy
    def test_truthy_value_is_instance(self, v):
        assert isinstance(v, Truthy)

    @parametrize_falsy
    def test_falsy_value_is_not_instance(self, v):
        assert not isinstance(v, Truthy)

    @parametrize_truthy
    def test_instantiation_returns_instance(self, v):
        assert v is Truthy.from_instance(v)

    @parametrize_falsy
    def test_instantiation_raises_for_falsy_value(self, v):
        with pytest.raises(TypeError):
            Truthy.from_instance(v)


class TestFalsy:
    @parametrize_falsy
    def test_falsy_value_is_instance(self, v):
        assert isinstance(v, Falsy)

    @parametrize_truthy
    def test_truthy_value_is_not_instance(self, v):
        assert not isinstance(v, Falsy)

    @parametrize_falsy
    def test_instantiation_returns_instance(self, v):
        assert v is Falsy.from_instance(v)

    @parametrize_truthy
    def test_instantiation_raises_for_truthy_value(self, v):
        with pytest.raises(TypeError):
            Falsy.from_instance(v)
