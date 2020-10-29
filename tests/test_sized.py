from typing import Final

import pytest

from phantom.sized import Empty
from phantom.sized import NonEmpty

parametrize_non_empty: Final = pytest.mark.parametrize(
    "container", ((1,), frozenset({1}), "foo")
)
parametrize_empty: Final = pytest.mark.parametrize("container", ((), frozenset(), ""))
parametrize_mutable: Final = pytest.mark.parametrize("container", ([], set(), {}))


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
        assert alias.__origin__ is NonEmpty
        (arg,) = alias.__args__
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
        assert alias.__origin__ is Empty
        (arg,) = alias.__args__
        assert arg is frozenset
