Getting Started
===============

Creating phantom types
----------------------

Phantom types are created by subclassing ``phantom.base.Phantom`` and defining an
``__instancecheck__`` method:

.. code-block:: python

    from typing import Any
    from typing import TYPE_CHECKING

    from phantom.base import PhantomBase

    class Greeting(PhantomBase):
        @classmethod
        def __instancecheck__(cls, instance: Any) -> bool:
            return (
                isinstance(instance, str)
                and instance.startswith(("Hello", "Hi"))
            )

    hello = "Hello there"
    # We can narrow types using mypy's type guards
    assert isinstance(hello, Greeting)
    # or explicitly when we need to
    hi = Greeting.parse("Hi there")

    # The runtime types are unchanged and will still be str for our greetings
    assert type(hello) is str
    assert type(hi) is str

    # But their static types will be Greeting, retaining the information that our
    # strings are not just any strs
    if TYPE_CHECKING:
        reveal_type(hello)
        reveal_type(hi)

    # As this string doesn't fulfill our __instancecheck__, it will not be an
    # instance of Greeting.
    assert not isinstance("Goodbye", Greeting)

Checkout out the [dacite example][dacite-example] for how to create dataclasses with
rich phantom-typed fields without duplicating type definitions or losing parsed
information.

[dacite-example]: examples/dacite/dacite_example.py

Using predicates
----------------

Most of the shipped phantom types are implemented using boolean predicates. A boolean
predicate is simply a function that takes a single argument and returns either ``True`` or
``False``. While using boolean predicates is not necessary to use phantom types, building
up a library of types doing so allows reusing small and easily testable functions to
create a plethora of specialized types. Boolean predicates are usually easy to reason
about as they are pure functions with only two possible return values.

Studying the phantom types shipped in this library is recommended for gaining deeper
insight into how to implement more complicated types.

Now, looking at the example we implemented by subclassing ``Phantom`` and providing an
``__instancecheck__`` method, let's try and achieve the same using predicates. The
``PredicateType`` class already implements an ``__instancecheck__`` method and will usually
reduce the amount of boilerplate required.

.. code-block:: python

    from phantom.base import Phantom

    # A boolean predicate that checks if a given string is a greeting. This function is of
    # type ``Predicate[str]`` as it requires its argument to be a ``str``.
    def is_greeting(instance: str) -> bool:
        return instance.startswith(("Hello", "Hi"))

    # Since our predicate requires its argument to be a ``str``, we must make the bound of the
    # phantom type ``str`` as well. We do that by making it it's first base. Any base
    # specified before Phantom is implicitly interpreted as its bound, unless an explicit
    # bound is specificed as a class argument.
    class Greeting(str, Phantom, predicate=is_greeting):
        ...

    # Now we can make the same operations as with our previous example.
    hello = "Hello there"
    assert isinstance(hello, Greeting)
    hi = Greeting.parse("Hi there")

As you can see, in addition to having less boilerplate than the previous example, this
style also has the added benefit of separating out business logic into simple reusable
functions.
