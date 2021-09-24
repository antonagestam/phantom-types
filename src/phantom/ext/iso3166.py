import warnings

from phantom.iso3166 import ALPHA2
from phantom.iso3166 import InvalidCountryCode
from phantom.iso3166 import ParsedAlpha2 as Alpha2
from phantom.iso3166 import is_alpha2_country_code
from phantom.iso3166 import normalize_alpha2_country_code

__all__ = (
    "Alpha2",
    "ALPHA2",
    "InvalidCountryCode",
    "normalize_alpha2_country_code",
    "is_alpha2_country_code",
    "CountryCode",
)
warnings.warn(
    (
        "`phantom.ext.iso3166` is deprecated in favor of `phantom.iso3166` and will be "
        "removed in phantom-types 0.13."
    ),
    DeprecationWarning,
)
CountryCode = Alpha2
