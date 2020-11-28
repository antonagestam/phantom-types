# phantom-types

[![](https://github.com/antonagestam/phantom-types/workflows/CI/badge.svg)](https://github.com/antonagestam/phantom-types/actions?query=workflow%3ACI)

Phantom types for Python.

_This project is in early development and major changes to core APIs should be expected.
Semantic versioning will be followed after version 1.0, but before that breaking changes
will happen between minor versions._

[Checkout the complete documentation on Read the Docs.](https://phantom-types.readthedocs.io/en/stable/)

## Installation

```bash
$  python3 -m pip install phantom-types
```

## Usage

```python
from typing import TypeVar

from phantom.sized import NonEmpty

T = TypeVar("T")


# The callee of this function is responsible to prove that the iterable isn't empty. The
# implementation is total and doesn't need special handling of empty iterables.
def head(iterable: NonEmpty[T]) -> T:
    return next(iter(iterable))


# We create a tuple of items and prove that it isn't empty. Proving that a value is of a
# phantom type can be done with all the regular mypy type guards, like
# `assert isinstance(t, T)`.
items = NonEmpty[int].parse((1, 2, 3))
first = head(items)

# Calling head() without proving that its argument is non-empty raises a type error:
# Argument 1 to "head" has incompatible type "Tuple[]"; expected "NonEmpty[<nothing>]"
head(())
```
