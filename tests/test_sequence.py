import pytest
from typing_extensions import get_args
from typing_extensions import get_origin

from phantom.sequence import SequenceNotStr

parametrize_instances = pytest.mark.parametrize(
    "value",
    (
        ("foo", "bar", "baz"),
        (1, 2, object()),
        (b"hello", b"there"),
    ),
)
parametrize_non_instances = pytest.mark.parametrize(
    "value",
    (
        "",
        "foo",
        object(),
        [],
        ["foo"],
        [b"bar"],
        b"",
        b"foo",
        {},
        set(),
        frozenset(),
    ),
)


class TestSequenceNotStr:
    @parametrize_instances
    def test_is_instance(self, value: object):
        assert isinstance(value, SequenceNotStr)

    @parametrize_non_instances
    def test_is_not_instance(self, value: object):
        assert not isinstance(value, SequenceNotStr)

    @parametrize_instances
    def test_parse_returns_instance(self, value: object):
        assert SequenceNotStr.parse(value) is value

    @parametrize_non_instances
    def test_parse_raises_for_non_instances(self, value: object):
        with pytest.raises(TypeError):
            SequenceNotStr.parse(value)

    def test_subscription_returns_type_alias(self):
        alias = SequenceNotStr[str]
        assert get_origin(alias) is SequenceNotStr
        (arg,) = get_args(alias)
        assert arg is str
