import datetime

import pytest

from phantom.predicates.datetime import is_tz_aware
from phantom.predicates.datetime import is_tz_naive

parametrize_aware = pytest.mark.parametrize(
    "dt", (datetime.datetime.now(tz=datetime.timezone.utc),)
)
parametrize_naive = pytest.mark.parametrize(
    "dt", (datetime.datetime.now(), datetime.datetime(1969, 12, 23))
)


class TestIsTZAware:
    @parametrize_aware
    def test_returns_true_for_aware_dt(self, dt: datetime.datetime) -> None:
        assert is_tz_aware(dt) is True

    @parametrize_naive
    def test_returns_false_for_naive_dt(self, dt: datetime.datetime) -> None:
        assert is_tz_aware(dt) is False


class TestIsTZNaive:
    @parametrize_naive
    def test_returns_true_for_naive_dt(self, dt: datetime.datetime) -> None:
        assert is_tz_naive(dt) is True

    @parametrize_aware
    def test_returns_false_for_aware_dt(self, dt: datetime.datetime) -> None:
        assert is_tz_naive(dt) is False
