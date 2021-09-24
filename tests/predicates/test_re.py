import re

from phantom.predicates.re import is_full_match
from phantom.predicates.re import is_match

from .utils import assert_predicate_name_equals

pattern = re.compile("abc@")
abc_match = is_match(pattern)
abc_full_match = is_full_match(pattern)


class TestIsMatch:
    def test_returns_true_for_matching_string(self) -> None:
        assert abc_match("abc@") is True
        assert abc_match("abc@ extra") is True

    def test_returns_false_for_non_matching_string(self) -> None:
        assert abc_match("abd@") is False
        assert abc_match("extra abc@") is False

    def test_repr_contains_bound_parameter(self):
        assert_predicate_name_equals(abc_match, "is_match('abc@')")


class TestIsFullMatch:
    def test_returns_true_for_matching_string(self) -> None:
        assert abc_full_match("abc@") is True

    def test_returns_false_for_non_matching_string(self) -> None:
        assert abc_full_match("abc@ extra") is False
        assert abc_full_match("abd@") is False
        assert abc_full_match("extra abc@") is False

    def test_repr_contains_bound_parameter(self):
        assert_predicate_name_equals(abc_full_match, "is_full_match('abc@')")
