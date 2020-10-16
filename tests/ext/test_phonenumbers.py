import pytest

from phantom.ext.phonenumbers import FormattedPhoneNumber
from phantom.ext.phonenumbers import InvalidPhoneNumber
from phantom.ext.phonenumbers import PhoneNumber


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
        number = FormattedPhoneNumber.from_instance("+46 (701) 234567")
        assert number == "+46701234567"
        assert isinstance(number, FormattedPhoneNumber)

    def test_from_instance_raises_for_invalid_phone_number(self):
        with pytest.raises(InvalidPhoneNumber):
            FormattedPhoneNumber.from_instance("+46")

    def test_raises_type_error_for_out_of_bound_type(self):
        """Since we override from_instance we need to test the bound check"""
        value = 123
        with pytest.raises(
            TypeError,
            match=(
                fr"Can't create phantom type {FormattedPhoneNumber.__name__} from "
                fr"{value}"
            ),
        ):
            FormattedPhoneNumber.from_instance(123)
