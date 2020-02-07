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

## Todo

- [ ] Add `Matches[r"^he(llo|j)$"]`.
- [ ] Generic of sized types should variate on `Iterable[T]`, not the type of
  the container. Syntax: `NonEmpty[int]`.
- [ ] Support e.g. `class NonEmptyTuple(NonEmpty, Tuple): ...`.
- [ ] Document discouragement and runtime check of mutable containers for Empty
  and NonEmpty.
