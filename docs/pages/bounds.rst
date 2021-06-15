Bounds
======

The bound of a phantom type is the type that its values will have at runtime, so when
checking if a value is an instance of a phantom type, it's first checked to be within
its bounds, so that the value can be safely passed as argument to the predicate
function of the type.

When subclassing, the bound of the new type must be a subtype of the bound of the super
class.

The bound of a phantom type is exposed as :attr:`phantom.Phantom.__bound__` for
introspection.

Resolution order
~~~~~~~~~~~~~~~~

The bound of a phantom type is resolved in the order: explicitly by class argument,
implicitly by base classes, or implicitly inheritance, e.g.::

    # Resolved by an explicit class arg:
    class A(Phantom, bound=str, predicate=...):
        ...

    # Resolved implicitly as any base classes before Phantom:
    class B(str, Phantom, predicate=...):
        ...

    # Resolves to str by inheritance from B:
    class C(B):
        ...

Abstract bounds
^^^^^^^^^^^^^^^

It's sometimes useful to create base classes without specifying a bound type. To do so
the class can be made abstract by passing ``abstract=True`` as a class argument::

    class Base(Phantom, abstract=True):
        ...

    class Concrete(str, Base):
        ...

This is for instance used by the shipped
:ref:`numeric interval types <numeric-intervals>`.

Bound erasure
^^^^^^^^^^^^^

If a phantom type doesn't properly specify its bounds, in addition to risking passing
invalid arguments to its predicate function, it is also likely that a static type
checker might inadvertently erase the runtime type when type guarding.

As an example, this code will error on the access to ``dt.year`` because
``UTCDateTime.parse()`` has made the type checker erase the knowledge that dt is a
``datetime``.

::

    class UTCDateTime(Phantom, predicate=is_utc):
        ...

    dt = UTCDateTime.parse(now())
    dt.year  # Error!

In this example we could remedy this by adding ``datetime`` as a base class and bound.

::

    class UTCDateTime(datetime.datetime, Phantom, predicate=is_utc):
        ...
