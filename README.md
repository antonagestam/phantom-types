# phantom-types

[![](https://github.com/antonagestam/phantom-types/workflows/CI/badge.svg)][ci]

[ci]: https://github.com/antonagestam/phantom-types/actions?query=workflow%3ACI

Phantom types for Python.

_This project is in early development and major changes to core APIs should be expected.
Semantic versioning will be followed after version 1.0, but before that breaking changes
will happen between minor versions._

## Installation

```bash
python3 -m pip install phantom-types
```

## Abstract

- Make illegal states unrepresentable.
- [Parse, don't validate][parse].
- [Ghosts of Departed Proofs][ghosts].
- Abuse `__instancecheck__` and type-guards.
- Values are checked at runtime but no extra instances/subclasses are instantiated.
- Boolean predicate design is heavily inspired by [fthomas/refined][refined].

[parse]: https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/
[ghosts]: https://kataskeue.com/gdp.pdf
[refined]: https://github.com/fthomas/refined

## Usage

### Shipped phantom types

#### Boolean

Describes objects that coerce to either `True` or `False` when calling `bool()` on them.

- `phantom.boolean.Truthy`
- `phantom.boolean.Falsy`

#### Datetime

- `phantom.datetime.TZAware`
- `phantom.datetime.TZNaive`

#### Interval

Describes narrower sets of numbers than `int` and `float`.

##### Base classes

- `phantom.interval.Interval`
  - Takes class arguments `check: IntervalCheck`, `low: float` (defaults to negative
    infinity), and `high: float` (defaults to positive infinity). Expects concrete
    subtypes to specify their runtime type bound as first base.
- `phantom.interval.Open`, `(low, high)`
  - Uses `check=phantom.predicates.interval.open`.
- `phantom.interval.Closed`, `[low, high]`
  - Uses `check=phantom.predicates.interval.closed`.
- `phantom.interval.OpenClosed`, `(low, high]`
  - Uses `check=phantom.predicates.interval.open_closed`.
- `phantom.interval.ClosedOpen`, `[low, high)`
  - Uses `check=phantom.predicates.interval.closed_open`.

##### Implemented intervals

- `phantom.interval.Natural`, `(0, ∞)`
- `phantom.interval.NegativeInt`, `(-∞, 0)`
- `phantom.interval.Portion`, `(0, 1)`

#### Regular expressions

Takes `pattern: Pattern[str]` as class argument.

- `phantom.re.Match`, uses `phantom.predicates.re.is_match`.
- `phantom.re.FullMatch`, uses `phantom.predicates.re.is_full_match`.

#### Sized collections

Describes collections with size boundaries. These types should only be used with
immutable collections. There is a naive check that eliminates some of the most common
mutable collections in the instance check, however a guaranteed check is probably
impossible to implement, so developer discipline is required.

- `phantom.sized.PhantomSized[T]`, takes class argument `len: Predicate[float]`.
- `phantom.sized.NonEmpty[T]`, a sized collection with at least one item.
- `phantom.sized.Empty[T]`, an empty collection.

### Shipped predicates and factories

#### Bool

- `phantom.predicates.bool.true: Predicate[object]` always returns `True`.
- `phantom.predicates.bool.false: Predicate[object]` always returns `False`.
- `phantom.predicates.bool.negate(p: Predicate[T]) -> Predicate[T]` negates a given
  predicate.
- `phantom.predicates.bool.truthy: Predicate[object]` returns `True` for truthy objects.
- `phantom.predicates.bool.falsy: Predicate[object]` returns `True` for falsy objects.
- `phantom.predicates.bool.both(p: Predicate[T], q: Predicate[T]) -> Predicate[T]`
  creates a new predicate that succeeds when both of the given predicates succeed.
- `phantom.predicates.bool.all_of(predicates: Iterable[Predicate[T]]) -> Predicate[T]`
  creates a new predicate that succeeds when all of the given predicates succeed.
- `phantom.predicates.bool.any_of(predicates: Iterable[Predicate[T]] -> Predicate[T]`
  creates a new predicate that succeeds when at least one of the given predicates
  succeed.

#### Collection

- `phantom.predicates.collection.contains(value: object) -> Predicate[Container]`
  creates a new predicate that succeeds when its argument contains `value`.
- `phantom.predicates.collection.contained(container: Container) -> Predicate[object]`
  creates a new predicate that succeeds when its argument is contained by `container`.
- `phantom.predicates.collection.count(predicate: Predicate[int]) -> Predicate[Sized]`
  creates a predicate that succeeds when the size of its argument satisfies the given
  `predicate`.
- `phantom.predicates.collection.exists(predicate: Predicate[object]) -> Predicate[Iterable]`
  creates a predicate that succeeds when one or more items in its argument satisfies
  `predicate`.

#### Datetime

- `phantom.predicates.datetime.is_tz_aware: Predicate[datetime.datetime]` succeeds if
  its argument is timezone aware.
- `phantom.predicates.datetime.is_tz_naive: Predicate[datetime.datetime]` succeeds if
  its argument is timezone naive.

#### Generic

- `phantom.predicates.generic.equal(a: object) -> Predicate[object]` creates a new
  predicate that succeeds when its argument is equal to `a`.
- `phantom.predicates.generic.identical(a: object) -> Predicate[object]` creates a new
  predicate that succeeds when its argument is identical to `a`.
- `phantom.predicates.generic.of_type(t: Union[Type, Tuple[Type, ...]]) -> Predicate[object]`
  creates a new predicate that succeeds when its argument is an instance of `t`.

#### Interval

See corresponding shipped phantom types. Creates new predicates that succeed when their
argument is strictly or non strictly between the upper and lower bounds.

- `phantom.predicates.interval.open(low: float, high: float) -> Predicate[float]`
- `phantom.predicates.interval.open_closed(low: float, high: float) -> Predicate[float]`
- `phantom.predicates.interval.closed_open(low: float, high: float) -> Predicate[float]`
- `phantom.predicates.interval.closed(low: float, high: float) -> Predicate[float]`

#### Numeric

- `phantom.predicates.numeric.less(n: float) -> Predicate[float]` creates a new
  predicate that succeeds when its argument is strictly less than `n`.
- `phantom.predicates.numeric.le(n: float) -> Predicate[float]` creates a new predicate
  that succeeds when its argument is less than or equal to `n`.
- `phantom.predicates.numeric.greater(n: float) -> Predicate[float]` creates a new
  predicate that succeeds when its argument is strictly greater than `n`.
- `phantom.predicates.numeric.ge(n: float) -> Predicate[float]` creates a new predicate
  that succeeds when its argument is greater than or equal to `n`.
- `phantom.predicates.numeric.positive: Predicate[float]` succeeds when its argument is
  strictly greater than zero.
- `phantom.predicates.numeric.non_positive: Predicate[float]` succeeds when its argument
  is less than or equal to zero.
- `phantom.predicates.numeric.negative: Predicate[float]` succeeds when its argument is
  strictly less than zero.
- `phantom.predicates.numeric.non_negative: Predicate[float]` succeeds when its argument
  is greater than or equal to zero.
- `phantom.predicates.numeric.modulo(n: float, p: Predicate[float]) -> Predicate[float]`
  creates a new predicate that succeeds when its argument modulo `n` satisfies the given
  predicate `p`.
- `phantom.predicates.numeric.even: Predicate[int]` succeeds when its argument is even.
- `phantom.predicates.numeric.odd: Predicate[int]` succeeds when its argument is odd.

#### Regular Expressions

- `phantom.predicates.re.is_match(pattern: Pattern[str]) -> Predicate[str]` creates a
  new predicate that succeeds when the start of its argument matches the given
  `pattern`.
- `phantom.predicates.re.is_full_match(pattern: Pattern[str]) -> Predicate[str]` creates
  a new predicate that succeeds when its whole argument matches the given `pattern`.

### External Wrappers

A collection of phantom types that wraps functionality of well maintained
implementations of third-party validation libraries. Importing from `phantom.ext.*` is a
hint that more dependencies need to be installed.

#### Phone numbers

Requires the [phonenumbers] package which can be installed with:

[phonenumbers]: https://pypi.org/project/phonenumbers/

```bash
pip install phantom-types[phonenumbers]
```

##### Types

- `phantom.ext.phonenumbers.PhoneNumber`
- `phantom.ext.phonenumbers.FormattedPhoneNumber`
  - `FormattedPhoneNumber.parse()` normalizes numbers using
    `phonenumbers.PhoneNumberFormat.E164` and might raise `InvalidPhoneNumber`.

##### Functions

- `phantom.ext.phonenumbers.is_phone_number: Predicate[str]`
- `phantom.ext.phonenumbers.is_formatted_phone_number: Predicate[str]`
- `phantom.ext.phonenumbers.normalize_phone_number(phone_number: str, country_code: Optional[str]=None) -> FormattedPhoneNumber`
  normalizes numbers using `phonenumbers.PhoneNumberFormat.E164` and might raise
  `InvalidPhoneNumber`.

##### Exceptions

- `phantom.ext.phonenumbers.InvalidPhoneNumber`

#### Country codes

Requires the [iso3166] package which can be installed with:

[iso3166]: https://pypi.org/project/iso3166/

```bash
pip install phantom-types[iso3166]
```

##### Types

- `phantom.ext.iso3166.Alpha2`
  - `Alpha2.parse()` normalizes mixed case codes.
- `phantom.ext.iso3166.CountryCode` alias of `Alpha2`

##### Functions

- `phantom.ext.iso3166.normalize_alpha2_country_code(country_code: str) -> Alpha2`
  normalizes mixed case country codes and might raise `InvalidCountryCode`.

##### Exceptions

- `phantom.ext.iso3166.InvalidCountryCode`

### Creating phantom types

Phantom types are created by subclassing `phantom.base.Phantom` and defining an
`__instancecheck__` method:

```python
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
```

Checkout out the [dacite example][dacite-example] for how to create dataclasses with
rich phantom-typed fields without duplicating type definitions or losing parsed
information.

[dacite-example]: examples/dacite/dacite_example.py

### Using predicates

Most of the shipped phantom types are implemented using boolean predicates. A boolean
predicate is simply a function that takes a single argument and returns either `True` or
`False`. While using boolean predicates is not necessary to use phantom types, building
up a library of types doing so allows reusing small and easily testable functions to
create a plethora of specialized types. Boolean predicates are usually easy to reason
about as they are pure functions with only two possible return values.

Studying the phantom types shipped in this library is recommended for gaining deeper
insight into how to implement more complicated types.

Now, looking at the example we implemented by subclassing `Phantom` and providing an
`__instancecheck__` method, let's try and achieve the same using predicates. The
`PredicateType` class already implements an `__instancecheck__` method and will usually
reduce the amount of boilerplate required.

```python
from phantom.base import Phantom


# A boolean predicate that checks if a given string is a greeting. This function is of
# type `Predicate[str]` as it requires its argument to be a `str`.
def is_greeting(instance: str) -> bool:
    return instance.startswith(("Hello", "Hi"))


# Since our predicate requires its argument to be a `str`, we must make the bound of the
# phantom type `str` as well. We do that by making it it's first base. Any base
# specified before Phantom is implicitly interpreted as its bound, unless an explicit
# bound is specificed as a class argument.
class Greeting(str, Phantom, predicate=is_greeting):
    ...


# Now we can make the same operations as with our previous example.
hello = "Hello there"
assert isinstance(hello, Greeting)
hi = Greeting.parse("Hi there")
```

As you can see, in addition to having less boilerplate than the previous example, this
style also has the added benefit of separating out business logic into simple reusable
functions.
