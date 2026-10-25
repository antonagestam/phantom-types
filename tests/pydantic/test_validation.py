import warnings
from typing import Any

import pytest
from pydantic import ConfigDict
from pydantic import TypeAdapter
from pydantic import ValidationError

from phantom import Phantom
from phantom._base import AbstractInstanceCheck
from phantom.datetime import TZAware
from phantom.interval import Interval
from phantom.interval import Natural
from phantom.negated import SequenceNotStr
from phantom.sized import NonEmpty

pytestmark = [pytest.mark.external]


class AbstractWithoutBound(Phantom[object], abstract=True): ...


class TestValidation:
    def test_decodes_input_into_bound(self):
        natural = TypeAdapter(Natural).validate_python(5.0)
        assert natural == 5
        assert type(natural) is int

    @pytest.mark.parametrize(
        ("type_", "value", "expected"),
        (
            (NonEmpty[int], [1, 2], (1, 2)),
            (NonEmpty[int], frozenset({1}), (1,)),
            (SequenceNotStr[int], [1, 2], (1, 2)),
        ),
    )
    def test_decodes_parametrized_iterable_into_tuple(
        self,
        type_: Any,
        value: object,
        expected: tuple[int, ...],
    ):
        assert TypeAdapter(type_).validate_python(value) == expected

    def test_decodes_json_array_into_sized_type(self):
        non_empty = TypeAdapter(NonEmpty[int])
        assert non_empty.validate_json("[1, 2]") == NonEmpty.parse((1, 2))

    def test_decodes_according_to_strict_mode(self):
        natural = TypeAdapter(Natural, config=ConfigDict(strict=True))

        with pytest.raises(ValidationError) as exception_info:
            natural.validate_python("5")

        (error,) = exception_info.value.errors()
        assert error["type"] == "int_type"

    def test_reports_decoding_error_from_pydantic(self):
        with pytest.raises(ValidationError) as exception_info:
            TypeAdapter(Natural).validate_python("five")

        (error,) = exception_info.value.errors()
        assert error["type"] == "int_parsing"

    def test_converts_type_error_from_parse_to_validation_error(self):
        with pytest.raises(ValidationError) as exception_info:
            TypeAdapter(NonEmpty[int]).validate_python(())

        (error,) = exception_info.value.errors()
        assert error["type"] == "type_error"
        assert error["msg"] == "Could not parse phantom.sized.NonEmpty from ()"

    @pytest.mark.parametrize("type_", (Interval, AbstractWithoutBound))
    def test_raises_for_abstract_type(self, type_: type):
        with pytest.raises(AbstractInstanceCheck):
            TypeAdapter(type_)


class TestSerialization:
    def test_serializes_validated_values_without_warnings(self):
        non_empty = TypeAdapter(NonEmpty[int])
        aware = TypeAdapter(TZAware)

        with warnings.catch_warnings():
            warnings.simplefilter("error")
            non_empty_value = non_empty.validate_python(frozenset({1}))
            aware_value = aware.validate_python("2026-10-25T00:00:00+00:00")
            assert non_empty.dump_json(non_empty_value) == b"[1]"
            assert aware.dump_json(aware_value) == b'"2026-10-25T00:00:00Z"'
