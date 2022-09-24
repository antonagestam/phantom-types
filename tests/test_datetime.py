import datetime

import pytest

from phantom import BoundError
from phantom.datetime import TZAware
from phantom.datetime import TZNaive
from phantom.errors import MissingDependency

parametrize_aware = pytest.mark.parametrize(
    "dt",
    (
        datetime.datetime.now(tz=datetime.timezone.utc),
        datetime.datetime(1969, 12, 23, tzinfo=datetime.timezone.utc),
        datetime.datetime.min.replace(tzinfo=datetime.timezone.utc),
        datetime.datetime.max.replace(tzinfo=datetime.timezone.utc),
    ),
)
parametrize_naive = pytest.mark.parametrize(
    "dt",
    (
        datetime.datetime.now(),
        datetime.datetime(1969, 12, 23),
        datetime.datetime.min,
        datetime.datetime.max,
    ),
)
parametrize_invalid_type = pytest.mark.parametrize(
    "value",
    (
        object(),
        datetime.time(),
        datetime.timedelta(),
        1,
        1.1,
        (),
    ),
)
min_utc = datetime.datetime.min.replace(tzinfo=datetime.timezone.utc)
max_utc = datetime.datetime.max.replace(tzinfo=datetime.timezone.utc)
parametrize_aware_str = pytest.mark.parametrize(
    "value, expected",
    [
        (min_utc.isoformat(), min_utc),
        (max_utc.isoformat(), max_utc),
        (
            "2022-09-24T10:40:20+00:00",
            datetime.datetime(2022, 9, 24, 10, 40, 20, 0, tzinfo=datetime.timezone.utc),
        ),
        (
            "2022-09-24T10:40:20.779388+00:00",
            datetime.datetime(
                2022, 9, 24, 10, 40, 20, 779388, tzinfo=datetime.timezone.utc
            ),
        ),
    ],
)
parametrize_naive_str = pytest.mark.parametrize(
    "value, expected",
    [
        (datetime.datetime.min.isoformat(), datetime.datetime.min),
        (datetime.datetime.max.isoformat(), datetime.datetime.max),
        (
            "2022-09-24T10:40:20",
            datetime.datetime(2022, 9, 24, 10, 40, 20, 0),
        ),
        (
            "2022-09-24T10:40:20.779388",
            datetime.datetime(2022, 9, 24, 10, 40, 20, 779388),
        ),
    ],
)


class TestTZAware:
    @parametrize_aware
    def test_aware_datetime_is_instance(self, dt: datetime.datetime):
        assert isinstance(dt, TZAware)

    @parametrize_naive
    def test_naive_datetime_is_not_instance(self, dt: datetime.datetime):
        assert not isinstance(dt, TZAware)

    @parametrize_naive
    def test_instantiation_raises_for_naive_datetime_instance(
        self, dt: datetime.datetime
    ):
        with pytest.raises(TypeError):
            TZAware.parse(dt)

    @parametrize_aware
    def test_instantiation_returns_instance(self, dt: datetime.datetime):
        assert dt is TZAware.parse(dt)

    @parametrize_invalid_type
    def test_parse_rejects_non_str_object(self, value: object):
        with pytest.raises(BoundError):
            TZAware.parse(value)

    @pytest.mark.external
    @parametrize_naive_str
    def test_parse_rejects_naive_str(self, value: str, expected: datetime.datetime):
        with pytest.raises(TypeError):
            TZAware.parse(value)

    @pytest.mark.external
    @parametrize_aware_str
    def test_can_parse_valid_str(self, value: str, expected: datetime.datetime):
        assert TZAware.parse(value) == expected

    @pytest.mark.no_external
    @parametrize_aware_str
    def test_parse_str_without_dateutil_raises_missing_dependency(
        self,
        value: str,
        expected: datetime.datetime,
    ):
        with pytest.raises(MissingDependency):
            TZAware.parse(value)


class TestTZNaive:
    @parametrize_naive
    def test_naive_datetime_is_instance(self, dt: datetime.datetime):
        assert isinstance(dt, TZNaive)

    @parametrize_aware
    def test_aware_datetime_is_not_instance(self, dt: datetime.datetime):
        assert not isinstance(dt, TZNaive)

    @parametrize_aware
    def test_instantiation_raises_for_aware_datetime_instance(
        self, dt: datetime.datetime
    ):
        with pytest.raises(TypeError):
            TZNaive.parse(dt)

    @parametrize_naive
    def test_instantiation_returns_instance(self, dt: datetime.datetime):
        assert dt is TZNaive.parse(dt)

    @parametrize_invalid_type
    def test_parse_rejects_non_str_object(self, value: object):
        with pytest.raises(BoundError):
            TZNaive.parse(value)

    @pytest.mark.external
    @parametrize_aware_str
    def test_parse_rejects_aware_str(self, value: str, expected: datetime.datetime):
        with pytest.raises(TypeError):
            TZNaive.parse(value)

    @pytest.mark.external
    @parametrize_naive_str
    def test_can_parse_valid_str(self, value: str, expected: datetime.datetime):
        assert TZNaive.parse(value) == expected

    @pytest.mark.no_external
    @parametrize_naive_str
    def test_parse_str_without_dateutil_raises_missing_dependency(
        self,
        value: str,
        expected: datetime.datetime,
    ):
        with pytest.raises(MissingDependency):
            TZNaive.parse(value)
