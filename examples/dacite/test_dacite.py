from __future__ import annotations

import datetime
import re
from dataclasses import dataclass
from typing import Any
from typing import Dict
from typing import TYPE_CHECKING

import pytest
from dacite import Config
from dacite import from_dict

from dept.base import Dependent
from dept.datetime import TZAware
from dept.numeric import Natural
from dept.re import Match
from dept.sized import NonEmpty


class Name(str, NonEmpty[str], max=20):
    ...


class Email(Match, pattern=re.compile(r"^[a-z._]+@[a-z\-]+\.(?:com|se|am)$")):
    ...


@dataclass(frozen=True)
class Author:
    name: Name
    email: Email


@dataclass(frozen=True)
class Book:
    id: Natural
    name: NonEmpty[str]
    published: TZAware
    author: Author

    @classmethod
    def parse(cls, data: Dict[str, Any]) -> Book:
        return from_dict(cls, data, config=Config(cast=[Dependent]))


def test_can_parse_valid_book() -> None:
    book = Book.parse(
        {
            "id": 1,
            "name": "foo",
            "published": datetime.datetime.now(tz=datetime.timezone.utc),
            "author": {"name": "Jane Doe", "email": "jane@doe.com"},
        }
    )
    assert isinstance(book, Book)

    # Fields are regular builtin Python types at runtime
    assert type(book.id) is int
    assert type(book.name) is str  # type: ignore[comparison-overlap]
    assert type(book.published) is datetime.datetime
    assert type(book.author.name) is str
    assert type(book.author.email) is str

    # But the dependent types let's us statically retain more information about
    # their shapes. This allows us to avoid shotgun parsing.
    if TYPE_CHECKING:
        reveal_type(book.id)
        reveal_type(book.name)
        reveal_type(book.published)
        reveal_type(book.author.name)
        reveal_type(book.author.email)


def test_negative_id_raises() -> None:
    with pytest.raises(TypeError, match=r"^Can't create Natural from -2$"):
        Book.parse(
            {
                "id": -2,
                "name": "foo",
                "published": datetime.datetime.now(tz=datetime.timezone.utc),
                "author": {"name": "Jane Doe", "email": "jane@doe.com"},
            }
        )


def test_empty_name_raises() -> None:
    with pytest.raises(TypeError, match=r"^Can't create NonEmpty from ''$"):
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
        TypeError, match=r"^Can't create TZAware from datetime\.datetime"
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
        TypeError, match="^Can't create Name from 'John Ronald Reuel Tolkien'$"
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
    with pytest.raises(TypeError, match=r"^Can't create Email from 'j@rr@john\.com'$"):
        Book.parse(
            {
                "id": 1,
                "name": "foo",
                "published": datetime.datetime.now(tz=datetime.timezone.utc),
                "author": {"name": "John", "email": "j@rr@john.com"},
            }
        )
