Functional composition
======================

When composing predicates for phantom types it won't take long before you reach after
functional composition.

``phantom.fn.*``

- ``compose2(a: Callable[[AA], AR], b: Callable[[BA], AA]) -> Callable[[BA], AR]``
  returns a function composed from the two given functions such that calling
  ``compose2(a, b)(x)`` is equivalent to calling ``a(b(x))``.
