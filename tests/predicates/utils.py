from phantom import Predicate


def assert_predicate_name_equals(predicate: Predicate, expected_name: str) -> None:
    assert predicate.__name__ == expected_name
    assert predicate.__qualname__ == expected_name
    assert repr(predicate).startswith(f"<function {expected_name} at ")
