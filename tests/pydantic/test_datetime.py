import datetime

import pytest

import pydantic
from phantom.datetime import TZAware
from phantom.datetime import TZNaive
from pydantic import ValidationError


class HasTZAware(pydantic.BaseModel):
    created_at: TZAware


class TestPydanticTZAware:
    @pytest.mark.parametrize(
        "value, expected",
        [
            (
                "2022-09-24T10:40:20+00:00",
                datetime.datetime(
                    2022, 9, 24, 10, 40, 20, 0, tzinfo=datetime.timezone.utc
                ),
            ),
            (
                "2022-09-24T10:40:20.779388+00:00",
                datetime.datetime(
                    2022, 9, 24, 10, 40, 20, 779388, tzinfo=datetime.timezone.utc
                ),
            ),
        ],
    )
    def test_can_parse_tz_aware(self, value: str, expected: datetime.datetime):
        object = HasTZAware.parse_obj({"created_at": value})
        assert type(object.created_at) is datetime.datetime
        assert object.created_at == expected

    def test_tz_aware_rejects_naive_datetime(self):
        with pytest.raises(ValidationError):
            HasTZAware.parse_obj({"created_at": "2022-09-24T10:40:20"})


class HasTZNaive(pydantic.BaseModel):
    time_of_day: TZNaive


class TestPydanticTZNaive:
    @pytest.mark.parametrize(
        "value, expected",
        [
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
    def test_can_parse_tz_naive(self, value: str, expected: datetime.datetime):
        object = HasTZNaive.parse_obj({"time_of_day": value})
        assert type(object.time_of_day) is datetime.datetime
        assert object.time_of_day == expected

    def test_tz_naive_rejects_aware_datetime(self):
        with pytest.raises(ValidationError):
            HasTZNaive.parse_obj({"time_of_day": "2022-09-24T10:40:20+00:00"})
