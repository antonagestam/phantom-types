from functools import partial

from phantom.predicates import boolean

from .utils import assert_predicate_name_equals


def foo(a: int, b: int, c: int) -> bool:
    return a > b > c


class TestFunctionRepr:
    def test_explodes_partial_arguments(self):
        predicate = partial(foo, 10, b=5)
        assert_predicate_name_equals(boolean.negate(predicate), "negate(foo(10, b=5))")
        predicate = partial(foo, "hello", c="goddag")
        assert_predicate_name_equals(
            boolean.negate(predicate), "negate(foo('hello', c='goddag'))"
        )
