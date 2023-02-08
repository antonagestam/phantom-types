from __future__ import annotations

from dataclasses import dataclass
from dataclasses import fields
from typing import Generic
from typing import TypeVar

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import builds
from typing_extensions import get_origin

from phantom.boolean import Falsy
from phantom.boolean import Truthy
from phantom.datetime import TZAware
from phantom.datetime import TZNaive
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

    parsed_alpha_2: ParsedAlpha2

    url: Url

    not_str: SequenceNotStr[str | int]

    non_empty: NonEmpty[int]
    non_empty_str: NonEmptyStr
    empty: Empty

    ints: Few[int]
    mixed: Few[int | str]


@given(builds(Model))
@settings(max_examples=100)
def test_can_generate_hypothesis_values(model: Model) -> None:
    for field in fields(Model):
        type_ = get_origin(field.type) or field.type
        assert isinstance(getattr(model, field.name), type_)
