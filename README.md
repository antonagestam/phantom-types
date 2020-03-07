# dependent-types

[![](https://github.com/antonagestam/dependent-types/workflows/CI/badge.svg)][CI]

[CI]: https://github.com/antonagestam/dependent-types/actions?query=workflow%3ACI

Dependent types for Python.

## Installation

```bash
python3 -m pip install dependent-types
```

## Abstract

- Make illegal states unrepresentable.
- Abuse `__instancecheck__` and type-guards.

## Usage

### Builtin types

#### `dept.datetime`

- `TZAware`
- `TZNaive`

#### `dept.numeric`

- `Natural`
- `NegativeInt`
- `Portion`

#### `dept.sized`

- `NonEmpty`
- `Empty`

### Creating dependent types

To create new dependent types, subclass `dept.base.Dependent` and define a
`__instancecheck__` method:

```python
from typing import Any
from dept.base import Dependent


class StartsWithHello(str, Dependent[str]):
    def __instancecheck__(self, instance: Any) -> bool:
        return isinstance(instance, str) and instance.startswith("Hello")


isinstance("Hello there", StartsWithHello)  # True
isinstance("Hi there", StartsWithHello)  # False
```

Checkout out the [dacite example] for how to create dataclasses with rich
dependently typed fields without duplicating type definitions or losing parsed
information.

[dacite example]: examples/dacite/test_dacite.py
