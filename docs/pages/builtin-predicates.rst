Builtin predicates and factories
================================

Boolean logic
-------------

``phantom.predicates.boolean.*``


* ``true: Predicate[object]`` always returns ``True``.
* ``false: Predicate[object]`` always returns ``False``.
* ``negate(p: Predicate[T]) -> Predicate[T]`` negates a given predicate.
* ``truthy: Predicate[object]`` returns ``True`` for truthy objects.
* ``falsy: Predicate[object]`` returns ``True`` for falsy objects.
* ``both(p: Predicate[T], q: Predicate[T]) -> Predicate[T]`` creates a new predicate
  that succeeds when both of the given predicates succeed.
* ``all_of(predicates: Iterable[Predicate[T]]) -> Predicate[T]`` creates a new predicate
  that succeeds when all of the given predicates succeed.
* ``any_of(predicates: Iterable[Predicate[T]] -> Predicate[T]`` creates a new predicate
  that succeeds when at least one of the given predicates succeed.

Collection
----------

``phantom.predicates.collection.*``

* `contains(value: object) -> Predicate[Container]`` creates a new predicate that
  succeeds when its argument contains ``value``.
* ``contained(container: Container) -> Predicate[object]`` creates a new predicate that
  succeeds when its argument is contained by ``container``.
* ``count(predicate: Predicate[int]) -> Predicate[Sized]`` creates a predicate that
  succeeds when the size of its argument satisfies the given ``predicate``.
* ``exists(predicate: Predicate[object]) -> Predicate[Iterable]`` creates a predicate
  that succeeds when one or more items in its argument satisfies ``predicate``.
* ``every(predicate: Predicate[object]) -> Predicate[Iterable]`` creates a predicate
  that succeeds when all items in its argument satisfy ``predicate``.

Datetime
--------

``phantom.predicates.datetime.*``

* ``is_tz_aware: Predicate[datetime.datetime]`` succeeds if its argument is timezone
  aware.
* ``is_tz_naive: Predicate[datetime.datetime]`` succeeds if its argument is timezone
  naive.

Generic
-------

``phantom.predicates.generic.*``

* ``equal(a: object) -> Predicate[object]`` creates a new predicate that succeeds when
  its argument is equal to ``a``.
* ``identical(a: object) -> Predicate[object]`` creates a new predicate that succeeds
  when its argument is identical to ``a``.
* ``of_type(t: Union[Type, Tuple[Type, ...]]) -> Predicate[object]`` creates a new
  predicate that succeeds when its argument is an instance of ``t``.

.. _numeric-interval-predicates:

Numeric intervals
-----------------

``phantom.predicates.interval.*``

Creates new predicates that succeed when their argument is strictly or non strictly
between the upper and lower bounds. :ref:`See corresponding shipped phantom
types<numeric-interval-types>`.

* ``open(low: float, high: float) -> Predicate[float]``
* ``open_closed(low: float, high: float) -> Predicate[float]``
* ``closed_open(low: float, high: float) -> Predicate[float]``
* ``closed(low: float, high: float) -> Predicate[float]``

Numeric
-------

``phantom.predicates.numeric.*``

* ``less(n: float) -> Predicate[float]`` creates a new predicate that succeeds when its
  argument is strictly less than ``n``.
* ``le(n: float) -> Predicate[float]`` creates a new predicate that succeeds when its
  argument is less than or equal to ``n``.
* ``greater(n: float) -> Predicate[float]`` creates a new predicate that succeeds when
  its argument is strictly greater than ``n``.
* ``ge(n: float) -> Predicate[float]`` creates a new predicate that succeeds when its
  argument is greater than or equal to ``n``.
* ``positive: Predicate[float]`` succeeds when its argument is strictly greater than
  zero.
* ``non_positive: Predicate[float]`` succeeds when its argument is less than or equal to
  zero.
* ``negative: Predicate[float]`` succeeds when its argument is strictly less than zero.
* ``non_negative: Predicate[float]`` succeeds when its argument is greater than or equal
  to zero.
* ``modulo(n: float, p: Predicate[float]) -> Predicate[float]`` creates a new predicate
  that succeeds when its argument modulo ``n`` satisfies the given predicate ``p``.
* ``even: Predicate[int]`` succeeds when its argument is even.
* ``odd: Predicate[int]`` succeeds when its argument is odd.

.. _regular-expression-predicates:

Regular expressions
-------------------

``phantom.predicates.re.*``

* ``is_match(pattern: Pattern[str]) -> Predicate[str]`` creates a new predicate that
  succeeds when the start of its argument matches the given ``pattern``.
* ``is_full_match(pattern: Pattern[str]) -> Predicate[str]`` creates a new predicate
  that succeeds when its whole argument matches the given ``pattern``.

