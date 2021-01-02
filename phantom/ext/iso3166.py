from __future__ import annotations

from typing import Final
from typing import cast

import iso3166

from phantom import Phantom
from phantom import get_bound_parser
from phantom.predicates.collection import contained

__all__ = (
    "ALPHA2",
    "is_alpha2_country_code",
    "InvalidCountryCode",
    "Alpha2",
    "CountryCode",
    "normalize_alpha2_country_code",
)

ALPHA2: Final = frozenset(iso3166.countries_by_alpha2.keys())
is_alpha2_country_code = contained(ALPHA2)
parse_str = get_bound_parser(str)


class InvalidCountryCode(TypeError):
    ...


def normalize_alpha2_country_code(country_code: str) -> Alpha2:
    normalized = country_code.upper()
    if not is_alpha2_country_code(normalized):
        raise InvalidCountryCode
    return cast(Alpha2, normalized)


class Alpha2(str, Phantom, predicate=is_alpha2_country_code):
    @classmethod
    def parse(cls, instance: object) -> Alpha2:
        return normalize_alpha2_country_code(parse_str(instance))


CountryCode = Alpha2
