import pydantic
from phantom.datetime import TZAware
from phantom.datetime import TZNaive
from phantom.ext.iso3166 import CountryCode
from phantom.ext.phonenumbers import FormattedPhoneNumber
from phantom.ext.phonenumbers import PhoneNumber
from phantom.interval import Closed
from phantom.interval import ClosedOpen
from phantom.interval import Natural
from phantom.interval import NegativeInt
from phantom.interval import Open
from phantom.interval import OpenClosed
from phantom.interval import Portion
from phantom.re import FullMatch
from phantom.re import Match
from phantom.sized import Empty
from phantom.sized import NonEmpty


class OpenType(int, Open, low=0, high=100):
    ...


class ClosedType(float, Closed, low=-1, high=1):
    ...


class OpenClosedType(float, OpenClosed, low=0, high=100):
    ...


class ClosedOpenType(float, ClosedOpen, low=-100, high=0):
    ...


class MatchType(Match, pattern=r"^[A-Z]{2}[0-9]{2}$"):
    ...


class FullMatchType(FullMatch, pattern=r"^[A-Z]{2}[0-9]{2}$"):
    ...


class DataModel(pydantic.BaseModel):
    open: OpenType
    closed: ClosedType
    open_closed: OpenClosedType
    closed_open: ClosedOpenType
    negative_int: NegativeInt
    natural: Natural
    portion: Portion
    tz_aware: TZAware
    tz_naive: TZNaive
    match: MatchType
    full_match: FullMatchType
    non_empty: NonEmpty[str]
    empty: Empty
    country: CountryCode
    phone_number: PhoneNumber
    formatted_phone_number: FormattedPhoneNumber


class TestShippedTypesImplementsSchema:
    def test_interval_open_implements_schema(self):
        assert DataModel.schema()["properties"]["open"] == {
            "minimum": 0,
            "maximum": 100,
            "description": "A value in the inclusive range (0, 100).",
            "title": "OpenType",
            "type": "integer",
        }

    def test_interval_closed_implements_schema(self):
        assert DataModel.schema()["properties"]["closed"] == {
            "description": "A value in the exclusive range [-1, 1].",
            "exclusiveMinimum": -1,
            "exclusiveMaximum": 1,
            "title": "ClosedType",
            "type": "number",
        }

    def test_interval_open_closed_implements_schema(self):
        assert DataModel.schema()["properties"]["open_closed"] == {
            "description": "A value in the half-open range (0, 100].",
            "minimum": 0,
            "exclusiveMaximum": 100,
            "title": "OpenClosedType",
            "type": "number",
        }

    def test_interval_closed_open_implements_schema(self):
        assert DataModel.schema()["properties"]["closed_open"] == {
            "title": "ClosedOpenType",
            "description": "A value in the half-open range [-100, 0).",
            "exclusiveMinimum": -100,
            "maximum": 0,
            "type": "number",
        }

    def test_interval_negative_int_implements_schema(self):
        assert DataModel.schema()["properties"]["negative_int"] == {
            "title": "NegativeInt",
            "maximum": 0,
            "description": "An integer value in the inclusive range (-∞, 0).",
            "type": "integer",
        }

    def test_interval_natural_implements_schema(self):
        assert DataModel.schema()["properties"]["natural"] == {
            "title": "Natural",
            "description": "An integer value in the inclusive range (0, ∞).",
            "minimum": 0,
            "type": "integer",
        }

    def test_interval_portion_implements_schema(self):
        assert DataModel.schema()["properties"]["portion"] == {
            "title": "Portion",
            "description": "A float value in the inclusive range (0, 1).",
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
            "format": "date-time",
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
