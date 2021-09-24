Getting Started
===============

Creating phantom types
----------------------

Phantom types are created by subclassing :class:`phantom.base.Phantom` and providing a
predicate function.

.. code-block:: python

    from phantom.base import Phantom

    # A boolean predicate that checks if a given string is a greeting. This function is
    # of type ``Predicate[str]`` as it requires its argument to be a ``str``.
    def is_greeting(instance: str) -> bool:
        return instance.startswith(("Hello", "Hi"))


    # Since our predicate requires its argument to be a ``str``, we must make the bound
    # of the phantom type ``str`` as well. We do that by making it it's first base. Any
    # base specified before Phantom is implicitly interpreted as its bound, unless an
    # explicit bound is specified as a class argument.
    class Greeting(str, Phantom, predicate=is_greeting):
        ...


    # Now we can make the same operations as with our previous example.
    hello = "Hello there"
    assert isinstance(hello, Greeting)
    hi = Greeting.parse("Hi there")

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

A motivating example
--------------------

Imagine that you're working on implementing a ``head()`` function that should return the
first item of any given iterable. You start out with a simple implementation:

.. code-block:: python

    def head(iterable: Iterable[T]) -> T:
        return next(iter(iterable))

You go ahead and use this function across your project, until suddenly you run into a
subtle issue that you didn't think of: this function raises ``StopIteration`` when
passed an empty iterable. In functional programming terms this is due to the function
being *partial* it specifies that it takes ``Iterable`` as argument, but in reality we
would need a narrower type to describe the set of valid arguments, and make the function
*total*.

You need to deal with the problem at hand so you go ahead and adjust all the call sites
of your function, and you now end up either asserting that the iterables are non-empty,
or catching the `StopIteration`.

.. code-block:: python

    items = get_values()
    if not len(items):
        return "empty"
    return f"first element is: {head(items)}"

This works, and you could move on like this from here, but, you have now introduced
shotgun parsing into your application, since further down the processing line you need
to check the length if the iterable for other purposes. Shotgun parsing is an
anti-pattern that results in a program state that is hard to predict and will very
likely lead to bugs down the line. So how should you deal with this?

Using phantom types you can use the builtin :class:`phantom.sized.NonEmpty` type.

.. code-block:: python

    def head(iterable: NonEmpty[T]) -> T:
        return next(iter(iterable))

The implementation is identical but you've now altered the signature of the function so
that it's total, it can deal with *all* values of its argument type without raising an
exception.

By using the narrower type at the call sites, you avoid shotgun parsing, since the other
logic further down in the processing chain can rely on the type as well, and you won't
need to check the length of the iterable again.

.. code-block:: python

    items = get_values()
    if not isinstance(items, NonEmpty):
        return "empty"
    return f"first element is: {head(items)}"

This strategy works in all places where a function works on a narrower type than you can
describe with the builtin types of Python, not only this made-up example. You can narrow
strings, integers, datetimes, and any other arbitrary types to completely rid of
duplicated validation throughout a code base.

There's a set of phantom types that ships builtin that are helpful to build on top of,
although you might mostly use your own custom phantom types that describe the exact
values that your implementations require.

Using predicates
----------------

The phantom-types library relies heavily on boolean predicates. A boolean predicate is
simply a function that takes a single argument and returns either ``True`` or ``False``.
While using boolean predicates is not necessary to create phantom types, building up a
library of types doing so allows reusing small and easily testable functions to create a
plethora of specialized types. Boolean predicates are usually easy to reason about as
they are pure functions with only two possible return values.

Studying the phantom types shipped in this library is recommended for gaining deeper
insight into how to implement more complicated types.
