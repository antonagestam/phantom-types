from .base import Predicate


def open(low: float, high: float) -> Predicate[float]:
    def check(value: float) -> bool:
        return low <= value <= high

    return check


def open_closed(low: float, high: float) -> Predicate[float]:
    def check(value: float) -> bool:
        return low <= value < high

    return check


def closed_open(low: float, high: float) -> Predicate[float]:
    def check(value: float) -> bool:
        return low < value <= high

    return check


def closed(low: float, high: float) -> Predicate[float]:
    def check(value: float) -> bool:
        return low < value < high

    return check
