phantom-types
-------------

[![CI](https://github.com/antonagestam/phantom-types/workflows/CI/badge.svg)](https://github.com/antonagestam/phantom-types/actions?query=workflow%3ACI+branch%3Amain)

Phantom types for Python.

[Phantom types][ghosts] will help you make illegal states unrepresentable and avoid
shotgun parsing by practicing ["Parse, don't validate"][parse].

_This project is in early development and fundamental changes should be expected.
Semantic versioning will be followed after version 1.0, but before that breaking changes
will occur between minor versions._

[Checkout the complete documentation on Read the Docs →][docs]

Installation
============

```bash
$  python3 -m pip install phantom-types
```

Motivating example
==================

Imagine that you're working on implementing a `head` function that should return the
first item of any given iterable. The implementation is simple:

```python
def head(iterable: Iterable[T]) -> T:
    return next(iter(iterable))
```

You go ahead and use this function across your project, until suddenly you run into a
subtle issue that you didn't think of: this function raises `StopIteration` when passed
an empty iterable. In functional programming terms this is due to the function being
_partial_ it specifies that it takes `Iterable` as argument, but in reality
we would need a narrower type to describe the set of valid arguments, and make the
function _total_.

You need to deal with the problem at hand so you go ahead and adjust all the call sites
of your function, and you now end up either asserting that the iterables are non-empty,
or catching the `StopIteration`.

```python
items = get_values()
if not len(items):
    return "empty"
return f"first element is: {head(items)}"
```

This works, and you could move on like this from here, but, you have now introduced
shotgun parsing into your application, since further down the processing line you need
to check the length if the iterable for other purposes. Shotgun parsing is an
antipattern that results in a program state that is hard to predict and will very likely
lead to bugs down the line. So how should you deal with this?

Using phantom types you can use the builtin `NonEmpty` type.

```python
def head(iterable: NonEmpty[T]) -> T:
    return next(iter(iterable))
```

The implementation is identical but you've now altered the signature of the function so
that it's total, it can deal with _all_ values of its argument type without raising an
exception.

By using the narrower type at the call sites, you avoid shotgun parsing, since the other
logic further down in the processing chain can rely on the type as well, and you won't
need to check the length of the iterable again.

```python
items = get_values()
if not isinstance(items, NonEmpty):
    return "empty"
return f"first element is: {head(items)}"
```

This strategy works in all places where a function works on a narrower type than you can
describe with the builtin types of Python, not only this made-up example. You can narrow
strings, integers, datetimes, and any other arbitrary types to completely rid of
duplicated validation throughout code bases.

There's a set of phantom types that ships builtin that is helpful to build on top of,
although you might mostly use your own custom phantom types that describe the exact
values that your implementations require. [The documentation contains examples of how to
create phantom types][docs].

How are phantom types implemented?
==================================

phantom-types make use of Python's `__instancecheck__` protocol to make types work with
the same checks that are recognized as type guards by static type checkers, e.g.
`isinstance()`. Phantom types are never instantiated at runtime and so will not add any
processing-, or memory overhead. Instead the question of whether a value is properly
parsed before it is processed is deffered to the static type checker.

The choice to design the library around boolean predicates, and much of the initially
shipped builtin predicates are heavily inspired by [fthomas/refined][refined].

[docs]: https://phantom-types.readthedocs.io/en/stable/
[parse]: https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/
[ghosts]: https://kataskeue.com/gdp.pdf
[refined]: https://github.com/fthomas/refined
