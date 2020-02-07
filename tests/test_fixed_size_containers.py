import pytest

from dependent import Empty
from dependent import NonEmpty


parametrize_non_empty = pytest.mark.parametrize(
    "container", ([1], (1,), {1}, {"a": "b"})
)
parametrize_empty = pytest.mark.parametrize("container", ([], (), set(), {}))


class TestNonEmpty:
    @parametrize_non_empty
    def test_non_empty_container_is_instance(self, container):
        assert isinstance(container, NonEmpty)

    @parametrize_empty
    def test_empty_container_is_instance(self, container):
        assert not isinstance(container, NonEmpty)

    @parametrize_empty
    def test_instantiation_raises_for_empty_container(self, container):
        with pytest.raises(ValueError):
            NonEmpty.from_instance(container)

    @parametrize_non_empty
    def test_instantiation_returns_instance(self, container):
        assert container is NonEmpty.from_instance(container)


class TestEmpty:
    @parametrize_non_empty
    def test_non_empty_container_is_instance(self, container):
        assert not isinstance(container, Empty)

    @parametrize_empty
    def test_empty_container_is_instance(self, container):
        assert isinstance(container, Empty)

    @parametrize_non_empty
    def test_instantiation_raises_for_non_empty_container(self, container):
        with pytest.raises(ValueError):
            Empty.from_instance(container)

    @parametrize_empty
    def test_instantiation_returns_instance(self, container):
        assert container is Empty.from_instance(container)
