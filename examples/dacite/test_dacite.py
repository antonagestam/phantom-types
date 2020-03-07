import datetime
from dataclasses import dataclass
from typing import Any
from typing import Dict

import pytest
from dacite import Config
from dacite import from_dict

from dept.base import Dependent
from dept.datetime import TZAware
from dept.numeric import Natural
from dept.sized import NonEmpty


@dataclass(frozen=True)
class Book:
    id: Natural
    name: NonEmpty[str]
    published: TZAware

    @classmethod
    def parse(cls, data: Dict[str, Any]):
        return from_dict(cls, data, config=Config(cast=[Dependent]))


def test_can_parse_valid_book():
    book = Book.parse(
        {
            "id": 1,
            "name": "foo",
            "published": datetime.datetime.now(tz=datetime.timezone.utc),
        }
    )
    assert isinstance(book, Book)


def test_negative_id_raises():
    with pytest.raises(TypeError, match=r"^Can't create Natural from -2$"):
        Book.parse(
            {
                "id": -2,
                "name": "foo",
                "published": datetime.datetime.now(tz=datetime.timezone.utc),
            }
        )


def test_empty_name_raises():
    with pytest.raises(TypeError, match=r"^Can't create NonEmpty from ''$"):
        Book.parse(
            {
                "id": 3,
                "name": "",
                "published": datetime.datetime.now(tz=datetime.timezone.utc),
            }
        )


def test_naive_datetime_raises():
    with pytest.raises(
        TypeError, match=r"^Can't create TZAware from datetime\.datetime"
    ):
        Book.parse({"id": 4, "name": "foo", "published": datetime.datetime.now()})
