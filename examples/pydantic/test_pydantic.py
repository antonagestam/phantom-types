from __future__ import annotations

import datetime
import re

import pytest
from pydantic import ValidationError
from pydantic_example import Book


def book_data(**overrides) -> dict[str, object]:
    return {
        "id": 2,
        "name": "foo",
        "published": datetime.datetime.now(tz=datetime.timezone.utc),
        "author": {"name": "Jane Doe", "email": "jane@doe.com"},
        **overrides,
    }


def raises_validation_error(field: str, type_: str, value: str):
    return pytest.raises(
        ValidationError,
        match=(
            fr"^1 validation error for Book\n{re.escape(field)}\n  Could not parse "
            fr"{re.escape(type_)} from {re.escape(value)} \(type=type_error\)$"
        ),
    )


def test_negative_id_raises() -> None:
    with raises_validation_error("id", "phantom.interval.Natural", "-2"):
        Book.parse_obj(book_data(id=-2))


def test_empty_name_raises() -> None:
    with raises_validation_error("name", "pydantic_example.Name", "''"):
        Book.parse_obj(book_data(name=""))


def test_naive_datetime_raises() -> None:
    dt = datetime.datetime.now()
    with raises_validation_error("published", "phantom.datetime.TZAware", repr(dt)):
        Book.parse_obj(book_data(published=dt))


def test_long_name_raises() -> None:
    long_name = "John Ronald Reuel Tolkien"
    with raises_validation_error("name", "pydantic_example.Name", f"'{long_name}'"):
        Book.parse_obj(book_data(name=long_name))


def test_invalid_email_raises() -> None:
    not_an_email = "hello@test@test.test"
    with raises_validation_error(
        "author -> email", "pydantic_example.Email", f"'{not_an_email}'"
    ):
        Book.parse_obj(book_data(author={"name": "John Doe", "email": not_an_email}))
