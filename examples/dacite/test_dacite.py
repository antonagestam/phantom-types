from __future__ import annotations

import datetime

import pytest
from dacite_example import Book


def test_negative_id_raises() -> None:
    with pytest.raises(TypeError, match=r"^Can't parse Natural from int value: -2$"):
        Book.parse(
            {
                "id": -2,
                "name": "foo",
                "published": datetime.datetime.now(tz=datetime.timezone.utc),
                "author": {"name": "Jane Doe", "email": "jane@doe.com"},
            }
        )


def test_empty_name_raises() -> None:
    with pytest.raises(TypeError, match=r"^Can't parse Name from str value: ''$"):
        Book.parse(
            {
                "id": 3,
                "name": "",
                "published": datetime.datetime.now(tz=datetime.timezone.utc),
                "author": {"name": "Jane Doe", "email": "jane@doe.com"},
            }
        )


def test_naive_datetime_raises() -> None:
    with pytest.raises(
        TypeError,
        match=(
            r"^Can't parse TZAware from datetime value: "
            r"datetime.datetime\([0-9, ]+\)$"
        ),
    ):
        Book.parse(
            {
                "id": 4,
                "name": "foo",
                "published": datetime.datetime.now(),
                "author": {"name": "Jane Doe", "email": "jane@doe.com"},
            }
        )


def test_long_name_raises() -> None:
    with pytest.raises(
        TypeError,
        match="^Can't parse Name from str value: 'John Ronald Reuel Tolkien'$",
    ):
        Book.parse(
            {
                "id": 1,
                "name": "foo",
                "published": datetime.datetime.now(tz=datetime.timezone.utc),
                "author": {
                    "name": "John Ronald Reuel Tolkien",
                    "email": "jrr@rings.com",
                },
            }
        )


def test_invalid_email_raises() -> None:
    with pytest.raises(
        TypeError, match=r"^Can't parse Email from str value: 'j@rr@john.com'$"
    ):
        Book.parse(
            {
                "id": 1,
                "name": "foo",
                "published": datetime.datetime.now(tz=datetime.timezone.utc),
                "author": {"name": "John", "email": "j@rr@john.com"},
            }
        )
