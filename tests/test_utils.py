from typing import Union

import pytest

from phantom.utils import BoundType
from phantom.utils import is_subtype


class A:
    ...


class B:
    ...


class C:
    ...


class AAndB(A, B):
    ...


class SubOfA(A):
    ...


class TestIsSubtype:
    # The cases are annotated with the numbered cases in the docstring of the function.
    @pytest.mark.parametrize(
        "a, b",
        [
            # 1
            (Union[int, float], Union[int, float]),
            # 2
            (int, Union[int, float]),
            # Special case of 3
            (Union[int], int),
            # 4
            (AAndB, (A, B)),
            (AAndB, (A,)),
            # 5
            ((B, SubOfA), A),
            # 6
            ((SubOfA, C), Union[A, B]),
            # Special case of 7
            (Union[int], (int,)),
            # 8
            ((AAndB, SubOfA), (A, B)),
            # 9
            (SubOfA, A),
        ],
    )
    def test_returns_true_for_valid_subtype(self, a: BoundType, b: BoundType) -> None:
        assert is_subtype(a, b) is True

    # The cases are annotated with the numbered cases in the docstring of the function.
    @pytest.mark.parametrize(
        "a, b",
        [
            # 1
            (Union[int, float], Union[int]),
            (Union[int, float], Union[A, B]),
            # 2
            (str, Union[int, float]),
            # 3
            (Union[int, float], float),
            # 4
            (SubOfA, (A, B)),
            (SubOfA, (B,)),
            # 5
            ((A, B), SubOfA),
            # 6
            ((int, C), Union[A, B]),
            # 7
            (Union[int, float], (int, float)),
            # 8
            ((AAndB, SubOfA), (A, B, C)),
            # 9
            (SubOfA, B),
            (A, B),
        ],
    )
    def test_returns_false_for_valid_subtype(self, a: BoundType, b: BoundType) -> None:
        assert is_subtype(a, b) is False
