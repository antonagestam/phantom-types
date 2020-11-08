import re

import pytest

from phantom.re import FullMatch
from phantom.re import Match


class A(Match, pattern=re.compile(r"abc")):
    ...


class TestMatch:
    def test_non_matching_string_is_not_instance(self):
        assert not isinstance("abd", A)

    def test_matching_string_is_instance(self):
        assert isinstance("abcd", A)

    def test_instantiation_raises_for_non_matching_string(self):
        with pytest.raises(TypeError):
            A.parse("b")

    def test_instantiation_returns_instance(self):
        s = "abc"
        assert s is A.parse(s)


class B(FullMatch, pattern=re.compile(r"abc")):
    ...


class TestFullMatch:
    def test_non_matching_string_is_not_instance(self):
        assert not isinstance("abcd", B)

    def test_matching_string_is_instance(self):
        assert isinstance("abc", B)

    def test_instantiation_raises_for_non_matching_string(self):
        with pytest.raises(TypeError):
            B.parse("b")

    def test_instantiation_returns_instance(self):
        s = "abc"
        assert s is B.parse(s)
