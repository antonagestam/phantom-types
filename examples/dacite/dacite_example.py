from __future__ import annotations

import datetime
import re
from dataclasses import dataclass
from typing import TYPE_CHECKING
from typing import Any

from dacite import Config
from dacite import from_dict

from phantom import Phantom
from phantom.datetime import TZAware
from phantom.interval import Natural
from phantom.predicates.interval import exclusive_inclusive
from phantom.re import Match
from phantom.sized import PhantomSized


class Name(str, PhantomSized[str], len=exclusive_inclusive(0, 20)):
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
    name: Name
    published: TZAware
    author: Author

    @classmethod
    def parse(cls, data: dict[str, Any]) -> Book:
        return from_dict(cls, data, config=Config(cast=[Phantom]))


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
assert type(book.name) is str
assert type(book.published) is datetime.datetime  # type: ignore[comparison-overlap]
assert type(book.author.name) is str
assert type(book.author.email) is str

# But the phantom types let's us statically retain more information about
# their shapes. This allows us to avoid shotgun parsing.
if TYPE_CHECKING:
    reveal_type(book.id)
    reveal_type(book.name)
    reveal_type(book.published)
    reveal_type(book.author.name)
    reveal_type(book.author.email)
