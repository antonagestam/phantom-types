from typing import Callable
from typing import Union

import pytest

from phantom import Phantom
from phantom import get_bound_parser
from phantom.base import AbstractInstanceCheck
from phantom.base import BoundError
from phantom.base import PhantomMeta
from phantom.predicates.numeric import positive
from phantom.utils import UnresolvedClassAttribute


class TestParseBound:
    def test_can_parse_simple_bound(self):
        value = 1
        assert get_bound_parser(int)(value) is value

    def test_raises_for_invalid_value(self):
        parser = get_bound_parser(int)
        with pytest.raises(
            BoundError,
            match=r"^Value is not within bound of 'int': '1'$",
        ):
            parser("1")

    def test_raises_for_invalid_intersection(self):
        parser = get_bound_parser((int, float))
        with pytest.raises(
            BoundError,
            match=r"^Value is not within bound of 'Intersection\[int, float\]': '2'$",
        ):
            parser("2")

    def test_raises_for_invalid_union(self):
        parser = get_bound_parser(Union[int, float])
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

        parser = get_bound_parser((A, B))
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
        assert parser(a := A()) is a
        assert parser(b := B()) is b
        assert parser(c := C()) is c


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
