from typing import Iterable

import pytest

from phantom.base import Predicate
from phantom.predicates import boolean


class TestTrue:
    @pytest.mark.parametrize("value", [0, False, 1, "test", ()])
    def test_returns_true_for_any_given_value(self, value: object) -> None:
        assert boolean.true(value) is True


class TestFalse:
    @pytest.mark.parametrize("value", [0, False, 1, "test", ()])
    def test_returns_false_for_any_given_value(self, value: object) -> None:
        assert boolean.false(value) is False


parametrize_truthy = pytest.mark.parametrize("value", [1, "a", (0,), [""], True])
parametrize_falsy = pytest.mark.parametrize("value", [0, "", (), [], False])


class TestTruthy:
    @parametrize_truthy
    def test_returns_true_for_truthy_value(self, value: object) -> None:
        assert boolean.truthy(value) is True

    @parametrize_falsy
    def test_returns_false_for_falsy_value(self, value: object) -> None:
        assert boolean.truthy(value) is False


class TestFalsy:
    @parametrize_falsy
    def test_returns_true_for_falsy_value(self, value: object) -> None:
        assert boolean.falsy(value) is True

    @parametrize_truthy
    def test_returns_false_for_truthy_value(self, value: object) -> None:
        assert boolean.falsy(value) is False


class TestBoth:
    def test_returns_true_for_two_succeeding_predicates(self) -> None:
        assert boolean.both(boolean.true, boolean.true)(0) is True

    @pytest.mark.parametrize(
        "a, b",
        [
            (boolean.false, boolean.true),
            (boolean.true, boolean.false),
            (boolean.false, boolean.false),
        ],
    )
    def test_returns_false_for_falsy_predicate(
        self, a: Predicate, b: Predicate
    ) -> None:
        assert boolean.both(a, b)(0) is False


class TestEither:
    @pytest.mark.parametrize(
        "a, b",
        [
            (boolean.false, boolean.true),
            (boolean.true, boolean.false),
            (boolean.true, boolean.true),
        ],
    )
    def test_returns_true_for_truthy_predicate(
        self, a: Predicate, b: Predicate
    ) -> None:
        assert boolean.either(a, b)(0) is True

    def test_returns_false_for_two_falsy_predicates(self) -> None:
        assert boolean.either(boolean.false, boolean.false)(0) is False


class TestXor:
    @pytest.mark.parametrize(
        "a, b",
        [
            (boolean.false, boolean.true),
            (boolean.true, boolean.false),
        ],
    )
    def test_returns_true_for_two_different_bools(
        self, a: Predicate, b: Predicate
    ) -> None:
        assert boolean.xor(a, b)(0) is True

    @pytest.mark.parametrize(
        "a, b",
        [
            (boolean.false, boolean.false),
            (boolean.true, boolean.true),
        ],
    )
    def test_returns_false_for_two_equal_bools(
        self, a: Predicate, b: Predicate
    ) -> None:
        assert boolean.xor(a, b)(0) is False


parametrize_all_true = pytest.mark.parametrize(
    "predicates",
    [
        (boolean.true,),
        (boolean.true, boolean.true),
        (boolean.true, boolean.true, boolean.true),
    ],
)
parametrize_some_false = pytest.mark.parametrize(
    "predicates",
    [
        (boolean.true, boolean.false),
        (boolean.false, boolean.true),
        (boolean.true, boolean.false, boolean.true),
    ],
)
parametrize_all_false = pytest.mark.parametrize(
    "predicates",
    [
        (boolean.false,),
        (boolean.false, boolean.false),
        (boolean.false, boolean.false, boolean.false),
    ],
)


class TestAllOf:
    def test_returns_true_for_empty_set_of_predicates(self) -> None:
        predicate: Predicate[int] = boolean.all_of(())
        assert predicate(0) is True

    @parametrize_all_true
    def test_returns_true_for_succeeding_predicates(
        self, predicates: Iterable[Predicate]
    ) -> None:
        assert boolean.all_of(predicates)(0) is True

    @parametrize_some_false
    def test_returns_false_for_some_failing_predicate(
        self, predicates: Iterable[Predicate]
    ) -> None:
        assert boolean.all_of(predicates)(0) is False

    @parametrize_all_false
    def test_returns_false_for_only_failing_predicate(
        self, predicates: Iterable[Predicate]
    ) -> None:
        assert boolean.all_of(predicates)(0) is False

    @parametrize_some_false
    def test_materializes_generated_predicates(
        self, predicates: Iterable[Predicate]
    ) -> None:
        predicate = boolean.all_of(predicate for predicate in predicates)
        assert predicate(0) is False
        assert predicate(0) is False


class TestAnyOf:
    def test_returns_false_for_empty_set_of_predicates(self) -> None:
        predicate: Predicate[int] = boolean.any_of(())
        assert predicate(0) is False

    @parametrize_all_true
    def test_returns_true_for_succeeding_predicates(
        self, predicates: Iterable[Predicate]
    ) -> None:
        assert boolean.any_of(predicates)(0) is True

    @parametrize_some_false
    def test_returns_true_for_some_failing_predicate(
        self, predicates: Iterable[Predicate]
    ) -> None:
        assert boolean.any_of(predicates)(0) is True

    @parametrize_all_false
    def test_returns_false_for_only_failing_predicate(
        self, predicates: Iterable[Predicate]
    ) -> None:
        assert boolean.any_of(predicates)(0) is False

    @parametrize_some_false
    def test_materializes_generated_predicates(
        self, predicates: Iterable[Predicate]
    ) -> None:
        predicate = boolean.any_of(predicate for predicate in predicates)
        assert predicate(0) is True
        assert predicate(0) is True


class TestOneOf:
    def test_returns_false_for_empty_set_of_predicates(self) -> None:
        predicate: Predicate[int] = boolean.one_of(())
        assert predicate(0) is False

    @pytest.mark.parametrize(
        "predicates",
        [
            (boolean.true, boolean.true),
            (boolean.true, boolean.true, boolean.true),
            (boolean.false, boolean.true, boolean.true),
            (boolean.true, boolean.true, boolean.false),
            (boolean.true, boolean.false, boolean.true),
        ],
    )
    def test_returns_false_for_more_than_one_succeeding_predicates(
        self, predicates: Iterable[Predicate]
    ) -> None:
        assert boolean.one_of(predicates)(0) is False

    @pytest.mark.parametrize(
        "predicates",
        [
            (boolean.true,),
            (boolean.true, boolean.false),
            (boolean.false, boolean.true),
            (boolean.true, boolean.false, boolean.false),
            (boolean.false, boolean.true, boolean.false),
            (boolean.false, boolean.false, boolean.true),
        ],
    )
    def test_returns_true_for_one_succeeding_predicate(
        self, predicates: Iterable[Predicate]
    ) -> None:
        assert boolean.one_of(predicates)(0) is True

    @parametrize_all_false
    def test_returns_false_for_only_failing_predicate(
        self, predicates: Iterable[Predicate]
    ) -> None:
        assert boolean.one_of(predicates)(0) is False

    @pytest.mark.parametrize(
        "predicates",
        [
            (boolean.true,),
            (boolean.false, boolean.true),
            (boolean.false, boolean.true, boolean.false),
        ],
    )
    def test_materializes_generated_predicates(
        self, predicates: Iterable[Predicate]
    ) -> None:
        predicate = boolean.one_of(predicate for predicate in predicates)
        assert predicate(0) is True
        assert predicate(0) is True
