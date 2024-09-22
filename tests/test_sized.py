from dataclasses import dataclass
from typing import Final
from typing import Generic
from typing import TypeVar

import pytest
from typing_extensions import get_args
from typing_extensions import get_origin

from phantom.predicates.numeric import odd
from phantom.sized import Empty
from phantom.sized import LSPViolation
from phantom.sized import NonEmpty
from phantom.sized import NonEmptyStr
from phantom.sized import PhantomBound
from phantom.sized import PhantomSized
from phantom.sized import UnresolvedBounds


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
    ([], [1], set(), {1}, {}, {1: 2}, MutableDataclass()),
)


T = TypeVar("T")


class OddSize(PhantomSized[T], Generic[T], len=odd): ...


class TestPhantomSized:
    odd_length = pytest.mark.parametrize(
        "container",
        [
            (1,),
            (1, 2, 3),
            (1, 2, 3, 4, 5),
            frozenset({1}),
            frozenset({1, 2, 3, 4, 5}),
        ],
    )
    even_length = pytest.mark.parametrize(
        "container",
        [
            (),
            (1, 1),
            (1, 1, 1, 2, 3, 6),
            frozenset(),
            frozenset({1, 2}),
        ],
    )

    @odd_length
    def test_value_fulfilling_predicate_is_instance(self, container: object):
        assert isinstance(container, OddSize)

    @even_length
    def test_value_not_fulfilling_predicate_is_not_instance(self, container: object):
        assert not isinstance(container, OddSize)

    @even_length
    def test_instantiation_raises_for_invalid_length(self, container: object):
        with pytest.raises(TypeError):
            OddSize.parse(container)

    @parametrize_mutable
    def test_instantiation_raises_for_mutable(self, container: object):
        with pytest.raises(TypeError):
            OddSize.parse(container)

    @parametrize_non_empty
    def test_instantiation_returns_instance(self, container: object):
        assert container is OddSize.parse(container)

    def test_subscription_returns_type_alias(self):
        alias = OddSize[tuple]
        assert get_origin(alias) is OddSize
        (arg,) = get_args(alias)
        assert arg is tuple


class Tens(PhantomBound[T], Generic[T], min=10, max=19): ...


class TestPhantomBound:
    valid = pytest.mark.parametrize(
        "container",
        [10 * (1,), 19 * (2,)],
    )
    invalid = pytest.mark.parametrize(
        "container",
        [9 * (1,), 20 * (2,)],
    )

    @valid
    def test_value_fulfilling_predicate_is_instance(self, container: object):
        assert isinstance(container, Tens)

    @invalid
    def test_value_not_fulfilling_predicate_is_not_instance(self, container: object):
        assert not isinstance(container, Tens)

    @invalid
    def test_instantiation_raises_for_invalid_length(self, container: object):
        with pytest.raises(TypeError):
            Tens.parse(container)

    @parametrize_mutable
    def test_instantiation_raises_for_mutable(self, container: object):
        with pytest.raises(TypeError):
            Tens.parse(container)

    @valid
    def test_instantiation_returns_instance(self, container: object):
        assert container is Tens.parse(container)

    def test_subscription_returns_type_alias(self):
        alias = Tens[tuple]
        assert get_origin(alias) is Tens
        (arg,) = get_args(alias)
        assert arg is tuple

    def test_raises_lsp_violation_when_attempting_to_decrease_min(self):
        with pytest.raises(LSPViolation):

            class Lower(Tens, min=9): ...

    def test_raises_lsp_violation_when_attempting_to_increase_max(self):
        with pytest.raises(LSPViolation):

            class Higher(Tens, max=20): ...

    def test_can_narrow_range_in_subclass(self):
        class Fewer(Tens, min=11, max=18): ...

        assert isinstance(11 * (0,), Fewer)
        assert isinstance(18 * (0,), Fewer)
        assert not isinstance(10 * (0,), Fewer)
        assert not isinstance(19 * (0,), Fewer)

    def test_abstract_subclass_can_omit_bounds(self):
        class A(PhantomBound, abstract=True): ...

        class B(A, min=10, max=20): ...

        assert B.__min__ == 10
        assert B.__max__ == 20

    def test_raises_unresolved_bounds_when_concrete_subclass_omits_bounds(self):
        with pytest.raises(UnresolvedBounds):

            class A(PhantomBound): ...


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
