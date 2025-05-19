from typing import Union

import pytest

from phantom._utils.misc import BoundType
from phantom._utils.misc import is_subtype


class A: ...


class B: ...


class C: ...


class AAndB(A, B): ...


class SubOfA(A): ...


class TestIsSubtype:
    # The cases are annotated with the numbered cases in the docstring of the function.
    @pytest.mark.parametrize(
        "a, b",
        [
            # 1
            (int | float, int | float),
            # 2
            (int, int | float),
            # Special case of 3
            (Union[int], int),  # noqa: UP007
            # 4
            (AAndB, (A, B)),
            (AAndB, (A,)),
            # 5
            ((B, SubOfA), A),
            # 6
            ((SubOfA, C), A | B),
            # Special case of 7
            (Union[int], (int,)),  # noqa: UP007
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
            (int | float, Union[int]),  # noqa: UP007
            (int | float, A | B),
            # 2
            (str, int | float),
            # 3
            (int | float, float),
            # 4
            (SubOfA, (A, B)),
            (SubOfA, (B,)),
            # 5
            ((A, B), SubOfA),
            # 6
            ((int, C), A | B),
            # 7
            (int | float, (int, float)),
            # 8
            ((AAndB, SubOfA), (A, B, C)),
            # 9
            (SubOfA, B),
            (A, B),
        ],
    )
    def test_returns_false_for_valid_subtype(self, a: BoundType, b: BoundType) -> None:
        assert is_subtype(a, b) is False
