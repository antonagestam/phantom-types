"""
Use ``Phantom`` to create arbitrary phantom types using boolean predicates.

.. code-block:: python

    from phantom import Phantom


    def is_big(value: int) -> bool:
        return value > 5


    class Big(int, Phantom, predicate=is_big): ...


    assert isinstance(10, Big)  # this passes
"""

from ._base import Phantom
from ._base import PhantomBase
from ._base import PhantomMeta
from ._version import __version__
from ._version import __version_tuple__
from .bounds import get_bound_parser
from .errors import BoundError
from .predicates import Predicate

__all__ = (
    "__version__",
    "__version_tuple__",
    "BoundError",
    "Phantom",
    "PhantomBase",
    "PhantomMeta",
    "get_bound_parser",
    "Predicate",
)
