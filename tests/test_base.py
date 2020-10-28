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
            type("A", (Phantom,), {}, bound=int)

    def test_concrecte_subclass_of_abstract_raises_for_missing_class_attribute(self):
        A = type("A", (Phantom,), {}, bound=int, abstract=True)
        with pytest.raises(
            UnresolvedClassAttribute, match="must define class attribute __predicate__"
        ):
            type("B", (A,), {})

    def test_can_subclass_without_predicate_if_abstract(self):
        type("A", (Phantom,), {}, bound=int, abstract=True)

    def test_can_subclass_without_kind(self):
        type("A", (Phantom,), {}, bound=int, predicate=positive)

    def test_subclass_outside_kind_raises(self):
        A = type("A", (Phantom,), {}, kind=int, abstract=True)
        with pytest.raises(NotWithinKind):
            type("B", (A,), {}, bound=str, abstract=True)

    def test_can_define_bound_implicitly(self):
        A = type("A", (float, Phantom), {}, abstract=True)
        assert A.__bound__ == (float,)

    def test_can_define_bound_explicitly(self):
        A = type("A", (Phantom,), {}, bound=float, abstract=True)
        assert A.__bound__ == (float,)

    def test_can_inherit_bound(self):
        A = type("A", (Phantom,), {}, bound=float, abstract=True)
        B = type("B", (A,), {}, abstract=True)
        assert B.__bound__ == (float,)

    def test_abstract_instance_check_raises(self):
        A = type("A", (Phantom,), {}, bound=float, abstract=True)
        with pytest.raises(AbstractInstanceCheck):
            isinstance(1, A)
