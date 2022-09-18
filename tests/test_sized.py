from dataclasses import dataclass

import pytest
from typing_extensions import Final
from typing_extensions import get_args
from typing_extensions import get_origin

from phantom.sized import Empty
from phantom.sized import NonEmpty
from phantom.sized import NonEmptyStr


@dataclass
class MutableDataclass:
    value: str = "foo"


parametrize_non_empty: Final = pytest.mark.parametrize(
    "container",
    ((1,), frozenset({1}), "foo"),
)
parametrize_empty: Final = pytest.mark.parametrize(
    "container",
    ((), frozenset(), ""),
)
parametrize_mutable: Final = pytest.mark.parametrize(
    "container",
    ([], set(), {}, MutableDataclass()),
)


class TestNonEmpty:
    @parametrize_non_empty
    def test_non_empty_container_is_instance(self, container):
        assert isinstance(container, NonEmpty)

    @parametrize_empty
    def test_empty_container_is_instance(self, container):
        assert not isinstance(container, NonEmpty)

    @parametrize_empty
    def test_instantiation_raises_for_empty_container(self, container):
        with pytest.raises(TypeError):
            NonEmpty.parse(container)

    @parametrize_mutable
    def test_instantiation_raises_for_mutable(self, container):
        with pytest.raises(TypeError):
            NonEmpty.parse(container)

    @parametrize_non_empty
    def test_instantiation_returns_instance(self, container):
        assert container is NonEmpty.parse(container)

    def test_subscription_returns_type_alias(self):
        alias = NonEmpty[tuple]
        assert get_origin(alias) is NonEmpty
        (arg,) = get_args(alias)
        assert arg is tuple


class TestEmpty:
    @parametrize_non_empty
    def test_non_empty_container_is_instance(self, container):
        assert not isinstance(container, Empty)

    @parametrize_empty
    def test_empty_container_is_instance(self, container):
        assert isinstance(container, Empty)

    @parametrize_non_empty
    def test_instantiation_raises_for_non_empty_container(self, container):
        with pytest.raises(TypeError):
            Empty.parse(container)

    @parametrize_mutable
    def test_instantiation_raises_for_mutable(self, container):
        with pytest.raises(TypeError):
            Empty.parse(container)

    @parametrize_empty
    def test_instantiation_returns_instance(self, container):
        assert container is Empty.parse(container)

    def test_subscription_returns_type_alias(self):
        alias = Empty[frozenset]
        assert get_origin(alias) is Empty
        (arg,) = get_args(alias)
        assert arg is frozenset


parametrize_non_empty_strs: Final = pytest.mark.parametrize(
    "value",
    ("foo", "bar", " "),
)


class TestNonEmptyStr:
    @parametrize_non_empty_strs
    def test_non_empty_str_is_instance(self, value: str):
        assert isinstance(value, NonEmptyStr)

    def test_empty_str_is_not_instance(self):
        assert not isinstance("", NonEmptyStr)

    def test_instantiation_raises_for_empty_str(self):
        with pytest.raises(TypeError):
            NonEmptyStr.parse("")

    @pytest.mark.parametrize(
        "value",
        (b"", b"foo", [], ["foo"], (), ("foo",)),
    )
    def test_instantiation_raises_for_non_str(self, value: object):
        with pytest.raises(TypeError):
            NonEmptyStr.parse(value)

    @parametrize_non_empty_strs
    def test_instantiation_returns_instance(self, value: str):
        assert value is NonEmptyStr.parse(value)
