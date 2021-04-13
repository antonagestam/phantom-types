Functional composition
======================

When composing predicates for phantom types it won't take long before you reach after
functional composition. Unfortunately, fully supporting a typed n-ary ``compose``
functions isn't yet feasible without shipping a custom mypy plugin. In lieu of having
that effort in place, a simpler but fully typed ``compose2`` function is shipped. The
door, however, is left wide open for the possibility of shipping an n-ary, generalized
compose function in the future.

``phantom.fn.*``

- ``compose2(a: Callable[[AA], AR], b: Callable[[BA], AA]) -> Callable[[BA], AR]``
  returns a function composed from the two given functions such that calling
  ``compose2(a, b)(x)`` is equivalent to calling ``a(b(x))``.
