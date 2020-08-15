def is_truthy(value: object) -> bool:
    """
    >>> is_truthy([1])
    True
    >>> is_truthy([])
    False
    """
    return bool(value)


def is_falsy(value: object) -> bool:
    """
    >>> is_falsy([])
    True
    >>> is_falsy([1])
    False
    """
    return not value
