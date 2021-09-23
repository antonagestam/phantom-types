<p align=center><img src=docs/phantom.svg alt="Depiction of phantom types in the wild"></p>

<h1 align=center>phantom-types</h1>

<p align=center>
    <a href=https://github.com/antonagestam/phantom-types/actions?query=workflow%3ACI+branch%3Amain><img src=https://github.com/antonagestam/phantom-types/workflows/CI/badge.svg alt="CI Build Status"></a>
    <a href=https://phantom-types.readthedocs.io/en/stable/><img src=https://readthedocs.org/projects/phantom-types/badge/?version=main alt="Documentation Build Status"></a>
    <a href=https://codecov.io/gh/antonagestam/phantom-types><img src=https://codecov.io/gh/antonagestam/phantom-types/branch/main/graph/badge.svg?token=UE85B7IA3Q alt="Test coverage report"></a>
</p>

[Phantom types][ghosts] for Python will help you make illegal states
unrepresentable and avoid shotgun parsing by enabling you to
practice ["Parse, don't validate"][parse].

_This project is in early development and fundamental changes should be expected.
Semantic versioning will be followed after version 1.0, but before that breaking
changes might occur between minor versions._

<p align=center>
    <a href=https://phantom-types.readthedocs.io/en/stable/>Checkout the complete documentation on Read the Docs →</a>
</p>

## Installation

```bash
$  python3 -m pip install phantom-types
```

## Example

```python
from phantom import Phantom
from phantom.predicates.collection import contained


class Name(str, Phantom, predicate=contained({"Jane", "Joe"})):
    ...


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


[parse]: https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/
[ghosts]: https://kataskeue.com/gdp.pdf
[build-status]: https://github.com/antonagestam/phantom-types/actions?query=workflow%3ACI+branch%3Amain
[coverage]: https://codecov.io/gh/antonagestam/phantom-types
