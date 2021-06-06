from __future__ import annotations

import datetime
import re

from pydantic import BaseModel

from phantom.datetime import TZAware
from phantom.ext.iso3166 import CountryCode
from phantom.interval import Natural
from phantom.predicates.interval import closed_open
from phantom.re import Match
from phantom.sized import PhantomSized


class Name(str, PhantomSized[str], len=closed_open(0, 20)):
    @classmethod
    def __schema__(cls):
        return {
            **super().__schema__(),  # type: ignore[misc]
            "title": "Person Name",
            "description": "A name between 1 and 20 characters",
        }


class Email(Match, pattern=re.compile(r"^[a-z._]+@[a-z\-]+\.(?:com|se|am)$")):
    ...


class Author(BaseModel):
    name: Name
    email: Email


class Book(BaseModel):
    id: Natural
    name: Name
    published: TZAware
    country: CountryCode
    author: Author


book = Book.parse_obj(
    {
        "id": 1,
        "name": "foo",
        "published": datetime.datetime.now(tz=datetime.timezone.utc),
        "author": {"name": "Jane Doe", "email": "jane@doe.com"},
        "country": "NR",
    }
)

assert isinstance(book, Book)

# Fields are regular builtin Python types at runtime
assert type(book.id) is int
assert type(book.name) is str
assert type(book.published) is datetime.datetime  # type: ignore[comparison-overlap]
assert type(book.author.name) is str
assert type(book.author.email) is str

import json

print(json.dumps(Book.schema(), indent=2))
