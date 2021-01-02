import pytest

from phantom.base import BoundError
from phantom.ext.phonenumbers import FormattedPhoneNumber
from phantom.ext.phonenumbers import InvalidPhoneNumber
from phantom.ext.phonenumbers import PhoneNumber
from phantom.ext.phonenumbers import _deconstruct_phone_number
from phantom.ext.phonenumbers import is_formatted_phone_number
from phantom.ext.phonenumbers import is_phone_number
from phantom.ext.phonenumbers import normalize_phone_number


class TestPhoneNumber:
    def test_unparsable_number_is_not_instance(self):
        assert not isinstance("+46", PhoneNumber)

    def test_invalid_number_is_not_instance(self):
        assert not isinstance("+467012345678", PhoneNumber)

    def test_unformatted_number_is_instance(self):
        assert isinstance("+46 (701) 234567", PhoneNumber)


class TestFormattedPhoneNumber:
    def test_unparsable_number_is_not_instance(self):
        assert not isinstance("+46", FormattedPhoneNumber)

    def test_invalid_number_is_not_instance(self):
        assert not isinstance("+467012345678", FormattedPhoneNumber)

    def test_unformatted_number_is_not_instance(self):
        assert not isinstance("+46 (701) 234567", FormattedPhoneNumber)

    def test_formatted_number_is_instance(self):
        assert isinstance("+46701234567", FormattedPhoneNumber)

    def test_normalizes_unformatted_number(self):
        number = FormattedPhoneNumber.parse("+46 (701) 234567")
        assert number == "+46701234567"
        assert isinstance(number, FormattedPhoneNumber)

    def test_parse_raises_for_invalid_phone_number(self):
        with pytest.raises(InvalidPhoneNumber):
            FormattedPhoneNumber.parse("+46")

    def test_raises_type_error_for_out_of_bound_type(self):
        """Since we override parse we need to test the bound check"""
        value = 123
        with pytest.raises(
            BoundError, match=fr"Value is not within bound of 'str': {value}"
        ):
            FormattedPhoneNumber.parse(123)


class TestDeconstructPhoneNumber:
    def test_can_parse_international_phone_number_without_country_code(self):
        result = _deconstruct_phone_number("123456789", "SE")
        assert result.country_code == 46
        assert result.national_number == 123456789

    def test_can_parse_international_phone_number_with_country_code(self):
        result = _deconstruct_phone_number("+46123456789", "NO")
        assert result.country_code == 46
        assert result.national_number == 123456789

    def test_can_parse_national_phone_number_with_country_code(self):
        result = _deconstruct_phone_number("0123456789", "SE")
        assert result.country_code == 46
        assert result.national_number == 123456789

    def test_raises_invalid_phone_number_for_insufficient_country_data(self):
        with pytest.raises(InvalidPhoneNumber) as exc_info:
            _deconstruct_phone_number("0701")
        assert exc_info.value.error_type == InvalidPhoneNumber.INVALID_COUNTRY_CODE

    def test_raises_invalid_phone_number_for_parse_exception(self):
        with pytest.raises(InvalidPhoneNumber) as exc_info:
            _deconstruct_phone_number("0")
        assert exc_info.value.error_type == InvalidPhoneNumber.NOT_A_NUMBER

    def test_raises_invalid_phone_number_for_invalid_phone_number(self):
        with pytest.raises(InvalidPhoneNumber) as exc_info:
            _deconstruct_phone_number("+461234567890")
        assert exc_info.value.error_type == InvalidPhoneNumber.INVALID


class TestNormalizePhoneNumber:
    def test_can_normalize_national_number_with_country_code(self):
        assert normalize_phone_number("(123) 456 789", "SE") == "+46123456789"

    def test_can_normalize_international_number_without_country_code(self):
        assert normalize_phone_number("+46 (123) 456 789") == "+46123456789"


class TestIsPhoneNumber:
    def test_returns_true_for_valid_number(self):
        assert is_phone_number("+46 (123) 456789") is True

    def test_returns_false_for_invalid_number(self):
        assert is_phone_number("+461234567890") is False


class TestIsFormattedPhoneNumber:
    def test_returns_true_for_formatted_number(self):
        assert is_formatted_phone_number("+46123456789") is True

    def test_returns_false_for_unformatted_number(self):
        assert is_formatted_phone_number("+46 (123) 456 789") is False
