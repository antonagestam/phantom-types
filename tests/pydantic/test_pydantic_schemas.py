import sys

import pytest

import pydantic
from phantom.datetime import TZAware
from phantom.datetime import TZNaive
from phantom.ext.phonenumbers import FormattedPhoneNumber
from phantom.ext.phonenumbers import PhoneNumber
from phantom.interval import Exclusive
from phantom.interval import ExclusiveInclusive
from phantom.interval import Inclusive
from phantom.interval import InclusiveExclusive
from phantom.interval import Natural
from phantom.interval import NegativeInt
from phantom.interval import Portion
from phantom.iso3166 import ParsedAlpha2
from phantom.negated import SequenceNotStr
from phantom.predicates.numeric import odd
from phantom.re import FullMatch
from phantom.re import Match
from phantom.sized import Empty
from phantom.sized import NonEmpty
from phantom.sized import NonEmptyStr
from phantom.sized import PhantomSized


class ExclusiveType(int, Exclusive, low=0, high=100):
    ...


class InclusiveType(float, Inclusive, low=-1, high=1):
    ...


class ExclusiveInclusiveType(float, ExclusiveInclusive, low=0, high=100):
    ...


class InclusiveExclusiveType(float, InclusiveExclusive, low=-100, high=0):
    ...


class MatchType(Match, pattern=r"^[A-Z]{2}[0-9]{2}$"):
    ...


class FullMatchType(FullMatch, pattern=r"^[A-Z]{2}[0-9]{2}$"):
    ...


class OddSize(PhantomSized[int], len=odd):
    ...


class DataModel(pydantic.BaseModel):
    open: ExclusiveType
    closed: InclusiveType
    exclusive_inclusive: ExclusiveInclusiveType
    inclusive_exclusive: InclusiveExclusiveType
    negative_int: NegativeInt
    natural: Natural
    portion: Portion
    tz_aware: TZAware
    tz_naive: TZNaive
    match: MatchType
    full_match: FullMatchType
    non_empty: NonEmpty[int]
    empty: Empty
    non_empty_str: NonEmptyStr
    odd_size: OddSize
    country: ParsedAlpha2
    phone_number: PhoneNumber
    formatted_phone_number: FormattedPhoneNumber
    sequence_not_str: SequenceNotStr[int]


class TestShippedTypesImplementsSchema:
    def test_interval_open_implements_schema(self):
        assert DataModel.schema()["properties"]["open"] == {
            "exclusiveMinimum": 0,
            "exclusiveMaximum": 100,
            "description": "A value in the exclusive range (0, 100).",
            "title": "ExclusiveType",
            "type": "integer",
        }

    def test_interval_closed_implements_schema(self):
        assert DataModel.schema()["properties"]["closed"] == {
            "description": "A value in the inclusive range [-1, 1].",
            "minimum": -1,
            "maximum": 1,
            "title": "InclusiveType",
            "type": "number",
        }

    def test_interval_exclusive_inclusive_implements_schema(self):
        assert DataModel.schema()["properties"]["exclusive_inclusive"] == {
            "description": "A value in the half-open range (0, 100].",
            "exclusiveMinimum": 0,
            "maximum": 100,
            "title": "ExclusiveInclusiveType",
            "type": "number",
        }

    def test_interval_inclusive_exclusive_implements_schema(self):
        assert DataModel.schema()["properties"]["inclusive_exclusive"] == {
            "title": "InclusiveExclusiveType",
            "description": "A value in the half-open range [-100, 0).",
            "minimum": -100,
            "exclusiveMaximum": 0,
            "type": "number",
        }

    def test_interval_negative_int_implements_schema(self):
        assert DataModel.schema()["properties"]["negative_int"] == {
            "title": "NegativeInt",
            "maximum": 0,
            "description": "An integer value in the inclusive range (-∞, 0].",
            "type": "integer",
        }

    def test_interval_natural_implements_schema(self):
        assert DataModel.schema()["properties"]["natural"] == {
            "title": "Natural",
            "description": "An integer value in the inclusive range [0, ∞).",
            "minimum": 0,
            "type": "integer",
        }

    def test_interval_portion_implements_schema(self):
        assert DataModel.schema()["properties"]["portion"] == {
            "title": "Portion",
            "description": "A float value in the inclusive range [0, 1].",
            "minimum": 0,
            "maximum": 1,
            "type": "number",
        }

    def test_tz_aware_implements_schema(self):
        assert DataModel.schema()["properties"]["tz_aware"] == {
            "title": "TZAware",
            "description": "A date-time with timezone data.",
            "type": "string",
            "format": "date-time",
        }

    def test_tz_naive_implements_schema(self):
        assert DataModel.schema()["properties"]["tz_naive"] == {
            "title": "TZNaive",
            "description": "A date-time without timezone data.",
            "type": "string",
            "format": "date-time-naive",
        }

    def test_re_match_implements_schema(self):
        assert DataModel.schema()["properties"]["match"] == {
            "title": "MatchType",
            "description": (
                "A string starting with a match of the format regular expression."
            ),
            "type": "string",
            "format": "^[A-Z]{2}[0-9]{2}$",
        }

    def test_re_full_match_implements_schema(self):
        assert DataModel.schema()["properties"]["full_match"] == {
            "title": "FullMatchType",
            "description": "A string that matches the format regular expression.",
            "type": "string",
            "format": "^[A-Z]{2}[0-9]{2}$",
        }

    def test_sized_non_empty_implements_schema(self):
        assert DataModel.schema()["properties"]["non_empty"] == {
            "allOf": [{"type": "integer"}],
            "title": "NonEmpty",
            "type": "array",
            "description": "A non-empty array.",
            "minItems": 1,
        }

    def test_sized_empty_implements_schema(self):
        assert DataModel.schema()["properties"]["empty"] == {
            "title": "Empty",
            "type": "array",
            "description": "An empty array.",
            "maxItems": 0,
        }

    def test_sized_non_empty_str_implements_schema(self):
        assert DataModel.schema()["properties"]["non_empty_str"] == {
            "title": "NonEmptyStr",
            "type": "string",
            "description": "A non-empty string.",
            "minLength": 1,
        }

    def test_phantom_sized_implements_schema(self):
        assert DataModel.schema()["properties"]["odd_size"] == {
            "title": "OddSize",
            "type": "array",
        }

    def test_country_code_implements_schema(self):
        assert DataModel.schema()["properties"]["country"] == {
            "title": "Alpha2",
            "description": "ISO3166-1 alpha-2 country code",
            "examples": ["NR", "KZ", "ET", "VC", "AE", "NZ", "SX", "XK", "AX"],
            "type": "string",
            "format": "iso3166-1 alpha-2",
        }

    def test_phone_number_implements_schema(self):
        assert DataModel.schema()["properties"]["phone_number"] == {
            "title": "PhoneNumber",
            "description": "A valid E.164 phone number.",
            "type": "string",
            "format": "E.164",
        }

    def test_formatted_phone_number_implements_schema(self):
        assert DataModel.schema()["properties"]["formatted_phone_number"] == {
            "title": "PhoneNumber",
            "description": "A valid E.164 phone number.",
            "type": "string",
            "format": "E.164",
        }

    @pytest.mark.skipif(
        sys.version_info < (3, 9),
        reason=(
            "Pydantic behavior oddly differs for Python 3.8 and below, where it "
            "instead of using the class name, uses the name of the field as title."
        ),
    )
    def test_sequence_not_str_implements_schema(self):
        assert DataModel.schema()["properties"]["sequence_not_str"] == {
            "title": "SequenceNotStr",
            "type": "array",
            "items": {"type": "integer"},
        }
