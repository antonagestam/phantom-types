import datetime

import pytest

from phantom.datetime import TZAware
from phantom.datetime import TZNaive

parametrize_aware = pytest.mark.parametrize(
    "dt", (datetime.datetime.now(tz=datetime.timezone.utc),)
)
parametrize_naive = pytest.mark.parametrize(
    "dt", (datetime.datetime.now(), datetime.datetime(1969, 12, 23))
)


class TestTZAware:
    @parametrize_aware
    def test_aware_datetime_is_instance(self, dt):
        assert isinstance(dt, TZAware)

    @parametrize_naive
    def test_naive_datetime_is_not_instance(self, dt):
        assert not isinstance(dt, TZAware)

    @parametrize_naive
    def test_instantiation_raises_for_naive_datetime(self, dt):
        with pytest.raises(TypeError):
            TZAware.parse(dt)

    @parametrize_aware
    def test_instantiation_returns_instance(self, dt):
        assert dt is TZAware.parse(dt)


class TestTZNaive:
    @parametrize_naive
    def test_naive_datetime_is_instance(self, dt):
        assert isinstance(dt, TZNaive)

    @parametrize_aware
    def test_aware_datetime_is_not_instance(self, dt):
        assert not isinstance(dt, TZNaive)

    @parametrize_aware
    def test_instantiation_raises_for_aware_datetime(self, dt):
        with pytest.raises(TypeError):
            TZNaive.parse(dt)

    @parametrize_naive
    def test_instantiation_returns_instance(self, dt):
        assert dt is TZNaive.parse(dt)
