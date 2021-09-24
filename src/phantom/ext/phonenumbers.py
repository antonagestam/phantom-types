"""
Requires the phonenumbers_ package which can be installed with:

.. _phonenumbers: https://pypi.org/project/phonenumbers/

.. code-block:: bash

    $ python3 -m pip install phantom-types[phonenumbers]
"""
from __future__ import annotations

from typing import cast

import phonenumbers
from typing_extensions import Final

from phantom import Phantom
from phantom import get_bound_parser
from phantom.fn import excepts
from phantom.schema import Schema

__all__ = (
    "InvalidPhoneNumber",
    "normalize_phone_number",
    "is_phone_number",
    "is_formatted_phone_number",
    "PhoneNumber",
    "FormattedPhoneNumber",
)


class InvalidPhoneNumber(phonenumbers.NumberParseException, TypeError):
    INVALID: Final = 99

    def __init__(self, error_type: int = INVALID, msg: str = "Invalid number") -> None:
        super().__init__(error_type, msg)


def _deconstruct_phone_number(
    phone_number: str, country_code: str | None = None
) -> phonenumbers.PhoneNumber:
    try:
        parsed_number = phonenumbers.parse(phone_number, region=country_code)
    except phonenumbers.NumberParseException as e:
        raise InvalidPhoneNumber(e.error_type, e._msg)
    if not phonenumbers.is_valid_number(parsed_number):
        raise InvalidPhoneNumber
    return parsed_number


def normalize_phone_number(
    phone_number: str, country_code: str | None = None
) -> FormattedPhoneNumber:
    """
    Normalize ``phone_number`` using :py:const:`phonenumbers.PhoneNumberFormat.E164`.

    :raises InvalidPhoneNumber:
    """
    normalized = phonenumbers.format_number(
        _deconstruct_phone_number(phone_number, country_code),
        phonenumbers.PhoneNumberFormat.E164,
    )
    return cast(FormattedPhoneNumber, normalized)


is_phone_number = excepts(InvalidPhoneNumber)(_deconstruct_phone_number)
parse_str = get_bound_parser(str)


def is_formatted_phone_number(number: str) -> bool:
    try:
        return number == normalize_phone_number(number)
    except InvalidPhoneNumber:
        return False


class PhoneNumber(str, Phantom, predicate=is_phone_number):
    @classmethod
    def __schema__(cls) -> Schema:
        return {
            **super().__schema__(),  # type: ignore[misc]
            "description": "A valid E.164 phone number.",
            "type": "string",
            "format": "E.164",
        }


class FormattedPhoneNumber(PhoneNumber, predicate=is_formatted_phone_number):
    @classmethod
    def parse(cls, instance: object) -> FormattedPhoneNumber:
        """
        Normalize number using :py:const:`phonenumbers.PhoneNumberFormat.E164`.

        :raises InvalidPhoneNumber:
        """
        return normalize_phone_number(parse_str(instance))

    @classmethod
    def __schema__(cls) -> Schema:
        return {
            **super().__schema__(),  # type: ignore[misc]
            "title": "PhoneNumber",
        }
