from phantom.base import Predicate


def equal(a: object) -> Predicate[object]:
    def compare(b: object) -> bool:
        return a == b

    return compare


def identical(a: object) -> Predicate[object]:
    def compare(b: object) -> bool:
        return a is b

    return compare
