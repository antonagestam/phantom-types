import pytest

from phantom import Phantom
from phantom.base import AbstractInstanceCheck
from phantom.base import NotWithinKind
from phantom.predicates.numeric import positive
from phantom.utils import UnresolvedClassAttribute


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

    def test_can_subclass_without_kind(self):
        class A(Phantom, bound=int, predicate=positive):
            ...

        class B(A, bound=str):
            ...

    def test_subclass_outside_kind_raises(self):
        class A(Phantom, kind=int, abstract=True):
            ...

        with pytest.raises(NotWithinKind):

            class B(A, bound=str, abstract=True):
                ...

    def test_can_define_bound_implicitly(self):
        class A(float, Phantom, abstract=True):
            ...

        assert A.__bound__ == (float,)  # type: ignore[misc]

    def test_can_define_bound_explicitly(self):
        class A(Phantom, bound=float, abstract=True):
            ...

        assert A.__bound__ == (float,)  # type: ignore[misc]

    def test_can_inherit_bound(self):
        class A(Phantom, bound=float, abstract=True):
            ...

        class B(A, abstract=True):
            ...

        assert B.__bound__ == (float,)  # type: ignore[misc]

    def test_abstract_instance_check_raises(self):
        class A(Phantom, bound=float, abstract=True):
            ...

        with pytest.raises(AbstractInstanceCheck):
            isinstance(1, A)
