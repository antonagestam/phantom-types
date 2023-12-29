.. _composing:

Composing types
***************

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
implicitly by base classes, or implicitly inheritance, e.g.:

.. code-block:: python

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
~~~~~~~~~~~~~~~

It's sometimes useful to create base classes without specifying a bound type. To do so
the class can be made abstract by passing ``abstract=True`` as a class argument:

.. code-block:: python

    class Base(Phantom, abstract=True):
        ...


    class Concrete(str, Base):
        ...

This is for instance used by the shipped
:ref:`numeric interval types <numeric-intervals>`.

Bound erasure
~~~~~~~~~~~~~

If a phantom type doesn't properly specify its bounds, in addition to risking passing
invalid arguments to its predicate function, it is also likely that a static type
checker might inadvertently erase the runtime type when type guarding.

As an example, this code will error on the access to ``dt.year`` because
``UTCDateTime.parse()`` has made the type checker erase the knowledge that dt is a
``datetime``.

.. code-block:: python

    class UTCDateTime(Phantom, predicate=is_utc):
        ...


    dt = UTCDateTime.parse(now())
    dt.year  # Error!

In this example we could remedy this by adding ``datetime`` as a base class and bound.

.. code-block:: python

    class UTCDateTime(datetime.datetime, Phantom, predicate=is_utc):
        ...

Mutability
==========

Phantom types are completely incompatible with mutable data and should never be used to
narrow a mutable type. The reason is that there is no way for a type checker to detect
that a mutation changes an object to no longer satisfy the predicate of a phantom
type. For example:

.. code-block:: python

    class Mutable:
        def __init__(self, len: int):
            self.len = len

        def __len__(self) -> int:
            return self.len


    # A phantom type that checks that a list has more than 2 items.
    class HasMany(Mutable, Phantom, predicate=count(greater(2))):
        ...


    # The check will pass because the instantiated object *currently* satisfies the
    # predicate, e.g. has len() > 2.
    instance = HasMany.parse(Mutable(3))

    # But! The object is mutable, so nothing is stopping us from altering it's length.
    # At this point the object will no longer satisfy the HasMany predicate.
    instance.len = 2

    # There is no way for a type checker to know that the predicate isn't fulfilled
    # anymore, so the revealed type here will still be HasMany.
    reveal_type(instance)  # Revealed type is HasMany

When subclassing from :py:class:`Phantom <phantom.Phantom>`, a check is made that raises
:py:class:`MutableType <phantom.utils.MutableType>` for known mutable types, such as
:py:class:`list`, :py:class:`set`, :py:class:`dict` and unfrozen dataclasses. In the
general case though, it isn't possible to detect mutability and so it's up to
developer discipline to make sure not to mix mutable data types with phantom types.

Metaclass conflicts
===================

Phantom types are implemented using a metaclass. When creating a phantom type that
narrows on a type that also uses a metaclass it's common to stumble into a metaclass
conflict. The usual solution to such situation is to create a new metaclass that
inherits both existing metaclasses and base the new type on it.

.. code-block:: python

    from phantom import PhantomMeta


    class NewMeta(PhantomMeta, OldMeta):
        ...


    class New(Old, Phantom, metaclass=NewMeta):
        ...
