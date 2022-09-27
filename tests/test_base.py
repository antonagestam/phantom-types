import sys
from dataclasses import dataclass
from typing import Callable
from typing import Union

import pytest

from phantom import Phantom
from phantom import PhantomMeta
from phantom._base import AbstractInstanceCheck
from phantom._base import MutableType
from phantom._utils.misc import UnresolvedClassAttribute
from phantom.bounds import Parser
from phantom.bounds import get_bound_parser
from phantom.errors import BoundError
from phantom.predicates import boolean
from phantom.predicates.numeric import positive


class TestParseBound:
    def test_can_parse_simple_bound(self):
        value = 1
        assert get_bound_parser(int)(value) is value

    def test_raises_for_invalid_value(self):
        parser: Parser[int] = get_bound_parser(int)
        with pytest.raises(
            BoundError,
            match=r"^Value is not within bound of 'int': '1'$",
        ):
            parser("1")

    def test_raises_for_invalid_intersection(self):
        parser: Parser[float] = get_bound_parser((int, float))
        with pytest.raises(
            BoundError,
            match=r"^Value is not within bound of 'Intersection\[int, float\]': '2'$",
        ):
            parser("2")

    def test_raises_for_invalid_union(self):
        parser: Parser[Union[int, float]] = get_bound_parser(Union[int, float])
        with pytest.raises(
            BoundError,
            match=r"^Value is not within bound of 'typing\.Union\[int, float\]': '3'$",
        ):
            parser("3")

    @pytest.mark.skipif(sys.version_info < (3, 10), reason="requires 3.10+")
    def test_raises_for_invalid_pep_604_union(self):
        parser: Parser[int | float] = get_bound_parser(  # type: ignore[misc]
            int | float  # type: ignore[operator]
        )
        with pytest.raises(
            BoundError,
            match=r"^Value is not within bound of 'typing\.Union\[int, float\]': '3'$",
        ):
            parser("3")

    def test_can_parse_intersection(self):
        class A:
            ...

        class B:
            ...

        class C(A, B):
            ...

        parser: Parser[C] = get_bound_parser((A, B))
        value = C()
        assert parser(value) is value

    def test_can_parse_union(self):
        class A:
            ...

        class B:
            ...

        class C(A, B):
            ...

        parser: Callable[[object], Union[A, B]] = get_bound_parser(Union[A, B])
        a = A()
        b = B()
        c = C()
        assert parser(a) is a
        assert parser(b) is b
        assert parser(c) is c


class TestPhantom:
    def test_subclass_without_predicate_raises(self):
        with pytest.raises(
            UnresolvedClassAttribute, match="must define class attribute __predicate__"
        ):

            class A(Phantom, bound=int):
                ...

    def test_subclass_without_bound_raises(self):
        with pytest.raises(
            UnresolvedClassAttribute, match="must define class attribute __bound__"
        ):

            class A(Phantom, predicate=positive):
                ...

    def test_rejects_partial_bound(self):
        class A(Phantom, predicate=positive, bound=(int, float)):
            ...

        assert not isinstance(1.0, A)

    def test_concrecte_subclass_of_abstract_raises_for_missing_class_attribute(self):
        class A(Phantom, bound=int, abstract=True):
            ...

        with pytest.raises(
            UnresolvedClassAttribute, match="must define class attribute __predicate__"
        ):

            class B(A):
                ...

    def test_can_subclass_without_predicate_if_abstract(self):
        class A(Phantom, bound=int, abstract=True):
            ...

    def test_can_subclass_without_bound_if_abstract(self):
        class A(Phantom, predicate=positive, abstract=True):
            ...

    def test_subclass_with_incompatible_bounds_raises(self):
        class A(Phantom, bound=Union[int, float], abstract=True):
            ...

        with pytest.raises(BoundError):

            class B(A, bound=str, abstract=True):
                ...

    def test_can_define_bound_implicitly(self):
        class A(float, Phantom, abstract=True):
            ...

        assert A.__bound__ is float

    def test_can_define_bound_explicitly(self):
        class A(Phantom, bound=float, abstract=True):
            ...

        assert A.__bound__ is float

    def test_can_inherit_bound(self):
        class A(Phantom, bound=float, abstract=True):
            ...

        class B(A, abstract=True):
            ...

        assert B.__bound__ is float

    @pytest.mark.parametrize(
        "bound_type",
        [
            list,
            set,
            dict,
            dataclass(type("A", (), {})),
        ],
    )
    def test_raises_mutable_type_for_mutable_bound_type(self, bound_type: type):
        with pytest.raises(MutableType):

            class A(
                bound_type,  # type: ignore[valid-type,misc]
                Phantom,
                abstract=True,
            ):
                ...

    def test_can_use_frozen_dataclass_as_bound(self):
        @dataclass(frozen=True)
        class A:
            ...

        class B(A, Phantom, predicate=boolean.true):
            ...

    def test_abstract_instance_check_raises(self):
        class A(Phantom, bound=float, abstract=True):
            ...

        with pytest.raises(AbstractInstanceCheck):
            isinstance(1, A)

    def test_phantom_meta_is_usable_without_phantom_base(self):
        class Alt(metaclass=PhantomMeta):
            ...

        assert isinstance("a", Alt) is False

        class AlwaysTrue(metaclass=PhantomMeta):
            @classmethod
            def __instancecheck__(self, instance: object) -> bool:
                return True

        assert isinstance("a", AlwaysTrue) is True
