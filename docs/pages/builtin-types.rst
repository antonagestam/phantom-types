Builtin types
=============

Boolean
-------

``phantom.boolean.*``

Types describing objects that coerce to either ``True`` or ``False`` respectively when
calling ``bool()`` on them.

* ``Truthy``
* ``Falsy``

Datetime
--------

``phantom.datetime.*``

* ``TZAware``
* ``TZNaive``

.. _numeric-interval-types:

Numeric intervals
-----------------

``phantom.interval.*``

Types describing narrower sets of numbers than ``int`` and ``float``.

Base classes
^^^^^^^^^^^^

All the interval types subclass from ``Interval`` which provides the following class
arguments.

* ``check: IntervalCheck``
* ``low: float`` (defaults to negative infinity)
* ``high: float`` (defaults to positive infinity)

Concrete subclasses must specify their runtime type bound as their first base. :ref:`See
corresponding predicate functions<numeric-interval-predicates>`.

* ``Interval``
* ``Open``
* ``Closed``
* ``OpenClosed``
* ``ClosedOpen``

Concrete intervals
^^^^^^^^^^^^^^^^^^

* ``Natural``, ``(0, ∞)``
* ``NegativeInt``, ``(-∞, 0)``
* ``Portion``, ``(0, 1)``

Regular expressions
-------------------

``phantom.re.*``

Takes ``pattern: Pattern[str]`` as class argument. :ref:`See corresponding predicate
functions<regular-expression-predicates>`.

* ``Match``, uses ``phantom.predicates.re.is_match``.
* ``FullMatch``, uses ``phantom.predicates.re.is_full_match``.

Sized collections
-----------------

``phantom.sized.*``

Types describing collections with size boundaries. These types should only be used with
immutable collections. There is a naive check that eliminates some of the most common
mutable collections in the instance check, however a guaranteed check is probably
impossible to implement, so some amount of developer discipline is required.

* ``PhantomSized[T]``, takes class argument ``len: Predicate[float]``.
* ``NonEmpty[T]``, a sized collection with at least one item.
* ``Empty[T]``, an empty collection.

Sized types are created by subclassing ``PhantomSized`` and providing a predicate that
will be called with the size of the tested collection. For instance, ``NonEmpty`` is
implemented using ``len=numeric.greater(0)``.
