Implementation
==============

How are phantom types implemented?
----------------------------------

phantom-types make use of Python's ``__instancecheck__`` protocol to make types work
with the same checks that are recognized as type guards by static type checkers, e.g.
``isinstance()``. Phantom types are never instantiated at runtime and so will not add
any processing-, or memory overhead. Instead the question of whether a value is properly
parsed before it is processed is deferred to the static type checker.

The choice to design the library around boolean predicates, and the fact that much of
the initially shipped builtin types use predicates, are heavily inspired by the
`fthomas/refined <https://github.com/fthomas/refined>`_ library.
