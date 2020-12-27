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

## Quick example

Imagine that you're working on implementing a `head` function that should return the first item
of any given iterable. The implementation is simple:

```python
def head(iterable: Iterable[T]) -> T:
    return next(iter(iterable))
```

You go ahead and use this function across your project, until suddenly you run into a subtle
issue that you didn't think of: this function raises `StopIteration` when passed an empty iterable.
In functional programming terms this is due to the function being _partial_, it specifies that it takes
`Iterable` as argument, but in reality we would need a narrower type to describe the set of valid arguments,
and make the function _total_.

You need to deal with the problem at hand so you go ahead and adjust the all the call sites of your function,
and you now end up either asserting that the iterables are non-empty, or catching the `StopIteration`.

```python
items = get_values()
if not len(items):
    return "empty"
return "first element is: {head(items)}"
```

This works, and you could totally move on like this from here, but, you've now introduced 
shotgun parsing into your application, since further down the processing line you need to check
the length if the iterable for other purposes. So how should you deal with this?

Using phantom types you can use the builtin `NonEmpty` type. 

```python
def head(iterable: NonEmpty[T]) -> T:
    return next(iter(iterable))
```

The implementation is identical but you've now altered the signature of the function so that it's
total, it can deal with _all_ values of its argument type without raising an exception.

By using the narrower type at the call sites, you avoid shotgun parsing, since the other logic
further down in the processing chain can rely on the type as well, and you won't need to check
the length of the iterable again.

```python
items = get_values()
if not isinstance(items, NonEmpty):
    return "empty"
return "first element is: {head(items)}"
```

This strategy works in all places where a function works on a narrower type than you can
describe with the builtin types of Python. You can narrow strings, integers, datetimes
and so on to completely reduce duplicated validation throughout your projects.

There's a set of phantom types that ships builtin, but you will probably mostly use
customized phantom types that narrows types to the exact values that your implementations
can handle.
