# phantom-types

[![CI Build Status](https://github.com/antonagestam/phantom-types/workflows/CI/badge.svg)][build-status]
[![Documentation Build Status](https://readthedocs.org/projects/phantom-types/badge/?version=main)][docs]


[Phantom types][ghosts] for Python that will help you make illegal states
unrepresentable and avoid shotgun parsing by practicing
["Parse, don't validate"][parse].

_This project is in early development and fundamental changes should be expected.
Semantic versioning will be followed after version 1.0, but before that breaking
changes might occur between minor versions._

[Checkout the complete documentation on Read the Docs →][docs]

## Installation

```bash
$  python3 -m pip install phantom-types
```

## Example

```python
from phantom import Phantom
from phantom.predicates.collection import contained

class Name(str, Phantom, predicate=contained({"Jane", "Joe"})): ...

def greet(name: Name):
    print(f"Hello {name}!")

# This is valid.
greet(Name.parse("Jane"))

# And so is this.
joe = "Joe"
assert isinstance(joe, Name)
greet(joe)

# But this will yield a static type checking error.
greet("bird")
```


[docs]: https://phantom-types.readthedocs.io/en/stable/
[parse]: https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/
[ghosts]: https://kataskeue.com/gdp.pdf
[build-status]: https://github.com/antonagestam/phantom-types/actions?query=workflow%3ACI+branch%3Amain
