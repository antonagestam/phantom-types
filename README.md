# dependent-types

Dependent types in Python using `__instancecheck__` and type-guards.

## Installation

## Todo

- `Matches[r"^he(llo|j)$"]`
- `TZAware`

## Usage

```python
from dep.sized import NonEmpty


def fst(col: NonEmpty[int]) -> int:
    return col[0]
```
