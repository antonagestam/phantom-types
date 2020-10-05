# phantom-types

[![](https://github.com/antonagestam/phantom-types/workflows/CI/badge.svg)][CI]

[CI]: https://github.com/antonagestam/phantom-types/actions?query=workflow%3ACI

Phantom types for Python.

## Installation

```bash
python3 -m pip install phantom-types
```

## Abstract

- Make illegal states unrepresentable.
- [Parse, don't validate]
- [Ghosts of Departed Proofs]
- Abuse `__instancecheck__` and type-guards.
- Values are checked at runtime but no extra instances/subclasses are
  instantiated.

[Parse, don't validate]: https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/
[Ghosts of Departed Proofs]: https://kataskeue.com/gdp.pdf

## Usage

### Shipped phantom types

#### `phantom.boolean`

Describes objects that coerce to either `True` or `False` when calling `bool()` on them.

- `Truthy`
- `Falsy`

#### `phantom.datetime`

- `TZAware`
- `TZNaive`

#### `phantom.interval`

Describes narrower sets of numbers than `int` and `float`.

##### Base classes

- `Interval`
  - Takes class arguments `check: IntervalCheck`, `low: float` (defaults to negative
    infinity), and `high: float` (defaults to positive infinity). Expects concrete
    subtypes to specify their runtime type bound as first base.
- `Open`, `(low, high)`
  - Uses `check=phantom.predicates.interval.open`.
- `Closed`, `[low, high]`
  - Uses `check=phantom.predicates.interval.closed`.
- `OpenClosed`, `(low, high]`
  - Uses `check=phantom.predicates.interval.open_closed`.
- `ClosedOpen`, `[low, high)`
  - Uses `check=phantom.predicates.interval.closed_open`.

##### Implemented intervals

- `Natural`, `(0, ∞)`
- `NegativeInt`, `(-∞, 0)`
- `Portion`, `(0, 1)`

#### `phantom.re`

Takes `pattern: Pattern[str]` as class argument.

- `Match`, uses `phantom.predicates.re.is_match`.
- `FullMatch`, uses `phantom.predicates.re.is_full_match`.

#### `phantom.sized`

Describes collections with size boundaries. These types should only be used with
immutable collections. There is a naive check that eliminates some of the most common
mutable collections in the instance check, however a guaranteed check is probably
impossible to implement, so developer discipline is required.

- `PhantomSized[T]`, takes class argument `len: Predicate[float]`.
- `NonEmpty[T]`, a sized collection with at least one item.
- `Empty[T]`, an empty collection.

### Creating phantom types

Phantom types are created by subclassing `phantom.base.Phantom` and defining an
`__instancecheck__` method:

```python
from typing import Any
from typing import TYPE_CHECKING

from phantom.base import Phantom


class Greeting(Phantom):
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
hi = Greeting.from_instance("Hi there")

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

Checkout out the [dacite example] for how to create dataclasses with rich
phantom-typed fields without duplicating type definitions or losing parsed
information.

[dacite example]: examples/dacite/test_dacite.py


### Using predicates

Most of the shipped phantom types are implemented using boolean predicates. A boolean
predicate is simply a function that takes a single argument and returns either `True`
or `False`. While using boolean predicates is not necessary to use phantom types,
building up a library of types doing so allows reusing small and easily testable
functions to create a plethora of specialized types. Boolean predicates are usually easy
to reason about as they are pure functions with only two possible return values.

Studying the phantom types shipped in this library is recommended for gaining deeper
insight into how to implement more complicated types.

Now, looking at the example we implemented by subclassing `Phantom` and providing
an `__instancecheck__` method, let's try and achieve the same using predicates. The
`PredicateType` class already implements an `__instancecheck__` method and will usually
reduce the amount of boilerplate required.

```python
from phantom.base import PredicateType


# A boolean predicate that checks if a given string is a greeting. This function is of
# type `Predicate[str]` as it requires its argument to be a `str`.
def is_greeting(instance: str) -> bool:
    return instance.startswith(("Hello", "Hi"))


# Since our predicate requires its argument to be a `str`, we must make the bound of the
# phantom type `str` as well.
class Greeting(PredicateType, bound=str, predicate=is_greeting):
    ...


# Now we can make the same operations as with our previous example.
hello = "Hello there"
assert isinstance(hello, Greeting)
hi = Greeting.from_instance("Hi there")
```

As you can see, in addition to having less boilerplate than the previous example, this
style also has the added benefit of separating out business logic into simple reusable
functions.
