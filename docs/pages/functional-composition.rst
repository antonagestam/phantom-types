Functional composition
======================

When composing predicates for phantom types it won't take long before you reach after
functional composition. Unfortunately, fully supporting a typed n-ary ``compose``
functions isn't yet feasible without shipping a custom mypy plugin. In lieu of having
that effort in place, a simpler but fully typed ``compose2`` function is shipped. The
door, however, is left wide open for the possibility of shipping an n-ary, generalized
compose function in the future.

.. automodule:: phantom.fn
    :members:
    :undoc-members:
    :show-inheritance:
