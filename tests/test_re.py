from __future__ import annotations

import re

import pytest

from phantom.re import FullMatch
from phantom.re import Match


class MatchPatternInstance(Match, pattern=re.compile(r"abc")):
    ...


class MatchPatternStr(Match, pattern=r"abc"):
    ...


parametrize_match = pytest.mark.parametrize(
    "match_type", (MatchPatternInstance, MatchPatternStr)
)


class TestMatch:
    @parametrize_match
    def test_non_matching_string_is_not_instance(self, match_type: type[Match]):
        assert not isinstance("abd", match_type)

    @parametrize_match
    def test_matching_string_is_instance(self, match_type: type[Match]):
        assert isinstance("abcd", match_type)

    @parametrize_match
    def test_instantiation_raises_for_non_matching_string(
        self, match_type: type[Match]
    ):
        with pytest.raises(TypeError):
            match_type.parse("b")

    @parametrize_match
    def test_instantiation_returns_instance(self, match_type: type[Match]):
        s = "abc"
        assert s is match_type.parse(s)


class FullMatchPatternInstance(FullMatch, pattern=re.compile(r"abc")):
    ...


class FullMatchStr(FullMatch, pattern=r"abc"):
    ...


parametrize_full_match = pytest.mark.parametrize(
    "full_match_type", (FullMatchPatternInstance, FullMatchStr)
)


class TestFullMatch:
    @parametrize_full_match
    def test_non_matching_string_is_not_instance(
        self, full_match_type: type[FullMatch]
    ):
        assert not isinstance("abcd", full_match_type)

    @parametrize_full_match
    def test_matching_string_is_instance(self, full_match_type: type[FullMatch]):
        assert isinstance("abc", full_match_type)

    @parametrize_full_match
    def test_instantiation_raises_for_non_matching_string(
        self, full_match_type: type[FullMatch]
    ):
        with pytest.raises(TypeError):
            full_match_type.parse("b")

    @parametrize_full_match
    def test_instantiation_returns_instance(self, full_match_type: type[FullMatch]):
        s = "abc"
        assert s is full_match_type.parse(s)
