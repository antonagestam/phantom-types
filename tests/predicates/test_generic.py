import pytest

from phantom.predicates import generic


class TestEqual:
    @pytest.mark.parametrize("a,b", [(1, 1.0), (False, 0), (True, 1)])
    def test_returns_true_for_equal_values(self, a: object, b: object) -> None:
        assert generic.equal(a)(b)
        assert generic.equal(b)(a)

    # @pytest.mark.parametrize("a,b", [(2,1), (1,1.1), (True, False)])
    # def test_returns_false_for_non_equal_values(self, a: object, b: object) -> None:
    #     assert not generic.equal(a)(b)
    #     assert not generic.equal(b)(a)
