import pytest
from functools import singledispatch
from dept.datetime import TZAware
from dept.datetime import TZNaive

import datetime


@singledispatch
def handle_date(dt):
    return "huh?"


@handle_date.register(TZAware)
def _handle_aware(dt):
    return "is aware and all good"


@handle_date.register(TZNaive)
def _handle_naive(dt):
    return "is is not so good"

aware = datetime.datetime.now(tz=datetime.timezone.utc)
naive = datetime.datetime.now()


print(issubclass(TZAware, datetime.datetime))
print(issubclass(datetime.datetime, TZAware))

print("aware", handle_date.dispatch(aware))


@pytest.mark.xfail(strict=True)
def test_dispatch():
    assert "huh?" == handle_date("not a date")
    assert "aware" == handle_date(aware)
    assert "naive" == handle_date(naive)
