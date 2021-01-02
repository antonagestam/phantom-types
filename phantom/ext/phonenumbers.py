from __future__ import annotations

from typing import Final
from typing import Optional
from typing import cast

import phonenumbers

from phantom import Phantom
from phantom import get_bound_parser
from phantom.utils import excepts

__all__ = (
    "InvalidPhoneNumber",
    "normalize_phone_number",
    "is_phone_number",
    "is_formatted_phone_number",
    "PhoneNumber",
    "FormattedPhoneNumber",
)


# Ignore due to subclassing Any, since phonenumbers isn't annotated.
class InvalidPhoneNumber(
    phonenumbers.NumberParseException, TypeError  # type: ignore[misc]
):
    INVALID: Final = 99

    def __init__(self, error_type: int = INVALID, msg: str = "Invalid number") -> None:
        super().__init__(error_type, msg)


def _deconstruct_phone_number(
    phone_number: str, country_code: Optional[str] = None
) -> phonenumbers.PhoneNumber:
    try:
        parsed_number = phonenumbers.parse(phone_number, region=country_code)
    except phonenumbers.NumberParseException as e:
        raise InvalidPhoneNumber(e.error_type, e._msg)
    if not phonenumbers.is_valid_number(parsed_number):
        raise InvalidPhoneNumber
    return parsed_number


def normalize_phone_number(
    phone_number: str, country_code: Optional[str] = None
) -> FormattedPhoneNumber:
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
    ...


class FormattedPhoneNumber(str, Phantom, predicate=is_formatted_phone_number):
    @classmethod
    def parse(cls, instance: object) -> FormattedPhoneNumber:
        return normalize_phone_number(parse_str(instance))
