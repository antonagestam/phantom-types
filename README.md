<p align=center><img src=docs/phantom.svg alt="Depiction of phantom types in the wild"></p>

<h1 align=center>phantom-types</h1>

<p align=center>
    <a href=https://github.com/antonagestam/phantom-types/actions?query=workflow%3ACI+branch%3Amain><img src=https://github.com/antonagestam/phantom-types/workflows/CI/badge.svg alt="CI Build Status"></a>
    <a href=https://phantom-types.readthedocs.io/en/stable/><img src=https://readthedocs.org/projects/phantom-types/badge/?version=main alt="Documentation Build Status"></a>
    <a href=https://codecov.io/gh/antonagestam/phantom-types><img src=https://codecov.io/gh/antonagestam/phantom-types/branch/main/graph/badge.svg?token=UE85B7IA3Q alt="Test coverage report"></a>
    <br>
    <a href=https://pypi.org/project/phantom-types/><img src=https://img.shields.io/pypi/v/phantom-types.svg?color=informational&label=PyPI alt="PyPI Package"></a>
    <a href=https://pypi.org/project/phantom-types/><img src=https://img.shields.io/pypi/pyversions/phantom-types.svg?color=informational&label=Python alt="Python versions"></a>
</p>

[Phantom types][ghosts] for Python will help you make illegal states unrepresentable and
avoid shotgun parsing by enabling you to practice ["Parse, don't validate"][parse].

<h4 align=center>
    <a href=https://phantom-types.readthedocs.io/en/stable/>Checkout the complete documentation on Read the Docs →</a>
</h4>

## Installation

```bash
$  python3 -m pip install phantom-types
```

## Examples

By introducing a phantom type we can define a pre-condition for a function argument.

```python
from phantom import Phantom
from phantom.predicates.collection import contained


class Name(str, Phantom, predicate=contained({"Jane", "Joe"})):
    ...


def greet(name: Name):
    print(f"Hello {name}!")
```

Now this will be a valid call.

```python
greet(Name.parse("Jane"))
```

... and so will this.

```python
joe = "Joe"
assert isinstance(joe, Name)
greet(joe)
```

But this will yield a static type checking error.

```python
greet("bird")
```

### Runtime type checking

By combining phantom types with a runtime type-checker like [beartype] or [typeguard],
we can achieve the same level of security as you'd gain from using [contracts][dbc].

```python
import datetime
from beartype import beartype
from phantom.datetime import TZAware


@beartype
def soon(dt: TZAware) -> TZAware:
    return dt + datetime.timedelta(seconds=10)
```

The `soon` function will now validate that both its argument and return value is
timezone aware, e.g. pre- and post conditions.

### Pydantic support

Phantom types are ready to use with [pydantic] and have [integrated
support][pydantic-support] out-of-the-box. Subclasses of `Phantom` work with both
pydantic's validation and its schema generation.

```python
class Name(str, Phantom, predicate=contained({"Jane", "Joe"})):
    @classmethod
    def __schema__(cls) -> Schema:
        return super().__schema__() | {
            "description": "Either Jane or Joe",
            "format": "custom-name",
        }


class Person(BaseModel):
    name: Name
    created: TZAware


print(json.dumps(Person.schema(), indent=2))
```

The code above outputs the following JSONSchema.

```json
{
  "title": "Person",
  "type": "object",
  "properties": {
    "name": {
      "title": "Name",
      "description": "Either Jane or Joe",
      "format": "custom-name",
      "type": "string"
    },
    "created": {
      "title": "TZAware",
      "description": "A date-time with timezone data.",
      "type": "string",
      "format": "date-time"
    }
  },
  "required": ["name", "created"]
}
```

## Development

Install development requirements, preferably in a virtualenv:

```bash
$ python3 -m pip install .[test,pydantic,phonenumbers]
```

Run tests:

```bash
$ pytest
# or
$ make test
```

Linting and static type checking is setup with [pre-commit], after installing it you can
setup hooks with the following command, so that checks run before you push changes.

```bash
# configure hooks to run when pushing
$ pre-commit install -t pre-push
# or when committing
$ pre-commit install -t pre-commit
# run all checks
$ pre-commit run --all-files
# or just a single hook
$ pre-commit run mypy --all-files
```

In addition to static type checking, the project is setup with [pytest-mypy-plugins] to
test that exposed mypy types work as expected, these checks will run together with the
rest of the test suite, but you can single them out with the following command.

```bash
$ make test-typing
```

[parse]: https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/
[ghosts]: https://kataskeue.com/gdp.pdf
[build-status]:
  https://github.com/antonagestam/phantom-types/actions?query=workflow%3ACI+branch%3Amain
[coverage]: https://codecov.io/gh/antonagestam/phantom-types
[typeguard]: https://github.com/agronholm/typeguard
[beartype]: https://github.com/beartype/beartype
[dbc]: https://en.wikipedia.org/wiki/Design_by_contract
[pydantic]: https://pydantic-docs.helpmanual.io/
[pydantic-support]:
  https://phantom-types.readthedocs.io/en/stable/pages/pydantic-support.html
[pre-commit]: https://pre-commit.com/
[pytest-mypy-plugins]: https://github.com/TypedDjango/pytest-mypy-plugins
