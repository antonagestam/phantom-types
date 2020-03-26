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

### Builtin types

#### `phantom.datetime`

- `TZAware`
- `TZNaive`

#### `phantom.numeric`

- `Natural`
- `NegativeInt`
- `Portion`

#### `phantom.re`

- `Match`

#### `phantom.sized`

- `NonEmpty`
- `Empty`

### Creating phantom types

To create new phantom types, subclass `phantom.base.Phantom` and define an
`__instancecheck__` method:

```python
from typing import Any
from typing import TYPE_CHECKING

from phantom.base import Phantom


class Greeting(str, Phantom):
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
