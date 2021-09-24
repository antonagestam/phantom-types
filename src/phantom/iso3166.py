"""
Exposes a :py:class:`CountryCode` type that is a union of a :py:class:`Literal`
containing all ISO3166 alpha-2 codes, and a phantom type that parses alpha-2 codes at
runtime. This allows mixing statically known values with runtime-parsed values, like
so:

.. code-block:: python

    countries: tuple[CountryCode] = ("SE", "DK", ParsedAlpha2.parse("FR"))
"""
from __future__ import annotations

from typing import Union
from typing import cast

from typing_extensions import Final
from typing_extensions import Literal
from typing_extensions import get_args

from phantom import Phantom
from phantom import get_bound_parser
from phantom.predicates.collection import contained
from phantom.schema import Schema

__all__ = (
    "LiteralAlpha2",
    "ParsedAlpha2",
    "Alpha2",
    "CountryCode",
    "is_alpha2_country_code",
    "normalize_alpha2_country_code",
    "InvalidCountryCode",
)

LiteralAlpha2 = Literal[
    "AF",
    "AX",
    "AL",
    "DZ",
    "AS",
    "AD",
    "AO",
    "AI",
    "AQ",
    "AG",
    "AR",
    "AM",
    "AW",
    "AU",
    "AT",
    "AZ",
    "BS",
    "BH",
    "BD",
    "BB",
    "BY",
    "BE",
    "BZ",
    "BJ",
    "BM",
    "BT",
    "BO",
    "BQ",
    "BA",
    "BW",
    "BV",
    "BR",
    "IO",
    "BN",
    "BG",
    "BF",
    "BI",
    "KH",
    "CM",
    "CA",
    "CV",
    "KY",
    "CF",
    "TD",
    "CL",
    "CN",
    "CX",
    "CC",
    "CO",
    "KM",
    "CG",
    "CD",
    "CK",
    "CR",
    "CI",
    "HR",
    "CU",
    "CW",
    "CY",
    "CZ",
    "DK",
    "DJ",
    "DM",
    "DO",
    "EC",
    "EG",
    "SV",
    "GQ",
    "ER",
    "EE",
    "ET",
    "FK",
    "FO",
    "FJ",
    "FI",
    "FR",
    "GF",
    "PF",
    "TF",
    "GA",
    "GM",
    "GE",
    "DE",
    "GH",
    "GI",
    "GR",
    "GL",
    "GD",
    "GP",
    "GU",
    "GT",
    "GG",
    "GN",
    "GW",
    "GY",
    "HT",
    "HM",
    "VA",
    "HN",
    "HK",
    "HU",
    "IS",
    "IN",
    "ID",
    "IR",
    "IQ",
    "IE",
    "IM",
    "IL",
    "IT",
    "JM",
    "JP",
    "JE",
    "JO",
    "KZ",
    "KE",
    "KI",
    "KP",
    "KR",
    "XK",
    "KW",
    "KG",
    "LA",
    "LV",
    "LB",
    "LS",
    "LR",
    "LY",
    "LI",
    "LT",
    "LU",
    "MO",
    "MK",
    "MG",
    "MW",
    "MY",
    "MV",
    "ML",
    "MT",
    "MH",
    "MQ",
    "MR",
    "MU",
    "YT",
    "MX",
    "FM",
    "MD",
    "MC",
    "MN",
    "ME",
    "MS",
    "MA",
    "MZ",
    "MM",
    "NA",
    "NR",
    "NP",
    "NL",
    "NC",
    "NZ",
    "NI",
    "NE",
    "NG",
    "NU",
    "NF",
    "MP",
    "NO",
    "OM",
    "PK",
    "PW",
    "PS",
    "PA",
    "PG",
    "PY",
    "PE",
    "PH",
    "PN",
    "PL",
    "PT",
    "PR",
    "QA",
    "RE",
    "RO",
    "RU",
    "RW",
    "BL",
    "SH",
    "KN",
    "LC",
    "MF",
    "PM",
    "VC",
    "WS",
    "SM",
    "ST",
    "SA",
    "SN",
    "RS",
    "SC",
    "SL",
    "SG",
    "SX",
    "SK",
    "SI",
    "SB",
    "SO",
    "ZA",
    "GS",
    "SS",
    "ES",
    "LK",
    "SD",
    "SR",
    "SJ",
    "SZ",
    "SE",
    "CH",
    "SY",
    "TW",
    "TJ",
    "TZ",
    "TH",
    "TL",
    "TG",
    "TK",
    "TO",
    "TT",
    "TN",
    "TR",
    "TM",
    "TC",
    "TV",
    "UG",
    "UA",
    "AE",
    "GB",
    "US",
    "UM",
    "UY",
    "UZ",
    "VU",
    "VE",
    "VN",
    "VG",
    "VI",
    "WF",
    "EH",
    "YE",
    "ZM",
    "ZW",
]
"""Literal of all ISO3166 alpha-2 codes. """

ALPHA2: Final = frozenset(get_args(LiteralAlpha2))
is_alpha2_country_code = contained(ALPHA2)
parse_str = get_bound_parser(str)


class InvalidCountryCode(TypeError):
    ...


def normalize_alpha2_country_code(country_code: str) -> ParsedAlpha2:
    """
    Normalize mixed case country code.

    :raises InvalidCountryCode:
    """
    normalized = country_code.upper()
    if not is_alpha2_country_code(normalized):
        raise InvalidCountryCode
    return cast(ParsedAlpha2, normalized)


class ParsedAlpha2(str, Phantom, predicate=is_alpha2_country_code):
    @classmethod
    def parse(cls, instance: object) -> ParsedAlpha2:
        """
        Normalize mixed case country code.

        :raises InvalidCountryCode:
        """
        return normalize_alpha2_country_code(parse_str(instance))

    @classmethod
    def __schema__(cls) -> Schema:
        return {
            **super().__schema__(),  # type: ignore[misc]
            "description": "ISO3166-1 alpha-2 country code",
            "examples": ["NR", "KZ", "ET", "VC", "AE", "NZ", "SX", "XK", "AX"],
            "format": "iso3166-1 alpha-2",
            "title": "Alpha2",
        }


Alpha2 = Union[LiteralAlpha2, ParsedAlpha2]
CountryCode = Alpha2
