from __future__ import annotations

from dataclasses import dataclass
from dataclasses import fields
from functools import total_ordering
from typing import Generic
from typing import TypeVar
from typing import get_type_hints

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import builds
from typing_extensions import get_origin

from phantom.boolean import Falsy
from phantom.boolean import Truthy
from phantom.datetime import TZAware
from phantom.datetime import TZNaive
from phantom.interval import Exclusive
from phantom.interval import ExclusiveInclusive
from phantom.interval import Inclusive
from phantom.interval import InclusiveExclusive
from phantom.interval import Natural
from phantom.interval import NegativeInt
from phantom.interval import Portion
from phantom.iso3166 import ParsedAlpha2
from phantom.negated import SequenceNotStr
from phantom.re import FullMatch
from phantom.sized import Empty
from phantom.sized import NonEmpty
from phantom.sized import NonEmptyStr
from phantom.sized import PhantomBound
from tests.types import FloatExc
from tests.types import FloatExcInc
from tests.types import FloatInc
from tests.types import FloatIncExc
from tests.types import IntExc
from tests.types import IntExcInc
from tests.types import IntInc
from tests.types import IntIncExc


class TensFloat(float, InclusiveExclusive, low=10, high=20):
    ...


class TensInt(int, InclusiveExclusive, low=10, high=20):
    ...


class Url(
    FullMatch,
    pattern=r"https?://www\.[A-z]+\.(com|se|org)",
):
    ...


T = TypeVar("T", bound=object, covariant=True)


class Few(PhantomBound[T], Generic[T], min=5, max=15):
    ...


@total_ordering
class Inf:
    def __eq__(self, other):
        return False

    def __lt__(self, other):
        return False


# Test can create types that don't map to a Hypothesis strategy.
class InmappableInc(int, Inclusive, low=Inf(), high=100):
    ...


class InmappableExc(float, Exclusive, low=Inf(), high=100):
    ...


class InmappableIncExc(int, InclusiveExclusive, low=Inf(), high=100):
    ...


class InmappableExcInc(float, ExclusiveInclusive, low=Inf(), high=100):
    ...


@dataclass
class Model:
    tz_aware: TZAware
    tz_naive: TZNaive
    truthy: Truthy
    falsy: Falsy

    tens_float: TensFloat
    tens_int: TensInt

    natural: Natural
    negative_int: NegativeInt
    portion: Portion
    float_inc: FloatInc
    int_inc: IntInc
    float_exc: FloatExc
    int_exc: IntExc
    float_inc_exc: FloatIncExc
    int_inc_exc: IntIncExc
    float_exc_inc: FloatExcInc
    int_exc_inc: IntExcInc

    parsed_alpha_2: ParsedAlpha2

    url: Url

    not_str: SequenceNotStr[str | int]

    non_empty: NonEmpty[int]
    non_empty_str: NonEmptyStr
    empty: Empty

    ints: Few[int]
    mixed: Few[int | str]


@given(builds(Model))
@settings(max_examples=10)
def test_can_generate_hypothesis_values(model: Model) -> None:
    hints = get_type_hints(Model)
    for field in fields(Model):
        type_ = hints[field.name]
        inner_type = get_origin(type_) or type_
        assert isinstance(getattr(model, field.name), inner_type)
