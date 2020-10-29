import pytest

from phantom.ext.iso3166 import Alpha2
from phantom.ext.iso3166 import InvalidCountryCode
from phantom.ext.iso3166 import normalize_alpha2_country_code


class TestNormalizeAlpha2CountryCode:
    @pytest.mark.parametrize(
        "given, normalized",
        (("sE", "SE"), ("dk", "DK"), ("IE", "IE")),
    )
    def test_normalizes_mixed_case_valid_country_code(
        self, given: str, normalized: str
    ) -> None:
        assert normalize_alpha2_country_code(given) == normalized

    @pytest.mark.parametrize("invalid", ("UK", "not a country code"))
    def test_raises_for_invalid_country_code(self, invalid: str) -> None:
        with pytest.raises(InvalidCountryCode):
            normalize_alpha2_country_code(invalid)


class TestAlpha2:
    @pytest.mark.parametrize("invalid", ("SP", "DA", "AV", 1))
    def test_invalid_country_code_is_not_instance(self, invalid: object) -> None:
        assert not isinstance(invalid, Alpha2)

    @pytest.mark.parametrize("country_code", ("PS", "AD", "VA"))
    def test_valid_country_code_is_instance(self, country_code: str) -> None:
        assert isinstance(country_code, Alpha2)

    def test_normalizes_valid_country_code(self) -> None:
        country_code = Alpha2.parse("ps")
        assert country_code == "PS"
        assert isinstance(country_code, Alpha2)

    @pytest.mark.parametrize("invalid", ("SP", "DA", "AV"))
    def test_raises_for_invalid_country_code(self, invalid: str) -> None:
        with pytest.raises(InvalidCountryCode):
            Alpha2.parse(invalid)
